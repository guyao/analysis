"""Statistical helpers with explicit uncertainty quantification.

Every estimate returned here carries an interval so that reports can state
uncertainty rather than point values alone.
"""

from __future__ import annotations

from typing import Callable, NamedTuple, Sequence

import numpy as np
from scipy import stats as _scipy_stats

__all__ = ["ConfidenceInterval", "summary_stats", "mean_ci", "bootstrap_ci"]


class ConfidenceInterval(NamedTuple):
    point: float
    low: float
    high: float
    confidence: float


def summary_stats(data: Sequence[float]) -> dict[str, float]:
    """Return a dictionary of common descriptive statistics."""
    arr = np.asarray(data, dtype=float)
    if arr.size == 0:
        raise ValueError("data must be non-empty")
    return {
        "n": int(arr.size),
        "mean": float(arr.mean()),
        "std": float(arr.std(ddof=1)) if arr.size > 1 else float("nan"),
        "min": float(arr.min()),
        "q25": float(np.percentile(arr, 25)),
        "median": float(np.median(arr)),
        "q75": float(np.percentile(arr, 75)),
        "max": float(arr.max()),
    }


def mean_ci(data: Sequence[float], confidence: float = 0.95) -> ConfidenceInterval:
    """t-based confidence interval for the population mean."""
    if not 0 < confidence < 1:
        raise ValueError("confidence must be in (0, 1)")
    arr = np.asarray(data, dtype=float)
    n = arr.size
    if n < 2:
        raise ValueError("need at least 2 observations for a mean CI")
    mean = float(arr.mean())
    sem = float(_scipy_stats.sem(arr))
    half = sem * _scipy_stats.t.ppf((1 + confidence) / 2, df=n - 1)
    return ConfidenceInterval(mean, mean - half, mean + half, confidence)


def bootstrap_ci(
    data: Sequence[float],
    statistic: Callable[[np.ndarray], float] = np.mean,
    confidence: float = 0.95,
    n_resamples: int = 10_000,
    seed: int | None = None,
) -> ConfidenceInterval:
    """Percentile bootstrap CI for an arbitrary statistic.

    Useful when the sampling distribution is unknown or the statistic is not a
    simple mean (e.g. median, ratio, Gini).
    """
    if not 0 < confidence < 1:
        raise ValueError("confidence must be in (0, 1)")
    arr = np.asarray(data, dtype=float)
    if arr.size == 0:
        raise ValueError("data must be non-empty")
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, arr.size, size=(n_resamples, arr.size))
    resampled = np.array([statistic(arr[row]) for row in idx])
    alpha = 1 - confidence
    low, high = np.percentile(resampled, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return ConfidenceInterval(float(statistic(arr)), float(low), float(high), confidence)
