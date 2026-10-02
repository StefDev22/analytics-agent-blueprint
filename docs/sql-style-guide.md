# SQL style guide

How SQL in this repo is laid out, in any dialect. The point is that a reader, or the next session, can check a query quickly. Where the dialect in `docs/access.md` forces something different, the dialect wins and the difference is noted here.

## Header comment

Every saved query starts with a short header, five lines or fewer:

```sql
-- What: daily count of completed orders by channel
-- Grain: one row per day per channel
-- Source: <orders_table>, <channels_table>
-- Window: last 28 full days
```

Anything longer (verification counts, history, design debates) belongs in the INDEX row or the table doc.

## Layout

- One statement per file.
- Build the query from CTEs, one step each, in reading order, each named for what it holds (`completed_orders`, not `t1`). The final `SELECT` reads from the last CTE.
- A one-line comment on any CTE whose purpose is not obvious from its name.
- Keywords in one consistent case; one column per line in select lists.

## Columns

- Name every column. No `SELECT *` in a saved query, except to pass through a CTE that already lists its columns.
- Alias computed columns with a name that states the unit or meaning (`revenue_net`, `orders_count`, `conversion_rate`).

## Joins

- Write the join keys explicitly and join on every column of the key.
- Before joining, know the cardinality of both sides from the table docs. If a join can fan out, aggregate to the target grain first.
- Prefer `LEFT JOIN` when rows on the left must survive; say in a comment why an `INNER JOIN` is safe when it drops rows.

## Filters

- Filter early: the date or partition filter and the standard filters from the table doc go in the first CTE that reads the table.
- State the date window with explicit bounds and the timezone it is in.
- Exclusions (test accounts, internal traffic, cancelled records) follow the table doc and the metric definition, never memory.
