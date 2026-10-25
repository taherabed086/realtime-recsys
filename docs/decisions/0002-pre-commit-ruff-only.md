# 0002: Pre-commit with ruff only

- Status: accepted
- Date: 2026-10-25

## Problem
Without automatic checks, badly formatted code or lint errors can be committed by mistake.

## Options considered
1. pre-commit with ruff only: simplest, checks and formats code on every commit; does not guard against big files.
2. pre-commit with ruff plus extra hooks (large-file check, trailing whitespace): also blocks accidental big data files; longer config.
3. No pre-commit, rely on CI only: no setup; errors are found only after pushing.

## Decision
Option 1: pre-commit with ruff (check + format) only.

## Why
It is the simplest option that solves the problem. Big data files are already
protected by `/data/` and `/models/` in `.gitignore`.

## Consequences
Every commit runs ruff first and is rejected if it fails. We can add more hooks later if needed.
