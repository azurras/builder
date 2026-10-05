# Kotlin

Follow the repository's Kotlin and JVM versions, Gradle setup, formatter (ktlint or the IDE profile), and detekt or compiler warning settings. This guide applies the shared rules and the [principles](jane-street-principles.md) to Kotlin, including Kotlin on Spring. Read the [Java guide](java.md) as well for JVM concerns that do not change with the language: `BigDecimal` for money, `java.time`, transactions, interrupts, and request DTOs.

Kotlin gives the style most of what it needs: null safety puts absence in the type, sealed types and `when` expressions make branching exhaustive, `val` makes immutability the default, and named arguments make calls read like sentences. The style's job is to stop code escaping those guarantees: `!!`, `else` branches on sealed types, `runCatching` around suspending code, `GlobalScope`, and `lateinit` all trade a compile-time guarantee for a runtime surprise.

The Kotlin examples in this guide were reviewed but not compiled in the Builder environment. Compile and test them with the target repository's toolchain before relying on them.

## Idioms at a Glance

| Prefer | Avoid | Why |
|---|---|---|
| Nullable types handled with `?:`, `?.`, and early returns | `!!` | Absence is handled where it occurs, with a message, instead of a bare `NullPointerException` |
| `val` and read-only collection types | `var` and `MutableList` in public signatures | State changes have one owner |
| Data classes that validate in `init` with `require` | Data classes whose comment states an invariant nothing checks | `copy()` calls the constructor, so validation also runs on copies |
| `@JvmInline value class CustomerId(val value: String)` | Bare `String` and `Long` IDs | Swapped IDs fail to compile at almost no runtime cost |
| Sealed interfaces and `when` expressions without `else` | `else ->` on sealed types or enums the module owns | New subtypes fail compilation where a decision is needed |
| Named arguments for booleans and same-type parameters | `sendReport(report, true, false)` | Call sites state each role |
| Default parameter values | Overload chains or boolean flags for options | One function with named options reads clearly |
| `require` for argument checks, `check` for state checks, specific exceptions for failures | `throw Exception("error")` | Exception type matches the kind of problem |
| Structured concurrency: `coroutineScope`, an injected `CoroutineScope` with an owner | `GlobalScope.launch`, unowned `launch` calls | Work is cancelled and failures surface |
| `try`/`catch` of specific exceptions in suspending code, rethrowing `CancellationException` | `runCatching` around suspending calls | `runCatching` catches cancellation and every `Throwable` |
| `withContext(Dispatchers.IO)` around blocking calls | Blocking I/O on `Dispatchers.Default` or the main thread | Blocking work does not starve other coroutines |
| `use { }` for `Closeable` resources | Manual `close()` | Cleanup runs on every exit |
| Early returns (`?: return`) and named intermediate values | Nested `let`, `also`, `apply`, and `run` pyramids | The data flow reads top to bottom |
| Validating values that arrive from Java (platform types) | Treating `String!` from Java as non-null | Java can return `null` regardless of what Kotlin assumes |

## Smells Reviewers Flag

- `!!` outside tests, especially on repository lookups and map reads.
- `else ->` in a `when` over a sealed type or enum the codebase owns.
- `runCatching` or `catch (e: Exception)` around suspending calls, which swallows `CancellationException`.
- `GlobalScope`, or `CoroutineScope(Dispatchers.IO).launch` created inline with no owner who cancels it.
- `lateinit var` in domain classes; `lateinit` used to postpone a required constructor argument.
- More than one level of nested scope functions, or `it` used across several nested lambdas.
- `List<T>` treated as immutable when the caller passed a `MutableList` it still changes. Read-only is not immutable; copy with `toList()` at boundaries that keep the value.
- Public `var` properties on data classes.
- Extension functions that hide I/O or mutation behind a property-like name.
- `object` singletons holding mutable state.
- Java interop results used without null checks.

## Good and Bad Pairs

### Handle Absence Instead of Asserting It Away

Bad (Kotlin fragment):

```kotlin
val customerEmail = customerRepository.findByIdOrNull(customerId)!!.email
```

A missing customer throws a `NullPointerException` with no ID and no hint about which lookup failed.

Good (Kotlin fragment):

