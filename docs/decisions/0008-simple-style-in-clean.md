# 0008: Simple (eager) Polars style in clean.py

- Status: accepted
- Date: 2026-10-28

## Problem
`clean.py` was written in lazy style (`scan_parquet`, `LazyFrame`, `sink_parquet`) to save memory.
That is harder to read for a beginner, and it is no longer needed for the cleaned data:
the table takes about 4 GB in memory and the laptop now has about 9 GB free.

## Options considered
1. Keep the lazy style: tested, lowest memory; harder to read and explain.
2. Eager style in `clean.py` only (`read_parquet`, `DataFrame`, `write_parquet`): reads like pandas; needs about 4 GB of RAM during cleaning.
3. Eager style everywhere: simplest; reading the full 5.3 GB CSV in `dataset.py` is risky for memory.

## Decision
Option 2. `dataset.py` stays lazy because the raw CSV is much larger in memory than the Parquet.

## Why
Readability matters for learning and for the portfolio, and the memory now fits.

## Consequences
Cleaning takes about 1 minute (it was a few seconds) and uses about 4 GB of RAM.
The output was compared with the previous file: same rows, `equals` is True.
Tests now use `DataFrame` and no longer call `collect()`. A new test checks that row order is kept.
