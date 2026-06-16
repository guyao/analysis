"""Tests for utils.money, including the property tests required by CLAUDE.md:

* integer-cent arithmetic loses no precision;
* allocation conserves the total (sum of parts == total).
"""

from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from utils import money


def test_to_cents_avoids_float_artifacts():
    assert money.to_cents(0.1) + money.to_cents(0.2) == money.to_cents(0.3)
    assert money.to_cents("19.99") == 1999
    assert money.to_cents(Decimal("19.99")) == 1999


def test_round_trip():
    assert money.from_cents(1999) == Decimal("19.99")
    assert money.from_cents(money.to_cents("123.45")) == Decimal("123.45")


# --- property: integer-cent arithmetic loses no precision -------------------
@given(
    st.lists(st.integers(min_value=-10_000_000, max_value=10_000_000), min_size=1)
)
def test_cent_sum_is_exact(cents):
    # Summing integer cents and converting equals converting then summing.
    via_cents = money.from_cents(sum(cents))
    via_decimal = sum((money.from_cents(c) for c in cents), Decimal("0"))
    assert via_cents == via_decimal


# --- property: allocation conserves the total -------------------------------
@given(
    total=st.integers(min_value=-1_000_000, max_value=1_000_000),
    weights=st.lists(
        st.floats(min_value=0, max_value=1000, allow_nan=False, allow_infinity=False),
        min_size=1,
        max_size=12,
    ).filter(lambda ws: sum(ws) > 0),
)
def test_allocate_conserves_total(total, weights):
    parts = money.allocate(total, weights)
    assert sum(parts) == total
    assert len(parts) == len(weights)


def test_allocate_rejects_zero_weights():
    with pytest.raises(ValueError):
        money.allocate(100, [0, 0, 0])


def test_allocate_largest_remainder_example():
    # 100 cents split three ways: 34/33/33, conserving the cent.
    assert money.allocate(100, [1, 1, 1]) == [34, 33, 33]
