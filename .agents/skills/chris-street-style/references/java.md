# Java

Use the repository's Java version, build, formatting and nullability conventions.
- Prefer records for immutable data, enums/sealed alternatives for closed states, and validated constructors for invariants. Do not default to factories or interfaces without a boundary.
- Distinguish Optional absence from domain rejection and exceptions. Preserve exception causes; avoid broad catch-and-continue.
- Keep constructor injection for stable dependencies; pass per-operation data explicitly. Avoid hidden static state.
- Use try-with-resources, explicit transaction boundaries and bounded executor/task ownership. Propagate interruption and cancellation.
- For persistence changes, test actual constraints, transaction behavior, query bounds and old/new data compatibility.
- Apply repository-native unit/integration tools; test public behavior rather than mocks or framework wiring already covered elsewhere.
