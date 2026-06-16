# Tech Capex → Semiconductor Transmission Chain

How does the capital expenditure of large technology companies (the
"hyperscalers") propagate down the semiconductor supply chain, and **which
companies' revenue/earnings growth is driven by it, with what time lag?**

## Research question (falsifiable)
When hyperscaler capex accelerates, does each downstream layer of the chip
supply chain show a measurable, *lagged* acceleration in revenue/earnings —
and can we estimate the lead time (in quarters) and strength of transmission
at each layer?

## The transmission chain (hypothesized)
```
Hyperscaler capex            MSFT, GOOGL, AMZN, META  (datacenter / AI buildout)
        │  (drives demand)
        ▼
Accelerator & chip designers NVDA, AMD, AVGO, MRVL
        │
        ▼
Foundry                      TSMC (TSM)
        │
        ▼
Semiconductor equipment      ASML, AMAT, LRCX, KLAC, TEL (8035.T)
        │
        ▼
Materials / substrates       Shin-Etsu, SUMCO, Entegris
```
The chain (layers + tickers + expected lag) is defined once in
`scripts/config.py` so the analysis is data-driven and easy to amend.

## Hypotheses
- **H1 (transmission exists).** YoY hyperscaler capex growth is positively
  correlated with each downstream layer's YoY revenue growth.
- **H2 (lead-lag ordering).** The driver *leads* each layer; the lead time is
  shortest for accelerators/foundry and longest for equipment and materials
  (capex → orders → shipments → recognized revenue).
- **H3 (amplification/attenuation).** Transmission strength differs by layer;
  some layers amplify the signal (higher growth beta) and some attenuate it.
- **H4 (winners).** An identifiable subset of companies shows revenue/earnings
  growth most tightly coupled to the capex cycle.

## Metrics & methods
- YoY and QoQ growth per company and per layer (`utils.timeseries`).
- Lead-lag cross-correlation between aggregate capex growth and each layer's
  growth; report best lag (quarters) and peak correlation
  (`utils.timeseries.lead_lag_correlation`).
- Growth "beta": regression of layer growth on lagged capex growth.
- Uncertainty via bootstrap CIs (`utils.stats.bootstrap_ci`).

## Data
Quarterly company financials (capex, revenue, operating income) from primary
filings — SEC EDGAR (10-K/10-Q) for US issuers and the equivalent disclosures
for TSMC / Tokyo Electron / ASML — plus each company's investor-relations
statements. Every series is logged in `sources.md` with URL and access date.
**No number enters the analysis without a logged source; nothing is fabricated.**

## How to reproduce
```bash
pip install -r ../requirements.txt          # from repo root
python scripts/01_collect.py                 # pull filings into data/raw/ (+ log sources)
python scripts/02_clean.py                   # reconcile units/calendars -> data/processed/
python scripts/03_analyze.py                 # growth, lead-lag, betas -> output/
```
Re-running the pipeline in order on `data/raw/` regenerates every file in
`data/processed/` and `output/`.

## Status
Structure scaffolded; pipeline scripts are runnable once raw filings are
collected in `data/raw/`. Conclusions will be filled in after analysis, each
number traceable to code + a source.