```kotlin
val customer = customerRepository.findByIdOrNull(customerId)
    ?: throw CustomerNotFoundException(customerId)
val customerEmail = customer.email
```

The failure names the missing thing. If absence is normal for this caller, return `null` from a function whose name says so, such as `findCustomerEmailOrNull(customerId)`.

### Exhaustive `when` over a Sealed Type

Bad (Kotlin fragment):

```kotlin
fun statusLineFor(download: Download): String = when (download) {
    is Download.InProgress -> "${download.bytesReceived} bytes"
    is Download.Complete -> "Saved to ${download.filePath}"
    else -> ""
}
```

`Failed` already renders as a blank line, and a new `Paused` state will too.

Good (Kotlin fragment):

```kotlin
sealed interface Download {
    data class InProgress(val bytesReceived: Long) : Download
    data class Complete(val filePath: Path) : Download
    data class Failed(val reason: String) : Download
}

fun statusLineFor(download: Download): String = when (download) {
    is Download.InProgress -> "${download.bytesReceived} bytes"
    is Download.Complete -> "Saved to ${download.filePath}"
    is Download.Failed -> "Failed: ${download.reason}"
}
```

The `when` expression names every subtype and has no `else`, so adding a subtype is a compile error here. Each state holds only its own data.

### Value Classes Stop Swapped IDs

Bad (Kotlin fragment):

```kotlin
fun linkCustomerToAccount(customerId: String, accountId: String) { ... }

linkCustomerToAccount(order.accountId, order.customerId)
```

Good (Kotlin fragment):

```kotlin
@JvmInline
value class CustomerId(val value: String) {
    init {
        require(value.isNotBlank()) { "CustomerId must not be blank" }
    }
}

@JvmInline
value class AccountId(val value: String) {
    init {
        require(value.isNotBlank()) { "AccountId must not be blank" }
    }
}

fun linkCustomerToAccount(customerId: CustomerId, accountId: AccountId) { ... }
```

The swapped call no longer compiles, blank IDs cannot be constructed, and on the JVM the wrapper is usually erased to the underlying `String`. Named arguments help too: `linkCustomerToAccount(customerId = order.customerId, accountId = order.accountId)`.

### Data Classes Validate in `init`

Bad (Kotlin fragment):

```kotlin
data class TimeWindow(var startsAt: Instant, var endsAt: Instant) // endsAt must be after startsAt
```

Good (Kotlin fragment):

```kotlin
data class TimeWindow(val startsAt: Instant, val endsAt: Instant) {
    init {
        require(endsAt.isAfter(startsAt)) { "endsAt ($endsAt) must be after startsAt ($startsAt)" }
    }

    fun includes(candidateInstant: Instant): Boolean =
        !candidateInstant.isBefore(startsAt) && candidateInstant.isBefore(endsAt)
}
```

`val` properties cannot be reassigned, and `copy(endsAt = ...)` calls the primary constructor, so the `init` check runs on copies too. `timeWindow.includes(candidateInstant)` reads as a question.

### `runCatching` Swallows Cancellation

Bad (Kotlin fragment):

```kotlin
suspend fun refreshPrices() {
    runCatching { priceClient.fetchPrices() }
        .onSuccess { prices -> priceCache.store(prices) }
        .onFailure { logger.warn("refresh failed") }
}
```

`runCatching` catches every `Throwable`, including the `CancellationException` that stops a coroutine. A cancelled refresh logs a warning and keeps going, and programming errors are logged as ordinary failures with no cause.

Good (Kotlin fragment):

```kotlin
suspend fun refreshPrices() {
    val fetchedPrices = try {
        priceClient.fetchPrices()
    } catch (cause: IOException) {
        throw PriceRefreshException("Could not fetch prices", cause)
    }
    priceCache.store(fetchedPrices)
}
```

Only the documented I/O failure is caught and translated with its cause. Cancellation and programming errors propagate. If a caller wants to log and continue, it catches `PriceRefreshException` at the boundary that owns that decision.

### Every Coroutine Has an Owner

Bad (Kotlin fragment):

```kotlin
fun notifyAll(recipients: List<Recipient>) {
    recipients.forEach { recipient ->
        GlobalScope.launch { notifier.notify(recipient) }
    }
}
```

