# Evals

The golden-question bank and the record of every run against it. It ships empty: you write the questions, with the agent's help, from your own business.

## What a golden question is

A question someone really asks, with an answer you have checked yourself. The agent answers it blind, the way it would answer anyone, and its result is compared with yours.

When the agent gets one wrong, the cause is almost always missing or wrong context: an undefined metric, a table doc that never mentioned a filter, a join that fans out. So the fix goes into the docs, the metric file or the check list, and then the question is run again. The bank tells you whether the repo is getting better or only feels like it.

## Principles

1. **You write or approve every gold answer.** The agent drafts; only you mark an entry `approved` (`ARCHITECTURE.md`, Human only).
2. **Gold is independent and hidden.** The gold query is written with you, not copied from the agent's answer, and the session that answers never opens `bank/gold/` (`AGENTS.md` hard rule 6, `docs/leakage-rule.md`).
3. **Gold is a query, not a number.** Each question has a fixed date window and its gold query is rerun at grading time. The bank survives new data and late corrections; nothing stores a number that can go stale or leak.
4. **Grade results, not SQL.** Two different queries that return the same rows within tolerance both pass.
5. **Whatever produced an answer never grades it.** The grading step is a different session, or you.
6. **A check that could not run is blocked, never a pass.** A gold query that errors or a warehouse that is unreachable is reported as blocked and counted in the total.
7. **Hold some questions out.** About one in three is `held_out: true`. Nobody reads those while tuning the docs; they are run once at the end of a tuning round to show whether the gains are real.
8. **Start small and grow from mistakes.** Five to ten questions is enough to start. Every correction that a check could catch adds one more (`docs/corrections.md`).

## Layout

```
evals/
  README.md            this file
  grade.py             compares a candidate result with a gold result
  log.md               one row per run, append-only
  bank/
    _entry-template.md the shape of an entry
    <id>.md            one golden question each
    gold/
      README.md
      <id>.sql         the gold query, read only by you and the grading step
  runs/
    README.md          what a run folder holds
    YYYY-MM-DD_<label>/
```

## How a run works

`skills/golden-questions/SKILL.md` is the runbook. In brief:

1. Pick the slice: the tuning questions, or the held-out ones at the end of a round.
2. Each approved question goes to a fresh session that has never opened `evals/`. It answers the stakeholder wording under the normal contract and saves its SQL and result into the run folder.
3. Only after every answer is saved, the gold queries run, read-only and preflighted.
4. Each result pair is graded with `python3 evals/grade.py`, or by hand where Python is not available. Questions whose right answer is to clarify or refuse are graded from the answer text against `expected_behaviour`.
5. The run gets a `summary.md` and a row in `log.md`.
6. Each failure gets a cause and a fix in the docs, never the answer itself. The tuning slice runs again; the held-out slice runs once, last.
