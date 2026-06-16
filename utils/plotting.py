"""Plotting wrappers.

Defaults to the headless ``Agg`` backend so figures render and save in CI and
non-interactive sessions. Each helper returns the Matplotlib ``Figure`` so the
caller can further customize before saving.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import matplotlib

matplotlib.use("Agg")  # noqa: E402  (must precede pyplot import)
import matplotlib.pyplot as plt  # noqa: E402

__all__ = ["apply_default_style", "save_figure", "line_chart", "bar_chart"]


def apply_default_style() -> None:
    """Apply a clean, report-friendly default style."""
    plt.rcParams.update(
        {
            "figure.figsize": (9, 5),
            "figure.dpi": 110,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "font.size": 11,
        }
    )


def save_figure(fig: plt.Figure, path: str | Path, dpi: int = 150) -> Path:
    """Save a figure, creating parent directories as needed."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=dpi, bbox_inches="tight")
    return out


def line_chart(
    x: Sequence[float],
    y: Sequence[float],
    *,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    label: str | None = None,
) -> plt.Figure:
    """Return a simple line chart figure."""
    fig, ax = plt.subplots()
    ax.plot(x, y, label=label)
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    if label:
        ax.legend()
    return fig


def bar_chart(
    categories: Sequence[str],
    values: Sequence[float],
    *,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
) -> plt.Figure:
    """Return a simple bar chart figure."""
    fig, ax = plt.subplots()
    ax.bar(categories, values)
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    fig.autofmt_xdate(rotation=45)
    return fig
