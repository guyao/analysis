# STATE

Read this at the **start** of every session; update it at the **end**.

## Last updated
2026-06-16

## Current status
Repository scaffolded. `CLAUDE.md` (operational contract), the `utils/` common
library, its test suite, the project generator, and the context docs are in
place. No research projects created yet.

## Done
- Authored `CLAUDE.md` (optimized from `GEMINI.md`).
- Built `utils/` library: `io`, `money`, `transforms`, `stats`, `plotting`.
- Added `tests/` with pytest + hypothesis property tests (all passing).
- Added `scripts/new_project.py` scaffolder and `docs/context/` files.
- Pinned the stack in `requirements.txt`; added `pyproject.toml`.

## Next steps
- Instantiate the first research project with `python scripts/new_project.py <name>`.
- Grow `utils/` as helpers are reused across >=2 projects.
