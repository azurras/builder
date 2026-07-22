# Python Guidance

Apply the house standard through the repository's supported Python version, type-checking policy, formatter, linter, packaging conventions, and test framework. Prefer idiomatic Python over ceremony copied from statically typed languages.

## Table of Contents

- [Decision guide](#decision-guide)
- [States and validation](#states-and-validation)
- [Interfaces and failures](#interfaces-and-failures)
- [Effects and concurrency](#effects-and-concurrency)
- [Modules and dependencies](#modules-and-dependencies)
- [Testing](#testing)
- [Good and bad](#good-and-bad)
- [Review checklist](#review-checklist)

## Decision Guide

| Need | Prefer | Avoid |
|---|---|---|
| Immutable domain value | Frozen dataclass, named tuple, enum, or validated class | Unstructured dictionary throughout the core |
| Structural collaborator | Protocol when multiple real implementations or test seams need it | Abstract base class by default |
| Legitimate absence | `T | None` with explicit handling | `None` for several failure categories |
| Expected local validation failure | Structured result or repository-standard validation exception | Broad `ValueError` with no field context everywhere |
| Unexpected fault | Specific exception with chaining | `except Exception: return None` |
| Pure transformation | Focused function with explicit inputs | Reading globals or environment inside the function |
| Repeated examples | `pytest.mark.parametrize` or unittest subtests | Copy-pasted test bodies |

Use an ordinary function or dataclass until an abstraction protects a real invariant or effect boundary.

## States and Validation

- Use dataclasses for data with named fields and useful generated equality; use `frozen=True` when mutation is not part of the domain.
- Validate in `__post_init__`, a named constructor, or a boundary parser when all instances must satisfy the invariant.
- Use enums for a closed set of values and distinct dataclasses/classes for cases with different payloads.
- Use type hints to communicate the contract, but remember they do not validate runtime input.
- Convert weak dictionaries, JSON, CLI values, environment strings, database rows, and external objects into validated domain representations at the boundary.
- Copy mutable inputs or document ownership explicitly.
- Prefer domain names that expose units and meaning over primitive positional tuples.

Do not build a class hierarchy when a small function plus a dataclass describes the behavior more directly.

## Interfaces and Failures

- Keep parallel functions consistent in names, positional versus keyword arguments, return shapes, and exception behavior.
- Use keyword-only parameters when several options are easy to confuse or future extension is likely and compatible.
- Return `None` only for legitimate absence that callers can handle without diagnostic detail.
- Use a structured result when expected failures are routine and callers branch on them.
- Raise specific exceptions for violated preconditions, parsing errors, and infrastructure faults according to the module's existing convention.
- Preserve error context with `raise DomainError(...) from error`.
- Use `raise ... from None` only when intentionally hiding an internal parsing detail improves the public contract and the diagnostic loss is acceptable.
- Never use a bare `except`; catch the narrowest exception at a layer that can recover or translate.
- Avoid returning both values and error strings in loosely structured tuples when a named result is clearer.

Exceptions are appropriate in Python. The standard requires classification and context, not replacement of every exception with a result type.

## Effects and Concurrency

- Pass clients, paths, clocks, random generators, or callables when behavior needs isolation and the repository normally uses dependency injection.
- Read environment and configuration at a clear startup or command boundary, not throughout core functions.
- Keep file and network lifetime explicit with context managers.
- Make generators and iterators clear about lazy I/O, resource ownership, and single-use behavior.
- In async code, await or return every coroutine and own every created task.
- Propagate cancellation; do not swallow `CancelledError` in broad handlers.
- Use task groups or the repository's structured concurrency pattern where supported.
- Protect shared mutable state with one owner, a queue, a lock, or an atomic storage operation.
- Do not hold a threading or async lock across blocking or remote work without a stated invariant.

Async syntax does not make blocking libraries non-blocking. Keep blocking work visible and move it to the repository's supported executor boundary only when needed.

## Modules and Dependencies

- Keep module public surfaces narrow; use leading underscores and explicit exports according to local convention.
- Avoid import-time I/O, network access, environment mutation, or registration unless the framework requires it and tests control it.
- Put reusable domain behavior below CLI, web, task-runner, and persistence adapters.
- Use Protocols at consumer-owned boundaries when multiple implementations or fakes benefit; avoid protocols that merely duplicate one concrete class.
- Break import cycles by correcting dependency direction, not by scattering local imports as a permanent default.
- Keep packaging and command entrypoints thin enough to test core behavior without starting the entire application.

## Testing

- Use pytest or unittest according to repository-native conventions.
- Name tests for behavior and condition.
- Use `pytest.mark.parametrize` or subtests for clear input partitions.
- Use Hypothesis or the existing property library for parsers, serializers, laws, and large state spaces when justified.
- Prefer temporary directories and real local files over mocking Python's file APIs when practical.
- Use small fakes for service boundaries; mock interaction only when the interaction is the contract.
- Assert exception types, structured attributes, and chained causes where failure behavior matters.
- Control time and randomness through explicit dependencies or established fixtures.
- Avoid asserting dictionary or string representations whose ordering or formatting is not contractual.

## Good and Bad

Bad: a dictionary permits invalid combinations and broad exception swallowing erases diagnostics.

```python
def schedule(raw: dict) -> bool:
    try:
        if raw.get("immediate"):
            raw["scheduled_at"] = None
        save(raw)
        return True
    except Exception:
        return False
```

Good: dataclass states and failure boundaries are explicit.

```python
from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias


@dataclass(frozen=True)
class Immediate:
    pass


@dataclass(frozen=True)
class Scheduled:
    scheduled_at: datetime


Timing: TypeAlias = Immediate | Scheduled


@dataclass(frozen=True)
class DeploymentRequest:
    version: str
    timing: Timing
```

A boundary parser constructs `DeploymentRequest` or returns structured validation errors. The persistence adapter may raise a specific fault with the original cause chained.

## Review Checklist

- Do dataclasses, enums, unions, and constructors clarify actual states without imitating Java?
- Are runtime inputs validated despite type hints?
- Does `None` mean one documented kind of absence?
- Are exceptions narrow, translated at boundaries, and chained?
- Are global state, environment reads, file lifetime, and lazy I/O visible?
- Are async tasks, cancellation, and shared-state ownership explicit?
- Do pytest or unittest tests prove public behavior and important partitions?
- Does the change remain simple and repository-native?
