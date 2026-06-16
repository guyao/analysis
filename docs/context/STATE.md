# STATE

Read this at the **start** of every session; update it at the **end**.

## Last updated
2026-06-16

## Current status
Completed the extended semiconductor sub-sectors mapping. Created the `doc/extended_semiconductor_subsectors.md` file and documented EDA/IP, ABF Substrates, MEMS Probe Cards, Specialty Chemicals, and the chronologically ordered transmission lag map.

## Done
- Authored `CLAUDE.md` (optimized from `GEMINI.md`).
- Built `utils/` library: `io`, `money`, `transforms`, `stats`, `plotting`,
  and `timeseries` (growth, YoY, CAGR, index-to-base, lead-lag correlation).
- Fixed a bug in `timeseries.lead_lag_correlation` where pandas Series date indices were dropped, causing misalignment.
- Added `tests/` with pytest + hypothesis property tests (all passing).
- Scaffolded and completed the `capex_chip_transmission/` research project.
- Scaffolded, collected data, cleaned, analyzed, and completed the `ai_power_demand/` research project comparing US and China.
- Enforced report naming conventions (.en.ipynb/.zh.ipynb) and generated Chinese reports.
- Mapped the HBM supply chain and created `research/capex_chip_transmission/doc/hbm_supply_chain.md`.
- Mapped the logic foundry and designer supply chain and created `research/capex_chip_transmission/doc/foundry_designer_chain.md`.
- Mapped the extended semiconductor sub-sectors (EDA/IP, ABF Substrates, MEMS Probe Cards, Chemicals) and created `research/capex_chip_transmission/doc/extended_semiconductor_subsectors.md`.




## Next steps
- Await user review of the HBM supply chain reference document.

