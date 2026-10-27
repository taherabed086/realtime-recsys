# 0006: Drop fully duplicated rows (keep one copy)

- Status: accepted
- Date: 2026-10-27

## Problem
After removing zero prices, 30,217 extra rows are exact copies of another row in every column,
including the timestamp to the second. 93% are cart events (28,072), 2,069 are views, 76 are purchases.
Some events repeat up to 41 times in the same second, which looks like a logging problem, not human behavior.

## Options considered
1. Keep one copy of each fully identical row: simple and safe; could remove a real double click in the same second (rare).
2. Keep all rows: loses nothing; cart events get counted many times and inflate their weight in later models (such as ALS).
3. Drop identical events within the same minute: removes more noise; too broad, may remove real behavior.

## Decision
Option 1: `unique(maintain_order=True)` over all columns.

## Why
It is the simplest option that removes the logging duplicates without touching real behavior.

## Consequences
Clean data has 42,349,874 rows, written to `data/processed/events_clean.parquet`.
`maintain_order=True` is required: plain `unique()` shuffled the rows, destroyed the time order
and doubled the file size (1.4 GB instead of 712 MB). The time order is needed for the temporal split.
