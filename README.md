# analytics-agent-blueprint

Turn your coding agent into a careful data analyst on your own warehouse. It looks things up before writing SQL, runs read-only, says what it did not check, and learns from every correction.

**10** skills | **1** contract | **0** dependencies | any agent that reads `AGENTS.md` | any warehouse it can reach | MIT

---

## What this is

- **A contract** (`AGENTS.md`): hard rules, a lookup order, and a router that sends each request to one runbook.
- **A knowledge base that starts empty** and fills from an interview with you: your business, tables, metrics and traps.
- **A filing system with receipts**: every filed answer says what it rests on and what was not checked.
- **Golden questions**: questions you know the answer to, answered blind, to show whether it is getting better.

What it is not: no sample data, nothing to install, not a semantic layer product. It is all Markdown.

---

## Quick start

```bash
git clone <repo-url>
```

Open the folder in your coding agent and type:

```
set this up
```

The agent interviews you, at most three questions at a time:

```
What does the business do, for whom, and how does it make money?
Which warehouse do you use, and how do you query it from this machine today?
What does a newcomer get wrong here? Which words have two meanings?
```

It inspects tables, columns and the SQL dialect itself, asks only what lives in your head, and never asks for a credential.

Five passes, each saving its files, so you can stop and resume:

| Pass | Writes |
|---|---|
| 1. Your business | `docs/business-context.md` |
| 2. Connection, tested | `docs/access.md` |
| 3. First domain and tables | `docs/domains/`, `docs/tables/` |
| 4. First metrics | `metrics/` |
| 5. First golden questions | `evals/bank/` |

It is useful after the connection and one documented table; later passes make answers better.

The connection can be whatever your agent already has: an MCP server, the warehouse's own CLI, a script, or exported files.

---

## Don't know what to do? Just ask.

The agent knows this repo. Ask it:

```
What is still open in setup?
Where is net revenue defined, and is it active or a draft?
What can you do here?
```

It answers from the files and names them. This README is the reference; the agent is the guide.

---

## Things you can do

### 1. Ask for a number

```
How many orders did we take last week?
```

It checks the docs, preflights its SQL, runs it read-only and answers with a three-line receipt. Nothing is filed.

### 2. Ask why something moved

```
Why did signups drop in March?
```

It asks what prompted it, checks whether the move is real, when it started and which segment carries it, then files the findings in `analyses/` with every query and a receipt.

### 3. Document a table

```
Document the new order_items table.
```

It reads the schema, profiles the table, proves the grain, and asks only what inspection cannot show. The doc lands in `docs/tables/`.

### 4. Define a metric

```
Define repeat purchase rate.
```

It pins numerator, denominator, grain, window and exclusions, and tests against a figure you trust. The file in `metrics/` stays a draft until you say yes.

### 5. Check data or reconcile two numbers

```
Finance and the dashboard disagree on last month's revenue. Reconcile them.
```

It aligns the two sides one axis at a time (definition, window, timezone, filters, grain) and concludes expected, bug or unresolved. The verdict is filed in `dq/`.

### 6. Write golden questions and run them blind

```
Write golden questions with me.
Run the evals.
```

You approve each gold query; the answering session never sees it. Fresh sessions answer blind, and a different session, or you, compares results by hand within a tolerance.

### 7. Correct it

```
That's wrong: revenue here excludes refunds.
```

It redoes the affected numbers, fixes the wrong doc and logs it in `docs/corrections.md`. If a check could catch it, it adds one to `docs/sql-checks.md` plus a golden question.

---

## How a question gets answered

```
question --> 1. route --> 2. look up --> 3. preflight --> 4. run read-only
                               ^                              |
                               |                              v
                               |                           5. verify
                               |                              |
                               |                              v
docs, checks, golden questions-+                  6. answer with a receipt
          ^                                                   |
          |                                                   v
          +--------------- you correct it <-------------- 7. file it
```

1. **Route** (`task-router`): one of nine task types, and how deep to go.
2. **Look up** (`knowledge-router`): metrics, domain and table docs, prior work, past corrections.
3. **Preflight** (`sql-preflight`): ten generic checks, then yours in `docs/sql-checks.md`. A FAIL blocks.
4. **Run read-only** through the connection in `docs/access.md`.
5. **Verify** (`answer-question`): row counts, fan-out, totals, nulls, freshness.
6. **Answer with a receipt** (`templates/receipt.md`); "Not checked" is never empty.
7. **File it** (`wrap-up-analysis`): a dated folder and its INDEX row.

