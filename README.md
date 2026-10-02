# analytics-agent-blueprint

Turn any coding agent into a governed data analyst on your own warehouse. It looks things up before writing SQL, runs read-only, says what it did not check, and learns from every correction.

This repo is an operating contract (`AGENTS.md`), a knowledge base that starts empty, a filing system for answers, and a way to measure whether the agent gets your numbers right. It is not a tool or a semantic layer product: no sample data, nothing to install, just Markdown and one optional standard-library Python grader.

## Quick start

1. Clone or download this repo.
2. Open the folder in your coding agent.
3. Say: **set this up**.

Setup is a free-text interview in five passes. Each pass writes its files, so you can stop anywhere and resume later.

| Pass | What it asks | What it writes |
|---|---|---|
| 1. Your business | What the business does, who asks for numbers, which metrics people argue about | `docs/business-context.md` |
| 2. Connection | Which warehouse, how you query it, which schemas, limits, what the credential can do | `docs/access.md`, after one test query |
| 3. First domain | Where most questions live, which tables you trust, what newcomers get wrong | docs in `docs/domains/` and `docs/tables/` |
| 4. First metrics | The most-asked metrics, pinned and tested against a figure you trust | drafts in `metrics/` |
| 5. Golden questions | Questions you already know the answer to | `evals/bank/` and `evals/bank/gold/` |

Setup is useful after pass 2 and one documented table; later passes make answers better.

It works with any agent that reads `AGENTS.md` and can run a query, on any warehouse the agent can reach: an MCP server, the warehouse's CLI, a script, or exported files. The agent never asks for or stores a credential.

## How a question gets answered

1. **Route the task** (`skills/task-router/SKILL.md`): one of nine task types, and how deep to go.
2. **Look it up before any SQL** (`skills/knowledge-router/SKILL.md`): metrics, the domain doc and its Must clarify list, table docs, prior work, past corrections.
3. **Preflight** (`skills/sql-preflight/SKILL.md`): ten generic checks, then yours in `docs/sql-checks.md`. A FAIL blocks.
4. **Run read-only** through the connection and limits in `docs/access.md`.
5. **Verify** (`skills/answer-question/SKILL.md`): row counts, fan-out, totals, nulls, freshness.
6. **Answer with a receipt** (`templates/receipt.md`): sources, window, checks, confidence, and a "Not checked" line that is never empty.
7. **File it** (`skills/wrap-up-analysis/SKILL.md`): a dated folder in `analyses/` or `dq/`, or a query in `queries/`, with its INDEX row.

## The ideas behind it

These come from a year of running this pattern in production on a private repo, and from the public write-ups under Credits.

- **Accuracy is a context problem more than a model problem.** Wrong numbers mostly come from an undefined metric, an unwritten filter or a join that fans out.
- **A thin router plus runbooks beats one giant prompt.** The agent reads only what the task needs.
- **Metric definitions are owned by a human.** The agent drafts; only your explicit yes makes one active.
- **Look things up before writing SQL**, and ask about ambiguity before the first query, not after the answer.
- **Every answer carries a receipt** that says what was not checked.
- **Every correction becomes a doc fix, a check and a test**, so the same mistake is harder to make twice.
- **Golden questions with hidden answers tell you whether a change helped.** A fresh session answers blind; another grades.
- **The knowledge base is plain Markdown in git**, reviewed and reverted like code.

## What is in the box

```
AGENTS.md        the contract: hard rules, lookup order, task router
ARCHITECTURE.md  the map: layers, request flow, who edits what
skills/          ten runbooks
docs/            access, business context, style guides, corrections, checks
docs/domains/    one doc per business area
docs/tables/     one doc per table
metrics/         metric definitions, draft or active
queries/         reusable SQL
analyses/        dated analyses
dq/              dated data-quality verdicts
evals/           golden questions, hidden gold, run records, grader
templates/       receipt and analysis templates
```

| Skill | When it runs | What it leaves behind |
|---|---|---|
| `setup` | First run, reconnect | Access, business context, first docs, metrics, questions |
| `task-router` | Every request, first | A task type and a hand-off |
| `knowledge-router` | Before SQL; lookups | An inline answer for a lookup |
| `answer-question` | A question needing SQL | An answer with a receipt, or a saved query |
| `sql-preflight` | Before SQL is saved or run | A verdict line per check |
| `onboard-table` | A new or undocumented table | A table doc |
| `define-metric` | Define or change a metric | A draft metric file |
| `data-quality-check` | Completeness, reconciliation | Verdicts filed in `dq/` |
| `wrap-up-analysis` | An analysis starts and ends | A dated folder with SQL, results, receipt |
| `golden-questions` | Writing or running the bank | Entries, gold queries, a graded run |

## Guardrails, honestly

The read-only rule is a sentence in `AGENTS.md`; the preflight is a checklist the agent reads its own SQL against. Neither is enforcement. The real guarantee is a credential that cannot write. Setup asks what yours can do and records it in `docs/access.md`.

The other rules (drafts stay drafts, gold stays hidden) hold because the agent is told so. Golden questions, including ones where the right answer is to ask or refuse, show whether it listens.

## Make it yours

The files you are expected to edit:

- `docs/sql-checks.md`: your own preflight checks, grown from corrections.
- `docs/sql-style-guide.md`, `docs/writing-style.md`, `docs/viz-style-guide.md`: house style.
- The router table in `AGENTS.md`, when you add a task type, and a new folder under `skills/` for its runbook.

Keep one owner per fact: each rule or fact lives in one file and everything else points to it. "Where new things go" in `AGENTS.md` says which file owns what.

## Later

Deliberately not in this version: a second opinion from a different model; reliability runs that ask the same question several times and compare; guided exploration and exploration notebooks; read-only editions for colleagues; a weekly curation routine; recurring reports; an audit script and session hooks that enforce what the prompts ask for.

## Tested with

<!-- TESTED-WITH -->

## Credits and sources

- "How Anthropic enables self-service data analytics with Claude", Anthropic: https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude
- "Inside OpenAI's in-house data agent", OpenAI.
- The AI Analyst Lab and `ai-analyst-plus` by Shane Butler (MIT), which inspired the phased setup interview and the confidence receipt: https://github.com/ai-analyst-lab/ai-analyst-plus

## Licence

MIT. See [LICENSE](LICENSE).
