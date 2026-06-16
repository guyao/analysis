"""Tests for utils.stats."""

import numpy as np
import pytest

from utils import stats


def test_summary_stats_keys():
    out = stats.summary_stats([1, 2, 3, 4])
    assert out["n"] == 4
    assert out["mean"] == 2.5
    assert out["median"] == 2.5
    assert out["min"] == 1 and out["max"] == 4


def test_mean_ci_brackets_mean():
    data = list(range(1, 101))
    ci = stats.mean_ci(data, confidence=0.95)
    assert ci.low < ci.point < ci.high
    assert np.isclose(ci.point, np.mean(data))


def test_mean_ci_requires_two_points():
    with pytest.raises(ValueError):
        stats.mean_ci([5.0])


def test_bootstrap_ci_is_deterministic_with_seed():
    data = list(range(50))
    a = stats.bootstrap_ci(data, seed=42, n_resamples=1000)
    b = stats.bootstrap_ci(data, seed=42, n_resamples=1000)
    assert a == b
    assert a.low < a.point < a.high


def test_bootstrap_ci_median_statistic():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
    ci = stats.bootstrap_ci(data, statistic=np.median, seed=1, n_resamples=2000)
    assert ci.low <= ci.point <= ci.high
