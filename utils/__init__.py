"""Shared, tested common library for reproducible quantitative research.

Promote any calculation reused across >=2 projects into this package, with
tests. Keep project-specific logic in each project's ``scripts/``.
"""

from . import io, money, plotting, stats, timeseries, transforms

__all__ = ["io", "money", "plotting", "stats", "timeseries", "transforms"]
__doc_modules__ = (
    "io: project paths, raw/processed IO, source logging",
    "money: precision-safe integer-cent arithmetic",
    "transforms: weights, rebalancing, outliers, z-scores",
    "stats: summary stats, confidence intervals, bootstrap",
    "timeseries: growth, CAGR, indexing, lead-lag correlation",
    "plotting: headless matplotlib styling and save helpers",
)
__version__ = "0.1.0"
