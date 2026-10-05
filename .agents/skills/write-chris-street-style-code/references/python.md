# Python

Follow the project's supported Python version, test runner, formatter, and type checker. This guide applies the shared rules and the [principles](jane-street-principles.md) to Python. Python trusts the programmer: nothing stops a function from mutating its argument, catching every exception, or returning `None` on one path and a list on another. The style supplies the discipline Python leaves out: validate at boundaries, keep values immutable where you can, use enums and dataclasses for closed states, catch narrowly, and make absence and failure visible in names and return types.

## Idioms at a Glance

| Prefer | Avoid | Why |
|---|---|---|
| Functions and small frozen dataclasses | Classes with mutable state by default, or bare dicts passed through many layers | Values with names and fixed fields are easier to trust |
| `Enum` (or `Literal` types) for closed sets | Raw strings compared throughout the code | Typos fail loudly; a type checker finds missing cases |
| `match` with `assert_never`, or a final branch that raises | `else: pass` or a default that returns a placeholder | New cases fail instead of passing silently |
| Validation once at CLI, config, HTTP, and file boundaries | Trusting type hints; re-checking in every function | Hints are not enforced at runtime |
| Specific exceptions, `raise ... from cause` | Bare `except:`, `except Exception: pass`, returning `None` or `0` on failure | Callers can separate absence, rejection, and failure |
| `None` for exactly one documented absence meaning | `None` meaning "missing", "error", and "not computed yet" in one function | Readers can tell outcomes apart |
| `with` statements for files, locks, connections, and temp dirs | Manual `close()` | Cleanup runs on every exit |
| `pathlib.Path` and `subprocess.run([...], check=True)` | String path concatenation, `shell=True`, `os.system` | Arguments are not reparsed by a shell |
| Keyword-only parameters (`*`) for flags and same-type arguments | Positional booleans and long positional lists | Call sites name every role |
| `datetime` with time zones, passed in as parameters | Naive datetimes and `datetime.now()` inside rules | Time is explicit and testable |
| `decimal.Decimal` or integer minor units for money | `float` for money | Binary floats cannot represent most decimal amounts |
| `None` defaults, with a new list or dict created inside | Mutable default arguments (`items=[]`) | Defaults are evaluated once and shared across calls |
| Explicit dependencies passed as parameters | Import-time I/O, module-level clients, global mutable config | Importing a module has no effects; tests do not need patching |
| `asyncio.TaskGroup` or awaited tasks with clear owners | `create_task` with no reference, blocking calls inside `async def` | Failures are observed and the event loop stays responsive |

## Smells Reviewers Flag

- `except:` or `except Exception:` that continues, returns a default, or only logs.
- `raise NewError(str(error))` without `from error`.
- A function that returns `None` on some paths and a value on others, without saying so in the name or annotation.
- Mutable default arguments.
- `dict` objects with stringly-typed keys passed through many functions where a dataclass would name the fields.
- Reassigning a variable to a different kind of data: `data = json.loads(data)`, `user = user["id"]`.
- `datetime.now()`, `time.time()`, or `random` inside business rules.
- `subprocess` with `shell=True` and interpolated values; `os.path.join` with untrusted segments and no containment check.
- Work at import time: network calls, file reads, environment parsing that raises.
- `assert` used for input validation (asserts are removed under `python -O`).
- `# type: ignore` without a reason; `Any` spreading through signatures.
- Tests that patch many internals or depend on dictionary or set ordering that the code does not guarantee.

## Good and Bad Pairs

