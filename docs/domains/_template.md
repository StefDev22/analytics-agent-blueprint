<!--
Template for a domain doc: one file per business area (for example orders, traffic, customers),
named docs/domains/<area>.md. A domain doc is a router: it says what to clarify, which tables
to use and which traps to avoid, and links to the table and metric docs for the detail.
Delete this comment in the copy.
-->
# [Domain name]

## Quick reference

[Two or three lines: what this area covers, the one or two tables most questions start from, and the metric files most often used.]

## Must clarify

The ambiguities to resolve with the user before any query in this area. Each one is a question with the readings it chooses between.

- **[Ambiguous term or ask]:** [reading A] or [reading B]? [Which one is the default if the user has no preference, and why.]

## Dimensions

| Dimension | Where it lives | Values or notes |
|---|---|---|
| [dimension] | [`<table>`.`<column>`] | [allowed values, known quirks] |

## Key tables

| Table | Grain | Use it for | Doc |
|---|---|---|---|
| `<table>` | [one row per ...] | [what questions it answers] | [link to docs/tables/<table>.md] |

## Gotchas

- [A trap specific to this area, the wrong result it produces, and how to avoid it.]

## Standard metrics

- [Metric name]: [link to metrics/<metric>.md], [status].

## Common query patterns

[A short pattern the area uses again and again, with a sentence on when to use it. Point to a filed query in `queries/` rather than repeating long SQL here.]

## Cross-references

- [Related domain docs, table docs, metric files, and `docs/corrections.md` entries about this area.]
