"""Tests for utils.transforms, including the property tests from CLAUDE.md:

* weights sum to 1 after normalization/rebalancing;
* frictionless rebalancing does not change total market value.
"""

import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from utils import transforms

_positive_weights = st.lists(
    st.floats(min_value=1e-6, max_value=1e6, allow_nan=False, allow_infinity=False),
    min_size=1,
    max_size=10,
)


# --- property: normalized weights sum to 1 ----------------------------------
@given(_positive_weights)
def test_normalize_sums_to_one(weights):
    w = transforms.normalize_weights(weights)
    assert np.isclose(w.sum(), 1.0)
    assert np.all(w >= 0)


# --- property: frictionless rebalance preserves total value -----------------
@given(
    weights=_positive_weights,
    total=st.floats(min_value=0, max_value=1e9, allow_nan=False, allow_infinity=False),
)
def test_rebalance_preserves_total_value(weights, total):
    alloc = transforms.rebalance(weights, total)
    assert np.isclose(alloc.sum(), total)


def test_normalize_rejects_negative():
    with pytest.raises(ValueError):
        transforms.normalize_weights([-1, 2])


def test_winsorize_clips_tails():
    s = transforms.winsorize(list(range(101)), lower=0.05, upper=0.95)
    assert s.min() >= 5
    assert s.max() <= 95


def test_zscore_is_standardized():
    s = transforms.zscore([1, 2, 3, 4, 5], ddof=0)
    assert np.isclose(s.mean(), 0.0)
    assert np.isclose(s.std(ddof=0), 1.0)


def test_zscore_rejects_constant():
    with pytest.raises(ValueError):
        transforms.zscore([3, 3, 3])
