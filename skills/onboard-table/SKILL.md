---
name: onboard-table
description: Use when the user says "we have a new table", "document this table", "there is a new column", or a task touches a table with no doc in docs/tables/. Reads the schema, profiles cheaply, asks only what inspection cannot reveal, writes the table doc and links it from its domain doc. Has a stub mode for mid-analysis use.
---

# Onboard a table

The deliverable is a doc in `docs/tables/` written from the table's real schema and a real profile, linked from its domain doc. Never infer a column, a value or a grain from the table's name or from one query that used it. What you could not verify is marked unverified, not guessed.

## Pick the mode

| Situation | Mode |
|---|---|
| The task is to document a table or a new column | Full: every step below |
| You are mid-analysis and need a table that has no doc | Stub: step 1, the grain check in step 3, a stub doc, step 6, then back to the task |
| A stub exists and the user wants it finished | Full, starting from the stub |

**Stub mode.** `AGENTS.md` forbids using a table's numbers before it has a doc. A stub lifts that block: Purpose and grain, Partition or date column, and `Stub, not profiled` under Last profiled, from `docs/tables/_template.md`. Prove the grain even for a stub: a wrong grain is the mistake a stub exists to prevent. Link it from its domain doc, tell the user the table is only stubbed, and offer to finish it later in full mode. A stub unblocks another task; it does not complete a "new table" task.

**New column on a documented table.** Run steps 1 to 3 for that column, add its row to Columns, add any new gotcha, and update Last profiled. If profiling shows the rest of the doc is wrong, fix it and follow step 7.

## Step 1: Get the schema

First check `docs/tables/` and `docs/domains/` for an existing doc or mention under another name, and update what exists rather than writing a second doc.

Then read the schema through the connection in `docs/access.md`: the warehouse's information schema, the dialect's describe command, or the header row of an export file. Record every column with its type as the warehouse reports it, including nested or repeated fields, and the partition or clustering columns if exposed.

## Step 2: Stay within the limits

Every profiling query goes through `skills/sql-preflight/SKILL.md` before it runs, and a FAIL is fixed. P2 (documented tables) is NA for the table being onboarded, since these queries exist to write its doc; any other table they read still needs one. Respect the limits in `docs/access.md` and estimate the cost first when it says how. On a large table, profile a bounded recent window of the date column and record which window. If a query would still exceed a limit, follow the access doc's rule: ask the user or do not run it. With file exports, profile the file and note that the profile covers that export, not the live table.

## Step 3: Profile cheaply

Collect these, and nothing more unless a later step needs it:

1. **Row count**, for the whole table if the estimate allows, otherwise for the window.
2. **Date range and freshness:** first and last date present, and how far the last date is from today. A future date or a stale last date is a gotcha.
3. **Grain:** name the candidate key, then prove it by comparing the row count with the distinct count of the key over the same rows. Equal means the grain holds; not equal means find the column that completes the key. Nulls in the key mean uniqueness is not proven: say so.
4. **Null rates** for every column the doc describes, always including the key and the date column.
5. **Distinct values with counts** for low-cardinality columns such as status, type or channel.
6. **Test or junk rows:** `test`, `null` or `undefined` stored as text, empty strings, placeholder ids, implausible dates, internal accounts. Count them; they usually become Standard filters.

For each join key, measure the match rate against the table it points to and the cardinality (one to one, one to many, many to many): distinct keys on each side, and how many keys have more than one row on each side.

## Step 4: Ask what inspection cannot reveal

Ask the user in plain free text, at most three questions per round, the most valuable first:

- what the table is for and which questions it should answer,
- who owns it and can answer questions about it,
- known traps, late-arriving data, or columns not to trust,
- the standard filters every query needs and why.

Include what you found so they can answer quickly ("`<status_column>` has five values; two look like test states: is that right?"). Never ask what a query could answer. What the user does not know stays unverified.

## Step 5: Write the doc

Copy `docs/tables/_template.md` to `docs/tables/<table>.md`, fill every section from steps 1 to 4, and delete the template comment. In particular:

- **Purpose and grain:** one row = one what, as proven in step 3.
- **Partition or date column:** its type and timezone, or `timezone unverified`.
- **Columns:** meaning, units, null rate, known values, with "profiled YYYY-MM-DD over <window>" next to profiled values.
- **Keys and joins:** every join key with cardinality and match rate.
- **Standard filters:** each with the reason it exists.
- **Gotchas:** every issue profiling found and every trap the user named.
- **Verified example queries:** only a query that ran and whose result you checked.
- **Last profiled:** date, row count, date range, null rates on key columns.

Mark anything not confirmed with `unverified:` and what would confirm it. An honest gap helps the next session; a plausible guess misleads it.

## Step 6: Link it from its domain doc

Add the table to Key tables in the best-fitting doc in `docs/domains/`, with its grain, its use and a link to the table doc. Add new dimensions to Dimensions and domain-level traps to Gotchas.

If no domain fits, create `docs/domains/<area>.md` from `docs/domains/_template.md`, put the ambiguities this table raised under Must clarify, add a line for it to `docs/INDEX.md`, and tell the user you created a domain and why.

## Step 7: Close the loop

- If profiling proved an existing doc wrong, fix it, and if an earlier answer relied on the wrong fact, add a `docs/corrections.md` entry.
- In stub mode, or when another task handed off here, return to that task.

## Done when

- `docs/tables/<table>.md` exists from the template: complete in full mode, the stub fields in stub mode.
- The grain was proven by a uniqueness check, and every join key has its cardinality.
- Nothing unverified is stated as fact, and Last profiled carries a date (or `Stub, not profiled`).
- The doc is linked from a domain doc; a new domain doc has its line in `docs/INDEX.md`.
- Every profiling query passed `skills/sql-preflight/SKILL.md` within the `docs/access.md` limits.
