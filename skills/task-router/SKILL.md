---
name: task-router
description: Use when any request arrives, first, before any other skill, lookup or SQL. Classifies the request into one row of the AGENTS.md task router, sets the depth it needs, and hands off to that row's skill. Does not answer, look things up or write SQL itself.
---

# Task router: classify first, then set the depth

Classify the request into one row of the task router in `AGENTS.md`, set its depth, then open that row's skill and follow it to the row's deliverable. This skill decides the lane; it does not do the work.

**Gate:** if `docs/access.md` says `Status: not set up`, any request goes to `skills/setup/SKILL.md` first. Keep the user's question and return to it once setup allows.

## Classify by the shape of the ask

Read what the user wants to end up with. A tool or file format named in the ask says where the answer lands, not what the task is.

| The ask ends in... | Row |
|---|---|
| a figure, said back in the chat | Quick answer |
| findings with a narrative, or "why did X move" | Analysis |
| SQL they will run again themselves | Reusable query |
| a verdict on whether data is complete or consistent | Data-quality check |
| a new table or column documented | New table or column |
| a metric defined or redefined | New or changed metric |
| a pointer to where something is defined | Lookup |
| golden questions written or run | Golden questions and evals |
| a working connection or onboarding | Setup or reconnect |

A request that fits no row (explain this SQL, how does the repo work) is answered directly, with nothing filed. Never invent a new deliverable type. A problem with the repo itself goes to `docs/findings.md`.

## Set the depth

Depth is set by what the question needs, not by how short the ask is.

| Depth | Rows | Do | Skip |
|---|---|---|---|
| L0, lookup | Lookup | Read the docs in `skills/knowledge-router/SKILL.md` order and answer | Any SQL, any filed artifact |
| L1, one query | Quick answer | Lookups, one query plus its sanity checks, preflight, inline answer with a mini receipt | A folder, a chart, an INDEX row, `wrap-up-analysis` |
| L2, one bounded deliverable | Reusable query, data-quality check, table, metric, golden questions | That skill's steps and its one deliverable | A narrative, charts nobody asked for, an analysis folder |
| L3, full loop | Analysis | All of `skills/answer-question/SKILL.md`, then `skills/wrap-up-analysis/SKILL.md` | Nothing |

**It is an analysis** when answering takes more than one query, compares periods or segments and interprets the difference, explains why something moved, or ends in a recommendation. "Quick" lowers the depth only when one query and one stated number really answer it. When your depth differs from what the wording suggests, say which you chose and why in one line, then proceed.

**Never default to the full loop.** An unrequested analysis folder is as much a miss as a bare number where findings were wanted.

## Ask or assume

- **Ask one question** only when two readings lead to a different deliverable or a materially different number and no doc settles it. Name the two readings, and wait for the answer.
- **Otherwise state the assumption in one line and proceed**, for example: "Reading this as a quick answer; say if you want it written up."
- Never ask what a doc answers or about style (the style guides decide). Must clarify items are asked in `skills/answer-question/SKILL.md`.

## Mixed requests

A session can mix types. Pick the **primary** deliverable, name the hand-off out loud, and never produce two terminal deliverables for one ask.

- An analysis touches a table with no doc: the analysis stays primary; the table gets a stub through `skills/onboard-table/SKILL.md` in the same session.
- A quick answer turns out to matter (surprising, or it needs a comparison): say so and offer the analysis. Do not upgrade silently.
- An analysis yields SQL the user wants to rerun: file it as a reusable query, a named hand-off.
- A correction mid-task runs the loop in `docs/corrections.md` in the same session, whatever the row.

## Hand-off

Open the row's skill (`skills/<name>/SKILL.md`) and follow it. For a data question, that skill runs `skills/knowledge-router/SKILL.md` before any SQL.
