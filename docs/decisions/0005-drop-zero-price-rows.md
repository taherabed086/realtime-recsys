# 0005: Drop rows with price equal to zero

- Status: accepted
- Date: 2026-10-27

## Problem
68,673 rows (0.16%) have price 0. Investigation showed: no negative prices, 99.8% are views
(150 carts, 0 purchases), they appear on all days with peaks on Oct 8-9 and Oct 24-25, and
9,948 of the 11,095 affected products have positive prices in other rows. So zero means a missing price, not a free product.

## Options considered
1. Drop all zero-price rows: simplest code and every remaining price is trustworthy; loses 0.16% of events.
2. Replace zero with the product median price and drop only the 8,030 rows of products with no known price: keeps about 60 thousand events; more code and an extra choice (median or last price).
3. Keep rows and add a flag: loses nothing; a later model might treat 0 as a real price.

## Decision
Option 1: drop all rows where price <= 0.

## Why
The share is tiny, so the effect on results is negligible, and prices matter later in ranking where a wrong price hurts.

## Consequences
Clean data is written to `data/processed/events_clean.parquet`. If error analysis (phase 7) shows
the lost events matter, we can revisit option 2.
