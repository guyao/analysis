# GLOSSARY

Shared definitions of domain and project terms. Keep entries short and precise.

- **Raw data** — immutable source data in `data/raw/`; never edited by hand.
- **Processed data** — cleaned/derived data in `data/processed/`, fully
  regenerable by re-running `scripts/` in order.
- **Allocation (largest remainder)** — integer split of a total across weights
  where leftover units go to the largest fractional remainders; the parts sum
  exactly to the total.
- **Frictionless rebalance** — reallocation to target weights assuming no fees
  or slippage; total market value is unchanged.
- **Bootstrap CI** — confidence interval built by resampling the data with
  replacement; used when the sampling distribution is unknown.
- **Winsorize** — clip a series to given quantiles to limit outlier influence.
