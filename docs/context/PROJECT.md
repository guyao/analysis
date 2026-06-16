# PROJECT

High-level description of what this repository is and how it is organized.

## Purpose
A meta-repository for reproducible quantitative research. Each research task
lives in its own `<project_name>/` directory; shared, tested helpers live in
`utils/`. Every quantitative conclusion is derived through executed code and
traceable to a cited source.

## Operating contract
- `CLAUDE.md` is the operational contract for any agent working here.
- `GEMINI.md` is the original framework specification (intent / source of truth).

## Components
- `utils/` — common library (IO, money, transforms, stats, plotting).
- `tests/` — pytest + hypothesis property tests for the library.
- `scripts/new_project.py` — scaffolds a new project skeleton.
- `docs/context/` — durable working memory (this file and the three below).

## Current projects
_None yet. Create one with `python scripts/new_project.py <name>`._
