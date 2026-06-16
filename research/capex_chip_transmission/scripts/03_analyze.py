"""03_analyze.py — quantify the capex -> semiconductor transmission chain.

Consumes data/processed/panel.parquet and produces, in output/:
  tables/layer_lead_lag.csv     YoY growth lead-lag & beta per layer
  tables/company_lead_lag.csv   YoY growth lead-lag & beta per company
  figures/transmission.png      indexed absolute levels of driver vs layers
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable
import pandas as pd
import numpy as np

PROJECT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT.parent
sys.path.insert(0, str(REPO_ROOT))

from utils import io, plotting, timeseries as ts  # noqa: E402
import config  # noqa: E402


def bootstrap_paired_statistic(
    x: pd.Series,
    y: pd.Series,
    statistic_func: Callable[[np.ndarray, np.ndarray], float],
    confidence: float = 0.95,
    n_resamples: int = 10_000,
    seed: int | None = 42
) -> tuple[float, float, float]:
    """Percentile bootstrap CI for a statistic computed on paired series."""
    df = pd.concat([x, y], axis=1).dropna()
    if len(df) < 5:
        return np.nan, np.nan, np.nan
        
    arr_x = df.iloc[:, 0].values
    arr_y = df.iloc[:, 1].values
    n = len(df)
    
    rng = np.random.default_rng(seed)
    estimates = []
    
    for _ in range(n_resamples):
        indices = rng.integers(0, n, size=n)
        resampled_x = arr_x[indices]
        resampled_y = arr_y[indices]
        
        try:
            val = statistic_func(resampled_x, resampled_y)
            if not np.isnan(val) and not np.isinf(val):
                estimates.append(val)
        except Exception:
            continue
            
    if len(estimates) < 100:
        return np.nan, np.nan, np.nan
        
    point_est = statistic_func(arr_x, arr_y)
    alpha = 1 - confidence
    low, high = np.percentile(estimates, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return point_est, low, high


def layer_revenue(panel: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue (capex for the driver layer) to one series per layer.

    The driver layer is measured by capex; downstream layers by revenue.
    Returns a wide frame indexed by quarter, one column per layer.
    """
    series = {}
    for layer in config.CHAIN:
        metric = "capex" if layer.name == config.DRIVER_LAYER else "revenue"
        sub = panel[(panel["layer"] == layer.name) & (panel["metric"] == metric)]
        if sub.empty:
            continue
        series[layer.name] = sub.groupby("period_end")["value_usd_m"].sum()
    return pd.DataFrame(series).sort_index()


def run_lead_lag_analysis(
    driver_yoy: pd.Series, 
    response_yoy: pd.Series, 
    max_lag: int = 8
) -> dict:
    """Find best non-negative lag, then calculate bootstrap CIs for correlation and beta."""
    try:
        ll = ts.lead_lag_correlation(driver_yoy, response_yoy, max_lag=max_lag)
        # We only consider non-negative lags (driver leading response)
        valid_lags = {k: v for k, v in ll.by_lag.items() if k >= 0}
        if not valid_lags:
            raise ValueError("No valid non-negative lags found")
            
        best_lag = max(valid_lags, key=lambda k: abs(valid_lags[k]))
    except Exception:
        return {
            "best_lag_q": np.nan, "peak_corr": np.nan, "corr_low": np.nan, "corr_high": np.nan,
            "beta": np.nan, "beta_low": np.nan, "beta_high": np.nan
        }
        
    # Align driver and response: response(t) aligns with driver(t - best_lag)
    aligned_driver = driver_yoy.shift(best_lag)
    
    corr_func = lambda a, b: float(np.corrcoef(a, b)[0, 1])
    beta_func = lambda a, b: float(np.polyfit(a, b, 1)[0])
    
    corr, corr_low, corr_high = bootstrap_paired_statistic(aligned_driver, response_yoy, corr_func)
    beta, beta_low, beta_high = bootstrap_paired_statistic(aligned_driver, response_yoy, beta_func)
    
    return {
        "best_lag_q": int(best_lag),
        "peak_corr": round(corr, 4) if not np.isnan(corr) else np.nan,
        "corr_low": round(corr_low, 4) if not np.isnan(corr_low) else np.nan,
        "corr_high": round(corr_high, 4) if not np.isnan(corr_high) else np.nan,
        "beta": round(beta, 4) if not np.isnan(beta) else np.nan,
        "beta_low": round(beta_low, 4) if not np.isnan(beta_low) else np.nan,
        "beta_high": round(beta_high, 4) if not np.isnan(beta_high) else np.nan,
    }


