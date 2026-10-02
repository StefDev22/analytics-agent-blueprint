# The leakage rule

Meaning is safe to give the agent. The query and the number are not.

A metric definition tells the agent what to compute. A gold query tells it exactly how a particular question is answered. A result value is the answer. The first is context; the last two are an answer key. A golden question whose answer the agent can read at answer time does not test the agent: it tests whether the agent can find the answer key.

## What may enter `metrics/` and `docs/`

- Definitions in plain words, and the canonical SQL fragment for a metric: the reusable expression that computes it.
- Known-wrong formulas and why they are wrong ("multiplying the line total by quantity counts it twice").
- Table grain, keys, filters, gotchas and verified example queries that illustrate a pattern.

## What may not

- The numeric result of any question in `evals/bank/`.
- The full gold query of any question in `evals/bank/`.
- Any sentence that settles a bank question outright ("last quarter's churn rate was N").

A metric fragment in `metrics/` is fine even when a golden question uses that metric: the question then tests whether the agent finds the definition, applies it to the right window and filters, and reads the result correctly. Write bank questions so that no file outside `evals/bank/gold/` states their answer. That includes filed work: if `queries/` or `analyses/` already holds the result for a question and its window, pick another window for the bank.

## Why the answering session never opens `evals/bank/gold/`

The gold folder holds the answer key. A session that reads it before or while answering would be graded on copying, and the eval would report a skill the agent does not have. So the session that answers a golden question never opens that folder, and opens nothing else under `evals/` either: bank entries carry hints and old run folders carry gold results. Grading happens in a separate step, by a separate session or by the user, after the answer is recorded.

## When a golden question fails

Fix the meaning, not the number. A failure leads to a correction (`docs/corrections.md`) that fixes the definition, the table doc or the check list. The gold number is never pasted into `docs/` or `metrics/` to make the question pass.
