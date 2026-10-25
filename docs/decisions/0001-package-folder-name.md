# 0001: Name and location of the code package

- Status: accepted
- Date: 2026-10-25

## Problem
CLAUDE.md said reusable code goes in `src/`, but the cookiecutter template
already created the package folder `realtime_recsys/`. We needed one agreed place for the code.

## Options considered
1. Keep `realtime_recsys/` at the project root: gives zero changes and the common
   cookiecutter layout; costs a small edit to CLAUDE.md (it said `src/`).
2. `src/realtime_recsys/` (src layout): the usual choice for published libraries and it
   avoids accidentally importing the package without installing it; costs moving the
   folder and changing `pyproject.toml` settings.
3. Rename to plain `src/`: matches the old CLAUDE.md wording; costs a generic,
   non-descriptive package name (`import src`) and is less common.

## Decision
Keep `realtime_recsys/` at the project root (option 1).

## Why
It is the simplest option and needs no moves or config changes. This project is an
application, not a library to publish, so the extra safety of the src layout is not needed now.

## Consequences
All reusable code lives in `realtime_recsys/` and is imported as
`from realtime_recsys.xxx import ...`. CLAUDE.md was updated to say `realtime_recsys/`
instead of `src/`. If we ever publish the code as a library, we can revisit this.
