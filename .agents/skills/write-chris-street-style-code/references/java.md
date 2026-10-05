# Java

Use the repository's Java version, build, formatter, and nullability conventions. This guide applies the shared rules and the [principles](jane-street-principles.md) to Java and Spring. Modern Java has most of what the style needs: records for values, sealed types and switch expressions for closed alternatives, `Optional` for absence, `java.time` for time, and try-with-resources for ownership. Use them before reaching for frameworks or patterns.

## Idioms at a Glance

| Prefer | Avoid | Why |
|---|---|---|
| Records with validating compact constructors | Mutable beans with setters for value data | The invariant is checked once and cannot be broken later |
| Enums, sealed interfaces, and switch expressions without `default` | String constants, `instanceof` chains, `default -> null` | New cases fail compilation instead of misbehaving |
| `Optional<T>` as a return type for documented absence | `Optional` fields, parameters, or collections; returning `null` | Absence is visible at the call site; `Optional` is not a general null replacement |
| `orElseThrow(() -> new SpecificException(id))`, `map`, `orElse` | `optional.get()` and `isPresent()` then `get()` | The failure names what was missing |
| Specific checked or unchecked exceptions with the cause attached | `catch (Exception e)`, empty catches, `throw new RuntimeException(e.getMessage())` | Callers can tell outcomes apart and operators can trace the cause |
| `Duration`, `Instant`, `LocalDate`, an injected `Clock` | `long` timestamps, `new Date()`, `System.currentTimeMillis()` in rules | Units and time zones are explicit; time is testable |
| `BigDecimal` with a stated rounding mode, or `long` minor units | `double` or `float` for money | Binary floating point cannot represent most decimal amounts |
| Small role types (`CustomerId`, `AccountId`) where swaps are real risks | Several same-type `String` or `long` parameters | Swapped arguments become compile errors |
| `List.copyOf`, `Map.copyOf`, unmodifiable views at boundaries | Returning internal mutable collections | Callers cannot bypass the owner's rules |
| Constructor injection with `final` fields | Field injection, static service lookup, mutable singletons | Dependencies are visible, required, and replaceable in tests |
| Try-with-resources | Manual `close()` or `finally` blocks that can mask the first failure | Cleanup runs on every exit and suppressed exceptions are kept |
| Restoring the interrupt flag or rethrowing `InterruptedException` | Swallowing interrupts | Cancellation keeps working |
| Plain loops when the body has effects; streams for pure transformation | `forEach` or `peek` that mutate outside state | The data flow stays visible |
| `var` when the right-hand side names the type | `var` that hides an important type | Readers still see what the value is |
| `Objects.equals` and primitives for value comparison | `==` on `String`, `Integer`, or other boxed values | `==` compares identity, which only sometimes matches |

## Smells Reviewers Flag

- `catch (Exception e)` or `catch (Throwable t)` outside a top-level boundary, or any catch that logs and continues as if the work succeeded.
- `new RuntimeException(e.getMessage())` or any rethrow that drops the cause.
- `Optional.get()`, `Optional` parameters, `Optional` fields, or methods returning `null` where neighbors return `Optional`.
- A `switch` on a domain enum with a `default` branch that returns a placeholder.
- `boolean` parameters at call sites: `send(message, true, false)`.
- `double` used for money; `long` used for time without a unit in its name.
- A getter that returns an internal `List`, `Map`, or array.
- `@Autowired` on fields, static mutable state, or `ApplicationContext.getBean` inside domain code.
- `@Transactional` methods that call external services, or that are invoked from the same class (Spring proxies do not intercept self-invocation).
- Entities bound directly from request bodies, or entities returned directly as API responses.
- Streams with side effects in `forEach`, `map`, or `peek`.
- Interfaces or factories with exactly one implementation and no seam a test needs.
- Tests that `verify` private interaction order instead of observable results.

## Good and Bad Pairs

