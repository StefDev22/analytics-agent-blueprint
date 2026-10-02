# Operating contract

The rules for any coding agent working in this repo. This file is hand-edited and is the single source of rules; `CLAUDE.md` imports it and every other file points here rather than repeating it.

## Purpose

This repo is an operating manual, a knowledge base and a filing system for analyst work that a coding agent does on the user's data warehouse. The agent follows the manual, looks facts up in the knowledge base before writing SQL, runs read-only queries, and files every deliverable in a dated, indexed folder. `ARCHITECTURE.md` is the map: open it when you need to find where something lives.

## First run

If `docs/access.md` says `Status: not set up`, follow `skills/setup/SKILL.md` before anything else. Do not answer a data question until setup has recorded how the agent reaches the warehouse.

## Hard rules

1. **The warehouse is read-only.** Never run a statement that writes, alters or deletes (insert, update, delete, merge, create, alter, drop, truncate, grant, or the dialect's equivalent). Never ask for wider access. Never ask for a credential, and never store one anywhere in this repo.
2. **Documented sources only.** Answer data questions only from the sources documented in `docs/`. A table with no doc gets at least a stub in `docs/tables/` before its numbers are used.
3. **Preflight before any SQL is saved or run.** Follow `skills/sql-preflight/SKILL.md`. A FAIL is fixed, not waived.
4. **Metric definitions are human-owned.** A file in `metrics/` moves from `draft` to `active` only on the user's explicit confirmation. The agent drafts and records the user's decision; it never decides.
5. **Every filed answer carries a receipt** (`templates/receipt.md`) whose `Not checked` line is never empty.
6. **The session that answers a golden question opens nothing under `evals/`** except to write its own answer files. Gold queries live in `evals/bank/gold/`. Why: `docs/leakage-rule.md`.

## Before any SQL

Look things up in this order. `skills/knowledge-router/SKILL.md` has the detail.

1. `metrics/INDEX.md`: an `active` definition is used as written.
2. The domain doc in `docs/domains/`, always including its Must clarify section. Resolve those ambiguities with the user before the first query.
3. `docs/tables/` for every table the query touches.
4. `queries/INDEX.md` and `analyses/INDEX.md` for prior work. Search them; do not read them whole.
5. `docs/corrections.md` and `docs/sql-checks.md` for mistakes already made on these tables.

## Task router

Classify every request first with `skills/task-router/SKILL.md`, follow that row's skill as the runbook, and stop at its deliverable.

| If the request is... | Task type | Skill | Deliverable |
|---|---|---|---|
| "what's the number for X", one figure, no write-up | Quick answer | `answer-question` (quick branch) | the answer inline, nothing filed |
| "why did X move", "analyze", findings with a narrative | Analysis | `answer-question`, then `wrap-up-analysis` | dated folder `analyses/YYYY-MM-DD_topic/` and its INDEX row |
| "give me a query I can rerun" | Reusable query | `answer-question`, then file the query | a `.sql` file in `queries/` and its INDEX row |
| "check that X populates", "reconcile A with B" | Data-quality check | `data-quality-check` | `dq/YYYY-MM-DD_topic/` and its INDEX row |
| "we have a new table or column" | New table or column | `onboard-table` | a doc in `docs/tables/` linked from its domain doc |
| "define X", "X should count Y instead" | New or changed metric | `define-metric` | a `draft` file in `metrics/` and its INDEX row |
| "where is X defined", "which table has Y" | Lookup | `knowledge-router` | the answer inline |
| "write golden questions", "run the evals" | Golden questions and evals | `golden-questions` | entries in `evals/bank/` and a run record |
| "set this up", "reconnect", the access changed | Setup or reconnect | `setup` | `docs/access.md` and `docs/business-context.md` filled in |

Skills are plain Markdown runbooks at `skills/<name>/SKILL.md`: open the file and follow it. A session can mix types; pick the primary deliverable and name the hand-off.

## Done

A task is done when its deliverable exists and is indexed. The per-type criteria are in `docs/definition-of-done.md`. Rules that bind every type:

- **No undocumented table.** Touching a table with no doc means writing at least a stub in `docs/tables/` in the same session.
- **No unindexed artifact.** Anything filed in `queries/`, `analyses/` or `dq/` gets its INDEX row in the same session.
- **A receipt on every filed answer**, with `Not checked` filled in.
- **A correction from the user becomes a doc fix and a `docs/corrections.md` entry in the same session.** When a check could catch it, it also becomes a `docs/sql-checks.md` entry and a golden question.

## Where new things go

| You are adding... | It goes in |
|---|---|
| a rule every task follows | this file, once; other files point here |
| a rule for one task type | that skill's `SKILL.md` |
| a fact about the warehouse or the business | `docs/` or `metrics/`, one owner each |
| a one-off result | its dated folder and its INDEX row |
| a mistake and its fix | `docs/corrections.md` |
| a recurring SQL trap | `docs/sql-checks.md` |
| a problem with the repo itself | `docs/findings.md` |

## Where things are

```
AGENTS.md        this contract
ARCHITECTURE.md  the map: layers, request flow, who edits what
skills/          the runbooks, one folder per skill
docs/            access, business context, style guides, process docs (docs/INDEX.md lists them)
docs/domains/    one doc per business area, each with a Must clarify section
docs/tables/     one doc per table the agent reads
metrics/         metric definitions and INDEX.md
queries/         reusable SQL and INDEX.md
analyses/        dated analyses and INDEX.md
dq/              dated data-quality verdicts and INDEX.md
evals/           the golden-question bank, gold answers in evals/bank/gold/, run records
templates/       the receipt and the analysis template
```
