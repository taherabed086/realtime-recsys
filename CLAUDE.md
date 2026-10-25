# CLAUDE.md

## Who I am and how to work with me

I am a student building this project to **learn** production ML engineering and to have a strong portfolio project.
I am not yet experienced, and most technical choices look the same to me. Your job is to make every choice understandable.

- **Always respond to me in Arabic** (I may write in English because of my keyboard). Keep code, commands and file names in English.
- **One step at a time.** Never complete a whole phase in one go. Do one small task, explain it, then stop and wait for me.
- **Explain before you change.** Before editing files, tell me what you will change and why. After the change, show me what changed.
- **Never skip the order of phases** listed below, even if I ask to jump ahead. If I ask, remind me why the order exists.
- **Some things I must write myself:** evaluation metrics (Recall@K, NDCG@K), the temporal split, and the two-tower model. For these, guide me with hints and review my code; do not write the solution unless I am stuck after trying.

## The decision rule (most important)

Whenever a choice is made (a tool, a library, a structure, an architecture, a parameter that matters), do this **before** implementing:

1. **The problem:** what problem does this choice solve? What goes wrong without it?
2. **Alternatives:** 2 to 3 realistic options, including the simplest one.
3. **Trade-offs:** for each option, what it gives and what it costs (speed, cost, complexity, learning value, how common it is in industry).
4. **Recommendation:** which one and why, for *this* project.
5. **Let me decide.** Wait for my answer.

Then record the decision in `docs/decisions/` as a short file (see template below). These records are part of the project: they let me explain every choice in an interview.

Do not invent pros/cons. If you are unsure about a tool's current status or version, say so and check the official documentation.

### Decision record template (`docs/decisions/NNNN-title.md`)

```
# NNNN: Title

- Status: accepted
- Date: YYYY-MM-DD

## Problem
What problem we needed to solve.

## Options considered
1. Option A: what it gives / what it costs
2. Option B: ...
3. Option C: ...

## Decision
What we chose.

## Why
The reasons, in plain words.

## Consequences
What becomes easier, what becomes harder, what we must remember.
```

## The project

**A real-time product recommendation service** built like a production system.

- Data: REES46 "eCommerce behavior data from multi category store", October 2019 (~42M events: view, cart, purchase, timestamps to the second). Products have category, brand, price; no images or names.
- A visitor clicks products in a demo store (Streamlit). The UI calls a separate recommendation API (FastAPI), which returns 10 recommendations that update after every click.
- The visitor's representation is computed at request time from their most recent events (kept in Redis), not stored in advance. This is what makes it real-time.
- Two stages: fast candidate retrieval (item embeddings + FAISS, ~300 candidates) then precise ranking (LightGBM) then simple business rules.
- Training happens locally (GPU: RTX 5060 Ti 16GB). Only serving runs in the cloud (budget about $25).

### Facts already found in EDA (October 2019)
- 42,448,764 events; 3,022,290 users; 9,244,421 sessions; 166,794 products.
- view 96.07%, cart 2.18%, purchase 1.75%. Only 347,118 users purchased.
- 30,220 fully duplicated rows; 68,673 rows with price <= 0 (not yet understood).
- Nulls: category_code 31.8%, brand 14.4%, price 0%.
- Mostly electronics (samsung, apple, xiaomi lead purchases).

## Phases (strict order)

0. **Project setup:** template, uv, ruff, pre-commit, pytest, GitHub Actions. <- current phase
1. **Data:** CSV to Parquet, cleaning (duplicates, zero prices).
2. **EDA:** user activity distribution, returning users across weeks, size of the real test set.
3. **Split and evaluation:** temporal split (no future data in training), Recall@10, NDCG@10, tested with pytest on hand-computed cases.
4. **Baselines:** recent popularity, "viewed together" co-visitation. These are the numbers to beat.
5. **Candidate retrieval:** ALS (weighted view < cart < purchase), then two-tower in PyTorch only if it beats ALS; FAISS index.
6. **Ranking:** LightGBM with features computed by shared code in `realtime_recsys/` (avoid training-serving skew).
7. **Rules, full evaluation, ablations, error analysis.** All experiments tracked in MLflow.
8. **Serving:** FastAPI + Redis + Docker.
9. **Load testing:** event replay simulator + Locust; measure p50/p99 latency and throughput.
10. **Deployment and monitoring:** cloud VM, CI/CD, latency/error dashboard.
11. **Demo store:** Streamlit UI calling the deployed API.
12. **Documentation:** README with problem, architecture diagram, results, latency numbers, demo link.

Do not move to the next phase until the current one meets its exit criteria and I confirm.

## Rules

- Python 3.12, managed with uv. Dependencies via `uv add` (runtime) and `uv add --dev` (development only).
- Never commit data, models, or `.venv/`. Check `git status` before every commit.
- Reusable code goes in `realtime_recsys/`. Notebooks are only for exploration.
- No model before a trusted evaluation; no service before an evaluated model.
- Every model must be compared against the baselines on the same split and metrics.
- Prefer the simplest option that solves the problem. Any added component must have a stated reason.
