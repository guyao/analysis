"""02_clean.py — reconcile raw filings into one tidy quarterly panel.

Reads every per-company file in data/raw/, harmonizes units (reported values ->
USD millions), aligns fiscal quarters to calendar quarters, tags each company
with its chain layer, and writes a single tidy panel to
data/processed/panel.parquet.

Output schema (one row per company-quarter-metric):
    ticker | layer | period_end (quarter) | metric | value_usd_m
"""

from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT.parent
sys.path.insert(0, str(REPO_ROOT))

from utils import io  # noqa: E402
import config  # noqa: E402

# Priority for merging US GAAP tags
TAG_PRIORITY = {
    "RevenueFromContractWithCustomerExcludingAssessedTax": 1,
    "SalesRevenueNet": 2,
    "Revenues": 3,
    "OperatingIncomeLoss": 1,
    "PaymentsToAcquirePropertyPlantAndEquipment": 1
}


def clean_us_non_capex(df_raw: pd.DataFrame, metric_name: str) -> pd.DataFrame:
    """Clean revenue or operating income for a US issuer."""
    df = df_raw[df_raw["metric"] == metric_name].copy()
    if df.empty:
        return pd.DataFrame(columns=["period_end", "metric", "value"])
        
    df = df.dropna(subset=["start", "end", "value"])
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])
    df["duration_days"] = (df["end"] - df["start"]).dt.days
    
    # Keep only quarterly statements (approx 3 months: 80 to 105 days)
    df = df[(df["duration_days"] >= 80) & (df["duration_days"] <= 105)]
    
    # Map to calendar quarter end
    df["period_end"] = pd.PeriodIndex(df["end"], freq="Q").to_timestamp(how="end")
    
    # Priority sorting to pick the best tag representation and form version
    df["priority"] = df["tag"].map(TAG_PRIORITY).fillna(99)
    df = df.sort_values(["period_end", "priority", "form"], ascending=[True, True, False])
    
    df_clean = df.groupby("period_end")["value"].first().reset_index()
    df_clean["metric"] = metric_name
    return df_clean


def clean_us_capex(df_raw: pd.DataFrame) -> pd.DataFrame:
    """De-accumulate cash flow Capex values for a US issuer."""
    df = df_raw[df_raw["metric"] == "capex"].copy()
    if df.empty:
        return pd.DataFrame(columns=["period_end", "metric", "value"])
        
    df = df.dropna(subset=["fy", "start", "end", "value"])
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])
    df["duration_days"] = (df["end"] - df["start"]).dt.days
    df["fy"] = df["fy"].astype("Int64")
    
    # Map duration to fiscal periods
    def get_period_type(days):
        if 80 <= days <= 105:
            return "Q1"
        elif 170 <= days <= 200:
            return "Q2"
        elif 260 <= days <= 295:
            return "Q3"
        elif 340 <= days <= 385:
            return "FY"
        return None
        
    df["period_type"] = df["duration_days"].apply(get_period_type)
    df = df.dropna(subset=["period_type"])
    
    # Sort and deduplicate to keep latest version of each period
    df = df.sort_values(["fy", "period_type", "form"], ascending=[True, True, False])
    df = df.drop_duplicates(subset=["fy", "period_type"], keep="first")
    
    pivoted = df.pivot(index="fy", columns="period_type", values="value")
    for col in ["Q1", "Q2", "Q3", "FY"]:
        if col not in pivoted.columns:
            pivoted[col] = np.nan
            
    # Calculate discrete values
    discrete = pd.DataFrame(index=pivoted.index)
    discrete["Q1"] = pivoted["Q1"]
    discrete["Q2"] = pivoted["Q2"] - pivoted["Q1"]
    discrete["Q3"] = pivoted["Q3"] - pivoted["Q2"]
    discrete["Q4"] = pivoted["FY"] - pivoted["Q3"]
    
    discrete_long = discrete.reset_index().melt(
        id_vars="fy", 
        value_vars=["Q1", "Q2", "Q3", "Q4"],
        var_name="fiscal_quarter",
        value_name="val_discrete"
    )
    
    discrete_long["period_type"] = discrete_long["fiscal_quarter"].map({
        "Q1": "Q1",
        "Q2": "Q2",
        "Q3": "Q3",
        "Q4": "FY"
    })
    
    merged = pd.merge(
        discrete_long,
        df[["fy", "period_type", "end"]],
        on=["fy", "period_type"],
        how="inner"
    )
    
    merged["period_end"] = pd.PeriodIndex(pd.to_datetime(merged["end"]), freq="Q").to_timestamp(how="end")
    
    merged = merged.sort_values("period_end")
    df_clean = merged.groupby("period_end")["val_discrete"].first().reset_index()
    df_clean = df_clean.rename(columns={"val_discrete": "value"})
    df_clean["metric"] = "capex"
    return df_clean


def main() -> None:
    paths = io.project_paths(PROJECT)
    
    raw_files = sorted(paths["raw"].glob("*.csv"))
    # Exclude exchange_rates.csv or dotfiles
    raw_files = [f for f in raw_files if f.name != "exchange_rates.csv" and not f.name.startswith(".")]
    
    if not raw_files:
        print("No raw files found. Run 01_collect.py first.")
        return
        
    all_frames = []
    
    for f in raw_files:
        ticker = f.stem
        layer = config.layer_of(ticker)
        df_raw = pd.read_csv(f)
        
        # Check if US issuer or non-US issuer
        is_us = "start" in df_raw.columns
        
        if is_us:
            # 1. Clean revenue
            rev = clean_us_non_capex(df_raw, "revenue")
            # 2. Clean operating income
            opinc = clean_us_non_capex(df_raw, "operating_income")
            # 3. Clean capex
            capex = clean_us_capex(df_raw)
            
            merged = pd.concat([rev, opinc, capex], ignore_index=True)
            # Scale to USD Millions
            merged["value_usd_m"] = merged["value"].astype(float) / 1e6
        else:
            # Macrotrends already formatted in USD millions and discrete quarterly
            df_raw["period_end"] = pd.PeriodIndex(
                pd.to_datetime(df_raw["period_end"]), freq="Q"
            ).to_timestamp(how="end")
            
            merged = df_raw.rename(columns={"value": "value_usd_m"})
            
        merged["ticker"] = ticker
        merged["layer"] = layer
        
        # Keep clean columns
        cleaned = merged[["ticker", "layer", "period_end", "metric", "value_usd_m"]]
        all_frames.append(cleaned)
        
    panel = pd.concat(all_frames, ignore_index=True)
    panel = panel.sort_values(["ticker", "metric", "period_end"])
    panel = panel.drop_duplicates(subset=["ticker", "metric", "period_end"], keep="first")
    
    out_path = paths["processed"] / "panel.parquet"
    io.write_processed(panel, out_path)
    
    print(f"wrote clean panel to {out_path} ({len(panel)} rows, {panel['ticker'].nunique()} tickers)")
    # Show count of data points per ticker
    print(panel.groupby(["ticker", "metric"]).size().unstack(fill_value=0))


if __name__ == "__main__":
    main()
