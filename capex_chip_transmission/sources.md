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
