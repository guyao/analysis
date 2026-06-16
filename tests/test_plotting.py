"""Tests for utils.plotting (headless)."""

from utils import plotting


def test_save_figure_creates_file(tmp_path):
    plotting.apply_default_style()
    fig = plotting.line_chart([0, 1, 2], [1, 3, 2], title="t", label="series")
    out = plotting.save_figure(fig, tmp_path / "figs" / "line.png")
    assert out.exists()
    assert out.stat().st_size > 0


def test_bar_chart_returns_figure(tmp_path):
    fig = plotting.bar_chart(["a", "b"], [1, 2], title="bars")
    out = plotting.save_figure(fig, tmp_path / "bar.png")
    assert out.exists()
