# SQL and Data Stores

Follow the repository's database engine, version, migration tool, and query style. This guide applies the shared rules and the [principles](jane-street-principles.md) to SQL queries, schema, migrations, and document stores such as MongoDB. In a database, "make illegal states unrepresentable" means constraints: `NOT NULL`, `CHECK`, foreign keys, and unique indexes enforce the invariant for every writer, including writers you did not write. "Make errors obvious" means distinguishing no rows from a failed query and checking how many rows a write changed. "Write for the reader" means explicit columns, real aliases, and queries split where meaning changes.

## Idioms at a Glance

| Prefer | Avoid | Why |
|---|---|---|
| Bound parameters for every value | String concatenation or interpolation of values | Prevents injection and type confusion |
| An allow-list mapping for dynamic identifiers (sort column, direction) | Interpolating request text into identifiers | Identifiers cannot be bound as parameters |
| Explicit column lists in `SELECT` and `INSERT` | `SELECT *`, `INSERT` without columns | Schema changes do not silently change results |
| Aliases that name the role: `buyer`, `seller`, `order_line` | `a`, `b`, `t1` | Joins read as sentences |
| `JOIN ... ON` | Comma joins with conditions in `WHERE` | Join conditions cannot be forgotten |
| `NOT EXISTS` for anti-joins | `NOT IN (subquery)` on nullable columns | One `NULL` makes `NOT IN` match nothing |
| `IS NULL` and `IS DISTINCT FROM` where supported | `= NULL` | `NULL = NULL` is unknown, not true |
| `NOT NULL`, `CHECK`, foreign keys, unique constraints | Application-only validation | The database rejects bad data from every writer |
| `ORDER BY` a unique key whenever results are paged or limited | `LIMIT` with no order or a non-unique order | Pages are deterministic and do not repeat or skip rows |
| `numeric`/`decimal` for money; timestamps with time zone for instants | `float` for money; local timestamps | Exact arithmetic; unambiguous instants |
| Short transactions with explicit boundaries | Transactions held open across network calls or user input | Avoids lock contention and long-held resources |
| Expand-and-contract migrations | Renaming or dropping columns that running code still reads | Old and new versions keep working during deployment |
| Checking affected-row counts on `UPDATE` and `DELETE` | Assuming a write changed one row | Missing rows and concurrent changes become visible |

## Smells Reviewers Flag

- Any query built with `+`, `f"..."`, `${...}`, or `String.format` that contains a value.
- `SELECT *` in application code.
- `UPDATE` or `DELETE` whose `WHERE` clause could match more rows than intended, or no `WHERE` at all.
- `NOT IN` against a subquery on a nullable column.
- `LIMIT`/`OFFSET` without `ORDER BY` a unique key; deep `OFFSET` paging on large tables.
- Validation in application code for an invariant the database could enforce.
- A migration that renames, retypes, or drops a column in the same release that changes the code reading it.
- A data backfill in one unbounded statement on a large table.
- Catching a query exception and returning an empty list.
- MongoDB filters built from request objects without checking that each value is a scalar.

## Good and Bad Pairs

### Bind Values; Never Build Queries from Input

Bad (Python fragment):

```python
cursor.execute(f"SELECT id, email FROM users WHERE email = '{email_address}'")
```

An address such as `x' OR '1'='1` returns every user.

Good (complete Python example using the standard `sqlite3` module):

```python
import sqlite3


def find_user_id_by_email(connection, email_address):
    found_row = connection.execute(
        "SELECT id FROM users WHERE email = ?",
        (email_address,),
    ).fetchone()
    return found_row[0] if found_row is not None else None
```

The value travels separately from the SQL text, so it can never change the query. `None` means no matching user; a database error still raises. Use the placeholder syntax of the repository's driver (`?`, `%s`, `$1`, or `:name`).

Check: a known address returns its ID; an unknown address returns `None`; the injection string returns `None`.

### Allow-List Dynamic Identifiers

Bad (Python fragment):

```python
query = f"SELECT id, name FROM products ORDER BY {request_sort_column} {request_direction}"
```

Column names and directions cannot be bound, so they are pasted in verbatim.

Good (Python fragment):

```python
SORTABLE_PRODUCT_COLUMNS = {"name": "name", "price": "price_in_cents", "newest": "created_at"}
SORT_DIRECTIONS = {"ascending": "ASC", "descending": "DESC"}

sort_column = SORTABLE_PRODUCT_COLUMNS[requested_sort_key]
sort_direction = SORT_DIRECTIONS[requested_sort_direction]
query = f"SELECT id, name FROM products ORDER BY {sort_column} {sort_direction}, id"
```

Only fixed strings from the mapping reach the SQL text; an unknown key raises `KeyError`, which the boundary turns into a 400 response. The trailing `id` makes the order deterministic.

### `NOT IN` Breaks on `NULL`

Bad (SQL):

