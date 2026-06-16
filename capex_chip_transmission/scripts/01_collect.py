"""01_collect.py — pull quarterly financials into data/raw/ and log sources.

data/raw/ is append-only; never edit files there by hand. For each company in
the transmission chain we collect quarterly revenue, operating income, and
capex from primary filings, and log every source in sources.md.

This script intentionally does NOT fabricate data. Wire each ticker to its
filing source below (SEC EDGAR company-facts API for US issuers; IR / local
regulator disclosures for TSM, ASML, TEL, etc.). Until a source is wired the
script reports what is missing rather than inventing numbers.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT.parent
sys.path.insert(0, str(REPO_ROOT))

from utils import io  # noqa: E402

import config  # noqa: E402

# Map each ticker to the source you collect it from. Fill these in as you wire
# real collectors; leave as None for not-yet-sourced tickers.
#   SEC EDGAR company facts: https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
SOURCES: dict[str, str | None] = {t: None for t in config.all_tickers()}


def collect_ticker(ticker: str, url: str) -> "object":
    """Download and persist one company's quarterly financials.

    Implement the actual fetch+parse here (e.g. SEC company-facts -> tidy
    DataFrame with columns: period_end, metric, value, unit). Returns the
    object written, or raises on failure. Kept abstract so the collector for
    each filing system can be plugged in independently.
    """
    raise NotImplementedError(
        f"wire a real collector for {ticker} ({url}) that writes "
        f"data/raw/{ticker}.csv and returns it"
    )


def main() -> None:
    paths = io.project_paths(PROJECT)
    paths["raw"].mkdir(parents=True, exist_ok=True)

    missing = [t for t, url in SOURCES.items() if not url]
    if missing:
        print("No source wired yet for:", ", ".join(missing))
        print(
            "Add each ticker's filing URL to SOURCES, implement collect_ticker, "
            "then re-run. Nothing was fabricated."
        )
        return

    for ticker, url in SOURCES.items():
        collect_ticker(ticker, url)
        io.log_source(
            paths["sources"], url, f"{ticker}: quarterly revenue/opinc/capex"
        )
        print(f"collected {ticker}")


if __name__ == "__main__":
    main()
