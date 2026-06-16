"""Tests for utils.timeseries."""

import numpy as np
import pandas as pd
import pytest

from utils import timeseries as ts


def test_growth_rate_qoq():
    g = ts.growth_rate([100, 110, 99])
    assert np.isclose(g.iloc[1], 0.10)
    assert np.isclose(g.iloc[2], -0.10)


def test_yoy_growth_quarterly():
    data = [100, 101, 102, 103, 110]  # 5 quarters
    g = ts.yoy_growth(data, periods_per_year=4)
    assert np.isclose(g.iloc[4], 0.10)  # Q5 vs Q1


def test_cagr_doubling_over_3_years():
    assert np.isclose(ts.cagr(100, 200, 3), 2 ** (1 / 3) - 1)


def test_cagr_rejects_nonpositive():
    with pytest.raises(ValueError):
        ts.cagr(0, 100, 2)
    with pytest.raises(ValueError):
        ts.cagr(100, 100, 0)


def test_index_to_base():
    s = ts.index_to_base([50, 75, 100], base=100)
    assert np.isclose(s.iloc[0], 100)
    assert np.isclose(s.iloc[1], 150)
    assert np.isclose(s.iloc[2], 200)


def test_lead_lag_detects_known_lag():
    # response is the driver shifted forward by 2 periods => driver leads by 2.
    rng = np.random.default_rng(0)
    driver = pd.Series(rng.normal(size=40))
    response = driver.shift(2)
    result = ts.lead_lag_correlation(driver, response, max_lag=5)
    assert result.best_lag == 2
    assert result.best_corr > 0.99


def test_lead_lag_zero_lag_for_aligned_series():
    rng = np.random.default_rng(1)
    driver = pd.Series(rng.normal(size=40))
    result = ts.lead_lag_correlation(driver, driver, max_lag=4)
    assert result.best_lag == 0
    assert np.isclose(result.best_corr, 1.0)
