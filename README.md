<div align="center">

# analytics-agent-blueprint

<strong>A blueprint for turning the coding agent you already use into a data analyst you can check.</strong>

looks it up before it queries · never writes to your warehouse · shows what an answer rests on · says what it did not check · keeps every correction

<a href="#what-it-is">What it is</a> ·
<a href="#getting-started">Getting started</a> ·
<a href="#what-to-ask-it">What to ask it</a> ·
<a href="#how-it-works">How it works</a> ·
<a href="#how-far-to-trust-it">How far to trust it</a> ·
<a href="#adapting-it">Adapting it</a>

</div>

---

## What it is

A folder of Markdown that you open in a coding agent. That is all of it: no package to install, no sample data, no service to run.

On day one the folder knows nothing about your business. You say "set this up" and the agent interviews you: what the company does, how it reaches your warehouse, which tables matter, which metrics people argue about. It looks at the tables itself and writes down what it learns. From then on, when you ask a data question, it reads those notes before it writes any SQL, checks its own query against a list of known traps, runs it read-only, and hands back the answer with a short receipt saying where the number came from and what it did not verify.

When it gets something wrong and you say so, the correction does not evaporate at the end of the chat. It goes into the notes, and where possible it becomes a check and a test question, so the same mistake is harder to make next month.

It is written for any agent that reads an `AGENTS.md` file and can run a query, and for any warehouse that agent can reach: an MCP server, the warehouse's own command line, a script, or a folder of exported files.

## Getting started

```bash
git clone <repo-url>
```

Open the folder in your coding agent and type:

```
set this up
```

The interview comes in five short passes, never more than three questions at a time, and you can skip anything or stop halfway. It will not ask for a password or a key, and it will not ask what it can find out by looking.

| Pass | What you talk about | What gets written |
|---|---|---|
| 1 | Your business and who asks you for numbers | `docs/business-context.md` |
| 2 | How the agent reaches the warehouse, and what it is allowed to do there | `docs/access.md` |
| 3 | The one area most questions come from, and its tables | `docs/domains/`, `docs/tables/` |
| 4 | The two or three metrics you are asked for most | `metrics/` |
| 5 | A few questions you already know the answer to | `evals/bank/` |

You do not need all five. Once the connection works and one table is documented, ask it something real.

## What to ask it

Plain sentences. There are no commands to learn.

**A number.** It answers inline with a three-line receipt and files nothing.
> How many orders did we take last week?

**An explanation.** It first checks the move is real, then when it started and which segment carries it, and files the write-up with every query behind it.
> Why did signups drop in March?

**A table it has not seen.** It reads the schema, profiles the data, proves what one row is, and asks you only for the parts that live in your head.
> We have a new order_items table. Document it.

**A metric.** It pins down numerator, denominator, window and exclusions, and lists the readings people confuse it with. The definition stays a draft until you say yes.
> Define repeat purchase rate.

**Two numbers that disagree.** It lines them up one difference at a time: definition, window, timezone, filters, grain.
> Finance and the dashboard disagree on last month's revenue. Find out why.

**A test of the agent itself.** You write questions you know the answer to; a fresh session answers them without seeing the key.
> Write golden questions with me.

**A correction.** It redoes the number, fixes the note that misled it, and logs what happened.
> That's wrong. Revenue here never includes cancelled orders.

**Where things stand.** The agent can read the whole folder, so it is the fastest way around it.
> What is still open in setup? Where is net revenue defined?

## How it works

Three parts, all of them files you can read.

**The contract** is `AGENTS.md`. It holds the few rules that apply to everything (read-only, look it up first, a human owns the metric definitions) and a table that sends each kind of request to one runbook. It is short on purpose, so the agent reads all of it every time.

**The runbooks** are the ten files under `skills/`. Each covers one job: answering a question, checking SQL before it runs, documenting a table, defining a metric, checking data quality, filing an analysis, writing and running test questions, and the setup interview itself. The agent opens only the one the request needs.

**The knowledge** is everything under `docs/` and `metrics/`. It starts as empty templates and becomes the description of your business: one note per business area with the questions that must be settled before querying, one per table, one per metric, plus a log of corrections and your own list of SQL traps in `docs/sql-checks.md`.

Every filed answer ends with a receipt. A short one looks like this:

```
Source: sales.orders; metric net_revenue (draft)
Window: 2026-09-01 to 2026-09-30, inclusive, UTC
Not checked: refunds booked after month end
```

The last line is never allowed to be empty. `ARCHITECTURE.md` has the full map.

## Why it is built this way

This comes out of a year of running the same pattern on a private production repo, and out of the public write-ups credited below. The short version:

- Wrong numbers mostly come from missing context, not a weak model: an undefined metric, an unwritten filter, a join that repeats rows.
- A short contract plus runbooks works better than one enormous prompt.
- Metric definitions belong to a person. The agent drafts; it does not decide.
- An answer you cannot trace is not finished.
- A correction that is not written down will be needed again.
- The only way to know whether a change helped is to ask questions whose answers the agent cannot see.

## How far to trust it

Be clear about what this is. The read-only rule is a sentence in a file, and the SQL check is the agent reading its own query against a list. Neither is enforcement. The guarantee that matters is a credential that cannot write, and setup asks about yours and records the answer.

The same goes for the other rules. Drafts stay drafts and answer keys stay hidden because the agent is told so. Golden questions are how you find out whether it listens, including questions where the right response is to ask you something or to refuse.

So far it has been run from a cold start, with scripted answers and a small fictional set of exported files, in Claude Code and in Codex CLI. Both completed setup and returned the known figure. Other agents and real warehouses are untried. If you run it on one, please open an issue and say how it went.

## Adapting it

| If you want to... | Change this |
|---|---|
| Add a rule for every task | `AGENTS.md`, once |
| Teach it a SQL trap specific to your data | `docs/sql-checks.md` |
| Set house style for SQL, prose or charts | `docs/sql-style-guide.md`, `docs/writing-style.md`, `docs/viz-style-guide.md` |
| Add a new kind of task | a new folder under `skills/` and a row in the router table in `AGENTS.md` |
| Cover another part of the business | ask for it: "set up a second domain" |

One habit keeps it healthy: each fact lives in exactly one file, and everything else points there.

## Not in this version

Left out on purpose, and natural next steps once the basics hold: a second opinion from a different model, asking the same question several times to see whether the answer is stable, guided exploration, notebooks, read-only copies for colleagues, a weekly tidy-up routine, recurring reports, and scripts or hooks that enforce what the prompts only ask for.

## Credits and licence

The ideas are not all mine. They lean on:

- "How Anthropic enables self-service data analytics with Claude", Anthropic: https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude
- "Inside OpenAI's in-house data agent", OpenAI.
- The AI Analyst Lab by Shane Butler, whose `ai-analyst` and `ai-analyst-plus` repos (MIT) inspired the setup interview and the receipt: https://github.com/ai-analyst-lab/ai-analyst

Licensed under [MIT](LICENSE).
