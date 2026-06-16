"""Data-cleaning and portfolio transforms.

Functions here are pure: they take values and return values, with no IO. That
keeps them trivially testable and safe to reuse across projects.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd

__all__ = ["normalize_weights", "rebalance", "winsorize", "zscore"]


def normalize_weights(weights: Sequence[float]) -> np.ndarray:
    """Scale non-negative weights so they sum to exactly 1.0.

    Raises if the weights are empty, negative, or all zero.
    """
    arr = np.asarray(weights, dtype=float)
    if arr.size == 0:
        raise ValueError("weights must be non-empty")
    if np.any(arr < 0):
        raise ValueError("weights must be non-negative")
    total = arr.sum()
    if total <= 0:
        raise ValueError("weights must sum to a positive value")
    return arr / total


def rebalance(
    target_weights: Sequence[float], total_value: float
) -> np.ndarray:
    """Return the dollar value to hold in each asset for a target allocation.

    ``target_weights`` need not be normalized; they are normalized internally.
    The result sums to ``total_value`` (frictionless: no fees or slippage), so
    rebalancing never changes the total market value.
    """
    if total_value < 0:
        raise ValueError("total_value must be non-negative")
    w = normalize_weights(target_weights)
    return w * total_value


def winsorize(
    series: pd.Series | Sequence[float],
    lower: float = 0.01,
    upper: float = 0.99,
) -> pd.Series:
    """Clip a series to its ``[lower, upper]`` quantiles to tame outliers."""
    if not 0.0 <= lower < upper <= 1.0:
        raise ValueError("require 0 <= lower < upper <= 1")
    s = pd.Series(series, dtype=float)
    lo, hi = s.quantile(lower), s.quantile(upper)
    return s.clip(lower=lo, upper=hi)


def zscore(series: pd.Series | Sequence[float], ddof: int = 0) -> pd.Series:
    """Standardize a series to zero mean and unit standard deviation."""
    s = pd.Series(series, dtype=float)
    std = s.std(ddof=ddof)
    if std == 0:
        raise ValueError("cannot z-score a constant series (zero variance)")
    return (s - s.mean()) / std
