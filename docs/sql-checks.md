# User checks for SQL preflight

`skills/sql-preflight/SKILL.md` runs its generic checks first, then every entry in this file. This file is owned by the user and grows from corrections: each entry is a check born from a mistake recorded in `docs/corrections.md`. It ships empty on purpose.

## When to add an entry

When a correction is detectable by reading the SQL text, add an entry in the same session as the correction. If the mistake can only be seen in the results, it belongs in a domain or table doc as a gotcha, not here.

## Entry format

```markdown
### SC<n>: short name

- **Rule:** what the SQL must or must not do, in one sentence.
- **Why:** the `docs/corrections.md` entry or the `dq/` folder it came from (date and title).
- **How to spot it:** what in the SQL text gives it away: a table, a column, a pattern.
- **Severity:** FAIL (blocks save and run) or WARN (reported, does not block).
- **Exceptions:** when the rule does not apply, or "none".
```

Number entries in order and never reuse a number. A retired check stays in place with `Retired YYYY-MM-DD: reason` as its first line.

## Example shapes

These are illustrations of the kinds of trap that tend to end up here. They are inside a comment, so preflight ignores them.

<!--
### SC1: no multiplication of a pre-multiplied line total
- **Rule:** never multiply `<line_total_column>` by `<quantity_column>`; it already includes quantity.
- **Why:** a revenue figure came out inflated because the total was multiplied a second time.
- **How to spot it:** `<line_total_column>` and `<quantity_column>` in the same arithmetic expression.
- **Severity:** FAIL
- **Exceptions:** none.

### SC2: no sum of a coarser-grain measure after a fan-out join
- **Rule:** an order-level measure is not summed after joining `<orders_table>` to a line-level table.
- **Why:** the join repeated each order once per line, so order totals were counted several times.
- **How to spot it:** `SUM(<order_level_measure>)` in a query that joins `<orders_table>` to `<order_lines_table>`.
- **Severity:** FAIL
- **Exceptions:** the measure is aggregated to order grain in a CTE before the join.

### SC3: test accounts are excluded
- **Rule:** any query on `<customers_table>` or a table joined to it filters `<is_test_column> = FALSE`.
- **Why:** internal test accounts inflated a customer count.
- **How to spot it:** `<customers_table>` appears and `<is_test_column>` does not.
- **Severity:** WARN
- **Exceptions:** a data-quality check that counts the test accounts on purpose.
-->

## Entries

None yet.
