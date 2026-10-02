<!--
Template for a table doc: one file per table the agent reads, named docs/tables/<table>.md and
linked from its domain doc. A stub keeps at least Purpose and grain, Partition or date column,
and a "Stub, not profiled" line under Last profiled. Delete this comment in the copy.
-->
# `<schema>.<table>`

## Purpose and grain

[What the table holds and what one row is: "one row per order line", "one row per session per day".]

## Owner and freshness

- Owner: [team or person role who can answer questions about it]
- Refreshed: [how often, and by when the previous day is complete]
- Latency or late-arriving data: [anything that makes recent days incomplete]

## Partition or date column

[The column every query filters on, its type and timezone. Say if the table is not partitioned.]

## Columns

| Name | Type | Meaning | Notes |
|---|---|---|---|
| `<column>` | [type] | [what it means in business terms] | [nulls, units, known values, quirks] |

## Keys and joins

| Joins to | On | Cardinality | Notes |
|---|---|---|---|
| `<other_table>` | `<key_column>` | [one to one, one to many, many to many] | [fan-out risk, unmatched rows] |

## Standard filters

[Filters almost every query needs: test accounts, internal traffic, cancelled or deleted records. Say why each one exists.]

## Gotchas

- [A trap in this table, the wrong result it produces, and how to avoid it.]

## Verified example queries

```sql
-- What: [what the query returns]
-- Verified: YYYY-MM-DD, [what was checked]
```

## Last profiled

[YYYY-MM-DD: row count, date range present, null rates on key columns, or "Stub, not profiled".]