The function returns immediately, failures go to a global handler, and nothing cancels the work when the request or application stops.

Good (Kotlin fragment):

```kotlin
suspend fun notifyAll(recipients: List<Recipient>) = coroutineScope {
    recipients.forEach { recipient ->
        launch { notifier.notify(recipient) }
    }
}
```

`coroutineScope` waits for every child, cancels the rest when one fails, and rethrows that failure to the caller. For long-running background work, inject a `CoroutineScope` owned by a component with a lifecycle (and cancelled when it stops). For large lists, limit concurrency with a `Semaphore` or `limitedParallelism`.

### Blocking Calls Leave the Default Dispatcher

Bad (Kotlin fragment):

```kotlin
suspend fun loadReportText(reportPath: Path): String = reportPath.readText()
```

`readText` blocks the thread. On `Dispatchers.Default`, a few slow disks stall unrelated coroutines.

Good (Kotlin fragment):

```kotlin
suspend fun loadReportText(reportPath: Path): String = withContext(Dispatchers.IO) {
    reportPath.readText()
}
```

The blocking call runs on the dispatcher meant for it, and the signature still tells callers the function suspends.

### Flat Code Instead of Scope-Function Pyramids

Bad (Kotlin fragment):

```kotlin
fun shippingLabelFor(order: Order?): String? =
    order?.let { o -> o.address?.let { a -> a.postalCode?.let { p -> "${a.street}, $p" } } }
```

Three nested lambdas, three one-letter names, and `null` returned for three different reasons.

Good (Kotlin fragment):

```kotlin
fun shippingLabelFor(order: Order): String {
    val address = order.address ?: throw MissingShippingAddressException(order.id)
    val postalCode = address.postalCode ?: throw MissingPostalCodeException(order.id)
    return "${address.street}, $postalCode"
}
```

Each missing piece is handled on its own line with its own outcome, and the normal result is the last line. Use `let` for a single short transformation; stop when it nests.

### Named Arguments Instead of Boolean Positions

Bad (Kotlin fragment):

```kotlin
reportSender.send(report, true, false)
```

Good (Kotlin fragment):

```kotlin
reportSender.send(report, includeDrafts = true, notifyOwner = false)
```

When the flags combine into modes, replace them with an enum: `reportSender.send(report, draftPolicy = DraftPolicy.INCLUDE_DRAFTS)`.

## Kotlin on Spring

- Use constructor injection with `private val` parameters; it is the natural Kotlin form.
- Apply the `kotlin-spring` (all-open) and `kotlin-jpa` (no-arg) compiler plugins the repository already uses rather than making classes `open` by hand.
- Keep JPA entities separate from validated domain values; entity requirements (no-arg constructors, mutable fields) work against `val` and `init` validation.
- Use `suspend` controller functions or `Mono`/`Flux` consistently with the existing stack; do not mix blocking calls into reactive or coroutine paths.

## Implementation Recipe

1. Inspect the Kotlin and JVM versions, compiler warnings (`allWarningsAsErrors`), ktlint or detekt rules, and how the code interoperates with Java.
2. Model states with sealed types and validated data or value classes; keep properties `val`.
3. Express absence with nullable types and handle it immediately; reserve `!!` for nothing outside tests.
4. Read every call as a sentence; use named arguments where roles could be confused and default parameters instead of flag overloads.
5. Own every coroutine through structured concurrency; catch specific exceptions and let `CancellationException` propagate; move blocking calls to `Dispatchers.IO`.
6. Build with warnings enabled, run detekt or ktlint if configured, and run the tests.

## Testing in Kotlin

- Use backtick test names that read as sentences: ``fun `refuses withdrawal larger than balance`()``.
- Use `kotlinx-coroutines-test` (`runTest`, virtual time) instead of real delays.
- Use parameterized tests (JUnit 5 or Kotest data tests) for case tables.
- Prefer real objects and small fakes; use MockK at effect boundaries you do not own.

## Evidence and Review

The compiler proves null safety and `when` exhaustiveness only where code does not opt out. Search the diff for `!!`, `else ->`, `runCatching`, `GlobalScope`, and `lateinit`, and check Java interop boundaries by hand.