The cross-language catalogue has Python pairs for [naming](good-and-bad-examples.md#1-names-explain-the-operation), [resource cleanup](good-and-bad-examples.md#6-resource-cleanup-covers-every-exit), [result-based assertions](good-and-bad-examples.md#7-assertions-prove-behavior), [flags to enums](good-and-bad-examples.md#9-replace-boolean-flags-with-named-choices), [closed values at the boundary](good-and-bad-examples.md#12-parse-strings-into-closed-values-at-the-boundary), [guard clauses](good-and-bad-examples.md#15-guard-clauses-keep-the-normal-path-flat), [passing the clock in](good-and-bad-examples.md#17-pass-the-clock-in), [named constants](good-and-bad-examples.md#19-named-constants-instead-of-magic-numbers-and-lying-comments), [fallible names](good-and-bad-examples.md#22-name-the-operation-that-can-fail), and [expect-style tests](good-and-bad-examples.md#24-expect-style-tests-show-the-whole-output). The pairs below are Python-specific.

### Parsing Keeps Its Cause and Its Range

Contract: input is text accepted by Python's decimal integer parser; valid attempt counts are integers from 1 through 10. Invalid textual values raise `ValueError` with useful context.

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

### A Frozen Dataclass Holds Its Invariant

Bad (complete Python example):

```python
class PriceRange:
    def __init__(self, low, high):
        self.low = low
        self.high = high
```

Nothing stops `PriceRange(50, 10)`, and any caller can later set `price_range.low = 999`.

Good (complete Python example):

```python
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class PriceRange:
    lowest_price: Decimal
    highest_price: Decimal

    def __post_init__(self):
        if self.lowest_price < 0:
            raise ValueError("lowest_price must not be negative")
        if self.highest_price < self.lowest_price:
            raise ValueError("highest_price must not be below lowest_price")

    def includes(self, candidate_price):
        return self.lowest_price <= candidate_price <= self.highest_price
```

Construction checks the invariant and `frozen=True` keeps it true. `price_range.includes(candidate_price)` reads as a question. The range is inclusive on both ends, which the method states by its comparison and a test should pin down.

Check: valid ranges construct; reversed or negative ranges raise `ValueError`; both endpoints are included; assigning a field raises `FrozenInstanceError`.

### Mutable Default Arguments Are Shared

Bad (complete Python example):

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags
```

The default list is created once. `add_tag("a")` then `add_tag("b")` returns `["a", "b"]`: the second call sees the first call's data.

Good (complete Python example):

```python
def with_added_tag(tag, existing_tags=None):
    updated_tags = list(existing_tags) if existing_tags is not None else []
    updated_tags.append(tag)
    return updated_tags
```

Each call builds its own list, the caller's list is not mutated, and the name `with_added_tag` says a new collection is returned.

Check: two calls without `existing_tags` return independent lists; a passed list is unchanged.

### Catch Narrowly; Absence Is Not Failure

Bad (complete Python example):

```python
import json


def load_settings(path):
    try:
        with open(path, encoding="utf-8") as settings_file:
            return json.load(settings_file)
    except Exception:
        return {}
```

A missing file, a permissions error, malformed JSON, and a typo in the code all become "no settings", and the program runs with defaults nobody chose.

Good (complete Python example):

```python
import json


class SettingsFileError(Exception):
    pass


def load_optional_settings_from(settings_path):
    try:
        with open(settings_path, encoding="utf-8") as settings_file:
            settings_text = settings_file.read()
    except FileNotFoundError:
        return None
    try:
        decoded_settings = json.loads(settings_text)
    except json.JSONDecodeError as cause:
        raise SettingsFileError(f"Settings file {settings_path} is not valid JSON") from cause
    if not isinstance(decoded_settings, dict):
        raise SettingsFileError(f"Settings file {settings_path} must contain a JSON object")
    return decoded_settings
```

Only a missing file means "no settings" and returns `None`, as the name `load_optional_settings_from` says. Unreadable files raise their own `OSError`, malformed content raises a specific error with the path and cause, and programming errors are not caught at all.

Check: a missing file returns `None`; valid JSON objects load; malformed JSON and a JSON list raise `SettingsFileError` with the path; a directory path raises an `OSError`.

### Subprocesses Take Argument Lists

Bad (Python fragment):

```python
os.system(f"git log --format=%H {branch_name}")
```

A branch name containing `; rm -rf ~` runs a second command. The exit status is ignored.

Good (Python fragment):

```python
completed_process = subprocess.run(
    ["git", "log", "--format=%H", "--end-of-options", branch_name],
    capture_output=True,
    text=True,
    check=True,
)
commit_hashes = completed_process.stdout.splitlines()
```

The argument list is passed without a shell, `--end-of-options` keeps a name starting with `-` from becoming an option (Git 2.24+), and `check=True` raises `CalledProcessError` with the exit code instead of continuing with empty output.

### Async Tasks Have Owners

Bad (Python fragment):

```python
async def refresh_all(feed_ids):
    for feed_id in feed_ids:
        asyncio.create_task(refresh_feed(feed_id))
    requests.get(STATUS_URL)
```

The tasks are not awaited, so failures disappear and the function returns before the work finishes. The event loop may even garbage-collect a task with no reference. `requests.get` blocks the event loop.

Good (Python 3.11+ fragment):

```python
async def refresh_all_feeds(feed_ids, status_client):
    async with asyncio.TaskGroup() as refresh_tasks:
        for feed_id in feed_ids:
            refresh_tasks.create_task(refresh_feed(feed_id))
    await status_client.report_refresh_complete()
```

The `TaskGroup` owns the tasks: it waits for all of them, cancels the rest when one fails, and raises the failures together. The status call uses an async client. Bound the number of concurrent tasks when `feed_ids` can be large.

## Implementation Recipe

1. Inspect the supported Python version and local formatter, analyzer or type checker, and tests. Use snake_case for functions and parameters unless an external protocol requires another form.
2. Choose functions and small data representations first. A frozen dataclass or validated constructor is useful when it preserves a joint invariant; typing alone does not reject bad runtime input.
3. Pair function names and parameters: `send_invoice_to(invoice, recipient)` and `load_orders_for(customer_id)`. Use keyword-only parameters for flags and easily swapped arguments. Inspect keyword callers before renaming parameters.
4. Give each material transformation its own binding. Keep `raw_attempt_count` distinct from `attempt_count` and `response_text` distinct from `validated_order`.
5. Catch intended exceptions only, chain translated failures with `raise ... from cause`, and keep `None` reserved for its documented absence meaning. Context managers own resources; async callers own awaits and cancellation.
6. Check parsing, boundaries, failures and causes, and outcomes with native tooling and focused tests. Avoid import-time I/O and CLI logic that cannot be used independently of global state.

## Testing in Python

- Use `pytest.mark.parametrize` with readable IDs so cases form a table.
- Assert exceptions with `pytest.raises(..., match=...)` and check `__cause__` when the cause is part of the contract.
- Use `tmp_path` and real files instead of mocking `open`.
- Pass clocks and random generators in; avoid patching `datetime` globally.
- Compare against an independent snapshot (`copy.deepcopy`) when you assert that input was not mutated.
- A test that needs many patches is telling you the code mixes decisions and effects. Fix the boundary before adding another mock.

## Evidence and Review

Check valid endpoints, invalid text, out-of-range values, and the error cause. Use the [selection and assertion examples](good-and-bad-examples.md#1-names-explain-the-operation) for sentence-like data flow and observable results. Run the type checker the repository uses, but remember that it proves only what the annotations claim; boundary validation still needs behavioral tests.
