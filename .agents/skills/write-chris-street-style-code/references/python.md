# Python

Follow the project's supported Python, test runner, formatter and type checker.
- Prefer functions and dataclasses; frozen values, enums and unions should clarify real states, not create a class hierarchy by default.
- Type hints do not validate runtime input. Validate once at CLI/configuration/deserialization boundaries.
- Use None for one legitimate absence case. Raise specific exceptions, preserve causes with exception chaining, and never hide faults behind success or empty values.
- Use context managers for resources. Avoid import-time I/O and global mutable configuration; expose lazy I/O and single-use generators.
- Own and await async tasks, propagate cancellation, and avoid blocking the event loop. Make shared-state synchronization explicit.
- Keep CLIs thin over reusable logic. Use Protocols only when consumers benefit from actual alternative implementations or a necessary test seam.
- Prefer temporary directories and real files; test outcomes, exception types and meaningful boundaries. Control clocks/randomness when they affect behavior.

## Implementation Recipe

1. Inspect the supported Python version and local formatter, analyzer/type-checker, and tests. Use snake_case for functions/parameters unless an external protocol requires another form.
2. Choose functions and small data representations first. A frozen dataclass or validated constructor is useful when it preserves a joint invariant; typing alone does not reject bad runtime input.
3. Pair method/function names and parameters: `send_invoice_to(invoice, recipient)` and `load_orders_for(customer_id)`. Inspect keyword callers before renaming parameters.
4. Give each material transformation its own binding. Keep `raw_attempt_count` distinct from `attempt_count` and `response_text` distinct from `validated_order`.
5. Catch intended exceptions only, chain translated failures with `raise ... from cause`, and keep None reserved for its documented absence meaning. Context managers own resources; async callers own awaits and cancellation.
6. Check parsing, boundaries, failures/causes, and outcomes with native tooling and focused tests. Avoid import-time I/O and CLI logic that cannot be used independently of global state.

## Good and Bad Parsing

Contract: input is text accepted by Python's decimal integer parser; valid attempt counts are integers from 1 through 10. Invalid textual values raise ValueError with useful context.

Bad (complete Python example):

```python
def parse_count(data):
    try:
        return int(data)
    except Exception:
        return 0
```

It accepts out-of-range values and converts every failure into an apparently usable sentinel.

Good (complete Python example):

```python
def parse_attempt_count_from(raw_attempt_count):
    try:
        attempt_count = int(raw_attempt_count)
    except ValueError as cause:
        raise ValueError("Attempt count must be an integer from 1 through 10") from cause
    if not 1 <= attempt_count <= 10:
        raise ValueError("Attempt count must be from 1 through 10")
    return attempt_count
```

The new variable names the parsed value; invalid text keeps its cause; the range is enforced. A non-text input violates this function's boundary contract: add shape validation at the external input boundary rather than pretending all programming errors are missing data.

## Evidence and Review

Check valid endpoints, invalid text, out-of-range values, and the error cause. Use the [selection and assertion examples](good-and-bad-examples.md#1-names-explain-the-operation) for sentence-like data flow and observable results. A difficult test that patches many internals is a reason to inspect the boundary before adding another mock layer.
