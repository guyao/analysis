"""02_clean.py — reconcile raw filings into one tidy quarterly panel.

Reads every per-company file in data/raw/, harmonizes units (reported values ->
USD millions), aligns fiscal quarters to calendar quarters, tags each company
with its chain layer, and writes a single tidy panel to
data/processed/panel.parquet.

Output schema (one row per company-quarter-metric):
    ticker | layer | period_end (quarter) | metric | value_usd_m

The panel is fully regenerable: delete data/processed/ and re-run.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT.parent
sys.path.insert(0, str(REPO_ROOT))

from utils import io  # noqa: E402

import config  # noqa: E402


def _load_raw_files(raw_dir: Path) -> list[Path]:
    files = sorted(raw_dir.glob("*.csv")) + sorted(raw_dir.glob("*.parquet"))
    return [f for f in files if not f.name.startswith(".")]


def main() -> None:
    paths = io.project_paths(PROJECT)
    raw_files = _load_raw_files(paths["raw"])
    if not raw_files:
        print(
            f"No raw files in {paths['raw']}. Run 01_collect.py first. "
            "Nothing to clean (and nothing fabricated)."
        )
        return

    frames = []
    for f in raw_files:
        df = io.read_raw(f)
        ticker = f.stem
        df = df.copy()
        df["ticker"] = ticker
        df["layer"] = config.layer_of(ticker)
        # Expected raw columns: period_end, metric, value, unit
        df["period_end"] = pd.PeriodIndex(
            pd.to_datetime(df["period_end"]), freq="Q"
        ).to_timestamp(how="end")
        # Harmonize to USD millions. FX/unit handling is wired per filing system;
        # default assumes values already reported in USD millions.
        df["value_usd_m"] = df["value"].astype(float)
        frames.append(
            df[["ticker", "layer", "period_end", "metric", "value_usd_m"]]
        )

    panel = pd.concat(frames, ignore_index=True)
    panel = panel[panel["metric"].isin(config.METRICS)]
    panel = panel.sort_values(["ticker", "metric", "period_end"])

    out = io.write_processed(panel, paths["processed"] / "panel.parquet")
    print(f"wrote {out} ({len(panel)} rows, {panel['ticker'].nunique()} tickers)")


if __name__ == "__main__":
    main()
