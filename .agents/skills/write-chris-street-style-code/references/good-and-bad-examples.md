# Good and Bad Examples

These original examples demonstrate the house rules. Each pair names the defect and the contract improved by the correction. Complete examples can be checked with the stated native tool; fragments and pseudocode illustrate structure and require the surrounding application's real contract.

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
