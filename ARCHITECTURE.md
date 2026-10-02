# Architecture

The map of where things live and how they connect. The rules are in `AGENTS.md` and are not repeated here.

## What this repo is

An operating manual, a knowledge base and a filing system for analyst work done by a coding agent on the user's warehouse. The agent reads the manual, looks things up in the knowledge base, writes SQL under a preflight checklist, runs it read-only through whatever connection the user set up, and files each deliverable where its task type says, with a receipt on every filed answer. It starts empty: the setup interview and every later correction fill it in.

## The request flow

| Hop | What happens | Where |
|---|---|---|
| First run | If access is not set up, the setup interview runs before anything else. | `skills/setup/SKILL.md` |
| Task router | The request is classified into one task type with one skill and one deliverable. | `skills/task-router/SKILL.md`, the table in `AGENTS.md` |
| Knowledge router | Metrics, the domain doc and its must-clarify list, table docs, prior work and past corrections are read before any SQL. | `skills/knowledge-router/SKILL.md` |
| Runbook skill | The task type's skill runs its steps. | `skills/<name>/SKILL.md` |
| Preflight | Every query is checked against the generic checklist, then the user's own checks. A FAIL blocks. | `skills/sql-preflight/SKILL.md`, `docs/sql-checks.md` |
| Execution | The query runs read-only through the connection the user chose. | `docs/access.md` |
| Verification | The result is sanity-checked (row counts, totals, freshness, grain) before anyone reads it. | the runbook skill |
| Deliverable | A quick answer or lookup is given inline. An analysis or data-quality check lands in its dated folder with its INDEX row and a receipt; a reusable query lands in `queries/` with its INDEX row; a table or metric doc is written in place. | `docs/definition-of-done.md`, `templates/receipt.md`, `skills/wrap-up-analysis/SKILL.md` |
| Correction loop | A mistake the user catches becomes a doc fix, a log entry and, when detectable, a new check and a golden question. | `docs/corrections.md`, `docs/sql-checks.md`, `evals/` |

## Layers

| Layer | What it holds | Folders | Who edits it |
|---|---|---|---|
| Instruction | The contract and the runbooks | `AGENTS.md`, `CLAUDE.md`, `skills/` | the user, and the agent when the user asks |
| Knowledge | What is true about the warehouse and the business | `docs/`, `metrics/` | the agent in a session; only the user sets a metric to `active` |
| Work | Filed deliverables, one dated folder or file each | `queries/`, `analyses/`, `dq/` | the agent, through the matching skill |
| Evaluation | Golden questions, their gold answers and run records | `evals/` | the agent drafts entries; only the user approves a gold answer |

## The skills

| Skill | Triggered by |
|---|---|
| `setup` | the first run, "set this up", a changed or broken connection |
| `task-router` | every request, before any other skill |
| `knowledge-router` | any data question before SQL, and lookups such as "where is X defined" |
| `answer-question` | a data question that needs SQL, quick or full |
| `sql-preflight` | any SQL about to be saved or run |
| `onboard-table` | a new table or column, or a table touched with no doc |
| `define-metric` | a new metric, or a change to how one is computed |
| `data-quality-check` | "check that X populates", "reconcile A with B", a coverage audit |
| `wrap-up-analysis` | an analysis ready to file |
| `golden-questions` | writing bank entries, or running and grading the bank |

## Human only

1. Provisioning the warehouse credential and setting its scope to read-only.
2. Promoting a metric from `draft` to `active`.
3. Approving a gold answer in the golden-question bank.

## How this grows

The repo gets better by being corrected. Each correction fixes the doc that was wrong, leaves a dated entry in `docs/corrections.md`, and, when a check could have caught it, adds an entry to `docs/sql-checks.md` and a golden question to `evals/bank/`. The knowledge base, the check list and the question bank all grow from the same mistakes, so the same mistake is harder to make twice and easy to detect if it is.
