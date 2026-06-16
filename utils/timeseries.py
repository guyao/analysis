"""Generic time-series computation modules.

Reusable math for growth and transmission-chain analysis: period-over-period
growth, year-over-year growth, CAGR, indexing to a base, and lead-lag
cross-correlation (used to measure how a driver series propagates to a
downstream series with a time lag).

All functions are pure and IO-free.
"""

from __future__ import annotations

from typing import NamedTuple, Sequence

import numpy as np
import pandas as pd

__all__ = [
    "growth_rate",
    "yoy_growth",
    "cagr",
    "index_to_base",
    "LeadLag",
    "lead_lag_correlation",
]


def growth_rate(series: pd.Series | Sequence[float], periods: int = 1) -> pd.Series:
    """Period-over-period fractional growth (e.g. QoQ for ``periods=1``)."""
    s = pd.Series(series, dtype=float)
    if periods < 1:
        raise ValueError("periods must be >= 1")
    return s.pct_change(periods=periods)


def yoy_growth(
    series: pd.Series | Sequence[float], periods_per_year: int = 4
) -> pd.Series:
    """Year-over-year fractional growth.

    ``periods_per_year`` is 4 for quarterly data, 12 for monthly, 1 for annual.
    """
    if periods_per_year < 1:
        raise ValueError("periods_per_year must be >= 1")
    return growth_rate(series, periods=periods_per_year)


def cagr(begin: float, end: float, years: float) -> float:
    """Compound annual growth rate between two values over ``years`` years."""
    if years <= 0:
        raise ValueError("years must be positive")
    if begin <= 0 or end <= 0:
        raise ValueError("begin and end must be positive")
    return (end / begin) ** (1.0 / years) - 1.0


def index_to_base(
    series: pd.Series | Sequence[float], base: float = 100.0
) -> pd.Series:
    """Rebase a series so its first non-null value equals ``base``.

    Useful for plotting several series of different magnitudes on one axis.
    """
    s = pd.Series(series, dtype=float)
    first_valid = s.first_valid_index()
    if first_valid is None:
        raise ValueError("series has no non-null values")
    anchor = s.loc[first_valid]
    if anchor == 0:
        raise ValueError("first value is zero; cannot rebase")
    return s / anchor * base


class LeadLag(NamedTuple):
    best_lag: int
    best_corr: float
    by_lag: dict[int, float]


def lead_lag_correlation(
    driver: pd.Series | Sequence[float],
    response: pd.Series | Sequence[float],
    max_lag: int = 8,
) -> LeadLag:
    """Cross-correlate a driver with a response across integer lags.

    For each ``lag`` in ``[-max_lag, max_lag]`` the Pearson correlation between
    ``driver[t]`` and ``response[t + lag]`` is computed on overlapping points.
    A positive ``best_lag`` means the driver *leads* the response by that many
    periods — the core quantity in transmission-chain analysis.
    """
    if not isinstance(driver, pd.Series):
        driver = pd.Series(driver)
    if not isinstance(response, pd.Series):
        response = pd.Series(response)
        
    # Align by index to ensure correct date-matching
    df = pd.concat([driver, response], axis=1).sort_index()
    d = df.iloc[:, 0]
    r = df.iloc[:, 1]
    
    if max_lag < 0:
        raise ValueError("max_lag must be non-negative")

    by_lag: dict[int, float] = {}
    for lag in range(-max_lag, max_lag + 1):
        shifted = r.shift(-lag)
        pair = pd.concat([d, shifted], axis=1).dropna()
        if len(pair) < 3 or pair.iloc[:, 0].std() == 0 or pair.iloc[:, 1].std() == 0:
            continue
        by_lag[lag] = float(pair.iloc[:, 0].corr(pair.iloc[:, 1]))

    if not by_lag:
        raise ValueError("not enough overlapping data to compute correlations")

    best_lag = max(by_lag, key=lambda k: abs(by_lag[k]))
    return LeadLag(best_lag, by_lag[best_lag], by_lag)
