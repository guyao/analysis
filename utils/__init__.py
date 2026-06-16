"""Shared, tested common library for reproducible quantitative research.

Promote any calculation reused across >=2 projects into this package, with
tests. Keep project-specific logic in each project's ``scripts/``.
"""

from . import io, money, plotting, stats, transforms

__all__ = ["io", "money", "plotting", "stats", "transforms"]
__version__ = "0.1.0"
