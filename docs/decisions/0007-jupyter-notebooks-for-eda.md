# 0007: Jupyter notebooks in VS Code for exploration

- Status: accepted
- Date: 2026-10-27

## Problem
EDA needs a place to run questions one after another, see tables and charts immediately,
and keep notes next to the results.

## Options considered
1. Jupyter notebooks inside VS Code: run cell by cell, results and charts shown inline, the standard tool for data exploration; needs `ipykernel` and `matplotlib` as dev dependencies.
2. Plain Python scripts: no extra dependencies; no inline charts, and each question reruns from scratch.

## Decision
Option 1: notebooks in `notebooks/`, using the project `.venv` kernel.

## Why
It is the most common way to explore data and it fits the existing template folder.
Notebooks are for exploration only. Code that becomes permanent moves to `realtime_recsys/`.

## Consequences
`ipykernel` and `matplotlib` are dev dependencies (not installed on the server).
Notebooks must not contain data and must not be relied on for production logic.
