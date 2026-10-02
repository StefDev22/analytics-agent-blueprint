---
name: answer-question
description: Use when a data question needs SQL, after task-router has picked quick answer, analysis or reusable query. The core loop: sharpen the ask, look things up, plan, write and preflight SQL, run it, verify the result, chart only when it earns it, and answer with a receipt. Includes the why-did-X-move, quick-answer and reusable-query branches.
---

# Answer a data question

The loop from a question to a checked answer. `skills/task-router/SKILL.md` has already chosen the depth: a **quick answer**, an **analysis**, or a **reusable query**. Steps 1 to 8 apply to all three; the branches below say what changes.

## Step 1: understand the ask and the decision behind it

A wrong but plausible number is the failure this step prevents, and it is cheapest to prevent here.

- **Sharpen a fuzzy question** into one you could write SQL for: what is counted or summed, over which population, in which window, compared with what, at what grain. Fill gaps from the docs and standing conventions first; ask only for what they leave open.
- **Ask what decision the answer feeds** when it is not obvious, once. "Just curious" is an answer. The decision tells you which comparison and which caveats matter.
- **Honour the domain doc's Must clarify.** Every item the ask leaves open is asked before the first query, together in one message, each with its documented default named so the user can just say yes. An item the ask or the docs already settle is not asked; say which reading you are using.
- **For an analysis**, open with a short free-text interview in one message: what prompted the question, what they already suspect, what decision it feeds, and anything that bears on it (a release, a campaign, a tracking change). Never a multiple-choice menu.
- When you interpreted anything, play the question back in one sentence before running.

## Step 2: look it up

Follow `skills/knowledge-router/SKILL.md`: metrics, the domain doc, table docs, prior work, past corrections. A table with no doc gets a stub through `skills/onboard-table/SKILL.md` before its numbers are used.

## Step 3: check prior work

If `queries/INDEX.md` or `analyses/INDEX.md` already has something that answers the question, reuse it: re-read it against the current docs and preflight it again. An old analysis's figures are context, not a current answer.

## Step 4: plan in two or three lines

State the tables and joins with their grain, the metric and where its definition comes from, the window and timezone, and the filters. If anything is still uncertain, say so and pause rather than picking silently.

## Step 5: write the SQL

Follow `docs/sql-style-guide.md`: header comment, one CTE per step, filters early, joins on explicit keys, aggregate to the target grain before a join that can fan out. Use an `active` metric's canonical fragment as written.

## Step 6: preflight

Run `skills/sql-preflight/SKILL.md` on the exact text. Fix every FAIL and preflight again. Any later edit means another preflight.

## Step 7: run it

Run it through the connection in `docs/access.md`, exactly as its Running a query section says, within its limits. For an analysis, at the first query that runs, open the dated folder and its `in progress` row in `analyses/INDEX.md` as Part 1 of `skills/wrap-up-analysis/SKILL.md` says, and save every query and result there as it runs. A quick answer writes nothing into the repo.

## Step 8: verify before you believe it

Check the result before anyone reads it. Run the checks that fit; name what ran on the receipt's `Checks run` line and what did not on `Not checked`.

- **Row count** fits the grain: the number of days times segments you expected, not more, not fewer.
- **Grain and fan-out:** the key is unique at the grain you claim (count against count distinct), and a measure's total is the same before and after each join.
- **Totals reconcile** to a figure you trust: a number the user knows, a filed analysis, or the sum of segments against the overall total.
- **Nulls** in keys, segment columns and measures. A null segment is a bucket of its own, not a rounding error.
- **Date coverage and freshness:** first and last date present against the window asked for, and whether the last day is complete, given the table doc's refresh timing.
- **Zero rows, or an empty segment that should not be empty, is a reason to investigate** (filter values, window, join keys, partition, value casing) before it is ever reported as a number.
- **A surprising number is checked a second way**: another table, a simpler query, or a different method. If the two disagree, say so; do not pick the one you like.

## Step 9: chart only when it earns it

Follow `docs/viz-style-guide.md`: a trend of six or more points, five or more segments compared, or the user asked. Use whatever charting tool you have. Save the image next to the data it was drawn from, in the analysis folder's results. Otherwise a sentence or a small table is the answer.

## Step 10: answer

Write it per `docs/writing-style.md`: the answer first with its number, window and definition, then the supporting points, then what was not checked. An analysis gets the full receipt from `templates/receipt.md` when it is filed; a quick answer gets the mini receipt below.

## Branch: why did X move

Decompose before you explain. Pull once, wide, at the grain the cuts need (numerator and denominator as separate columns for a rate), so later cuts can be made from that result rather than new scans where your tools allow.

1. **Is it real?** Compare the move with normal variation: the same metric over the several periods before, and the same period a year earlier when the business has seasonality (`docs/business-context.md`). Rule out a data cause: incomplete recent days, a tracking or definition change, a known gotcha or correction. If it is within the normal range, say "it did not move beyond normal variation", with the numbers, and stop.
2. **When did it start?** Find the break in a daily or weekly series. A step change points to an event (a release, a price change, a tracking change); a slow drift points to mix or trend.
3. **Numerator or denominator?** For a rate, say which side moved.
4. **Mix or rate?** Split by segment and separate the two effects: did segments' own rates change, or did volume shift between segments with different rates? If the topline moves against every segment, report the split, never the topline alone.
5. **Which segment?** On the dimensions the user named or the domain doc lists, rank segments by their share of the absolute change, not by percentage change in small segments. One segment carrying most of it is a clear finding; a change spread across everything is also a finding.
6. **Stop.** Say what the data shows. A cause the data cannot show is a labelled hypothesis, not a finding. No further cuts unless asked.

## Branch: quick answer

Same lookups, same preflight, the verification that fits a single number (row count, nulls, freshness at least). Answer inline with a mini receipt and file nothing:

```
Source: <tables>; metric <metrics/ file and status, or "ad hoc: <definition in plain words>">
Window: <start> to <end>, <inclusive or exclusive>, <timezone>; data through <latest date present>
Not checked: <what a careful analyst would still verify>
```

No chart unless asked. A chart asked for on a quick answer is shown inline or written to a temporary location outside the repo, and is not filed; if the user wants it kept, the request becomes an analysis. If the number turns out to matter (it is surprising, or it needs a comparison to mean anything), say so and offer an analysis; do not upgrade silently.

## Branch: reusable query

Write it so it can be rerun: the window's bounds in one place near the top, and a header comment per `docs/sql-style-guide.md`. Preflight it, run it once to confirm the result is sane, save it as `queries/<what_it_returns>.sql`, and add exactly one row to `queries/INDEX.md` (File, Purpose, Tables, Added). Tell the user the path.

## When the user corrects you

Stop and take it seriously, in the same session:

1. Say which earlier numbers the correction affects, and redo them.
2. Fix the doc that was wrong (domain, table or metric doc).
3. Add an entry to `docs/corrections.md` in its format.
4. If the mistake is visible in the SQL text, add an entry to `docs/sql-checks.md`. If a question could catch it coming back, draft one through `skills/golden-questions/SKILL.md`.
5. Tell the user which files changed.

## Hand-off

- **Analysis:** when the user is satisfied with the findings, hand off to `skills/wrap-up-analysis/SKILL.md` to file `analysis.md`, the receipt and the INDEX row.
- **Quick answer:** done when answered.
- **Reusable query:** done when the file and its INDEX row exist (`docs/definition-of-done.md`).