A quick answer's receipt; filed work gets the full one:

```
Source: sales.orders; metric net_revenue (draft)
Window: 2026-09-01 to 2026-09-30, inclusive, UTC; data through 2026-09-30
Not checked: refunds booked after month end
```

---

## The ideas behind it

From a year of running this pattern in production on a private repo, and from the write-ups under Credits.

- **Accuracy is a context problem more than a model problem.** Wrong numbers mostly come from an undefined metric, an unwritten filter, a join that fans out.
- **A thin router plus runbooks beats one giant prompt.** The agent reads only what the task needs.
- **A human owns metric definitions.** The agent drafts; only your explicit yes makes one active.
- **Look it up before writing SQL**, and settle ambiguity before the first query runs.
- **Every answer carries a receipt** that says what was not checked.
- **Every correction becomes a doc fix, a check and a test.**
- **Golden questions with hidden answers show whether a change helped.**
- **The knowledge base is plain Markdown in git**, reviewed and reverted like code.

---

## What is in the box

```
AGENTS.md        the contract: hard rules, lookup order, task router
ARCHITECTURE.md  the map: layers, request flow, who edits what
skills/          ten runbooks
docs/            access, business context, style guides, corrections, checks,
                 domains/ and tables/
metrics/         metric definitions, draft or active
queries/         reusable SQL
analyses/        dated analyses
dq/              dated data-quality verdicts
evals/           golden questions, hidden gold, run records
templates/       receipt and analysis templates
```

| Skill | When it runs |
|---|---|
| `setup` | First run, reconnect |
| `task-router` | Every request, first |
| `knowledge-router` | Before SQL; lookups |
| `answer-question` | A question needing SQL |
| `sql-preflight` | Before SQL is saved or run |
| `onboard-table` | A new or undocumented table |
| `define-metric` | Define or change a metric |
| `data-quality-check` | Completeness, reconciliation |
| `wrap-up-analysis` | An analysis starts and ends |
| `golden-questions` | Writing or running the bank |

---

## Guardrails, honestly

The read-only rule is a sentence in `AGENTS.md`; the preflight is a checklist the agent reads its own SQL against. Neither is enforcement. The real guarantee is a credential that cannot write; setup records what yours can do in `docs/access.md`.

The other rules (drafts stay drafts, gold stays hidden) hold because the agent is told so. Golden questions, including ones where the right answer is to ask or refuse, show whether it listens.

---

## Make it yours

The files you are expected to edit:

- `docs/sql-checks.md`: your own preflight checks, grown from corrections.
- `docs/sql-style-guide.md`, `docs/writing-style.md`, `docs/viz-style-guide.md`: house style.
- The router table in `AGENTS.md`, when you add a task type, and a new folder under `skills/` for its runbook.

Keep one owner per fact: each rule or fact lives in one file and everything else points to it. "Where new things go" in `AGENTS.md` says which file owns what.

---

## Later

Deliberately not in this version: a second opinion from a different model; reliability runs that ask the same question several times and compare; guided exploration and exploration notebooks; read-only editions for colleagues; a weekly curation routine; recurring reports; an audit script and session hooks that enforce what the prompts ask for.

---

## Tested with

The onboarding and the question loop were run cold, in fresh headless sessions with scripted answers, on a small fictional set of CSV exports:

| Agent | Result |
|---|---|
| Claude Code | all five setup passes ran, the quick answer matched the known figure |
| Codex CLI | all five setup passes ran, the quick answer matched the known figure |

Other agents and real warehouses are untested. If you try one, open an issue with what happened.

---

## Credits and sources

- "How Anthropic enables self-service data analytics with Claude", Anthropic: https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude
- "Inside OpenAI's in-house data agent", OpenAI.
- The AI Analyst Lab and `ai-analyst-plus` by Shane Butler (MIT), which inspired the phased setup interview and the confidence receipt: https://github.com/ai-analyst-lab/ai-analyst-plus

---

## Licence

MIT. See [LICENSE](LICENSE).
