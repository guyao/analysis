"""Data IO and provenance helpers.

These helpers encode two invariants from CLAUDE.md:

* ``data/raw/`` is immutable — :func:`write_processed` refuses to write there.
* every source is logged — :func:`log_source` appends to ``sources.md``.
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path

import pandas as pd

__all__ = [
    "project_paths",
    "read_raw",
    "write_processed",
    "log_source",
]


def project_paths(project_dir: str | Path) -> dict[str, Path]:
    """Return the standard sub-paths for a project directory."""
    root = Path(project_dir)
    return {
        "root": root,
        "raw": root / "data" / "raw",
        "processed": root / "data" / "processed",
        "scripts": root / "scripts",
        "figures": root / "output" / "figures",
        "tables": root / "output" / "tables",
        "sources": root / "sources.md",
    }


def read_raw(path: str | Path, **kwargs) -> pd.DataFrame:
    """Read a raw data file (CSV/Parquet/JSON) into a DataFrame."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"raw file not found: {p}")
    suffix = p.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(p, **kwargs)
    if suffix in {".parquet", ".pq"}:
        return pd.read_parquet(p, **kwargs)
    if suffix in {".json", ".ndjson"}:
        return pd.read_json(p, **kwargs)
    raise ValueError(f"unsupported raw file type: {suffix}")


def write_processed(df: pd.DataFrame, path: str | Path, **kwargs) -> Path:
    """Write a derived DataFrame, refusing to write into ``data/raw/``."""
    p = Path(path)
    if "raw" in p.parts and "data" in p.parts:
        raise ValueError(
            "data/raw/ is append-only and must not be written by code; "
            "write derived data under data/processed/ instead"
        )
    p.parent.mkdir(parents=True, exist_ok=True)
    suffix = p.suffix.lower()
    if suffix == ".csv":
        df.to_csv(p, index=kwargs.pop("index", False), **kwargs)
    elif suffix in {".parquet", ".pq"}:
        df.to_parquet(p, **kwargs)
    else:
        raise ValueError(f"unsupported processed file type: {suffix}")
    return p


def log_source(
    sources_path: str | Path,
    url: str,
    description: str,
    access_date: str | None = None,
) -> Path:
    """Append a data source entry to ``sources.md``.

    Creates the file with a header if it does not yet exist. ``access_date``
    defaults to today (UTC) in ISO format.
    """
    p = Path(sources_path)
    access_date = access_date or _dt.date.today().isoformat()
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# Sources\n\n| URL | Access date | Description |\n| --- | --- | --- |\n")
    safe_desc = description.replace("|", "\\|").replace("\n", " ")
    with p.open("a", encoding="utf-8") as fh:
        fh.write(f"| {url} | {access_date} | {safe_desc} |\n")
    return p
