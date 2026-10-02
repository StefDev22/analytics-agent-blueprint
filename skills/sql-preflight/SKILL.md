---
name: sql-preflight
description: Use before any SQL is saved or run, including one-off, catalog and test queries, and whenever a query changes. A reading checklist: ten generic checks, then every entry in docs/sql-checks.md, one PASS, WARN, FAIL or NA line each. Any FAIL blocks the save or run until fixed.
---

# SQL preflight

Read the SQL against this checklist before it is saved or run. Any FAIL blocks: fix it and run the whole checklist again. A FAIL is fixed, never waived (`AGENTS.md`, hard rule 3). Any edit, even one character, needs a new preflight.

**This is a reading checklist, not a parser.** It catches what a careful reader catches and can miss what a reader misses. It does not replace a read-only credential, the only real guarantee against a write (`docs/access.md`).

Have open: `docs/access.md`, the `docs/tables/` doc for every table read, any `metrics/` file computed, and `docs/sql-checks.md`.

## The generic checks

**P1 Read-only.** One statement, starting with `SELECT`, `WITH` or the dialect's read-only catalog command. FAIL: more than one statement, or any write or DDL anywhere, including inside a CTE, subquery or scripting block: insert, update, delete, merge, create, alter, drop, truncate, grant, revoke, `SELECT ... INTO` a new table, a procedure call, dynamic SQL, an export or copy, or the dialect's equivalent. WARN: a write keyword only inside a string or comment.

**P2 Documented tables.** FAIL: a table read has no doc in `docs/tables/`; write a stub through `skills/onboard-table/SKILL.md`. NA: catalog-only queries, and the schema and profiling queries `onboard-table` runs on the table it is onboarding, because they exist to write that doc; say so in the reason.

**P3 Partition or date filter.** Each table whose doc says a partition or date filter is needed, for cost or for correctness, is filtered on it in the first CTE that reads it. FAIL: missing. WARN: the column is wrapped in a function the doc does not say still prunes. NA, with the reason: the doc asks for no filter (not partitioned, or a small dimension table), the logic needs the full history (first-ever events, lifetime totals), filtering would change the meaning of a join, or catalog-only.

**P4 Cost and rows.** Run the estimate method in `docs/access.md` and compare with its limits; the result must fit the row cap. FAIL: over a limit whose policy is "do not run it". WARN: over a limit whose policy is "ask the user first"; give the estimate in one sentence and run only after a yes for this exact query. NA: no estimate method; then an exploratory query carries a row limit and a narrow window (a row limit caps rows returned, not scan).

**P5 Join grain.** Each join's cardinality is known from the table docs' Keys and joins. FAIL: a measure is summed or counted across a one-to-many or unknown join without first aggregating to the target grain. WARN: a cardinality is undocumented but no measure crosses it. NA: no joins.

**P6 No `SELECT *` on a wide table.** FAIL: in a saved query, except passing through a CTE that lists its columns. WARN: in an exploratory query on a table of more than about twenty columns.

**P7 Metric fragment.** FAIL: an `active` metric computed other than with its canonical fragment as written. WARN: the metric is `draft`, so the answer states it. NA: no governed metric; the receipt states the ad hoc definition.

**P8 Explicit date window.** FAIL: a time question with no date bound. WARN: timezone, or whether each end is inclusive or exclusive, not stated in the header or a comment. NA: not about a period.

**P9 Standard filters.** Every standard filter in the table docs and exclusion in the metric file is applied. FAIL: one is missing with no reason. WARN: omitted on purpose, with the reason in a comment and in the receipt.

**P10 Header comment** with What, Grain and Source (`docs/sql-style-guide.md`). FAIL: missing on a query being saved. WARN: missing on a one-off run.

## The user's checks

Then apply every entry under Entries in `docs/sql-checks.md`, with its own severity, reported as `SC<n>`. Skip entries marked `Retired` and anything inside HTML comments.

## Output

```
Preflight: <file path, or "inline query">
P1 read-only: PASS, one SELECT, no write keywords
P3 partition filter: FAIL, <table_b> has no filter on its date column
SC1 <short name>: NA, <the table it guards> not read
Verdict: BLOCKED by P3   |   CLEAR, 2 WARN
```

One line per check, every line with a reason, NA included. Carry WARNs into the answer or receipt where they matter, and list the checks that ran on the receipt's `Checks run` line.

## When a check is wrong

Do not work around it. Tell the user. A wrong generic check gets a row in `docs/findings.md`; a wrong user check is changed or retired only by the user.
