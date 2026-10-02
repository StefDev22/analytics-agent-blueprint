---
name: wrap-up-analysis
description: Use when an analysis starts its first query, or when the user says "wrap this up", "file this", or "we are done". Opens the dated analyses/ folder and its in-progress INDEX row early, files the SQL, results, charts and analysis.md with its receipt, then checks every number against the files before calling it filed.
---

# File an analysis

The deliverable is `analyses/YYYY-MM-DD_topic/` holding `analysis.md` (from `templates/analysis.md`, ending in a receipt), the SQL behind every number, the result data behind every finding, any charts, and a row in `analyses/INDEX.md` with status `filed`.

This skill runs twice: once at the first query of an analysis, to open the folder, and once at the end, to close it. An analysis rebuilt from memory at the end loses the queries that were tried and dropped, and the numbers drift from the files. Filing as you go prevents both.

## Part 1: Open the folder at the first query

`skills/answer-question/SKILL.md` opens the folder when the first query of an analysis runs. This part says how; if the folder already exists, check it against these steps.

1. **Name the folder** `analyses/YYYY-MM-DD_topic/`: today's date checked against the system clock, and a topic in short lowercase words joined by hyphens, specific enough to make sense in a folder list six months from now. Search `analyses/INDEX.md` first: a follow-up to an open analysis reuses its folder.
2. **Create** `analysis.md` from `templates/analysis.md` with `status: in progress` and the Question section filled in as agreed with the user.
3. **Add the INDEX row now:** folder, the question in one line, status `in progress`.

### While the work runs

- **Every query that runs** has passed `skills/sql-preflight/SKILL.md` and is saved to `queries_used/` exactly as run, numbered in run order with a slug (`03_orders_by_week.sql`). Save the queries that led nowhere too; they show what was ruled out. Never tidy a query after the fact: the file must be what produced the number.
- **Every result a finding may rest on** is saved to `results/` under the same number (`03_orders_by_week.csv`).
- **Every chart** follows `docs/viz-style-guide.md`, including its rule on when a chart earns its place, and is saved next to the data it was drawn from (`results/03_orders_by_week.png`).
- **Anything learned about the data** (a table doc that was wrong, a filter nobody wrote down, a trap) is noted as you find it, so Part 2 can write it back.

### What is not kept in the folder

Do not file a result that is large or sensitive: a row-level extract, anything with personal data, or anything bigger than the aggregate a finding needs (as a rough guide, more than a few thousand rows or a few megabytes). Instead keep:

- the query that produced it, in `queries_used/`,
- a small aggregate that carries the finding (counts, totals, rates by segment), in `results/`,
- a line in the Evidence section saying the full result was not kept and that the query regenerates it.

If you need the large file during the work, keep it outside the repo, or in a location the repo's version control ignores, and delete it when the analysis is filed. Never put personal data in a file name, a chart or `analysis.md`.

## Part 2: Close the folder

### Step 1: Write analysis.md

Fill every section of `templates/analysis.md` in the style of `docs/writing-style.md`:

- **What we found** leads with the answer and its number, then at most three findings, each with its own number.
- **Evidence** names, for each finding, the query file, the result file and the chart if there is one.
- **Data profile** gives the grain, rows and date range, the metric files used with their status, and the gaps.
- **Caveats** and **Follow-ups** are filled from the work, not from habit.
- **Communication log** stays empty unless the user shares a message they actually sent.
- The **receipt** from `templates/receipt.md` goes at the end, every field filled, `Not checked` never empty, and `Query files` listing the actual paths.

A metric that is still `draft` is named as a draft wherever it is used. A measure with no file in `metrics/` is defined in plain words in the Data profile, and you offer to run `skills/define-metric/SKILL.md` for it.

If the work stopped without a conclusion, file it anyway: say in What we found that no conclusion was reached and why. Do not delete the folder.

Set `status: filed` in the frontmatter.

### Step 2: Write back what the work taught you

In the same session:

- A table or domain doc that turned out to be wrong or incomplete gets fixed.
- A new trap visible in the SQL text becomes an entry in `docs/sql-checks.md`; a trap that shows only in the data becomes a Gotcha in the table doc.
- A table touched with no doc gets at least a stub through `skills/onboard-table/SKILL.md`.
- A correction from the user becomes a `docs/corrections.md` entry, as `AGENTS.md` requires.
- A convention agreed with the user is written into the doc that owns it.

### Step 3: Verify against the filesystem

Do not report the analysis as filed from memory. List the folder's files, then check:

1. **Every number** in What we found, Evidence and the receipt traces to a result file that exists in `results/`, produced by a query file that exists in `queries_used/`. Open the result file and confirm the number is in it, or is plain arithmetic on numbers in it (a difference, a ratio) that the text states. A number with no file behind it is removed or backed by a query before filing.
2. **Every path** named in Evidence and in the receipt's `Query files` exists, spelled exactly.
3. **Every chart** named in the text exists, next to its data.
4. **The receipt** has no bracketed placeholder left, and `Not checked` says something specific.
5. **No large or sensitive result file** is in the folder.
6. **The INDEX row** reads `filed` and its question matches the analysis.

Fix anything that fails and check again. Report what you verified, not what you meant to file.

### Step 4: Close the INDEX row

Set the row's status in `analyses/INDEX.md` to `filed`. A row left `in progress` on a finished folder, or `filed` on an unfinished one, makes the index lie.

## Tell the user

Briefly: the folder path, the answer in one sentence, the one caveat that travels with the number, and any doc you changed. Do not read `analysis.md` back to them.

## Done when

- `analyses/YYYY-MM-DD_topic/` holds `analysis.md` with `status: filed` and a complete receipt, `queries_used/` with every query that ran, `results/` with the data behind every finding, and any charts.
- Every number in `analysis.md` traced to a query file and a result file that exist, checked in Step 3.
- No large or sensitive result file is filed; the query and a small aggregate stand in for it.
- `analyses/INDEX.md` has exactly one row for the folder, status `filed`.
- Doc fixes and new traps found during the work are written back to `docs/`.
