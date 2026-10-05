# What Jane Street Style Means

This reference explains the ideas behind the house standard. Jane Street writes most of its code in OCaml, and its public writing describes a culture built around code that many people read, review, and change for years. The house standard carries those ideas into every language. [Sources and adaptation](sources-and-adaptation.md) separates claims taken from Jane Street's public writing from house rules added for this skill.

Each principle below has the same parts:

- **Meaning:** what the principle asks for.
- **Why:** the failure it prevents.
- **In any language:** how to apply it without OCaml.
- **Smells:** signs in a diff that the principle is being broken.
- **Pair:** a short bad and good example. Longer pairs are in [good and bad examples](good-and-bad-examples.md) and the language guides.

The style in one paragraph: write for the reader who arrives later, with no context, in a hurry, during an incident. Let the representation make wrong states impossible. Make every case and every failure visible. Keep interfaces small, uniform, and honest about effects. Prefer boring, direct code to clever code. Name things for what they are now, and give data a new name when its meaning changes. Prove behavior with tests a reviewer can read as a story of input and output.

---

## 1. Write for the Reader

**Meaning:** Code is read many more times than it is written. Optimize for the person who reviews it today and the person who debugs it in a year. Saving a keystroke for the author is never worth a minute of confusion for a reader.

**Why:** Jane Street's review process has every change read by someone other than its author, and trading code is expensive to misunderstand. A reader who has to reconstruct intent will eventually reconstruct it wrongly.

**In any language:**

- Choose names that make the call site read like a sentence (house rule 1).
- Put the normal path first and in order; move unusual cases into guard clauses.
- Split a long expression where its meaning changes, and name each stage.
- Comment on *why*: intent, invariants, surprising constraints. Do not comment on *what* a clear line already says.
- Keep the diff to one purpose so the reviewer can hold it in their head.

**Smells:** single-letter names outside tiny scopes; comments that translate code into English; chained ternaries; a function that needs scrolling to find its return; "clever" tricks that need a comment to explain; mixed refactor-plus-feature diffs.

**Pair:**

```text
Bad:   r = [x for x in d if x[2] and not x[3] > t]
Good:  open_orders = [order for order in orders if order.is_open]
       recent_open_orders = [order for order in open_orders if order.placed_at >= cutoff_time]
```

---

## 2. Make Illegal States Unrepresentable

**Meaning:** Design the data so that a value of the type can only hold a valid combination. If a state cannot happen in the domain, the program should not be able to build it.

**Why:** Every invalid state the type allows must be checked for by every reader and every function, forever. Somebody will forget. When the representation forbids it, nobody can forget. This is a heading in Yaron Minsky's *Effective ML Revisited*.

**In any language:**

- Replace groups of booleans and optional fields with one tagged alternative per real state: a sum type, sealed interface, enum with payload, discriminated union, or a class per state.
- Validate in the constructor or factory, and do not offer setters that can break the invariant afterwards.
- Wrap primitives that carry identity or units (`AccountId`, `Duration`, `Money`) when mixing them up is a real risk.
- In dynamic languages, enforce the same rule at the module boundary and keep construction private by convention.

**Smells:** `isLoading`, `data`, and `error` fields that could all be set at once; "only one of these may be non-null" comments; `status: string`; a `validate()` method callers must remember to call; objects built half-empty and filled in later.

**Pair:**

```text
Bad:   Connection { isConnected: bool, sessionId: string | null, lastError: string | null }
       // sessionId is only set when connected. lastError is only set when disconnected.
Good:  Connection = Connecting
                  | Connected    { sessionId }
                  | Disconnected { reason }
```

The good shape cannot express "connected with no session" or "connected with an error". Code that handles it must say what it does in each real state.

---

## 3. Code for Exhaustiveness

**Meaning:** When you branch on a closed set of cases, handle every case by name, and make the compiler or a check fail when a new case appears.

**Why:** Adding a new case should break every place that must decide what to do with it. A `default:` or `else` that quietly catches "everything else" turns a new case into silent wrong behavior instead of a compile error. This is also a heading in *Effective ML Revisited*.

**In any language:**

- Java: switch expressions over enums or sealed types without `default`. Kotlin: `when` over sealed classes as an expression.
- TypeScript: switch on the discriminant and end with an `assertNever(value)` call that takes `never`.
- Rust and OCaml: `match` without a wildcard arm for domain enums.
- Python: `match` plus `typing.assert_never` (3.11+), checked by the type checker; otherwise, a final branch that raises.
- Go: a final `default` that panics or returns an error naming the unexpected value, plus an exhaustiveness linter if the repository uses one.

**Smells:** `default: return null`; `else: pass`; `_ -> ()` on a domain type; mapping tables that silently miss new keys; handling three of four cases and logging the fourth.

**Pair:**

