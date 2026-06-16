# DECISIONS

Append-only log of notable technical decisions. Before adding a new dependency
or algorithm, do a comparative investigation and record the outcome here.

## 2026-06-16 — Initial library & repo scaffolding
- **Money as integer cents (`Decimal`-backed).** Avoids float rounding error in
  financial calculations. Allocation uses the largest-remainder (Hamilton)
  method so splits conserve the total to the cent.
- **Headless matplotlib (`Agg`).** Plotting helpers render and save without a
  display, so figures are reproducible in CI and non-interactive sessions.
- **Property testing with `hypothesis`.** Financial/stat invariants (weights
  sum to 1, frictionless rebalance preserves total value, integer-cent
  arithmetic is exact) are enforced as properties, not just examples.
- **Pinned scientific stack** in `requirements.txt`: pandas, numpy, scipy,
  statsmodels, matplotlib/plotly, jupyter.
