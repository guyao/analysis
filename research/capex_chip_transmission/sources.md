# Sources

Every data series used in this project is logged here with its URL, the date it
was accessed, and a description. `scripts/01_collect.py` appends rows via
`utils.io.log_source`. No data point enters the analysis without an entry here.

## Candidate primary sources (to be wired in 01_collect.py)

| Source | What it provides |
| --- | --- |
| SEC EDGAR company-facts API (`https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json`) | Quarterly revenue, operating income, capex for US issuers: MSFT, GOOGL, AMZN, META, NVDA, AMD, AVGO, MRVL, AMAT, LRCX, KLAC, ENTG |
| TSMC Investor Relations (`https://investor.tsmc.com`) | Quarterly revenue & capex for TSM |
| ASML Investor Relations (`https://www.asml.com/en/investors`) | Quarterly revenue, bookings, capex for ASML |
| Tokyo Electron IR (`https://www.tel.com/ir/`) | Quarterly results for TEL (8035.T) |
| Shin-Etsu / SUMCO IR | Quarterly wafer/materials revenue |

## Collected series log

| URL | Access date | Description |
| --- | --- | --- |
<!-- rows appended automatically by 01_collect.py -->
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json | 2026-06-16 | MSFT: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001652044.json | 2026-06-16 | GOOGL: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001018724.json | 2026-06-16 | AMZN: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001326801.json | 2026-06-16 | META: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json | 2026-06-16 | NVDA: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000002488.json | 2026-06-16 | AMD: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001730168.json | 2026-06-16 | AVGO: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000707549.json | 2026-06-16 | LRCX: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000319201.json | 2026-06-16 | KLAC: quarterly financials from SEC EDGAR |
| https://finance.yahoo.com/quote/TSM/financials | 2026-06-16 | TSM: quarterly financials from Yahoo Finance |
| https://finance.yahoo.com/quote/ASML/financials | 2026-06-16 | ASML: quarterly financials from Yahoo Finance |
| https://finance.yahoo.com/quote/8035.T/financials | 2026-06-16 | 8035.T: quarterly financials from Yahoo Finance |
| https://finance.yahoo.com/quote/SHECY/financials | 2026-06-16 | SHECY: quarterly financials from Yahoo Finance |
| https://finance.yahoo.com/quote/3436.T/financials | 2026-06-16 | 3436.T: quarterly financials from Yahoo Finance |
| https://finance.yahoo.com/quote/EURUSD=X | 2026-06-16 | Daily historical exchange rates (EURUSD, USD/TWD, USD/JPY) |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json | 2026-06-16 | MSFT: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001652044.json | 2026-06-16 | GOOGL: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001018724.json | 2026-06-16 | AMZN: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001326801.json | 2026-06-16 | META: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json | 2026-06-16 | NVDA: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000002488.json | 2026-06-16 | AMD: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001730168.json | 2026-06-16 | AVGO: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001037949.json | 2026-06-16 | MRVL: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000006951.json | 2026-06-16 | AMAT: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000707549.json | 2026-06-16 | LRCX: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000319201.json | 2026-06-16 | KLAC: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001103982.json | 2026-06-16 | ENTG: quarterly financials from SEC EDGAR |
| https://finance.yahoo.com/quote/TSM/financials | 2026-06-16 | TSM: quarterly financials from Yahoo Finance |
| https://finance.yahoo.com/quote/ASML/financials | 2026-06-16 | ASML: quarterly financials from Yahoo Finance |
| https://finance.yahoo.com/quote/8035.T/financials | 2026-06-16 | 8035.T: quarterly financials from Yahoo Finance |
| https://finance.yahoo.com/quote/SHECY/financials | 2026-06-16 | SHECY: quarterly financials from Yahoo Finance |
| https://finance.yahoo.com/quote/3436.T/financials | 2026-06-16 | 3436.T: quarterly financials from Yahoo Finance |
| https://finance.yahoo.com/quote/EURUSD=X | 2026-06-16 | Daily historical exchange rates (EURUSD, USD/TWD, USD/JPY) |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json | 2026-06-16 | MSFT: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001652044.json | 2026-06-16 | GOOGL: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001018724.json | 2026-06-16 | AMZN: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001326801.json | 2026-06-16 | META: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json | 2026-06-16 | NVDA: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000002488.json | 2026-06-16 | AMD: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001730168.json | 2026-06-16 | AVGO: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001037949.json | 2026-06-16 | MRVL: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000006951.json | 2026-06-16 | AMAT: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000707549.json | 2026-06-16 | LRCX: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000319201.json | 2026-06-16 | KLAC: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001103982.json | 2026-06-16 | ENTG: quarterly financials from SEC EDGAR |
| https://www.macrotrends.net/stocks/charts/TSM/taiwan-semiconductor-manufacturing/revenue | 2026-06-16 | TSM: quarterly financials from Macrotrends |
| https://www.macrotrends.net/stocks/charts/ASML/asml-holding/revenue | 2026-06-16 | ASML: quarterly financials from Macrotrends |
| https://www.macrotrends.net/stocks/charts/TOELY/tokyo-electron/revenue | 2026-06-16 | 8035.T: quarterly financials from Macrotrends |
| https://www.macrotrends.net/stocks/charts/SHECY/shin-etsu-chemical/revenue | 2026-06-16 | SHECY: quarterly financials from Macrotrends |
| https://www.macrotrends.net/stocks/charts/SUOPY/sumco/revenue | 2026-06-16 | 3436.T: quarterly financials from Macrotrends |
| https://finance.yahoo.com/quote/EURUSD=X | 2026-06-16 | Daily historical exchange rates (EURUSD, USD/TWD, USD/JPY) |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json | 2026-06-16 | MSFT: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001652044.json | 2026-06-16 | GOOGL: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001018724.json | 2026-06-16 | AMZN: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001326801.json | 2026-06-16 | META: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json | 2026-06-16 | NVDA: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000002488.json | 2026-06-16 | AMD: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001730168.json | 2026-06-16 | AVGO: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001037949.json | 2026-06-16 | MRVL: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000006951.json | 2026-06-16 | AMAT: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000707549.json | 2026-06-16 | LRCX: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0000319201.json | 2026-06-16 | KLAC: quarterly financials from SEC EDGAR |
| https://data.sec.gov/api/xbrl/companyfacts/CIK0001103982.json | 2026-06-16 | ENTG: quarterly financials from SEC EDGAR |
| https://www.macrotrends.net/stocks/charts/TSM/taiwan-semiconductor-manufacturing/revenue | 2026-06-16 | TSM: quarterly financials from Macrotrends |
| https://www.macrotrends.net/stocks/charts/ASML/asml-holding/revenue | 2026-06-16 | ASML: quarterly financials from Macrotrends |
| https://www.macrotrends.net/stocks/charts/TOELY/tokyo-electron/revenue | 2026-06-16 | 8035.T: quarterly financials from Macrotrends |
| https://www.macrotrends.net/stocks/charts/SHECY/shin-etsu-chemical/revenue | 2026-06-16 | SHECY: quarterly financials from Macrotrends |
| https://www.macrotrends.net/stocks/charts/SUOPY/sumco/revenue | 2026-06-16 | 3436.T: quarterly financials from Macrotrends |
| https://finance.yahoo.com/quote/EURUSD=X | 2026-06-16 | Daily historical exchange rates (EURUSD, USD/TWD, USD/JPY) |
