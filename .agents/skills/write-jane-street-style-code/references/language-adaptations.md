# Language Adaptations

Load only the section for the language or artifact being changed. Repository instructions and established local patterns take precedence.

### Java

- Use records, enums, sealed hierarchies, and validated value objects to model domain states.
- Prefer constructor injection and explicit dependencies; keep I/O at service or adapter boundaries.
- Return domain results or throw specific exceptions. Avoid `null` when an explicit absence type or result is practical.
- Keep Spring controllers thin and move business invariants into focused domain or service units.
- Use JUnit tests for observable behavior; use parameterized or property-based tests for input spaces with strong invariants.

### JavaScript

- Validate data at network, DOM, storage, and serialization boundaries.
- Prefer immutable bindings and pure transformations; isolate DOM mutation and browser APIs.
- Use explicit result objects or typed errors for expected failures instead of ambiguous sentinels.
- Keep modules small, exports narrow, and asynchronous control flow linear and visible.
- Test public behavior and boundary cases with the repository's existing runner.

### Python

- Use dataclasses, enums, protocols, and type hints where they make valid states and interfaces clearer.
- Validate external input at the boundary and keep core transformations pure when practical.
- Raise specific exceptions or return explicit result objects; avoid broad exception swallowing.
- Keep modules and functions focused, with dependencies passed explicitly when effects need isolation.
- Use pytest or unittest according to the repository, including parametrized or property-based coverage when useful.

### Templates

- Keep executable expressions minimal and move business logic into testable source modules.
- Escape untrusted output with the framework's native mechanism and preserve security boundaries.
- Use explicit data attributes and stable selectors when scripts depend on rendered structure.
- Treat code-bearing configuration like an interface: validate values, document invariants, and avoid hidden defaults.
