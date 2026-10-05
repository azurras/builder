# Good and Bad Examples

These original examples demonstrate the house rules across languages. Each pair names the defect, shows how it fails, and explains the contract the correction protects. Complete examples can be checked with the stated native tool; fragments and pseudocode illustrate structure and require the surrounding application's real contract. Complete Java examples keep several package-private types in one file for brevity; in a project, give each top-level type its own file. The [principles reference](jane-street-principles.md) explains the ideas behind each pair, and each language guide adds native pairs.

## Catalogue

| # | Example | Principle | Language |
|---|---|---|---|
| 1 | [Names explain the operation](#1-names-explain-the-operation) | Write for the reader | Python |
| 2 | [Parameter roles complement method names](#2-parameter-roles-complement-method-names) | Sentence-like calls | Pseudocode |
| 3 | [Model an invariant instead of trusting a comment](#3-model-an-invariant-instead-of-trusting-a-comment) | Illegal states unrepresentable | Java |
| 4 | [Preserve failure categories](#4-preserve-failure-categories-and-name-each-transformation) | Make errors obvious | JavaScript |
| 5 | [Effects belong to an explicit owner](#5-effects-belong-to-an-explicit-owner) | Explicit effects | Pseudocode |
| 6 | [Resource cleanup covers every exit](#6-resource-cleanup-covers-every-exit) | Ownership | Python |
| 7 | [Assertions prove behavior](#7-assertions-prove-behavior) | Tests show behavior | Python |
| 8 | [Review comments explain a correction](#8-review-comments-explain-a-concrete-correction) | Review covers content | Prose |
| 9 | [Replace boolean flags with named choices](#9-replace-boolean-flags-with-named-choices) | Sentence-like calls | Python |
| 10 | [One tagged state instead of loose flags](#10-one-tagged-state-instead-of-loose-flags) | Illegal states unrepresentable | TypeScript |
| 11 | [Exhaustive branches, no silent default](#11-exhaustive-branches-no-silent-default) | Exhaustiveness | Java |
| 12 | [Parse strings into closed values at the boundary](#12-parse-strings-into-closed-values-at-the-boundary) | Validate at the boundary | Python |
| 13 | [Units live in the type or the name](#13-units-live-in-the-type-or-the-name) | Uniform interfaces | Java |
| 14 | [Distinct identity types stop swapped arguments](#14-distinct-identity-types-stop-swapped-arguments) | Illegal states unrepresentable | Java |
| 15 | [Guard clauses keep the normal path flat](#15-guard-clauses-keep-the-normal-path-flat) | Write for the reader | Python |
| 16 | [Named stages instead of a clever chain](#16-named-stages-instead-of-a-clever-chain) | Simple beats clever | JavaScript |
| 17 | [Pass the clock in](#17-pass-the-clock-in) | Explicit effects | Python |
| 18 | [Do not swallow failures](#18-do-not-swallow-failures) | Make errors obvious | Java |
| 19 | [Named constants instead of magic numbers and lying comments](#19-named-constants-instead-of-magic-numbers-and-lying-comments) | Write for the reader | Python |
| 20 | [Retry only idempotent work](#20-retry-only-idempotent-work) | Explicit effects | Pseudocode |
| 21 | [Late async results must not overwrite newer state](#21-late-async-results-must-not-overwrite-newer-state) | Ownership | JavaScript |
| 22 | [Name the operation that can fail](#22-name-the-operation-that-can-fail) | Make errors obvious | Python |
| 23 | [Do not leak mutable internals](#23-do-not-leak-mutable-internals) | Immutability | Java |
| 24 | [Expect-style tests show the whole output](#24-expect-style-tests-show-the-whole-output) | Tests show behavior | Python |
| 25 | [Earn the abstraction](#25-earn-the-abstraction) | Simple beats clever | Java |

## 1. Names Explain the Operation

Assume invoice records are already validated domain input with a documented `status` field. This function selects records; it is not their input validator.

Bad (complete Python example):

```python
def process(data):
    return [x for x in data if x["status"] == "paid"]
```

The function and variables do not identify the domain or the selection rule.

Good (complete Python example):

```python
def select_paid_invoices_from(invoices):
    return [invoice for invoice in invoices if invoice["status"] == "paid"]
```

The call `select_paid_invoices_from(invoices)` reads as a sentence. The function names the rule; the parameter names its input; singular and plural names distinguish one record from a collection. A larger API can replace dictionaries with validated domain types without changing this naming decision.

Check: empty input returns an empty collection; paid invoices are selected; unpaid invoices are excluded; the input remains unchanged.

## 2. Parameter Roles Complement Method Names

Bad illustrative pseudocode:

```text
send(x, y)
copy(a, b, true)
```

Good illustrative pseudocode:

```text
sendInvoiceTo(invoice, recipient)
copyFile(sourcePath, destinationPath, existingFilePolicy = REPLACE)
```

The relation in `sendInvoiceTo` is completed by `invoice` and `recipient`. The copy call exposes direction and the selected policy. Use the language's valid labeled/named-argument syntax. With positional-only syntax, use clear variables and a small validated or role-bearing value when accidental reversal is an actual risk. Do not change a public argument order without caller and compatibility checks.

## 3. Model an Invariant Instead of Trusting a Comment

Contract: a time window has non-null ordered endpoints and includes its start but excludes its end. A zero-length window is invalid.

Bad (Java fragment):

```java
class MutableWindow {
    // end must be after start
    java.time.Instant start;
    java.time.Instant end;
}
```

Nothing enforces the comment. Construction or later mutation can create null or reversed endpoints.

Good (complete Java example; save as `TimeWindow.java`):

```java
import java.time.Instant;
import java.util.Objects;

public record TimeWindow(Instant startsAt, Instant endsAt) {
    public TimeWindow {
        Objects.requireNonNull(startsAt, "startsAt");
        Objects.requireNonNull(endsAt, "endsAt");
        if (!endsAt.isAfter(startsAt)) {
            throw new IllegalArgumentException("endsAt must be after startsAt");
        }
    }

    public boolean includes(Instant candidateInstant) {
        Objects.requireNonNull(candidateInstant, "candidateInstant");
        return !candidateInstant.isBefore(startsAt)
                && candidateInstant.isBefore(endsAt);
    }
}
```

The constructor enforces the joint invariant, immutable fields preserve it, and `timeWindow.includes(candidateInstant)` states the question. Use a validated module or struct when records are unavailable. Do not introduce a hierarchy solely to model two endpoints.

Check: compilation; start is included; end is excluded; before/after candidates are excluded; null, equal, and reversed endpoints are rejected.

## 4. Preserve Failure Categories and Name Each Transformation

Contract: JSON `null` means no user. A present user must be an object with a positive safe integer ID and a nonblank string display name. Malformed JSON or an invalid shape is a protocol error, not absence.

Bad (complete JavaScript example):

```javascript
function getUser(data) {
  try {
    data = JSON.parse(data);
    return data;
  } catch {
    return null;
  }
}
```

The variable changes from response text to unchecked fields. Malformed JSON becomes the same result as absence; valid JSON with an invalid domain shape is accepted.

Good (complete JavaScript example):

```javascript
class UserProtocolError extends Error {
  constructor(message, options) {
    super(message, options);
    this.name = "UserProtocolError";
  }
}

function decodeUserFrom(responseText) {
  let decodedUserFields;
  try {
    decodedUserFields = JSON.parse(responseText);
  } catch (cause) {
    if (!(cause instanceof SyntaxError)) {
      throw cause;
    }
    throw new UserProtocolError("User response is not valid JSON", { cause });
  }

  if (decodedUserFields === null) {
    return null;
  }

  if (
    typeof decodedUserFields !== "object" ||
    Array.isArray(decodedUserFields) ||
    !Number.isSafeInteger(decodedUserFields.id) ||
    decodedUserFields.id <= 0 ||
    typeof decodedUserFields.displayName !== "string" ||
    decodedUserFields.displayName.trim().length === 0
  ) {
    throw new UserProtocolError("User response has invalid fields", {
      cause: new TypeError("Expected a positive user ID and nonblank display name"),
    });
  }

  const validatedUser = Object.freeze({
    id: decodedUserFields.id,
    displayName: decodedUserFields.displayName,
  });
  return validatedUser;
}
```

`responseText`, `decodedUserFields`, and `validatedUser` retain distinct meanings. The parser catches only its syntax failure, preserves the cause, validates domain shape, and constructs an immutable trusted value. The documented transport boundary supplies text; a transport failure belongs to the calling I/O layer.

Check: syntax; valid user; legitimate absence; malformed JSON with SyntaxError cause; wrong primitive/array shapes; missing/invalid IDs; blank names; immutable result; unexpected failures are not turned into absence. This uses native Error cause support; verify the repository's supported JavaScript runtime before adopting it.

## 5. Effects Belong to an Explicit Owner

Bad illustrative pseudocode:

```text
calculateInvoiceTotal(invoiceId):
    invoice = database.load(invoiceId)
    exchangeRate = network.fetchExchangeRate()
    invoice.total = sumConvertedAmounts(invoice, exchangeRate)
    database.save(invoice)
    return invoice.total
```

An apparently computational operation performs reads, a remote request, and a write. Tests cannot isolate the rule without mocking all three effects.

Good illustrative pseudocode:

```text
calculateTotalFor(invoiceLines, exchangeRate):
    convertedAmounts = convertAmounts(invoiceLines, exchangeRate)
    return sumAmounts(convertedAmounts)

updateInvoiceTotalFor(invoiceId):
    invoice = invoiceRepository.load(invoiceId)
    exchangeRate = exchangeRateClient.fetchCurrentRate()
    totalAmount = calculateTotalFor(invoice.lines, exchangeRate)
    invoiceRepository.saveTotalFor(invoiceId, totalAmount)
    return totalAmount
```

The rule has explicit inputs. The updating operation exposes and owns effects. The real application still needs domain rounding/currency, missing-invoice and service-failure behavior, transaction boundaries, and concurrency policy; this sketch does not choose those requirements.

## 6. Resource Cleanup Covers Every Exit

Bad (Python fragment):

```python
response_file = open(response_path, encoding="utf-8")
response_text = response_file.read()
response_file.close()
```

If reading fails, cleanup is skipped.

Good (Python fragment):

```python
with open(response_path, encoding="utf-8") as response_file:
    response_text = response_file.read()
```

The context manager owns file cleanup across normal and exceptional exit. Use the language's native scope/cleanup equivalent. Do not hide read failure behind an empty response unless the API explicitly defines that recovery.

## 7. Assertions Prove Behavior

Bad illustrative pseudocode:

```text
runSelection()
assert privateFilterHelper.wasCalledOnce()
```

That assertion can pass even if the result contains unpaid invoices.

Good (Python test fragment for the complete selection example above):

```python
from copy import deepcopy


def test_select_paid_invoices_excludes_unpaid_invoices():
    paid_invoice = {"id": "invoice-1", "status": "paid"}
    unpaid_invoice = {"id": "invoice-2", "status": "unpaid"}
    invoices = [paid_invoice, unpaid_invoice]
    original_invoices = deepcopy(invoices)

    selected_invoices = select_paid_invoices_from(invoices)

    assert selected_invoices == [paid_invoice]
    assert invoices == original_invoices
```

The result detects an incorrect selection rule, and the second assertion compares input against an independent snapshot. Reusing the same dictionary objects in both sides of that assertion would conceal mutation. Add other tests for distinct requirements rather than for every private helper.

## 8. Review Comments Explain a Concrete Correction

Bad: “This is weird. Use better names.”

Good: “Warning at `send` and its caller: `x` and `y` hide whether this sends an invoice or a message and which value is the destination. Name the operation `sendInvoiceTo(invoice, recipient)` or the equivalent domain action, inspect its public callers, and retain their direction and behavior.”

A review-only request returns that finding with location and evidence. Applying the suggested edit requires authorized implementation scope.

## 9. Replace Boolean Flags with Named Choices

Bad (Python call site):

```python
sections_to_export = select_sections_for_export(sections, True)
```

A reader cannot tell what `True` selects without opening the definition. A second boolean doubles the confusion, and swapping two booleans is invisible to every tool.

Good (complete Python example):

```python
from enum import Enum


class DraftPolicy(Enum):
    EXCLUDE_DRAFTS = "exclude_drafts"
    INCLUDE_DRAFTS = "include_drafts"


def select_sections_for_export(sections, *, draft_policy):
    if draft_policy is DraftPolicy.INCLUDE_DRAFTS:
        return list(sections)
    return [section for section in sections if not section["is_draft"]]
```

The call `select_sections_for_export(sections, draft_policy=DraftPolicy.EXCLUDE_DRAFTS)` reads as a sentence. The keyword-only `*` forces the role to be named, and the enum lets a third policy be added later without another flag. A single boolean whose meaning is plain from the function name, such as `set_enabled(is_enabled)`, does not need this treatment.

Check: drafts are excluded by `EXCLUDE_DRAFTS`; all sections are returned by `INCLUDE_DRAFTS`; a positional call raises `TypeError`.

## 10. One Tagged State Instead of Loose Flags

Bad (TypeScript fragment):

```typescript
interface ProfileView {
  isLoading: boolean;
  profile?: { displayName: string };
  errorMessage?: string;
}
```

This shape allows eight combinations, and only three are real. `isLoading: true` with an `errorMessage`, or a `profile` and an `errorMessage` together, can both be built, and every renderer has to guess which field wins.

Good (complete TypeScript example; Node 22.6+ can strip the types to run it, `tsc` checks them):

```typescript
type ProfileState =
  | { kind: "loading" }
  | { kind: "loaded"; profile: { displayName: string } }
  | { kind: "failed"; reason: string };

function assertNever(unexpectedValue: never): never {
  throw new Error(`Unexpected value: ${JSON.stringify(unexpectedValue)}`);
}

function describeProfileState(profileState: ProfileState): string {
  switch (profileState.kind) {
    case "loading":
      return "Loading profile";
    case "loaded":
      return `Signed in as ${profileState.profile.displayName}`;
    case "failed":
      return `Could not load profile: ${profileState.reason}`;
    default:
      return assertNever(profileState);
  }
}
```

Each state carries exactly the data that exists in that state. `profile` can only be read after the code has checked `kind === "loaded"`. Adding a fourth state makes `assertNever` fail to type-check until every switch handles it.

Check: each state renders its message; with `tsc --strict`, removing a case is a compile error; an object with an unknown `kind` reaching runtime throws instead of rendering blank.

## 11. Exhaustive Branches, No Silent Default

Bad (Java fragment):

```java
static String customerLabelFor(PaymentStatus paymentStatus) {
    switch (paymentStatus) {
        case PENDING: return "Awaiting payment";
        case PAID: return "Paid";
        default: return "";
    }
}
```

`REFUNDED` already falls into `default` and shows customers a blank label. When someone adds `DISPUTED`, it will too, and nothing will fail.

Good (complete Java example; save as `PaymentStatusLabels.java`):

```java
enum PaymentStatus { PENDING, PAID, REFUNDED }

final class PaymentStatusLabels {
    private PaymentStatusLabels() {
    }

    static String customerLabelFor(PaymentStatus paymentStatus) {
        return switch (paymentStatus) {
            case PENDING -> "Awaiting payment";
            case PAID -> "Paid";
            case REFUNDED -> "Refunded";
        };
    }
}
```

A switch expression over an enum with no `default` must cover every constant, so adding `DISPUTED` stops compilation at every label that needs a decision. Use the same approach with sealed interfaces and record patterns on Java 21+.

Check: compiles with javac 21+; each constant maps to its label; deleting a case fails compilation.

## 12. Parse Strings into Closed Values at the Boundary

Bad (Python fragment):

```python
if order["status"] == "canceled":
    refund(order)
```

The system writes `"cancelled"`. The comparison is never true, no error is raised, and refunds silently stop. Every comparison against a raw string repeats this risk.

Good (complete Python example):

```python
from enum import Enum


class OrderStatus(Enum):
    OPEN = "open"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


def parse_order_status_from(raw_status):
    try:
        return OrderStatus(raw_status)
    except ValueError as cause:
        raise ValueError(f"Unsupported order status: {raw_status!r}") from cause
```

The raw text is parsed once at the boundary. After that, code compares `order_status is OrderStatus.CANCELLED`; a misspelled member name raises `AttributeError` the first time it runs, and a type checker reports it before that. Unknown input is rejected with the offending value and the original cause.

Check: each known string parses; `"canceled"` raises `ValueError` with a `__cause__`; the parsed value is an `OrderStatus` member.

## 13. Units Live in the Type or the Name

Bad (Java fragment):

```java
void scheduleRetry(long delay) { ... }

scheduleRetry(30);
```

Is that 30 seconds or 30 milliseconds? Callers will guess differently, and the bug will look like a timing flake.

Good (Java fragment):

```java
void scheduleRetryAfter(Duration retryDelay) { ... }

scheduleRetryAfter(Duration.ofSeconds(30));
```

`Duration` carries its unit, so the caller states it and the callee cannot misread it. Where a unit type does not exist, put the unit in the name: `retry_delay_seconds`, `amountInCents`, `distanceMeters`. Use one unit convention across a module.

## 14. Distinct Identity Types Stop Swapped Arguments

Bad (Java fragment):

```java
void linkCustomerToAccount(String customerId, String accountId) { ... }

linkCustomerToAccount(order.accountId(), order.customerId());
```

Both IDs are strings, so the swapped call compiles and links the wrong records.

Good (complete Java example; save as `CustomerLinks.java`):

```java
import java.util.Objects;

record CustomerId(String value) {
    CustomerId {
        Objects.requireNonNull(value, "value");
        if (value.isBlank()) {
            throw new IllegalArgumentException("CustomerId must not be blank");
        }
    }
}

record AccountId(String value) {
    AccountId {
        Objects.requireNonNull(value, "value");
        if (value.isBlank()) {
            throw new IllegalArgumentException("AccountId must not be blank");
        }
    }
}

final class CustomerLinks {
    private CustomerLinks() {
    }

    static String describeLink(CustomerId customerId, AccountId accountId) {
        return "customer " + customerId.value() + " -> account " + accountId.value();
    }
}
```

Passing an `AccountId` where a `CustomerId` is expected is now a compile error, and a blank ID cannot be constructed. Use this where a swap is a real risk, such as IDs of different entities. Two values of the same role type, like source and destination accounts, still need named variables or a parameter object.

Check: compiles; swapped arguments fail compilation; blank IDs are rejected.

## 15. Guard Clauses Keep the Normal Path Flat

Bad (complete Python example):

```python
def shipping_label_for(order):
    if order is not None:
        if order["is_paid"]:
            if order["address"]:
                return f"Ship to {order['address']}"
            else:
                raise ValueError("Order has no address")
        else:
            raise ValueError("Order is not paid")
    else:
        raise ValueError("Order is required")
```

Each error is far from the condition that causes it, and the one line that matters is buried three levels deep.

Good (complete Python example):

```python
def shipping_label_for(order):
    if order is None:
        raise ValueError("Order is required")
    if not order["is_paid"]:
        raise ValueError("Order is not paid")
    if not order["address"]:
        raise ValueError("Order has no address")
    return f"Ship to {order['address']}"
```

Each rejection sits next to its condition, and the normal result is the last line at the left margin. Behavior is identical, which a characterization check should confirm before such a refactor.

Check: both versions return the same label and raise the same messages for missing, unpaid, and addressless orders.

## 16. Named Stages Instead of a Clever Chain

Bad (JavaScript fragment):

```javascript
const t = o.filter((x) => x.s === "paid" && !x.r).reduce((a, x) => a + x.q * x.p, 0);
```

It works, but a reviewer must decode `s`, `r`, `q`, `p`, and the unit of `t`.

Good (complete JavaScript example):

```javascript
function totalPaidRevenueInCentsFrom(orders) {
  const paidOrders = orders.filter((order) => order.status === "paid");
  const unrefundedPaidOrders = paidOrders.filter((order) => !order.isRefunded);
  const orderTotalsInCents = unrefundedPaidOrders.map(
    (order) => order.quantity * order.unitPriceInCents,
  );
  return orderTotalsInCents.reduce(
    (runningTotalInCents, orderTotalInCents) => runningTotalInCents + orderTotalInCents,
    0,
  );
}
```

Each stage has a name that says what it holds, and the unit is visible. The extra passes over a small array cost nothing measurable; if profiling shows they matter, combine stages and keep the names.

Check: empty input returns 0; unpaid and refunded orders are excluded; totals use quantity times unit price.

## 17. Pass the Clock In

Bad (Python fragment):

```python
def is_expired(token):
    return token["expires_at"] < datetime.now(timezone.utc)
```

The rule reads a global clock, so tests must patch time, two checks in one request can disagree, and the boundary instant is unclear.

Good (complete Python example):

```python
def is_expired_as_of(token, as_of_time):
    return as_of_time >= token["expires_at"]
```

The caller reads the clock once at the boundary: `is_expired_as_of(token, as_of_time=datetime.now(timezone.utc))`. The rule is now pure, testable with fixed instants, and states its boundary: a token is expired at exactly `expires_at`.

Check: one second before is not expired; the exact instant is expired; one second after is expired.

## 18. Do Not Swallow Failures

Bad (Java fragment):

```java
try {
    invoiceRepository.save(invoice);
} catch (Exception e) {
    log.warn("save failed");
}
return SaveStatus.SAVED;
```

The caller is told the invoice was saved when it was not. The log line has no ID and no cause. `catch (Exception e)` also catches programming errors.

Good (Java fragment; `DataAccessException` stands in for the repository's documented failure type):

```java
try {
    invoiceRepository.save(invoice);
} catch (DataAccessException cause) {
    throw new InvoiceSaveException("Could not save invoice " + invoice.id(), cause);
}
return SaveStatus.SAVED;
```

Only the documented failure is caught, it is translated into the caller's vocabulary with the invoice ID, and the original cause is kept. Success is reported only after the save returns. If the caller may continue, return an explicit failed outcome instead of throwing; never return success.

## 19. Named Constants Instead of Magic Numbers and Lying Comments

Bad (Python fragment):

```python
# Retry up to 3 times
for i in range(5):
    if send(message):
        break
    time.sleep(2 ** i * 0.1)
```

The comment says 3; the code tries 5. The backoff rule has to be reverse-engineered. Comments drift because nothing checks them.

Good (Python fragment):

```python
MAX_SEND_ATTEMPTS = 3
INITIAL_BACKOFF_SECONDS = 0.1

for attempt_number in range(1, MAX_SEND_ATTEMPTS + 1):
    if send(message):
        break
    backoff_seconds = INITIAL_BACKOFF_SECONDS * 2 ** (attempt_number - 1)
    time.sleep(backoff_seconds)
```

The names carry what the comment tried to say, so there is nothing to drift. Units are in the names. Keep a comment only for the reason behind a number, such as "the provider rate-limits at 10 requests per second". A real sender also decides what happens after the last failed attempt; see example 20.

## 20. Retry Only Idempotent Work

Bad illustrative pseudocode:

```text
retry(times = 3):
    paymentGateway.charge(cardToken, amountInCents)
```

If the first charge succeeds but its response times out, the retry charges the customer again.

Good illustrative pseudocode:

```text
idempotencyKey = paymentAttempt.id
retry(times = 3, retryOn = [ConnectionTimeout, ServiceUnavailable]):
    paymentGateway.charge(cardToken, amountInCents, idempotencyKey)
```

The key makes the operation safe to repeat, so the gateway charges once. Only failures known to be transient are retried; a declined card is a domain result and is not retried. The retry count and backoff are bounded and named.

## 21. Late Async Results Must Not Overwrite Newer State

Bad (JavaScript fragment):

```javascript
async function onSearchInput(queryText) {
  const searchResults = await searchClient.search(queryText);
  renderResults(searchResults);
}
```

If the user types "ca" then "cat", and the "ca" response arrives last, the screen shows results for "ca" under the "cat" search box.

Good (complete JavaScript example):

```javascript
function createLatestOnlySearch(searchClient, renderResults) {
  let latestRequestNumber = 0;

  return async function searchFor(queryText) {
    latestRequestNumber += 1;
    const requestNumber = latestRequestNumber;
    const searchResults = await searchClient.search(queryText);
    if (requestNumber !== latestRequestNumber) {
      return;
    }
    renderResults(searchResults);
  };
}
```

Only the newest request may render. Failures still reject to the caller, which owns error display. When the client supports it, also pass an `AbortSignal` so superseded requests stop using the network.

Check: with a fake client that resolves "cat" before "ca", only the "cat" results render.

## 22. Name the Operation That Can Fail

Bad (complete Python example):

```python
def first(items):
    return items[0] if items else 0
```

An empty list returns `0`, which looks like a real item for a list of numbers. The caller has no sign that absence is possible.

Good (complete Python example):

```python
def first_or_none(items):
    return items[0] if items else None


def first_or_raise(items, item_description):
    if not items:
        raise LookupError(f"Expected at least one {item_description}")
    return items[0]
```

The name says what happens when the list is empty, so the call site shows the risk. This follows the Jane Street convention of marking the raising variant (`_exn`) and making the safe one the default. Use `first_or_none` only when `None` cannot also be a valid item.

Check: non-empty lists return the first item; empty lists return `None` or raise `LookupError` naming the missing thing.

## 23. Do Not Leak Mutable Internals

Bad (Java fragment):

```java
final class Cart {
    private final List<String> itemIds = new ArrayList<>();

    List<String> itemIds() {
        return itemIds;
    }
}
```

`cart.itemIds().clear()` empties the cart without going through any rule the class enforces. `private final` protects the reference, not the contents.

Good (complete Java example; save as `Cart.java`):

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

final class Cart {
    private final List<String> itemIds = new ArrayList<>();

    void addItem(String itemId) {
        Objects.requireNonNull(itemId, "itemId");
        itemIds.add(itemId);
    }

    List<String> itemIds() {
        return List.copyOf(itemIds);
    }
}
```

The only way to change the cart is through `addItem`, which can enforce rules. Callers get an unmodifiable snapshot. Prefer a fully immutable value when the object does not need to change at all.

Check: compiles; `cart.itemIds().add(...)` throws `UnsupportedOperationException`; the snapshot does not change after a later `addItem`.

## 24. Expect-Style Tests Show the Whole Output

Bad (Python test fragment):

```python
def test_summary():
    summary = render_invoice_summary(lines)
    assert "Total" in summary
```

The test passes if every amount is wrong, the lines are missing, or the total is negative.

Good (complete Python example with its test):

```python
def format_cents(amount_in_cents):
    return f"{amount_in_cents // 100}.{amount_in_cents % 100:02d}"


def render_invoice_summary(invoice_lines):
    rendered_lines = []
    total_in_cents = 0
    for item_name, quantity, unit_price_in_cents in invoice_lines:
        line_total_in_cents = quantity * unit_price_in_cents
        total_in_cents += line_total_in_cents
        rendered_lines.append(f"{item_name} x{quantity}: {format_cents(line_total_in_cents)}")
    rendered_lines.append(f"Total: {format_cents(total_in_cents)}")
    return "\n".join(rendered_lines)


def test_render_invoice_summary_shows_each_line_and_the_total():
    invoice_lines = [("Widget", 2, 250), ("Gadget", 1, 1000)]

    summary = render_invoice_summary(invoice_lines)

    assert summary == (
        "Widget x2: 5.00\n"
        "Gadget x1: 10.00\n"
        "Total: 15.00"
    )
```

The input and the full expected output sit together, as in an expect test. Any change in formatting or arithmetic shows up as a readable diff, and the reviewer judges behavior directly. Keep the scenario small and deterministic so the expected output stays readable. `format_cents` assumes non-negative amounts; credits need their own rule and test.

Check: the test passes; changing a price or the format fails it with a readable diff.

## 25. Earn the Abstraction

Bad (Java fragment):

```java
interface DiscountStrategy { Money apply(Money price); }
final class DiscountStrategyFactory { static DiscountStrategy create(String type) { ... } }
final class TenPercentDiscountStrategy implements DiscountStrategy { ... }
```

There is one discount and no plan for another. Readers must walk an interface, a factory, and a string switch to find one multiplication.

Good (Java fragment):

```java
static Money applyLoyaltyDiscountTo(Money price) {
    return price.multipliedBy(LOYALTY_DISCOUNT_FACTOR);
}
```

Write the direct version. Introduce the interface when a second real discount exists, when tests need a seam at an effect boundary, or when the interface protects an invariant. The name `applyLoyaltyDiscountTo(price)` reads as a sentence and says which rule applies.
