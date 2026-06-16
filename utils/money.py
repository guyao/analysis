"""Precision-safe money arithmetic.

Money is represented internally as an integer number of cents so that no
floating-point rounding error can accumulate. Conversions from human-facing
decimal amounts go through :class:`decimal.Decimal` to avoid binary float
artifacts (e.g. ``0.1 + 0.2``).
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Sequence

__all__ = ["to_cents", "from_cents", "allocate"]


def to_cents(amount: str | int | float | Decimal) -> int:
    """Convert a decimal currency amount to an integer number of cents.

    Floats are accepted for convenience but are first stringified so the value
    the user *sees* is what gets rounded, not its binary approximation.
    Half-way values round up (banker-free, matches everyday money rounding).
    """
    if isinstance(amount, float):
        amount = repr(amount)
    dec = Decimal(amount)
    return int((dec * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def from_cents(cents: int) -> Decimal:
    """Convert integer cents back to a two-decimal :class:`Decimal` amount."""
    if not isinstance(cents, int):
        raise TypeError(f"cents must be an int, got {type(cents).__name__}")
    return (Decimal(cents) / 100).quantize(Decimal("0.01"))


def allocate(total_cents: int, weights: Sequence[float]) -> list[int]:
    """Split ``total_cents`` across ``weights`` with no remainder lost.

    Uses the largest-remainder (Hamilton) method: each bucket gets the floor of
    its ideal share, then the leftover cents go one-by-one to the buckets with
    the largest fractional remainders. The returned integers always sum exactly
    to ``total_cents``.
    """
    if not isinstance(total_cents, int):
        raise TypeError("total_cents must be an int (cents)")
    if len(weights) == 0:
        raise ValueError("weights must be non-empty")
    if any(w < 0 for w in weights):
        raise ValueError("weights must be non-negative")

    weight_total = sum(weights)
    if weight_total <= 0:
        raise ValueError("weights must sum to a positive value")

    # Work with the sign separately so flooring behaves for negative totals.
    sign = -1 if total_cents < 0 else 1
    magnitude = abs(total_cents)

    ideal = [magnitude * w / weight_total for w in weights]
    floors = [int(x) for x in ideal]
    remainder = magnitude - sum(floors)

    # Distribute leftover cents to the largest fractional parts.
    order = sorted(
        range(len(weights)),
        key=lambda i: (ideal[i] - floors[i], weights[i]),
        reverse=True,
    )
    for i in order[:remainder]:
        floors[i] += 1

    return [sign * c for c in floors]