```sql
SELECT customer.id
FROM customers AS customer
WHERE customer.id NOT IN (SELECT blocked.customer_id FROM blocked_customers AS blocked);
```

If any `blocked_customers.customer_id` is `NULL`, the condition is unknown for every row and the query returns nothing.

Good (SQL):

```sql
SELECT customer.id
FROM customers AS customer
WHERE NOT EXISTS (
    SELECT 1
    FROM blocked_customers AS blocked
    WHERE blocked.customer_id = customer.id
);
```

`NOT EXISTS` ignores the `NULL` row and returns every unblocked customer. Better still, make `blocked_customers.customer_id` `NOT NULL`.

Check: with a `NULL` in `blocked_customers`, the bad query returns no rows and the good query returns the unblocked customers.

### Let the Database Enforce the Invariant

Bad (SQL):

```sql
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount_in_cents INTEGER,
    status TEXT
);
```

Any writer can insert an invoice with no customer, a negative amount, or the status `'payed'`.

Good (SQL; SQLite syntax, which most engines share):

```sql
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers (id),
    amount_in_cents INTEGER NOT NULL CHECK (amount_in_cents > 0),
    status TEXT NOT NULL CHECK (status IN ('draft', 'sent', 'paid', 'void'))
);
```

The table rejects invalid rows from every writer: this service, a script, a migration, or a future service. Keep the matching validation in the application too, so users get a clear message before the database refuses the write. SQLite enforces foreign keys only after `PRAGMA foreign_keys = ON`.

Check: valid rows insert; a missing customer, a zero amount, and status `'payed'` are rejected by the database.

### Page Deterministically

Bad (SQL):

```sql
SELECT id, title FROM articles ORDER BY published_at DESC LIMIT 20 OFFSET 40;
```

Articles with the same `published_at` can appear on two pages or none, and deep offsets scan and discard rows.

Good (SQL; keyset pagination with parameters from the previous page's last row):

```sql
SELECT id, title, published_at
FROM articles
WHERE (published_at, id) < (:last_published_at, :last_id)
ORDER BY published_at DESC, id DESC
LIMIT 20;
```

The unique `id` breaks ties, so the order is total, and the next page starts exactly after the last row seen. Row-value comparison is supported by PostgreSQL, MySQL 8, and SQLite 3.15+; otherwise write the equivalent `OR` condition.

### Expand and Contract Instead of Renaming in Place

Bad (migration):

```sql
ALTER TABLE users RENAME COLUMN name TO display_name;
```

During a rolling deployment, the old application version still reads `name` and fails.

Good (sequence of releases):

```text
Release 1: add display_name (nullable); write both columns; backfill display_name in bounded batches.
Release 2: read display_name; keep writing both; verify every row has display_name.
Release 3: stop writing name; make display_name NOT NULL.
Release 4: drop name after confirming no reader remains.
```

Each release works with the schema before and after it, and each step can be rolled back. Batch the backfill with a bounded `WHERE id BETWEEN ...` range or a `LIMIT` loop, and record progress.

### MongoDB: Filters Take Validated Scalars

Bad (JavaScript fragment):

```javascript
const orders = await ordersCollection.find({ customerId: request.query.customerId }).toArray();
```

With a query string such as `customerId[$ne]=x`, the extended query parser (the Express 4 default) produces the object `{ $ne: "x" }`, and the filter returns every other customer's orders.

Good (JavaScript fragment):

```javascript
const requestedCustomerId = request.query.customerId;
if (typeof requestedCustomerId !== "string" || !CUSTOMER_ID_PATTERN.test(requestedCustomerId)) {
  throw new BadRequestError("customerId must be a customer ID string");
}
const customerOrders = await ordersCollection
  .find({ customerId: requestedCustomerId }, { projection: { _id: 1, total: 1, placedAt: 1 } })
  .toArray();
```

The value is checked to be a well-formed string before it reaches the filter, and the projection names the fields returned. Back the invariant with a collection `$jsonSchema` validator and unique indexes where the data store owns it, as relational tables use constraints.

## Implementation Recipe

1. Inspect the engine and version, the migration tool and its history, existing constraints and indexes, and how the application maps rows to domain values.
2. Put invariants into constraints when the database owns the data; keep application validation for clear user messages.
3. Bind every value; allow-list every dynamic identifier.
4. Name columns and aliases for their role; split complex queries with CTEs that name each stage.
5. Distinguish no rows from failure in the calling code; check affected-row counts for writes that must change exactly one row.
6. Plan migrations as expand-and-contract with bounded backfills and a stated rollback.
7. Run queries against the real engine; inspect query plans for new filters, joins, and sorts on large tables.

## Evidence and Review

A migration that parses or a query that runs once does not prove correctness under real data volumes, `NULL` values, or concurrent writers. Test constraints by attempting invalid writes, test queries with `NULL` and duplicate sort keys, and record the actual database behavior. See [configuration and templates](templates-and-configuration.md) for migration deployment rules.
