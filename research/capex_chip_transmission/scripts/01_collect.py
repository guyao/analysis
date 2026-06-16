"""01_collect.py — pull quarterly financials into data/raw/ and log sources.

data/raw/ is append-only; never edit files there by hand. For each company in
the transmission chain we collect quarterly revenue, operating income, and
capex from primary filings, and log every source in sources.md.
"""

from __future__ import annotations

import sys
import time
import random
import urllib.request
import json
from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup

PROJECT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT.parent
sys.path.insert(0, str(REPO_ROOT))

from utils import io  # noqa: E402
import config  # noqa: E402

# CIKs for US issuers (from SEC EDGAR)
US_CIKS = {
    "MSFT": "0000789019",
    "GOOGL": "0001652044",
    "AMZN": "0001018724",
    "META": "0001326801",
    "NVDA": "0001045810",
    "AMD": "0000002488",
    "AVGO": "0001730168",
    "MRVL": "0001037949",
    "AMAT": "0000006951",
    "LRCX": "0000707549",
    "KLAC": "0000319201",
    "ENTG": "0001103982",
}

# Non-US tickers to collect from Macrotrends (using their ADR tickers and slugs)
NON_US_MAPPING = {
    "TSM": {"macrotrends_ticker": "TSM", "slug": "taiwan-semiconductor-manufacturing"},
    "ASML": {"macrotrends_ticker": "ASML", "slug": "asml-holding"},
    "8035.T": {"macrotrends_ticker": "TOELY", "slug": "tokyo-electron"},
    "SHECY": {"macrotrends_ticker": "SHECY", "slug": "shin-etsu-chemical"},
    "3436.T": {"macrotrends_ticker": "SUOPY", "slug": "sumco"},
}


def collect_us_issuer(ticker: str, cik: str, raw_dir: Path) -> str:
    """Fetch quarterly financials from SEC EDGAR companyfacts API."""
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "MyResearchProject/1.0 (yaogu@analysis.com)"}
    )
    
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        
    facts = data.get("facts", {}).get("us-gaap", {})
    
    # Target tag maps
    tag_mapping = {
        "revenue": [
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "SalesRevenueNet",
            "Revenues"
        ],
        "operating_income": [
            "OperatingIncomeLoss"
        ],
        "capex": [
            "PaymentsToAcquirePropertyPlantAndEquipment"
        ]
    }
    
    all_frames = []
    
    for metric_name, tags in tag_mapping.items():
        for tag in tags:
            if tag in facts:
                units = facts[tag].get("units", {})
                for unit, values in units.items():
                    for entry in values:
                        row = {
                            "start": entry.get("start"),
                            "end": entry.get("end"),
                            "period_end": entry.get("end"),
                            "value": entry.get("val"),
                            "unit": unit,
                            "fy": entry.get("fy"),
                            "fp": entry.get("fp"),
                            "form": entry.get("form"),
                            "frame": entry.get("frame"),
                            "metric": metric_name,
                            "tag": tag
                        }
                        all_frames.append(row)
                
    if not all_frames:
        raise ValueError(f"No financial data found for {ticker}")
        
    df = pd.DataFrame(all_frames)
    out_path = raw_dir / f"{ticker}.csv"
    df.to_csv(out_path, index=False)
    return url


def get_macrotrends_page(session: requests.Session, ticker: str, slug: str, metric: str) -> str | None:
    """Fetch one page from Macrotrends with retries and delays to avoid Cloudflare blocks."""
    url = f"https://www.macrotrends.net/stocks/charts/{ticker}/{slug}/{metric}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Connection": "keep-alive"
    }
    
    for attempt in range(4):
        try:
            response = session.get(url, headers=headers, timeout=15)
            if response.status_code == 200 and "just a moment" not in response.text.lower():
                return response.text
            print(f"  Attempt {attempt+1} failed for {ticker} {metric} (status {response.status_code}).")
        except Exception as e:
            print(f"  Attempt {attempt+1} error for {ticker} {metric}: {e}")
            
        # exponential-ish backoff with jitter
        wait_time = 35 + random.uniform(5, 15)
        print(f"  Rate limited / Cloudflare challenge. Retrying in {wait_time:.1f} seconds...")
        time.sleep(wait_time)
    return None


def parse_macrotrends_html(html: str, metric_name: str) -> list[dict]:
    """Parse Macrotrends table 2 (quarterly data) into list of dictionaries."""
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    if len(tables) < 2:
        return []
        
    table = tables[1]
    rows = []
    for tr in table.find_all("tr")[1:]:
        tds = tr.find_all("td")
        if len(tds) >= 2:
            date_str = tds[0].text.strip()
            val_str = tds[1].text.strip().replace("$", "").replace(",", "")
            if val_str == "" or val_str == "-" or val_str == "null":
                continue
            rows.append({
                "period_end": date_str,
                "metric": metric_name,
                "value": float(val_str),
                "unit": "USD_M"
            })
    return rows


