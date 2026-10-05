# Applying the Standard in Any Language

The standard applies to every language. A dedicated language guide adds native detail; its absence never removes the shared obligations. Syntax and mechanisms vary, but behavior, naming, valid states, ownership, failure classification, and evidence remain the contract.

## Required Adaptation Procedure

1. Identify the repository's supported runtime/compiler, formatter, analyzer, test runner, and existing public-interface conventions. Use the inspected versions rather than assuming the newest feature is available.
2. Describe each domain invariant and trust boundary before choosing a mechanism.
3. Select the simplest idiomatic representation that enforces the invariant: a sum type, enum, validated constructor, constrained record, module boundary, or explicit runtime check.
4. Map absence, rejection, infrastructure failure, and defects to the language's native result or exception conventions. Explain which outcomes callers must handle.
5. Identify the owner and cleanup mechanism for each resource and asynchronous activity. Check cancellation and error paths as well as normal return.
6. Apply the naming guide to the native definition and actual invocation syntax. Use normal casing and standard protocol names; make domain roles legible through receiver and parameters.
7. Verify with native tools at the relevant boundary. When a tool is unavailable, report the exact unverified claim and use available evidence; do not describe an uncompiled example as checked.

## Mechanism Map

These are candidates, not requirements to introduce machinery into every function.

| Language family | Valid states and failures | Ownership and evidence |
|---|---|---|
| Java, Kotlin, C# | Validated records/value objects, enums or sealed alternatives; nullable/optional results and specific exceptions | Scoped disposal or try/finally, explicit transactions, owned tasks, native compiler and tests |
| JavaScript, TypeScript | Runtime validation, tagged alternatives; explicit absence and typed/domain errors | Await/return promises, abort signals, listener/timer cleanup, actual browser checks when behavior depends on the DOM |
| Python, Ruby, PHP | Runtime validation behind constructors/modules; specific exceptions and a defined absence result | Context managers/ensure/finally, scoped state, native parser/analyzer and behavior tests |
| Go | Private fields with validated constructors, explicit states; `(value, error)` with checked errors | Context cancellation, defer after successful acquisition, documented channel/goroutine ownership and native tests |
| Rust | Newtypes and enums; `Option`/`Result` with intentional propagation | Borrowing, ownership, Drop, explicit task cancellation/joining, compiler and behavior tests |
| C, C++ | Validated structures and opaque modules; status/result or native exception conventions | RAII/smart pointers where supported, one cleanup owner on every path, bounds checks and native diagnostics/sanitizers when relevant |
| OCaml, F#, Haskell | Algebraic types and module interfaces; explicit options/results and effect conventions | Make I/O and asynchronous lifetimes visible; compile exhaustiveness and test observable behavior |
| Swift | Enums, validated structs, optionals/results, meaningful argument labels | defer, explicit ownership and structured tasks, supported compiler and tests |
| SQL | Constraints, keys, transactions, explicit result sets; distinguish no rows from query failure | State migration/read/write roles, parameterize values, inspect plans and actual database behavior for affected contracts |
| Shell, PowerShell | Validated arguments and deliberate exit/error handling | Quote literal paths, check statuses, bound external work, own processes/resources and use actual dry-run/parser evidence |
| Templates and configuration | Schema and boundary validation; required values and explicit precedence | Check rendered/effective output and every meaningful branch; apply the configuration guide |

For any language not listed, follow the procedure above and record the chosen native equivalents in the current task brief. Preserve established library and framework contracts unless the task explicitly changes them.

## Avoid Mechanical Translation

Do not transplant OCaml module layout, exception conventions, type names, or argument order into another ecosystem. Likewise, do not introduce Java class hierarchies into a small script merely to satisfy a principle. Encode the needed contract with the language's economical mechanism.

A type is not enough when its data enters through a runtime boundary. A runtime check is not enough when later mutation can break the invariant. Choose a representation and owner that keep the guarantee true after validation.
