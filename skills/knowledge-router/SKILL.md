---
name: knowledge-router
description: Use before writing SQL for any data question, and for lookups such as "where is X defined" or "which table has Y". Gives the order to look things up in this repo, how to search instead of reading whole files, and what to do when a lookup finds nothing. Does not write SQL.
---

# Knowledge router: look it up before you write SQL

Nothing about the warehouse or the business is taken from memory. It is looked up here, in this order, every time, even when you think you know.

## Lookup order

1. **`metrics/INDEX.md`** for every metric the question names. An `active` file is used as written, its canonical SQL fragment included. A `draft` file may be used, with its status stated in the answer.
2. **The domain doc** in `docs/domains/` for the area, always, even when a metric file covers the question. Read its **Must clarify** section: every item the ask leaves open is resolved with the user before the first query. Its Key tables and Gotchas tell you where to look next.
3. **`docs/tables/`** for every table the query will touch: grain, partition or date column, keys and join cardinality, standard filters, gotchas.
4. **Prior work:** search `queries/INDEX.md` and `analyses/INDEX.md` for the metric, the tables and the topic.
5. **Past mistakes:** search `docs/corrections.md` and `docs/sql-checks.md` for the tables and metrics involved.

Also check `docs/business-context.md` for the user's words: a glossary term can tell you which metric or segment they mean.

## Search, do not read whole

- **Read whole:** the one domain doc for the area, and each table doc for a table the query touches. They are short and they are the point.
- **Search:** every INDEX file, `docs/corrections.md`, `analyses/`, and any doc you are not sure is relevant. Search for the metric name, the table name, the key columns, and the user's own words plus their glossary synonyms. Open only the files and sections the search hits.
- One search with several terms beats several reads.

## When a lookup finds nothing

| Missing | What to do |
|---|---|
| No domain doc for the area | Say so. Use the table docs, ask the user the ambiguities you can see in the ask, and offer to create the domain doc from `docs/domains/_template.md` afterwards. |
| No doc for a table the query needs | Write at least a stub through `skills/onboard-table/SKILL.md` before any of its numbers are used (`AGENTS.md`, hard rule 2). |
| No metric file | Say so in the answer. Use an explicit ad hoc definition, written in plain words in the receipt or mini receipt, and offer to draft it through `skills/define-metric/SKILL.md`. |
| No table doc names the column or concept | Say it is not documented. Offer a catalog query to find it (it goes through preflight like any SQL); any table it finds is onboarded before its numbers are used. |
| Nothing in prior work | Fine. Write the query fresh. |

## When docs disagree

- An `active` metric decides how the metric is computed. A table doc decides facts about its table.
- A dated `docs/corrections.md` entry shows which doc was fixed; trust the fix.
- Any remaining conflict: tell the user which two files disagree and about what, use the reading they choose, and add a row to `docs/findings.md`.

## Using prior work

- A filed query that answers the question is reused: read it, check it against the current table docs and corrections, and preflight it again before running. Docs may have changed since it was saved.
- A filed analysis is context, not a current number. Cite it; rerun before quoting its figures as current.

## Answering a lookup

For "where is X defined" or "which table has Y", answer inline with no SQL:

- the answer in one or two sentences,
- the file it came from, and the section,
- the status when it is a metric (`active` or `draft`).

If nothing documents it, say so plainly and offer the skill that would document it: `skills/define-metric/SKILL.md` for a metric, `skills/onboard-table/SKILL.md` for a table or column. Nothing is filed for a lookup.
