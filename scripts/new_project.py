#!/usr/bin/env python3
"""Scaffold a new research project skeleton.

Usage:
    python scripts/new_project.py <project_name> [--title "Research question"]

Creates the mandatory per-project structure described in CLAUDE.md:

    <project_name>/
    ├── README.md
    ├── data/{raw,processed}/
    ├── scripts/
    ├── output/{figures,tables}/
    └── sources.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DIRS = [
    "data/raw",
    "data/processed",
    "scripts",
    "output/figures",
    "output/tables",
]

GITKEEP_DIRS = [
    "data/raw",
    "data/processed",
    "output/figures",
    "output/tables",
]

README_TEMPLATE = """\
# {title}

## Research question
<!-- Restate the question as a precise, falsifiable analytical question. -->

## Hypotheses
- H1:
- H2:

## Metrics & data needed
<!-- What must be computed, and which data feeds each metric. -->

## Conclusions
<!-- Filled in after analysis; every number traceable to code + a source. -->

## How to reproduce
```bash
# Run the pipeline in order on the raw data:
python scripts/01_collect.py
python scripts/02_clean.py
python scripts/03_analyze.py
```
Re-running these reproduces every file in `data/processed/` and `output/`.
"""

SOURCES_TEMPLATE = """\
# Sources

| URL | Access date | Description |
| --- | --- | --- |
"""

COLLECT_STUB = '''\
"""01_collect.py — pull raw data into data/raw/ and log every source.

data/raw/ is append-only; never edit files there by hand.
"""

from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent

# Example:
# from utils import io
# io.log_source(PROJECT / "sources.md", url, "what this dataset is")


def main() -> None:
    raise NotImplementedError("collect raw data here")


if __name__ == "__main__":
    main()
'''


def create_project(name: str, title: str | None) -> Path:
    project = REPO_ROOT / name
    if project.exists():
        print(f"error: {project} already exists", file=sys.stderr)
        sys.exit(1)

    for rel in DIRS:
        (project / rel).mkdir(parents=True, exist_ok=True)
    for rel in GITKEEP_DIRS:
        (project / rel / ".gitkeep").touch()

    (project / "README.md").write_text(
        README_TEMPLATE.format(title=title or name)
    )
    (project / "sources.md").write_text(SOURCES_TEMPLATE)
    (project / "scripts" / "01_collect.py").write_text(COLLECT_STUB)

    return project


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="project directory name (e.g. ev_adoption_2026)")
    parser.add_argument("--title", default=None, help="human-readable research title")
    args = parser.parse_args()

    project = create_project(args.name, args.title)
    print(f"created project skeleton at {project.relative_to(REPO_ROOT)}/")


if __name__ == "__main__":
    main()
