---
name: data-quality-check
description: Use when the user says "check that X populates", "did the new column roll out correctly", "does this data look right", "reconcile A with B", or "why do these two numbers differ". Picks checks from a menu, runs them, gives each a pass, warn or fail verdict with evidence, and files the result in dq/.
---

# Data-quality check

The deliverable is a verdict, not a narrative: `dq/YYYY-MM-DD_topic/check.md` with a verdict per check and a receipt, the SQL that ran, and a row in `dq/INDEX.md`. No findings narrative, and a chart only when it makes a verdict clearer.

## Step 1: Pin the scope

Settle with the user before the first query, in plain free text, at most three questions per round: what is under check (a table, a column, two numbers), the window and its timezone, and what "correct" means here (a clean rollout from a date, a match to another source within a tolerance, full coverage of an expected list). A check with no stated expectation cannot fail, so it proves nothing.

Read the table docs for everything you will touch. A table with no doc gets a stub through `skills/onboard-table/SKILL.md` before its numbers are used.

## Step 2: Pick the checks

Pick the checks that test the user's idea of "correct". Write each threshold down before running it: a threshold chosen after seeing the result is not a check.

| Check | Catches | How |
|---|---|---|
| Schema and types | a column missing, renamed or retyped | the schema through `docs/access.md`, against the table doc |
| Completeness and null rates | an empty or partly filled column | null rate per day, and per segment if a rollout could differ; the date filling starts |
| Freshness and gaps | stale data, missing or half-loaded days | the latest date against today; rows per day, looking for missing days and days far below their weekday's usual level |
| Uniqueness of the key | duplicates, a wrong grain | row count against distinct key count; nulls in the key make it unprovable, never a pass |
| Referential consistency | orphan rows, one code with several labels | keys with no match in the table they point to; codes mapping to more than one label |
| Value hygiene | placeholder and junk values | empty strings, `null` or `undefined` as text, zeros meaning missing, values outside the documented set, future dates |
| Parts sum to the whole | a stray total row, a dropped or new segment | segments' sum against the total; segment values against the expected list |
| Ratio bounds | a fan-out in the numerator, a lost denominator | every rate between 0 and 1, or inside the band the metric allows |
| Reconciliation with a second source | two systems that should agree but do not | the same measure from both for the same window, against a tolerance stated in advance; on a gap, the procedure below |
| Mix shift | a rate that moved because the mix moved | each segment's rate and share in both periods; how much of the total's change comes from shares rather than rates |

Every query goes through `skills/sql-preflight/SKILL.md`, stays within the `docs/access.md` limits, and is saved as it runs.

## Two numbers disagree

When someone holds two numbers for what they take to be one metric:

1. **Write both down exactly as quoted:** the value, its source, and the window it claims, plus the SQL or definition behind it. A side you cannot read is marked unknown and named under Not checked.
2. **Run the asker's SQL unchanged first** as the control. Before trusting a rewrite of your own, confirm it reproduces a period whose answer is known. A result that contradicts a number the asker can reproduce is a suspicion about your query before it is a finding about the data.
3. **State the tolerance** that counts as agreement.
4. **Align the sides one axis at a time, in this order:** definition (numerator, denominator, metric file), window boundaries, timezone, filters and exclusions, grain and deduplication, and only then the source. After each axis, apply one side's choice to the other, measure again, and record how much of the gap closed. Stop when the gap is within the tolerance.
5. **Conclude with one of:** **expected** (a genuine definition difference: name the axis and the side that fits the question), **bug** (name the wrong side and the axis), or **unresolved** (the gap stays above the tolerance after every axis: state it and the axes tried). Never "both are right" without the axis that separates them.

In `check.md`, expected is a `pass` with the axis named, bug is a `fail`, unresolved is a `warn`.

## Step 3: Give each check a verdict

- **pass:** the result meets the threshold.
- **warn:** usable with a stated caveat, or the check could not be evaluated (nulls in a key, too little history). Say which.
- **fail:** wrong, or not usable for the purpose stated in Step 1.

Each verdict carries the number observed, the threshold and the query file. The overall verdict is the worst one.

## Step 4: File it

Create `dq/YYYY-MM-DD_topic/` (today's date from the system clock, a topic in lowercase hyphenated words) holding:

- `queries_used/` with every query exactly as run, numbered in run order (`01_null_rate_by_day.sql`).
- Small result files only when a verdict needs them as evidence.
- `check.md`, in this shape:

```markdown
# <What was checked>

**Overall verdict:** pass | warn | fail. <one line: usable, usable with a caveat, or blocked, and why>

## Scope
What is under check, the window and timezone, and what "correct" means here.

## Checks
| Check | Threshold | Observed | Verdict | Query |
|---|---|---|---|---|

## Definition diff
Reconciliation only: both numbers as quoted, the gap closed per axis, the remaining gap against the tolerance, the conclusion.

## Recommendation
Use the data, wait, or raise it upstream. Never try to fix upstream data yourself.

## Receipt
```

The receipt is copied from `templates/receipt.md` with every field filled and `Not checked` never empty. Then add a row to `dq/INDEX.md` with the folder, what was checked, and the overall verdict.

## Step 5: Write back what you learned

- A failed or warned check that reveals a trap someone could fall into again is written down now. Visible in the SQL text (a column that must always be filtered, a join that fans out): an entry in `docs/sql-checks.md` in its format. Visible only in the data (a column unreliable before a date, a junk value): a Gotcha in the table doc.
- A table doc the check proved wrong gets fixed; if an earlier answer relied on it, add a `docs/corrections.md` entry.

## Done when

- `check.md` has a verdict with evidence per check, an overall verdict, and a receipt with `Not checked` filled in.
- Every query that ran passed preflight and is in `queries_used/`; `dq/INDEX.md` has its row.
- Every table touched has at least a stub doc, and any trap found is recorded.
