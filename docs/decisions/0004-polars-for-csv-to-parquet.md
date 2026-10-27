# 0004: Polars for CSV to Parquet conversion and data processing

- Status: accepted
- Date: 2026-10-27

## Problem
The raw CSV is 5.3 GB (42M rows) and the laptop has about 6 GB of free RAM. Loading it fully
with the default pandas approach would likely freeze or crash. It is also slow to read as text,
and it does not store column types.

## Options considered
1. Polars: reads and writes in streaming mode without loading the whole file, uses all CPU cores,
   very short code; newer than pandas, so fewer tutorials.
2. DuckDB: also streams from CSV to Parquet with one SQL statement; adds SQL as a second language to the project.
3. pandas in chunks: most familiar and most tutorials; slower and needs extra code to read chunks and merge them.

## Decision
Polars (option 1).

## Why
It is the simplest code for this task, it is fast, and it works within the laptop memory.
It can also be used for the cleaning step and the EDA later.

## Consequences
Data code uses the Polars API instead of pandas. Parquet files go to `data/interim/` (ignored by git).
Conversion is raw: no rows are removed. Cleaning is a separate step.
