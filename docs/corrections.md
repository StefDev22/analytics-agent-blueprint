# Corrections log

Append-only, newest first. One entry per mistake the agent made and someone caught, whether or not it ever reached anyone.

## Why this exists

When a mistake is found, the doc that was wrong gets fixed in the same session. That is right, but it erases the event: once the doc says the right thing, nothing shows it ever said the wrong thing, or what shipped in the meantime. This log is that record. It is the first thing a new reader should open to see where this repo has actually been wrong, and it is the raw material for the check list and the golden questions.

## What every correction produces

In the same session:

1. **A doc fix**: the domain, table or metric doc that was wrong now says the right thing.
2. **An entry here**, in the format below.
3. **When a check could catch it**: a new entry in `docs/sql-checks.md` if the mistake is visible in the SQL text, and a golden question in `evals/bank/` that would fail if the mistake came back.

## Entry format

```markdown
## YYYY-MM-DD: one-line title

**What went wrong:** what the agent did or said, and what was true instead.
**Blast radius:** what was affected, and whether it reached anyone.
**Root cause:** the underlying reason, not the symptom.
**Fix:** what changed, in which file.
**Detectable by a check?** yes, no or partly, and by what: a `docs/sql-checks.md` entry, a golden question, or nothing yet.
```

Cite an entry by its date and title, never by its position in this file.

## Entries

None yet.