```text
Bad:   switch (status) { case PAID: ...; case REFUNDED: ...; default: return "unknown"; }
Good:  return switch (status) { case PAID -> ...; case REFUNDED -> ...; case VOIDED -> ...; };
```

When `DISPUTED` is added, the good version stops compiling. The bad version prints "unknown" to customers.

---

## 4. Make Common Errors Obvious

**Meaning:** A reader should see at the call site which operations can fail and how. Functions that may fail return an explicit result; functions that throw or crash say so in their name or signature. *Effective ML Revisited* describes the Jane Street convention: a function that raises carries an `_exn` suffix, and the default version returns an option.

**Why:** Hidden failure turns into crashes far away from the cause, or worse, into wrong answers. When failure is in the type or the name, the caller must decide what to do.

**In any language:**

- Pair a safe and a throwing version when both are useful, and name the throwing one honestly: `findUser` / `getUserOrThrow`, `first_or_none` / `first_or_raise`.
- Use the native explicit form: `Optional`, `Result`, `(value, error)`, a union, or a checked exception, according to repository convention.
- Never represent failure as a plausible value: `0`, `-1`, `""`, `[]`, or `null` that also means "not found".
- Error values carry context: what was attempted, with which input, and the original cause. *How to fail: introducing Or_error.t* argues for errors that say what happened.

**Smells:** `catch (Exception e) { return null; }`; `except: pass`; `get` that throws on absence with no hint in the name; error messages like "failed"; errors rethrown without their cause.

**Pair:**

```text
Bad:   price = parsePrice(text)        // returns 0 when text is malformed
Good:  price = parsePrice(text)        // returns Result<Price, PriceParseError>
       priceOrThrow = parsePriceOrThrow(text)   // for trusted, already validated input
```

---

## 5. Use Uniform Interfaces

**Meaning:** Similar things look and behave the same. If one module has `find_by_id(id) -> Optional`, its neighbors should not have `getById(id) -> throws` and `lookup(key) -> null`. Parameter order, units, naming, result shape, and failure behavior should be predictable.

**Why:** Each arbitrary difference must be learned, remembered, and checked. Uniformity lets a reader trust a pattern once and reuse it everywhere. This is the subject of *Core Principles: Uniformity of Interface* and a heading in *Effective ML Revisited*.

**In any language:**

- Before adding an operation, read its neighbors and copy their vocabulary and shapes.
- Keep the "subject" parameter in the same position across a module (for example, always first).
- Use one unit per concept across an API, or a unit-bearing type.
- If the existing convention is bad, change it deliberately and everywhere, not just in your new function.

**Smells:** `getX`, `fetchY`, and `loadZ` that all do the same kind of read; timeouts in seconds in one call and milliseconds in the next; `(from, to)` in one function and `(to, from)` in another; some methods throw on absence and others return null.

**Pair:**

```text
Bad:   orders.getById(id)        // throws when missing
       customers.find(id)        // returns null when missing
       invoices.lookupInvoice(id, true)
Good:  orders.findById(orderId)          -> Optional<Order>
       customers.findById(customerId)    -> Optional<Customer>
       invoices.findById(invoiceId)      -> Optional<Invoice>
```

---

## 6. Open Few Modules: Keep Names Traceable

**Meaning:** A reader should be able to tell where a name comes from. *Effective ML Revisited* advises opening few modules, so names stay qualified by the module that owns them.

**Why:** Wildcard imports and global namespaces make it hard to find definitions, cause silent shadowing, and let a dependency upgrade change which function you call.

**In any language:**

- Avoid wildcard imports such as Python's `from module import *` and JavaScript's `import * as` used only to save typing; follow the repository's rule for Java wildcard and static imports.
- Qualify names whose origin matters: `Duration.ofSeconds`, `json.loads`, `path.join`.
- Do not monkey-patch, extend built-in prototypes, or rely on implicit globals.
- Keep dependency injection explicit: constructor parameters, not service locators.

**Smells:** `from utils import *`; a helper named `parse` imported from three places; `Array.prototype.last = ...`; a static `Context.current()` lookup deep in a domain function.

---

## 7. Labeled Roles and Sentence-Like Calls

**Meaning:** OCaml's labeled arguments (`~src ~dst`) let callers see each argument's role. The house standard asks every language to reach the same result: a call reads like a sentence, and parameter names complement the function name. This is house rule 1, and it is the rule users of this skill care most about.

**Why:** Positional arguments of the same type are easy to swap, and the compiler will not notice. A call site that reads clearly is also easier to review.

