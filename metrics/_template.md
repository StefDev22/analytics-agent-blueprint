---
name: [metric_name]
status: draft | active | deprecated
owner: [the person who confirms this definition]
last_reviewed: never   # YYYY-MM-DD once the user confirms it
---
<!--
Template for a metric file, named metrics/<metric_name>.md. The agent creates it as draft.
Only the user moves it to active (AGENTS.md hard rule 4). Delete this comment in the copy.
-->

## Definition

[The exact calculation in plain words: what is counted or summed, over what population, at what grain, in which timezone.]

## Canonical SQL fragment

```sql
-- The one way this metric is computed. A reusable expression or CTE, not a full answer to a question.
```

## Valid dimensions

[What it is safe to cut this metric by, and what it is not.]

## Known exclusions

[Records left out on purpose: test accounts, internal traffic, cancelled records, and why.]

## Do not confuse with

[The readings that were considered and rejected for this name, and why each is wrong here.]

## Changelog

- YYYY-MM-DD: [created as draft | what changed and why | promoted to active on the user's confirmation]