The cross-language catalogue already has Java pairs for [invariants in records](good-and-bad-examples.md#3-model-an-invariant-instead-of-trusting-a-comment), [exhaustive switch](good-and-bad-examples.md#11-exhaustive-branches-no-silent-default), [units with Duration](good-and-bad-examples.md#13-units-live-in-the-type-or-the-name), [identity types](good-and-bad-examples.md#14-distinct-identity-types-stop-swapped-arguments), [swallowed failures](good-and-bad-examples.md#18-do-not-swallow-failures), [leaked internals](good-and-bad-examples.md#23-do-not-leak-mutable-internals), and [unearned abstraction](good-and-bad-examples.md#25-earn-the-abstraction). The pairs below are Java-specific.

### Resource Ownership

Bad method fragment (imports and containing class omitted):

```java
long countLinesIn(Path filePath) throws IOException {
    return Files.lines(filePath).count();
}
```

The stream owns a file handle but nothing guarantees it closes.

Good method fragment with the same contract:

```java
long countLinesIn(Path filePath) throws IOException {
    try (Stream<String> lines = Files.lines(filePath)) {
        return lines.count();
    }
}
```

The scope owns cleanup even when processing fails. Keep the `IOException` visible to the caller instead of converting unreadability into a zero-line file.

### Optional Says What Was Missing

Bad fragment:

```java
Optional<User> user = userRepository.findById(userId);
if (user.isPresent()) {
    return user.get().email();
}
return null;
```

The method throws away the explicit absence and returns `null`, so the next caller has to guess again.

Good fragment:

```java
return userRepository.findById(userId)
        .map(User::email)
        .orElseThrow(() -> new UserNotFoundException(userId));
```

If a missing user is a failure for this caller, the exception names the ID. If absence is normal, return `Optional<String>` and let the caller decide. Use `Optional` for return values; do not store it in fields or accept it as a parameter.

### Interrupts Are Cancellation, Not Noise

Bad fragment:

```java
try {
    Thread.sleep(backoffDelay.toMillis());
} catch (InterruptedException e) {
    // ignore
}
```

Whoever interrupted the thread wanted it to stop. Swallowing the interrupt makes shutdown hang and retries run forever.

Good fragment:

```java
try {
    Thread.sleep(backoffDelay.toMillis());
} catch (InterruptedException cause) {
    Thread.currentThread().interrupt();
    throw new RetryCancelledException("Interrupted while waiting to retry", cause);
}
```

The interrupt flag is restored for code further up the stack, and the retry loop stops with a distinct cancellation outcome. Declaring `throws InterruptedException` is better still when the caller can handle it.

### Money Is Not a Double

Bad fragment:

```java
double salesTax = subtotal * 0.0825;
```

`double` cannot represent most decimal amounts exactly, rounding is implicit, and the rate is a magic number.

Good (complete Java example; save as `SalesTax.java`):

```java
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Objects;

final class SalesTax {
    private static final BigDecimal SALES_TAX_RATE = new BigDecimal("0.0825");
    private static final int CENTS_SCALE = 2;

    private SalesTax() {
    }

    static BigDecimal salesTaxFor(BigDecimal subtotalInDollars) {
        Objects.requireNonNull(subtotalInDollars, "subtotalInDollars");
        if (subtotalInDollars.signum() < 0) {
            throw new IllegalArgumentException("subtotalInDollars must not be negative");
        }
        return subtotalInDollars.multiply(SALES_TAX_RATE).setScale(CENTS_SCALE, RoundingMode.HALF_UP);
    }
}
```

The rate and scale are named, the rounding rule is explicit, and negative subtotals are rejected. Build `BigDecimal` from strings, not doubles: `new BigDecimal("0.1")`, never `new BigDecimal(0.1)`. The rounding mode is a business decision; take it from the requirement.

Check: `salesTaxFor(new BigDecimal("10.00"))` is `0.83`; a negative subtotal is rejected.

### Sealed Outcomes for Expected Domain Results

Bad fragment:

```java
boolean withdraw(BigDecimal amount) { ... }   // false means... insufficient funds? frozen account? invalid amount?
```

A boolean cannot say why a withdrawal was refused, and throwing an exception for an everyday "insufficient funds" result forces callers into exception-driven control flow.

Good (complete Java 21+ example; save as `Withdrawals.java`):

```java
import java.math.BigDecimal;
import java.util.Objects;

sealed interface WithdrawalDecision permits WithdrawalDecision.Approved, WithdrawalDecision.Refused {
    record Approved(BigDecimal remainingBalance) implements WithdrawalDecision {
    }

    record Refused(String reason) implements WithdrawalDecision {
    }
}

final class Withdrawals {
    private Withdrawals() {
    }

    static WithdrawalDecision decideWithdrawalOf(BigDecimal requestedAmount, BigDecimal availableBalance) {
        Objects.requireNonNull(requestedAmount, "requestedAmount");
        Objects.requireNonNull(availableBalance, "availableBalance");
        if (requestedAmount.signum() <= 0) {
            throw new IllegalArgumentException("requestedAmount must be positive");
        }
        if (requestedAmount.compareTo(availableBalance) > 0) {
            return new WithdrawalDecision.Refused("Insufficient funds");
        }
        return new WithdrawalDecision.Approved(availableBalance.subtract(requestedAmount));
    }

    static String describe(WithdrawalDecision withdrawalDecision) {
        return switch (withdrawalDecision) {
            case WithdrawalDecision.Approved approved -> "Approved; remaining balance " + approved.remainingBalance();
            case WithdrawalDecision.Refused refused -> "Refused: " + refused.reason();
        };
    }
}
```

The expected business outcomes are values the caller must handle, and the switch is exhaustive over the sealed type. A non-positive amount is a caller defect and throws. Infrastructure failure, such as a database outage, would still be an exception from the code that loads the balance.

Check: compiles on Java 21+; a covered amount is approved with the right remainder; an excessive amount is refused; zero throws.

### Streams Transform; Loops Perform Effects

Bad fragment:

```java
List<String> emails = new ArrayList<>();
users.stream().filter(User::isActive).forEach(user -> emails.add(user.email()));
```

The stream is used as a loop with a side effect on outside state.

Good fragment:

```java
List<String> activeUserEmails = users.stream()
        .filter(User::isActive)
        .map(User::email)
        .toList();
```

The pipeline is a pure transformation with a named result. When each step sends, saves, or logs, write a plain `for` loop so the effect is obvious.

### Compare Values, Not Identities

Bad fragment:

```java
Integer requestedQuantity = request.quantity();
Integer availableQuantity = stock.quantity();
if (requestedQuantity == availableQuantity) { ... }
```

`==` compares object identity. Boxed integers from -128 to 127 are usually cached, so this passes in small tests and fails in production with larger numbers. The same bug appears with `String`.

Good fragment:

```java
if (Objects.equals(requestedQuantity, availableQuantity)) { ... }
```

Or use primitives (`int`) when null is not a valid value, so `==` compares numbers.

### Spring: Constructor Injection and an Injected Clock

Bad fragment:

```java
@Service
public class InvoiceService {
    @Autowired
    private InvoiceRepository invoiceRepository;

    public boolean isOverdue(Invoice invoice) {
        return invoice.dueDate().isBefore(LocalDate.now());
    }
}
```

Dependencies are hidden and optional to the compiler, and the rule reads the system clock in the server's default time zone.

Good fragment:

```java
@Service
public class InvoiceService {
    private final InvoiceRepository invoiceRepository;
    private final Clock clock;

    public InvoiceService(InvoiceRepository invoiceRepository, Clock clock) {
        this.invoiceRepository = invoiceRepository;
        this.clock = clock;
    }

    public boolean isOverdueToday(Invoice invoice) {
        LocalDate today = LocalDate.now(clock);
        return invoice.isOverdueOn(today);
    }
}
```

Required collaborators are constructor parameters, the clock is a bean that tests replace with `Clock.fixed`, and the rule lives on `Invoice.isOverdueOn(LocalDate)` where it can be tested without Spring.

### Spring: Keep Transactions Local and Short

Bad fragment:

```java
@Transactional
public void completeOrder(OrderId orderId) {
    Order order = orderRepository.findById(orderId).orElseThrow(() -> new OrderNotFoundException(orderId));
    paymentClient.capture(order.paymentId());
    orderRepository.save(order.markCompleted());
    emailClient.sendReceiptFor(order);
}
```

The transaction holds database resources across a remote payment call. If the commit fails after the email is sent, the customer receives a receipt for an order that was not completed.

Good fragment:

```java
public void completeOrder(OrderId orderId) {
    Order order = orderQueries.findByIdOrThrow(orderId);
    PaymentCapture paymentCapture = paymentClient.capture(order.paymentId(), order.captureIdempotencyKey());
    Order completedOrder = orderCommands.markCompleted(orderId, paymentCapture);
    receiptPublisher.publishAfterCommit(completedOrder);
}
```

The remote call happens outside the transaction and is idempotent. `orderCommands.markCompleted` is the short `@Transactional` unit on a separate bean, so the Spring proxy applies. The receipt is sent only after the commit, through an after-commit hook or an outbox. The exact recovery rules (capture succeeded but commit failed) are requirements the design must state.

### Spring: Bind Requests to DTOs, Not Entities

Bad fragment:

```java
@PostMapping("/invoices")
Invoice createInvoice(@RequestBody Invoice invoice) {
    return invoiceRepository.save(invoice);
}
```

Clients can set any entity field, including `id`, `status`, or `paidAt`, and the response exposes the storage model.

Good fragment:

```java
public record CreateInvoiceRequest(@NotBlank String customerId, @Positive long amountInCents) {
}

@PostMapping("/invoices")
ResponseEntity<InvoiceResponse> createInvoice(@Valid @RequestBody CreateInvoiceRequest createInvoiceRequest) {
    CustomerId customerId = new CustomerId(createInvoiceRequest.customerId());
    Invoice createdInvoice = invoiceService.createInvoiceFor(customerId, createInvoiceRequest.amountInCents());
    return ResponseEntity.status(HttpStatus.CREATED).body(InvoiceResponse.from(createdInvoice));
}
```

The request record lists exactly what a client may send, Bean Validation rejects malformed shapes before the service runs, and the response record decides what is exposed. The raw request, the domain ID, and the created invoice each have their own name.

## Implementation Recipe

1. Inspect the supported JDK, neighboring package and API style, nullability rules, and formatter. Use only supported language features: records need 16+, sealed types 17+, pattern matching in switch 21+.
2. Choose a record or value class for data whose invariants survive construction; use closed alternatives for genuinely distinct states. Validate the joint invariant in the constructor, not only at one caller.
3. Read each actual invocation as a sentence. Parameter names complement the method: `sendInvoiceTo(Invoice invoice, Recipient recipient)`. Give same-type inputs distinct role names; use enums or role types when accidental misuse is likely.
4. State whether each operation can be absent, rejected, or fail. Use `Optional` for documented absence, a sealed result for an expected domain choice, and a specific exception for failure. Inspect public consumers before changing that contract.
5. Make resource and transaction boundaries explicit. Use try-with-resources, own executor and task lifetimes, and propagate cancellation and interruption according to the existing contract. Awaiting a future does not by itself cancel its work.
6. Compile, apply native analysis, and test constructors, public outcomes, causes, cleanup, and real persistence constraints where relevant.

## Testing in Java

- Name tests for the behavior: `rejectsWithdrawalLargerThanBalance`, not `test2`.
- Use `@ParameterizedTest` tables when cases differ only by data, so the rows read as a specification.
- Assert outcomes and causes: `assertThrows(...)` followed by checks on the message and `getCause()`.
- Use `Clock.fixed(...)` instead of mocking static time.
- Test persistence against the real database engine (Testcontainers, an embedded engine, or the repository's established harness) when constraints, indexes, or transactions are the contract. A mocked repository proves nothing about the query.
- Use Mockito at effect boundaries you do not own; do not `verify` calls between your own private helpers.

```java
@ParameterizedTest(name = "{0} is labeled \"{1}\"")
@CsvSource({
    "PENDING, Awaiting payment",
    "PAID, Paid",
    "REFUNDED, Refunded",
})
void labelsEveryPaymentStatusForCustomers(PaymentStatus paymentStatus, String expectedLabel) {
    assertEquals(expectedLabel, PaymentStatusLabels.customerLabelFor(paymentStatus));
}
```

## Evidence and Review

Use the complete [TimeWindow example](good-and-bad-examples.md#3-model-an-invariant-instead-of-trusting-a-comment) for constructor-enforced invariants and sentence-like predicates. Review callers before renaming public methods or reflective properties, including JSON property names and Spring bean names. Test the actual boundary: database transaction and constraint behavior needs integration evidence; compile success alone does not prove it. New factories and interfaces need a present invariant, consumer, or effect seam.
