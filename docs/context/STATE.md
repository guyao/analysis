# STATE

Read this at the **start** of every session; update it at the **end**.

## Last updated
2026-06-16

## Current status
Framework in place plus the first research project scaffolded. The common
library now includes generic time-series computation modules. All 30 tests
pass; the project's pipeline runs end-to-end and refuses to fabricate when raw
data is absent.

## Done
- Authored `CLAUDE.md` (optimized from `GEMINI.md`).
- Built `utils/` library: `io`, `money`, `transforms`, `stats`, `plotting`,
  and `timeseries` (growth, YoY, CAGR, index-to-base, lead-lag correlation).
- Added `tests/` with pytest + hypothesis property tests (all passing).
- Added `scripts/new_project.py` scaffolder and `docs/context/` files.
- Scaffolded project `capex_chip_transmission/`: README (question, chain,
  hypotheses), `scripts/config.py` (chain definition), and a 3-stage pipeline
  (`01_collect` → `02_clean` → `03_analyze`) wired to `utils`.

## Next steps
- Wire real collectors in `capex_chip_transmission/scripts/01_collect.py`
  (SEC EDGAR company-facts for US issuers; IR disclosures for TSM/ASML/TEL),
  logging each source in `sources.md`.
- Run the pipeline, then fill in README conclusions with code-derived numbers.
- Promote any new reusable helper (e.g. growth-beta regression) into `utils/`.
