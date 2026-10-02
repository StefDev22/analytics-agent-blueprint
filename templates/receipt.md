# Receipt

The provenance receipt at the end of every filed answer: an `analysis.md`, a `dq/*/check.md`, or any other filed result. It tells a reader who did not produce the answer what it rests on, so they can judge it without rerunning anything.

Copy the block below to the end of the filed document and replace every bracketed slot with what was actually done in this session. No field is left blank. `Not checked` is never empty and never "nothing": there is always something a careful analyst would still verify.

---

```markdown
## Receipt

- **Question as understood:** [the question in one sentence, as agreed with the user, including any must-clarify choices]
- **Source tables:** [every table read, fully qualified]
- **Metric definitions used:** [each metrics/ file and its status (active or draft), or "none governed" plus the definition in plain words]
- **Date window and timezone:** [start and end dates, inclusive or exclusive, and the timezone]
- **Filters:** [every filter and exclusion applied, and where each came from]
- **Data freshness:** [the latest date present in the pulled data]
- **Checks run:** [preflight, plus any sanity checks, reconciliations or data-quality checks]
- **Not checked:** [what a careful analyst would still verify before acting on this]
- **Assumptions:** [every assumption the answer rests on, or "none beyond the documented conventions"]
- **Confidence:** [high | medium | low], because [the reason]
- **Query files:** [paths to the SQL that produced every number]
```