**In any language:** use keyword arguments (Python, Kotlin, C#, Swift), parameter objects or builders with named fields (Java, JavaScript), role types (`SourcePath`, `DestinationPath`) for dangerous swaps, and enums instead of boolean flags. See [naming and readability](naming-and-readability.md).

**Smells:** `copy(a, b, true, false)`; `transfer(String, String, long)`; `new Rectangle(10, 20, 30, 40)` with no way to tell x from width.

---

## 8. Explicit Effects and Ownership

**Meaning:** A reader should be able to tell what a function does to the outside world: I/O, mutation, time, randomness, threads, locks. Pure decisions live apart from the code that performs effects, and each resource has one owner who cleans it up.

**Why:** Hidden effects make code hard to test, hard to reason about, and dangerous to reuse. A function named `calculateTotal` that writes to the database will eventually be called in a loop, a retry, or a read-only context.

**In any language:**

- Pass time, randomness, and clients in as parameters instead of reaching for globals.
- Keep a "functional core" of decisions and an "imperative shell" that loads, decides, and saves.
- Use scope-based cleanup: `with`, `try-with-resources`, `using`, `defer`, RAII, `finally`.
- Name effectful operations with effectful verbs: `load`, `save`, `send`, `fetch`, `publish`.

**Smells:** `now()` inside a business rule; a getter that writes; static mutable caches; threads started with no one to join or cancel them; `open()` with no matching close.

---

## 9. Prefer Immutability; Own Every Mutation

**Meaning:** Values do not change after construction unless there is a reason. When state must change, one owner changes it in one place.

**Why:** Shared mutable state is the main source of action-at-a-distance bugs and race conditions. Immutable values can be shared, cached, and passed across threads freely.

**In any language:** records, frozen dataclasses, `readonly`/`const`/`final`, `Object.freeze`, persistent collections, copies at trust boundaries. Return new values from transformations instead of editing arguments.

**Smells:** functions that edit their arguments; getters that return internal mutable lists; default mutable parameters in Python; a global `config` dictionary edited at runtime.

---

## 10. Small, Honest Interfaces

**Meaning:** In OCaml, a module's interface file (`.mli`) is a contract that exposes only what callers need and hides the representation. Every language has a way to do this: access modifiers, module exports, package-private types, leading underscores.

**Why:** Whatever you expose, someone will depend on. A small interface keeps you free to change the inside and makes the invariant enforceable at one gate.

**In any language:** export the operations, not the fields. Make constructors that validate the only way in. Keep helper functions private. Document the contract at the interface: inputs, outputs, failures, effects.

**Smells:** public setters on value objects; "util" modules that export everything; tests that reach into private fields because the public interface cannot express the behavior.

---

## 11. Different Meanings, Different Names

**Meaning:** House rule 3. When data changes meaning (raw to parsed, parsed to validated, items to totals), bind it to a new, accurately named variable.

**Why:** A variable that changes meaning halfway through a function lies to every reader after the change. It also hides which stage a bug lives in.

**Smells:** `data = json.loads(data)`; `user = user.id`; `list = list.filter(...)` where the new list is a different concept.

---

## 12. Simple and Boring Beats Clever

**Meaning:** Choose the most direct code that does the job. Add abstraction only for real reuse, a protected invariant, or an isolated effect (house rule 9). Avoid complex type tricks, metaprogramming, and reflection unless they remove a real and repeated cost.

**Why:** Clever code is expensive to review and easy to break. Abstractions with one user add a layer of indirection with no payoff.

**Smells:** a generic `Processor<T, R, C>` with one implementation; an interface with one class and no test seam need; a decorator stack that hides control flow; regular expressions where a parser exists.

---

## 13. Tests Show Behavior as a Story

**Meaning:** A good test reads like a scenario: here is the input, here is what happened. Jane Street uses *expect tests*, which print the observed output next to the test code and turn a change in behavior into a readable diff ([Testing with expectations](https://blog.janestreet.com/testing-with-expectations/), [What if writing tests was a joyful experience?](https://blog.janestreet.com/the-joy-of-expect-tests/)).

**Why:** Tests that assert implementation details pass while behavior is wrong. Tests that show output let the reviewer judge behavior directly.

**In any language:** snapshot or approval tests with small, deterministic, human-readable output; table-driven tests whose rows read as a spec; plain assertions on observable results. Read every changed expected output before accepting it.

**Smells:** mocks verifying private calls; giant snapshots no one reads; `sleep` for synchronization; tests named `test1`.

---

## 14. Review Covers Every Line That Ships

**Meaning:** *How Jane Street Does Code Review* describes a process where review tracks which content each reviewer has seen, so later edits, rebases, and merge resolutions are reviewed too.

**Why:** Approval of an old version says nothing about lines added afterwards. Conflict resolutions are new code.

**In any language:** record the revision you reviewed; re-review changed content and conflict resolutions; review tests as carefully as production code. See [testing and review](testing-and-review.md).

---

## Applying the Principles Together

When the principles pull in different directions, use this order:

1. Correctness and safety: valid states, explicit failures, owned effects.
2. Readability for the next reader.
3. Uniformity with the surrounding code.
4. Brevity and performance, unless performance is the stated contract.

When a language cannot enforce a principle in its type system, enforce it at a boundary and in tests, and say so in the code's contract. The goal is the same guarantee, not the same syntax.
