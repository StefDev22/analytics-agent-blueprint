---
name: define-metric
description: Use when the user says "define X", "X should count Y instead", "how should we measure X", or an analysis needs a measure that has no file in metrics/. Pins the calculation, tests the SQL fragment, writes a draft metric file and its INDEX row, and promotes it to active only on the user's explicit yes.
---

# Define or change a metric

The deliverable is `metrics/<metric_name>.md` from `metrics/_template.md` with `status: draft`, a Changelog line, and its row in `metrics/INDEX.md`. The agent drafts. Only the user makes a metric `active` (`AGENTS.md` hard rule 4).

## Step 1: Check what already exists

Search `metrics/INDEX.md` for the name and close synonyms, and read the metric's domain doc in `docs/domains/`, including Must clarify. If a file with this meaning exists, go to "Changing a metric" below. If one has this name but another meaning, ask the user which they mean: two meanings never share one name.

## Step 2: Capture the meaning in the user's words

Ask what the metric is for and which decision it informs, and write the answer down in the user's terms before translating it into columns. Ask in plain free text, at most three questions per round, the most valuable first.

## Step 3: Pin every part of the calculation

A definition is complete when two analysts would write the same SQL from it. Pin each of these, from the user's answers and the table docs, never from memory:

| Part | What to settle |
|---|---|
| Numerator | what is counted or summed: distinct entities or events, amounts with or without tax, refunds or discounts |
| Denominator | for a rate or average: the population divided by, filtered like the numerator or not |
| Grain | the unit one value describes: per day, per entity, per order |
| Window | calendar or rolling, inclusive or exclusive ends, the timezone, late-arriving data |
| Filters | what is in scope: segments, statuses, channels |
| Exclusions | what is left out on purpose and why: test accounts, internal traffic, cancelled or deleted records |
| Source | the tables and columns it reads, each with a doc in `docs/tables/` |

If a table it reads has no doc, run `skills/onboard-table/SKILL.md` (stub mode at least) first.

## Step 4: List the plausible wrong readings

For each part above, ask how someone could reasonably compute a different number under the same name: another denominator, gross instead of net, all records instead of completed ones, events instead of distinct entities, local time instead of the stored timezone. Each goes under "Do not confuse with" with one sentence on why it is wrong here, and the metric file that covers it if one does.

## Step 5: Write and test the canonical SQL fragment

Write the reusable expression or CTE that computes the metric, following `docs/sql-style-guide.md`. It is a building block, not the answer to a particular question: no hard-coded date window unless the window is part of the definition. Run it through `skills/sql-preflight/SKILL.md`.

Then test it:

1. Ask the user for a figure they already trust for this metric (a report, a dashboard tile), with its window and source. Agree the tolerance before you compute.
2. Compute the fragment for exactly that window and compare. On a match, record in the Changelog the source and window it was tested against, without the numbers.
3. On a mismatch, do not tweak the fragment until it agrees. Find out why with the "Two numbers disagree" procedure in `skills/data-quality-check/SKILL.md`; the gap is often a definition choice the user has to make.
4. With no trusted figure, run a sanity check instead (a plausible range, parts that add up to the whole) and record in the Changelog that it was not tested against a trusted figure.

## Step 6: Write the draft file

Copy `metrics/_template.md` to `metrics/<metric_name>.md` (lower case, underscores) and fill it:

- `status: draft`.
- `owner:` the person the user names as the one who confirms this definition. If they name no one, ask.
- `last_reviewed: never` for a new metric. A metric is reviewed only when the user confirms it.
- Definition, Canonical SQL fragment, Valid dimensions, Known exclusions and Do not confuse with, from steps 2 to 5.
- Changelog: `YYYY-MM-DD: created as draft`, plus the test line from step 5.

Delete the template comment. Add the row to `metrics/INDEX.md` with status `draft`, and add the metric to Standard metrics in its domain doc with its status.

### The leakage rule

A metric file holds meaning and a fragment, never a result: not the trusted figure, not your test result, not "currently around N", and not the full query that answers a specific question. Never open `evals/bank/gold/` to check a definition. Why: `docs/leakage-rule.md`.

## Step 7: Ask for confirmation

Show the user the definition in plain words, the fragment, the exclusions, the readings it rules out, and how the test went. Ask whether it is right as written.

- **An explicit yes** ("yes", "confirmed", "make it active"): set `status: active` and `last_reviewed` to today, add `YYYY-MM-DD: promoted to active on the user's confirmation` to the Changelog, and update the INDEX row and the domain doc.
- **Anything else** (a change, a "probably", silence, "looks fine for now"): apply any change, keep `status: draft`, and say plainly that the metric is a draft and that every answer using it will say so.

Never promote on your own judgement, on a test passing, or on a past confirmation of a different version.

## Changing a metric

A change to an `active` metric puts it back to draft:

1. Set `status: draft`. Leave `last_reviewed` at the date of the last confirmed version.
2. Edit the definition and fragment, and add the old reading to "Do not confuse with" if people might still compute it.
3. Add a Changelog line: `YYYY-MM-DD: <what changed and why>, back to draft`.
4. Retest (step 5), update the INDEX row, then ask for confirmation (step 7).
5. Search `queries/INDEX.md` and `analyses/INDEX.md` for work that used the old definition, and list it for the user. Do not rewrite filed work.

If the user is correcting a definition the agent applied wrongly, also add a `docs/corrections.md` entry. A change in what the business wants to measure is not a correction.

Retire a metric only when the user asks: `status: deprecated`, a Changelog line with the reason and the replacement, and its INDEX row moved under a Deprecated heading (`docs/definition-of-done.md` rule 6). Never delete the file.

## Done when

- `metrics/<metric_name>.md` exists from the template, `status: draft` (or `active` after an explicit yes), every section filled, with a Changelog line for this session.
- The fragment passed preflight and was tested against a trusted figure, or the Changelog says why not.
- The file holds no result number and no full gold query.
- `metrics/INDEX.md` has exactly one row for it with the current status, and its domain doc lists it.
