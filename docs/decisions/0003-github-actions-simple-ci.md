# 0003: Simple GitHub Actions CI

- Status: accepted
- Date: 2026-10-26

## Problem
Local pre-commit checks only run on our own machine. Broken code could still reach `main`.

## Options considered
1. One simple workflow (install with uv, run ruff and pytest on Linux): simplest and most common; checks only one OS and Python version.
2. Matrix workflow (several OS and Python versions): wider coverage; slower and more complex, and not needed because serving runs on one Linux VM.
3. No CI for now: no work; mistakes are found late.

## Decision
Option 1: a single workflow `.github/workflows/ci.yml`.

## Why
It solves the problem with the least complexity. The project targets Python 3.12 on one Linux server.

## Consequences
Every push to `main` and every pull request runs ruff and pytest. `uv sync --locked`
fails if `uv.lock` is out of date, which keeps installs reproducible. We can add steps later
(for example Docker build in phase 8).
