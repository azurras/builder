# Python

Follow the project's supported Python, test runner, formatter and type checker.
- Prefer functions and dataclasses; frozen values, enums and unions should clarify real states, not create a class hierarchy by default.
- Type hints do not validate runtime input. Validate once at CLI/configuration/deserialization boundaries.
- Use None for one legitimate absence case. Raise specific exceptions, preserve causes with exception chaining, and never hide faults behind success or empty values.
- Use context managers for resources. Avoid import-time I/O and global mutable configuration; expose lazy I/O and single-use generators.
- Own and await async tasks, propagate cancellation, and avoid blocking the event loop. Make shared-state synchronization explicit.
- Keep CLIs thin over reusable logic. Use Protocols only when consumers benefit from actual alternative implementations or a necessary test seam.
- Prefer temporary directories and real files; test outcomes, exception types and meaningful boundaries. Control clocks/randomness when they affect behavior.
