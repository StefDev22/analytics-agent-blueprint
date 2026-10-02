---
name: setup
description: Use when docs/access.md says "Status: not set up", when the user says "set this up", "continue setup" or "reconnect", or when the warehouse connection changed or broke. Runs a resumable free-text onboarding interview in five passes: business, connection, first domain and tables, first metrics, first golden questions.
---

# Setup: the onboarding interview

Setup fills this empty repo from a conversation with the user and from what you can see yourself. Every pass ends with files written, so stopping halfway loses nothing.

**Setup does not need to be finished to be useful.** After pass 2 (the connection) and one documented table, you can answer real questions. Passes 3 to 5 make answers better; they do not unlock them.

## Rules for the whole interview

1. **Plain conversation.** Free text, never a multiple-choice menu or a form. At most three questions per message, the most valuable first. Wait for the answer before the next round.
2. **Never ask what you can find out.** Table names, columns, types, row counts, date ranges, partition columns and the SQL dialect are inspected, not asked. Ask only for what lives in the user's head: meaning, intent, history, and what people get wrong.
3. **Anything can be skipped.** If the user says skip, later or does not know, write "Not given yet." in that slot and move on.
4. **Never ask for, echo or store a credential** in the chat, a file or a command you print. If the user pastes one, do not repeat or write it; tell them to rotate it and keep it where the connection method keeps it (the MCP server's config, the CLI's own login, an environment variable outside this repo).
5. **No answer numbers in docs.** Docs hold meaning in the user's own words, never figures a golden question could ask for (`docs/leakage-rule.md`).
6. **A data question asked mid-setup** is noted and answered as soon as pass 2 and one table doc exist. Before that, say why you are waiting.

## Step 0: find where setup stopped

Read the repo before asking anything. This is what makes setup resumable: a second "set this up" continues and never re-asks what is written.

| Check | Pass |
|---|---|
| `docs/business-context.md` status line, and sections still showing `[bracketed]` placeholders | 1 |
| `docs/access.md` status line (`Status: set up YYYY-MM-DD` means done) | 2 |
| Files in `docs/domains/` and `docs/tables/` other than `_template.md` | 3 |
| Rows in `metrics/INDEX.md` | 4 |
| Entries in `evals/bank/` | 5 |

"Not given yet." means offered and skipped: it does not reopen the pass, is listed once under Still open, and is re-asked only if the user asks.

Tell the user in two or three lines what is done and which pass is next.

- "Reconnect", or the access changed or broke: run pass 2 only.
- The user arrived with a data question and nothing is set up: offer pass 2 first so the question can be answered sooner, then pass 1.
- Everything is filled: say so, and offer a second domain (pass 3) or more golden questions (pass 5).

## Pass 1: you and your business

Writes `docs/business-context.md`. Over two or three rounds, for example:

- What does the business do, for whom, and how does it make money? What is your role, and who do you answer data questions for?
- Who asks for numbers most, and what decisions do they make with them? Which five or so metrics do people argue about, in the words they use?
- How do people cut the business? Any calendar quirks: fiscal year, week start, timezone of record, peak periods, one-off events? Any words that mean something specific here?

Fill each section from the answers, the glossary as its table. Set the status line to `Status: set up YYYY-MM-DD` once the first three sections are filled; until then, `Status: in progress YYYY-MM-DD`.

## Pass 2: the connection

Writes `docs/access.md`. Detect first, then ask only what you could not see.

