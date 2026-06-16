"""Transmission-chain definition for the capex -> semiconductor study.

Editing the chain here (layers, members, expected lag) is the single place that
drives collection, cleaning, and analysis. Keeping it as data — not scattered
constants — is what makes the pipeline reproducible and easy to amend.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Layer:
    name: str
    role: str
    tickers: tuple[str, ...]
    # Hypothesized lead time (quarters) by which capex leads this layer.
    expected_lag_q: int


# Ordered upstream (demand driver) -> downstream.
CHAIN: tuple[Layer, ...] = (
    Layer(
        name="hyperscaler_capex",
        role="Demand driver: datacenter / AI capital spending",
        tickers=("MSFT", "GOOGL", "AMZN", "META"),
        expected_lag_q=0,
    ),
    Layer(
        name="accelerators_designers",
        role="Chip designers / AI accelerators / networking",
        tickers=("NVDA", "AMD", "AVGO", "MRVL"),
        expected_lag_q=1,
    ),
    Layer(
        name="foundry",
        role="Leading-edge wafer foundry",
        tickers=("TSM",),
        expected_lag_q=2,
    ),
    Layer(
        name="equipment",
        role="Semiconductor manufacturing equipment",
        tickers=("ASML", "AMAT", "LRCX", "KLAC", "8035.T"),
        expected_lag_q=3,
    ),
    Layer(
        name="materials_substrates",
        role="Silicon wafers, substrates, specialty materials",
        tickers=("SHECY", "3436.T", "ENTG"),
        expected_lag_q=4,
    ),
)

# Driver layer = first element of the chain.
DRIVER_LAYER = CHAIN[0].name

# Metrics pulled per company per quarter.
METRICS = ("revenue", "operating_income", "capex")

# Max lag (quarters) to scan in lead-lag cross-correlation.
MAX_LAG_Q = 8


def all_tickers() -> list[str]:
    return [t for layer in CHAIN for t in layer.tickers]


def layer_of(ticker: str) -> str | None:
    for layer in CHAIN:
        if ticker in layer.tickers:
            return layer.name
    return None
