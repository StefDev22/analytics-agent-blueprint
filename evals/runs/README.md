# Eval runs

One folder per run, `evals/runs/YYYY-MM-DD_<label>/`, written by `skills/golden-questions/SKILL.md`. A run is never edited after its summary is written; a rerun is a new folder with a new label.

Run folders hold gold results, so they are part of the answer key: a session answering golden questions never opens this folder except to write its own two files.

## What a run folder holds

```
YYYY-MM-DD_<label>/
  summary.md
  <id>/
    candidate.sql    the SQL the answering session ran
    candidate.csv    its full result, with a header row
    answer.md        the answering session's final reply, as given
    gold.csv         the gold query's result, written after every answer is in
    grade.md         the grade: the comparison, the verdict, and the cause of a failure
```

A clarify or refuse question has only `answer.md` and `grade.md`. A blocked question keeps whatever was written and says in `grade.md` what could not run.

## grade.md

```markdown
# <id>: PASS | FAIL | BLOCKED

- Graded by: [the session or person, never the one that answered]
- Column renames: [candidate column -> gold column, or "none"]
- Differences: [missing rows, extra rows, duplicate keys and missing columns; each mismatching cell with gold value, candidate value and difference; or "none". Rules: `skills/golden-questions/SKILL.md`, step 4]
- Behaviour: [for clarify, refuse or flag questions: what the answer did against expected_behaviour]
- Cause: [failures only, one from the list below]
- Blocked because: [blocked only: what could not run]
```

## summary.md

```markdown
# Run YYYY-MM-DD_<label>

- Agent and model: [the coding agent and the model it ran on]
- Repo commit: [the commit the answering sessions ran on, or "not under version control"]
- Slice: tuning | held-out | both
- Answered by: [one fresh session per question | one fresh session for all, with the reason]
- Tuning: [passed] passed, [failed] failed, [blocked] blocked, of [total]
- Held-out: [passed] passed, [failed] failed, [blocked] blocked, of [total], or "not run"
- Not run: [approved questions left out of this run and why, or "none"]

## Failures

| Id | Slice | Cause | One line on what went wrong |
|---|---|---|---|

## Blocked

| Id | What could not run |
|---|---|
```

Causes, one per failure:

- **undefined metric**: no governed definition, so the agent picked a reading.
- **wrong grain or fan-out**: the rows were at the wrong level, or a join repeated them.
- **wrong filter**: an exclusion missed or one applied that should not have been.
- **wrong window**: the dates, their edges or the timezone.
- **wrong source**: a table or column other than the documented one.
- **missing doc**: the fact it needed was not written anywhere it looks.
- **other**: say what.

## evals/log.md

After the summary, append one row to `evals/log.md`: date, label, commit, agent and model, tuning passed/total, held-out passed/total (or "not run"), and a short note that names any blocked questions. The total counts blocked questions, so a check that could not run lowers the score instead of disappearing. Never edit an earlier row.
