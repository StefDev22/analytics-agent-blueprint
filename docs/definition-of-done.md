# Definition of done

What "done" means for each task type in the router in `AGENTS.md`, plus the rules every type follows. Each skill also carries its own done criteria; where they differ, the skill is more specific, never looser.

| Task type | Done when |
|---|---|
| Quick answer | The answer was given inline with its number, window and definition, and what was not checked. Nothing is filed. |
| Analysis | `analyses/YYYY-MM-DD_topic/` holds `analysis.md` (from `templates/analysis.md`, ending in a receipt), the SQL that produced every number, the result data behind each finding, any charts, and a row in `analyses/INDEX.md`. |
| Reusable query | The `.sql` file is in `queries/` with its header comment, passed preflight, and has exactly one accurate row in `queries/INDEX.md`. |
| Data-quality check | `dq/YYYY-MM-DD_topic/` holds `check.md` with a verdict per check and a receipt, the SQL that ran, and a row in `dq/INDEX.md`. |
| New table or column | A complete doc (not a stub) in `docs/tables/` from its template, linked from the right domain doc, with its Last profiled date. |
| New or changed metric | A file in `metrics/` from the template with `status: draft`, a changelog line, and its row in `metrics/INDEX.md`. It becomes `active` only when the user says so. |
| Lookup | The answer was given inline with the file it came from. Nothing is filed. |
| Golden questions and evals | New entries sit in `evals/bank/` with gold answers in `evals/bank/gold/` approved by the user; a run has a dated record of the questions, the grades and the failures. |
| Setup or reconnect | `docs/access.md` and `docs/business-context.md` are filled in, one test query ran, and the status line reads `Status: set up YYYY-MM-DD`. |

## Universal rules

1. **Preflight before save or run.** Every query passes `skills/sql-preflight/SKILL.md` first. A FAIL is fixed, not waived.
2. **No undocumented table.** A table touched with no doc gets at least a stub in `docs/tables/` in the same session, linked from its domain doc.
3. **No unindexed artifact.** Anything filed in `queries/`, `analyses/` or `dq/` gets its INDEX row in the same session.
4. **A receipt on every filed answer**, from `templates/receipt.md`, every field filled, `Not checked` never empty.
5. **Corrections land the same session.** When the user corrects a table, column, filter or metric assumption, fix the doc that was wrong and add a `docs/corrections.md` entry. If a check could catch it, add a `docs/sql-checks.md` entry and a golden question too.
6. **Deprecations are explicit.** A retired query, table or metric keeps its INDEX row, moved under a Deprecated heading with a one-line reason. Nothing is deleted silently.
7. **Conventions are written down** in the doc that owns them, in the same session they are agreed.
8. **The leakage rule decides what enters `metrics/` and `docs/`** (`docs/leakage-rule.md`).