def main() -> None:
    paths = io.project_paths(PROJECT)
    panel_path = paths["processed"] / "panel.parquet"
    if not panel_path.exists():
        print(f"{panel_path} not found. Run 01_collect.py and 02_clean.py first.")
        return

    panel = pd.read_parquet(panel_path)
    
    # 1. Aggregate Layer Analysis
    wide_layers = layer_revenue(panel)
    yoy_layers = wide_layers.apply(lambda col: ts.yoy_growth(col, periods_per_year=4)).dropna()
    driver_yoy = yoy_layers[config.DRIVER_LAYER]
    
    layer_results = []
    for layer in config.CHAIN:
        if layer.name == config.DRIVER_LAYER or layer.name not in yoy_layers:
            continue
            
        res = run_lead_lag_analysis(driver_yoy, yoy_layers[layer.name], max_lag=config.MAX_LAG_Q)
        res["layer"] = layer.name
        res["expected_lag_q"] = layer.expected_lag_q
        layer_results.append(res)
        
    df_layers = pd.DataFrame(layer_results)
    # Reorder columns
    cols = ["layer", "expected_lag_q", "best_lag_q", "peak_corr", "corr_low", "corr_high", "beta", "beta_low", "beta_high"]
    df_layers = df_layers[cols]
    io.write_processed(df_layers, paths["tables"] / "layer_lead_lag.csv")
    
    # 2. Company-specific Analysis
    company_results = []
    for layer in config.CHAIN:
        if layer.name == config.DRIVER_LAYER:
            continue
            
        for ticker in layer.tickers:
            t_sub = panel[(panel["ticker"] == ticker) & (panel["metric"] == "revenue")]
            if t_sub.empty:
                continue
                
            t_series = t_sub.groupby("period_end")["value_usd_m"].sum().sort_index()
            t_yoy = ts.yoy_growth(t_series, periods_per_year=4).dropna()
            
            res = run_lead_lag_analysis(driver_yoy, t_yoy, max_lag=config.MAX_LAG_Q)
            res["ticker"] = ticker
            res["layer"] = layer.name
            company_results.append(res)
            
    df_companies = pd.DataFrame(company_results)
    comp_cols = ["ticker", "layer", "best_lag_q", "peak_corr", "corr_low", "corr_high", "beta", "beta_low", "beta_high"]
    df_companies = df_companies[comp_cols]
    io.write_processed(df_companies, paths["tables"] / "company_lead_lag.csv")
    
    # 3. Figure: indexed absolute levels of driver vs layers
    plotting.apply_default_style()
    indexed = wide_layers.apply(lambda col: ts.index_to_base(col, base=100.0))
    fig = plotting.line_chart(
        indexed.index, indexed[config.DRIVER_LAYER],
        title="Capex driver vs downstream layers (indexed absolute levels)",
        xlabel="Quarter", ylabel="Index (base=100)",
        label=config.DRIVER_LAYER
    )
    ax = fig.axes[0]
    for col in indexed.columns:
        if col != config.DRIVER_LAYER:
            ax.plot(indexed.index, indexed[col], label=col)
    ax.legend()
    plotting.save_figure(fig, paths["figures"] / "transmission.png")
    
    print("\nanalysis complete. Wrote:")
    print("  output/tables/layer_lead_lag.csv")
    print("  output/tables/company_lead_lag.csv")
    print("  output/figures/transmission.png")
    
    print("\nLayer Level Summary:")
    print(df_layers.to_string(index=False))


if __name__ == "__main__":
    main()
