# Gold queries

One file per golden question, `<id>.sql`, matching `evals/bank/<id>.md`. Each is the query you approved as the right answer to that question for its fixed window.

This folder is the answer key. **The session that answers a golden question never opens it** (`AGENTS.md` hard rule 6, `docs/leakage-rule.md`). Only you and the grading step read it, and nothing in it is copied into `docs/`, `metrics/`, `queries/` or `analyses/`.

A gold query is preflighted (`skills/sql-preflight/SKILL.md`) before it is saved and before every run. Changing one sets its entry back to `status: proposed` until you approve the new result.