def collect_non_us_issuer(ticker: str, mapping: dict, session: requests.Session, raw_dir: Path) -> str:
    """Fetch quarterly revenue and operating income from Macrotrends."""
    mt_ticker = mapping["macrotrends_ticker"]
    slug = mapping["slug"]
    
    # 1. Fetch Revenue
    rev_html = get_macrotrends_page(session, mt_ticker, slug, "revenue")
    if not rev_html:
        raise ValueError(f"Failed to fetch revenue page for {ticker}")
    rev_rows = parse_macrotrends_html(rev_html, "revenue")
    print(f"  Successfully parsed {len(rev_rows)} revenue periods for {ticker}")
    time.sleep(random.uniform(2, 5)) # delay between pages
    
    # 2. Fetch Operating Income
    op_html = get_macrotrends_page(session, mt_ticker, slug, "operating-income")
    if not op_html:
        raise ValueError(f"Failed to fetch operating-income page for {ticker}")
    op_rows = parse_macrotrends_html(op_html, "operating_income")
    print(f"  Successfully parsed {len(op_rows)} operating income periods for {ticker}")
    
    # Merge and save
    all_rows = rev_rows + op_rows
    if not all_rows:
        raise ValueError(f"No financial data found for {ticker} on Macrotrends")
        
    df = pd.DataFrame(all_rows)
    out_path = raw_dir / f"{ticker}.csv"
    df.to_csv(out_path, index=False)
    
    return f"https://www.macrotrends.net/stocks/charts/{mt_ticker}/{slug}/revenue"


def collect_fx_rates(raw_dir: Path) -> str:
    """Fetch daily exchange rates for EURUSD=X, TWD=X, JPY=X from Yahoo Finance chart API."""
    pairs = {
        "EURUSD": "EURUSD=X",
        "TWD": "TWD=X",
        "JPY": "JPY=X"
    }
    
    all_rates = []
    for currency, pair in pairs.items():
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{pair}?interval=1d&range=5y"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        result = data.get("chart", {}).get("result", [{}])[0]
        timestamps = result.get("timestamp", [])
        closes = result.get("indicators", {}).get("quote", [{}])[0].get("close", [])
        
        for ts, close in zip(timestamps, closes):
            if close is not None:
                all_rates.append({
                    "date": pd.to_datetime(ts, unit="s").date().isoformat(),
                    "currency": currency,
                    "rate": close
                })
                
    df = pd.DataFrame(all_rates)
    out_path = raw_dir / "exchange_rates.csv"
    df.to_csv(out_path, index=False)
    return "https://finance.yahoo.com/quote/EURUSD=X"


def main() -> None:
    paths = io.project_paths(PROJECT)
    paths["raw"].mkdir(parents=True, exist_ok=True)
    
    # 1. Collect US Issuers from SEC EDGAR
    print("Collecting US Issuers from SEC EDGAR...")
    for ticker in config.all_tickers():
        if ticker in US_CIKS:
            cik = US_CIKS[ticker]
            try:
                url = collect_us_issuer(ticker, cik, paths["raw"])
                io.log_source(paths["sources"], url, f"{ticker}: quarterly financials from SEC EDGAR")
                print(f"  Successfully collected {ticker}")
                time.sleep(0.5) # respect rate limits
            except Exception as e:
                print(f"  FAILED to collect {ticker}: {e}")
                
    # 2. Collect Non-US Issuers from Macrotrends
    print("Collecting Non-US Issuers from Macrotrends...")
    session = requests.Session()
    # Warm up session
    try:
        session.get("https://www.macrotrends.net", headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    except Exception as e:
        print(f"  Macrotrends warm-up failed: {e}")
        
    for ticker, mapping in NON_US_MAPPING.items():
        try:
            print(f"Collecting {ticker} from Macrotrends...")
            url = collect_non_us_issuer(ticker, mapping, session, paths["raw"])
            io.log_source(paths["sources"], url, f"{ticker}: quarterly financials from Macrotrends")
            print(f"  Successfully collected {ticker}")
            time.sleep(random.uniform(3, 7)) # delay between tickers
        except Exception as e:
            print(f"  FAILED to collect {ticker} from Macrotrends: {e}")
            
    # 3. Collect FX Rates
    print("Collecting FX Rates from Yahoo Finance...")
    try:
        url = collect_fx_rates(paths["raw"])
        io.log_source(paths["sources"], url, "Daily historical exchange rates (EURUSD, USD/TWD, USD/JPY)")
        print("  Successfully collected exchange rates.")
    except Exception as e:
        print(f"  FAILED to collect exchange rates: {e}")


if __name__ == "__main__":
    main()