1. **Look at what this agent already has:** a warehouse or database server in your own tool list (an MCP server), an export folder or a query script in the working folder. For a warehouse CLI the user names, check it is installed and logged in with its own status or version command, never by printing a config or token file.
2. **Ask what is left**, for example: "Which warehouse do you use, and how do you query it from this machine today?" and "Which projects, databases or schemas should I read?"
3. **Pick the method** with the user: an MCP server already configured in this agent, the warehouse's CLI already logged in, a script the user runs, or file exports in a folder. Record the exact steps to run one read query and get rows back. For exports, record the folder and format and never modify the files. The runbooks still need SQL, so for exports, or a script that does not take SQL, load the files into an in-memory database in a local SQL engine this agent already has (read-only where it allows) and write the exact load-and-query steps into `docs/access.md`; preflight, `.sql` files and receipts are unchanged. With no local SQL engine, say so, record the method as blocked under Last verified, and leave `Status: not set up`.
4. **Dialect:** infer it from the warehouse; confirm with a version query if the dialect has one.
5. **Cost before a run:** if the warehouse can estimate scan or cost without running (a dry run, an explain plan), record how and how to read it. If not, write "not available".
6. **Limits:** propose defaults in one line and let the user change them: rows returned per query, a scan or cost cap if they want one, and whether to ask first or not run when a query would exceed one.
7. **Read-only:** ask what role or grants the credential holds and who provisioned it. If a read query can list the current role's grants, run it and record the result. Never test write access by attempting a write. Then say plainly: "The read-only rule in AGENTS.md is a prompt rule, not a guarantee. The only real guarantee is a credential that cannot write. If yours can, I recommend asking for one that cannot." If the answer is unknown or yes, the file says so.
8. **One harmless test query**, such as selecting a constant, then a catalog listing of the tables in scope for pass 3. Both go through `skills/sql-preflight/SKILL.md` first.
9. **Write the file:** every section filled, the test query and its result under Last verified, and only then the status line set exactly to `Status: set up YYYY-MM-DD`. If the test failed, leave `Status: not set up`, record what failed under Last verified, and give the user the one next step.

## Pass 3: first domain and tables

1. Ask which business area most of their frequent questions live in. Pick one.
2. From the catalog listing, propose the three to five tables behind it and ask the user to confirm or swap. Ask which they trust when two seem to hold the same thing.
3. Ask for the **Must clarify** list: "What does a newcomer get wrong here? Which words have two meanings?" Each item becomes a question naming its readings and the default.
4. Create `docs/domains/<area>.md` from `docs/domains/_template.md`, Must clarify filled, other sections as far as you know them. Add its line to `docs/INDEX.md`.
5. Hand each table to `skills/onboard-table/SKILL.md`, one at a time; it writes the table doc and links it from the domain doc.

## Pass 4: first metrics

Hand the two or three most-asked metrics from the business context to `skills/define-metric/SKILL.md`. Each lands as `draft` and stays draft until the user explicitly confirms it (`AGENTS.md`, hard rule 4). A draft can be used with its status stated.

## Pass 5: first golden questions

Hand off to `skills/golden-questions/SKILL.md` for three to five questions the user already knows the answer to, ideally ones passes 3 and 4 can answer. Gold answers go in `evals/bank/gold/` only. This session has seen them, so it must not be the one that answers them: tell the user the bank is answered in a fresh session (`docs/leakage-rule.md`).

## End of each pass: the recap

One screen, nothing more:

```
Pass N done: <name>
Written: <file>: <what it now holds>   (one line per file)
Not given yet: <skipped items, or "nothing">
Next: pass N+1, <name>. Say "carry on", "skip", "stop here", or ask me a real question.
```

## Close

When the last pass ends, or the user stops:

1. **Set up:** each filled file, one line each.
2. **Still open:** skipped items and passes not run; "set this up" resumes from here.
3. **Three things to try:** ask me a real question you answered recently and compare; ask where a metric or table is defined; ask why something moved last month.
4. **How this improves:** each correction fixes the doc that was wrong, is logged in `docs/corrections.md`, and when a check could catch it, becomes a preflight check and a golden question. The same mistake gets harder to make twice.

## Done

`docs/access.md` and `docs/business-context.md` are filled in, one test query ran, and the access status line reads `Status: set up YYYY-MM-DD` (`docs/definition-of-done.md`). Passes 3 to 5 follow their hand-off skills' criteria.
