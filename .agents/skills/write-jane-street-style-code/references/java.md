# Java Guidance

Apply the house standard with the Java version, frameworks, and repository-native conventions already in use. Do not introduce preview features, libraries, or architectural layers solely to imitate another language.

## Table of Contents

- [Decision guide](#decision-guide)
- [States and validation](#states-and-validation)
- [Interfaces and failures](#interfaces-and-failures)
- [Effects and concurrency](#effects-and-concurrency)
- [Spring boundaries](#spring-boundaries)
- [Testing](#testing)
- [Good and bad](#good-and-bad)
- [Review checklist](#review-checklist)

## Decision Guide

| Need | Prefer | Avoid |
|---|---|---|
| Closed set of cases | `enum` or sealed interface hierarchy | Strings and boolean combinations |
| Immutable data with validation | Record with compact constructor or focused final value object | Public setters and partially valid beans |
| Legitimate absence | `Optional` at a suitable return boundary | `null` with undocumented meaning |
| Expected domain rejection | Domain result/sealed outcome or repository-standard typed exception | Catch-all exception or sentinel |
| External effect | Focused service/adapter dependency | Static ambient lookup or hidden I/O |
| Variable behavior with real consumers | Small interface owned by the consumer | Interface for every class |
| Input-space coverage | JUnit parameterized tests or existing property library | Repeated near-identical tests |

Use the repository's established choice when it already expresses the same semantics clearly.

## States and Validation

- Use records for immutable product data when their generated equality and accessors match the domain.
- Use a compact record constructor to enforce field invariants; copy mutable collections before storing them.
- Use enums when all cases share one behavior shape and sealed hierarchies when cases carry different data or behavior.
- Keep entity identity and lifecycle explicit; do not convert every domain object into a record when mutation is inherent and owned.
- Replace primitive parameter clusters with a value object when they form one invariant or are easily swapped.
- Validate request DTO syntax at the transport boundary and construct validated domain values before core behavior.
- Treat persistence rows and third-party DTOs as external representations; map them rather than leaking annotations and weak states through the core without reason.

Avoid adding JavaBean setters solely for framework convenience when constructor binding, builders, or dedicated transport DTOs preserve invariants better.

## Interfaces and Failures

- Keep parallel method names and argument order consistent across services and repositories.
- Use `Optional<T>` for legitimate single-value absence at a return boundary, not for parameters, fields, collections, or every internal step.
- Return an empty collection rather than `null` when zero elements is a valid collection result.
- Use a domain result or sealed outcome when callers routinely branch on expected rejection.
- Throw a specific exception for programmer errors, violated trusted preconditions, or infrastructure faults that cannot be handled locally.
- Chain causes: `new DeploymentException("failed to store deployment " + safeId, cause)`.
- Do not catch `Exception` unless operating at a deliberate top-level boundary that maps, logs, or terminates failures.
- Keep checked versus unchecked exception choices consistent with the module; do not introduce a second error convention casually.

If a non-throwing method has a throwing counterpart, use a predictable repository-native suffix or name and preserve equivalent success semantics.

## Effects and Concurrency

- Prefer constructor injection for stable dependencies; use method parameters for per-operation collaborators or data.
- Pass `Clock` when business behavior depends on current time and deterministic testing matters.
- Pass or encapsulate randomness when identity or selection behavior must be controlled.
- Keep transactions around the smallest complete invariant-preserving operation.
- Give executors, scheduled tasks, and background jobs an explicit lifecycle owner.
- Use structured concurrency facilities available in the project's supported Java version only when the repository has adopted them.
- Prefer immutable messages and one owner for shared mutable state.
- Document thread-safety and ordering only where consumers can rely on it.
- Never hold a monitor or lock across remote I/O unless the invariant requires it and the cost is understood.

Use `CompletableFuture` only when asynchronous composition is actually part of the boundary. Wrapping blocking work in a future does not make the underlying resource non-blocking.

## Spring Boundaries

- Keep controllers responsible for transport parsing, authorization integration, status mapping, and response serialization.
- Move domain invariants and reusable decisions into focused services or domain values.
- Use `@ControllerAdvice` or the repository's existing boundary for uniform HTTP error mapping.
- Distinguish validation errors, domain rejections, authentication/authorization failures, and infrastructure faults in response contracts.
- Do not expose persistence entities directly when doing so leaks lazy loading, internal fields, or weakly valid states.
- Keep configuration properties typed and validated; fail startup for invalid required configuration.
- Make transactional behavior explicit at the service operation that owns the transition, not scattered across helpers.

Thin controllers are a default, not a ritual. A simple endpoint may remain direct when it owns no reusable rule and its behavior stays clear and tested.

## Testing

- Use JUnit tests through the repository's current version and conventions.
- Name tests for behavior and condition.
- Use parameterized tests for boundary partitions and repeated domain examples.
- Use the existing property-testing library when laws, parsers, or large state spaces justify it; do not add a dependency for one trivial property.
- Prefer real value objects and focused fakes over mocking every collaborator.
- Use Spring slice tests only when binding, serialization, security integration, or framework wiring is the behavior.
- Use integration tests for database constraints, transactions, queries, and migrations.
- Test exception type, structured fields, and preserved cause where failure contracts matter; avoid asserting entire volatile messages.

## Good and Bad

Bad: weak state plus ambiguous failure.

```java
record PortConfig(Integer port, boolean enabled) {}

Integer connect(PortConfig config) {
    if (!config.enabled() || config.port() == null) {
        return null;
    }
    return socket.connect(config.port());
}
```

This permits enabled-without-port, returns `null` for multiple meanings, and hides the external effect behind a generic verb.

Good: valid cases and outcomes are explicit.

```java
sealed interface Endpoint permits Endpoint.Disabled, Endpoint.Enabled {
    record Disabled() implements Endpoint {}

    record Enabled(int port) implements Endpoint {
        public Enabled {
            if (port < 1 || port > 65_535) {
                throw new IllegalArgumentException("port out of range");
            }
        }
    }
}

record SessionId(String value) {}

enum Reason {
    REFUSED
}

sealed interface ConnectResult permits ConnectResult.Connected, ConnectResult.Rejected {
    record Connected(SessionId sessionId) implements ConnectResult {}
    record Rejected(Reason reason) implements ConnectResult {}
}
```

An adapter can perform the socket effect while domain code operates on a valid endpoint and explicit outcome.

## Review Checklist

- Do records, enums, sealed types, or constructors represent the actual valid cases without ornamental complexity?
- Can `null` still carry more than one meaning?
- Are exceptions specific and causes preserved?
- Are Spring and persistence representations prevented from weakening domain invariants?
- Does one service operation own each transaction and mutable transition?
- Are asynchronous lifetimes and executor ownership clear?
- Do JUnit tests prove behavior at the appropriate boundary?
- Does the code remain idiomatic for the repository's supported Java version?
