"""Tests for utils.io."""

import pandas as pd
import pytest

from utils import io


def test_project_paths_layout(tmp_path):
    paths = io.project_paths(tmp_path / "proj")
    assert paths["raw"].parts[-2:] == ("data", "raw")
    assert paths["processed"].parts[-2:] == ("data", "processed")
    assert paths["sources"].name == "sources.md"


def test_write_processed_round_trip(tmp_path):
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    out = io.write_processed(df, tmp_path / "data" / "processed" / "x.csv")
    assert out.exists()
    back = io.read_raw(out)  # CSV reader works for any CSV
    pd.testing.assert_frame_equal(df, back)


def test_write_processed_refuses_raw(tmp_path):
    df = pd.DataFrame({"a": [1]})
    with pytest.raises(ValueError):
        io.write_processed(df, tmp_path / "data" / "raw" / "x.csv")


def test_log_source_appends(tmp_path):
    sources = tmp_path / "sources.md"
    io.log_source(sources, "https://example.com", "Example dataset", "2026-06-16")
    io.log_source(sources, "https://example.org", "Second | source", "2026-06-16")
    text = sources.read_text()
    assert "https://example.com" in text
    assert "Second \\| source" in text  # pipe escaped for the markdown table
    assert text.count("\n|") >= 3  # header + separator + 2 rows
