# SQL checks

Use with [languages.md](languages.md).

Find the dialect first: the project's documentation, the database driver, the migration tool. The same statement can be valid in one engine and wrong in another. Say which dialect you assumed.

## Build and tools

| Tool | Command | Finds |
|---|---|---|
| Scratch database | Load the schema into an empty database (`sqlite3 :memory:`, a throwaway PostgreSQL or MySQL database) and run each statement | Syntax errors, missing tables and columns, wrong results on test data |
| Query plan | `EXPLAIN` or `EXPLAIN QUERY PLAN` | Full scans, an index that is not used |
| SQLFluff | `sqlfluff lint --dialect <dialect>` | Ambiguous columns, unused aliases and CTEs, style the project has configured |
| Tests | The project's own query or migration tests | Runtime behaviour |

Run statements only against a scratch database you created. Never connect to a database named in the project's configuration, and never apply a migration anywhere else.

## Frequent bugs

- **NULL logic**: `= NULL` and `<> NULL`, which are never true; `NOT IN (subquery)` when the subquery can return a NULL, which returns no rows; `<>` silently dropping NULL rows; `COUNT(column)` where `COUNT(*)` was meant; `SUM` over no rows giving NULL.
- **Join fan-out**: joining a one-to-many table and then summing or counting, so each row counts several times. `DISTINCT` added to hide it.
- **Outer join turned inner**: a `WHERE` condition on the optional side of a `LEFT JOIN`. It belongs in the `ON` clause.
- **Missing join condition**: a comma join or a join with no usable condition, giving every combination.
- **`UPDATE` or `DELETE` with no `WHERE`**, or with a condition that ignores a parameter the statement is given.
- **`GROUP BY`**: a selected column that is neither grouped nor aggregated, which some engines accept and fill with an arbitrary row; a filter in `HAVING` that belongs in `WHERE`.
- **`AND` and `OR` mixed without parentheses**. `AND` binds first.
- **Order and limits**: `LIMIT` with no `ORDER BY`; paging over an order that is not unique.
- **Types**: numbers or dates compared as text; `BETWEEN` on timestamps losing the last day; integer division; money in floats.
- **Injection**: a statement built by concatenating input, in a stored procedure or in the code that calls the query.
- **Transactions**: several statements that must all succeed with no transaction around them; read, decide, then write with no lock or constraint.
- **Migrations**: `INSERT INTO ... SELECT *` and other positional column lists, which break when column order differs between databases; a `NOT NULL` column added with no default to a table that has rows; a destructive step with no way back; an applied migration edited afterwards.

## Not slop in SQL

- Applied migrations. They are history: never edit, merge, reorder or tidy them, whatever they contain.
- Indexes, constraints, triggers and views that nothing in the repository names. The engine uses them, or a reporting tool or another service does.
- Seed and fixture data, even when rows look repeated.
- `WHERE 1 = 1` and placeholder comments in a query the application completes.
- `IF EXISTS` and `IF NOT EXISTS`, `COALESCE` defaults, an explicit transaction around statements that belong together, an explicit lock.
- Explicit column lists, `INNER`, `AS` and `ASC`. They are the long form, not noise.
- Two queries that look alike but answer different questions. Do not merge them into one view or one parameterised query.
- A join, a `DISTINCT` or a condition that looks unneeded. Removing one can change the rows returned. Report it; do not remove it as cleanup unless a test proves the result is the same.
- `-- noqa` and other linter directives.
