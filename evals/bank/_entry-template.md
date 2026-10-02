---
id: [short id, never reused, same as the file name]
question: "[the wording as a stakeholder would ask it, naming the window]"
sharp_question: "[the unambiguous version: metric, population, grain, filters, window, timezone]"
domain: [the doc in docs/domains/ this question belongs to]
task_type: [a task type from the router in AGENTS.md]
expected_shape: number | table | clarify | refuse
window:
  start: YYYY-MM-DD
  end: YYYY-MM-DD
keys: []
measures: []
tolerance: 0.02
held_out: false
status: proposed
approved_by:
approved_on:
source: "[a real ask and its date | a correction: its date and title in docs/corrections.md]"
expected_behaviour: "[clarify, refuse or flag questions only: what the agent must do]"
---
<!--
Template for one golden question, named evals/bank/<id>.md. Delete this comment in the copy.

- window: inclusive dates in the timezone the domain doc names, closed and in the past. Never a
  rolling phrase such as "last month": the gold query is rerun at every grading.
- keys: the result columns that identify a row (a date, a region). Empty for a single-number answer.
- measures: the result columns compared numerically within tolerance. Empty for clarify and refuse.
- tolerance: relative; when the gold value is 0 it is absolute.
- held_out: true for about one in three questions, never for one written from a correction.
- status: the agent writes proposed. Only the user sets approved, approved_by and approved_on.
- expected_behaviour: required for clarify and refuse; on a number or table question it is an
  extra check, such as "states that one day of data is missing".

The gold query lives at evals/bank/gold/<id>.sql, never in this file. Nothing here states the answer.
-->

## Why this is a trap

[What a careless answer would get wrong: the metric with two readings, the filter a newcomer misses, the join that fans out, the window edge. Describe the trap, not the result.]
