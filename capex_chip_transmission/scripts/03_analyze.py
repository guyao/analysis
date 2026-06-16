"""03_analyze.py — quantify the capex -> semiconductor transmission chain.

Consumes data/processed/panel.parquet and produces, in output/:
  tables/layer_growth.csv      YoY growth per layer per quarter
  tables/lead_lag.csv          best lag (q) and peak correlation per layer
  figures/transmission.png     indexed growth of driver vs each layer

Every number is computed here from the cleaned panel via utils; none are
hand-entered. Re-running regenerates all outputs.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT.parent
sys.path.insert(0, str(REPO_ROOT))

from utils import io, plotting, timeseries  # noqa: E402

import config  # noqa: E402


def layer_revenue(panel: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue (capex for the driver layer) to one series per layer.

    The driver layer is measured by capex; downstream layers by revenue.
    Returns a wide frame indexed by quarter, one column per layer.
    """
    series = {}
    for layer in config.CHAIN:
        metric = "capex" if layer.name == config.DRIVER_LAYER else "revenue"
        sub = panel[(panel["layer"] == layer.name) & (panel["metric"] == metric)]
        if sub.empty:
            continue
        series[layer.name] = sub.groupby("period_end")["value_usd_m"].sum()
    return pd.DataFrame(series).sort_index()


def main() -> None:
    paths = io.project_paths(PROJECT)
    panel_path = paths["processed"] / "panel.parquet"
    if not panel_path.exists():
        print(
            f"{panel_path} not found. Run 01_collect.py and 02_clean.py first. "
            "No outputs fabricated."
        )
        return

    panel = pd.read_parquet(panel_path)
    wide = layer_revenue(panel)

    # 1) YoY growth per layer.
    yoy = wide.apply(lambda col: timeseries.yoy_growth(col, periods_per_year=4))
    io.write_processed(
        yoy.reset_index(), paths["tables"] / "layer_growth.csv"
    )

    # 2) Lead-lag of the capex driver vs each downstream layer's growth.
    driver = yoy[config.DRIVER_LAYER]
    rows = []
    for layer in config.CHAIN:
        if layer.name == config.DRIVER_LAYER or layer.name not in yoy:
            continue
        try:
            ll = timeseries.lead_lag_correlation(
                driver, yoy[layer.name], max_lag=config.MAX_LAG_Q
            )
        except ValueError:
            continue
        rows.append(
            {
                "layer": layer.name,
                "expected_lag_q": layer.expected_lag_q,
                "best_lag_q": ll.best_lag,
                "peak_corr": round(ll.best_corr, 4),
            }
        )
    lead_lag = pd.DataFrame(rows)
    io.write_processed(lead_lag, paths["tables"] / "lead_lag.csv")

    # 3) Figure: indexed growth, driver vs layers.
    plotting.apply_default_style()
    indexed = wide.apply(lambda col: timeseries.index_to_base(col, base=100))
    fig = plotting.line_chart(indexed.index, indexed[config.DRIVER_LAYER],
                              title="Capex driver vs downstream layers (indexed)",
                              xlabel="Quarter", ylabel="Index (base=100)",
                              label=config.DRIVER_LAYER)
    ax = fig.axes[0]
    for col in indexed.columns:
        if col != config.DRIVER_LAYER:
            ax.plot(indexed.index, indexed[col], label=col)
    ax.legend()
    plotting.save_figure(fig, paths["figures"] / "transmission.png")

    print("wrote output/tables/layer_growth.csv, output/tables/lead_lag.csv, "
          "output/figures/transmission.png")
    if not lead_lag.empty:
        print(lead_lag.to_string(index=False))


if __name__ == "__main__":
    main()
