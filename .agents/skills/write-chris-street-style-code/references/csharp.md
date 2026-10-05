# C#

Follow the repository's .NET and C# version, nullable settings, analyzers, `.editorconfig`, and test framework. This guide applies the shared rules and the [principles](jane-street-principles.md) to C# and .NET. Modern C# supports the style well: nullable reference types make absence visible, records and `required` members model values, switch expressions and pattern matching handle alternatives, and named arguments make call sites read like sentences. The style asks you to turn those features on and not escape them with `!`, `async void`, or broad catches.

The C# examples in this guide were reviewed but not compiled in the Builder environment. Compile and test them with the target repository's SDK before relying on them.

## Idioms at a Glance

| Prefer | Avoid | Why |
|---|---|---|
| `<Nullable>enable</Nullable>` and honest `T?` annotations | The null-forgiving `!` to silence warnings | The compiler tracks absence for you |
| Records or classes whose constructors validate, with get-only properties | `init` setters on types with invariants, public setters | `with` expressions and object initializers bypass constructor checks |
| Switch expressions with every enum member or sealed subtype named | `default` branches returning placeholder values | New cases are found, not hidden |
| `async Task` all the way, with a `CancellationToken` parameter | `async void`, `.Result`, `.Wait()` | Exceptions are observed; no deadlocks; work can be cancelled |
| `using` and `await using` declarations | Manual `Dispose` calls | Cleanup runs on every exit |
| `throw;` to rethrow; `new SpecificException(message, innerException)` to translate | `throw ex;`, or translating without the inner exception | Stack traces and causes survive |
| Named arguments for booleans and same-type parameters | `Send(report, true, false)` | Call sites state each role |
| `TimeProvider` or an injected clock (.NET 8+) | `DateTime.Now` in rules | Time is explicit and testable; `DateTime.Now` is also local time |
| `decimal` for money; `DateTimeOffset` for instants | `double` for money; `DateTime` with unspecified kind | Exact decimal arithmetic and explicit offsets |
| Constructor injection; options validated at startup (`ValidateOnStart`) | Service locator calls; options read and checked lazily | Misconfiguration fails at startup, not at the first request |
| LINQ for pure queries; `foreach` when the body has effects | `Select` with side effects; multiple enumeration of a lazy query | Data flow is visible and runs once |
| `IReadOnlyList<T>` and immutable collections in public APIs | Exposing `List<T>` fields | Callers cannot bypass the owner's rules |

## Smells Reviewers Flag

- `catch (Exception)` that logs and continues, or `catch { }`.
- `throw ex;` (resets the stack trace).
- `async void` outside UI event handlers; `.Result` or `.Wait()` on tasks.
- A public async method with no `CancellationToken` when it does I/O.
- `!` used to silence nullable warnings rather than to state a proven invariant.
- `init` accessors or public setters on a type whose constructor validates.
- `DateTime.Now`, `Guid.NewGuid()`, or `Random.Shared` called inside domain rules that tests need to control.
- `bool` parameters at call sites without names.
- `IEnumerable<T>` from a lazy query enumerated more than once.
- Static mutable state in ASP.NET services that handle concurrent requests.

## Good and Bad Pairs

### Constructors Validate; `with` Must Not Bypass Them

Bad (C# fragment):

```csharp
public record TimeWindow(DateTimeOffset StartsAt, DateTimeOffset EndsAt);
```

Positional records generate `init` properties, so `new TimeWindow(end, start)` and `window with { EndsAt = window.StartsAt }` both build reversed windows.

Good (C# fragment):

```csharp
public sealed record TimeWindow
{
    public TimeWindow(DateTimeOffset startsAt, DateTimeOffset endsAt)
    {
        if (endsAt <= startsAt)
        {
            throw new ArgumentException("endsAt must be after startsAt.", nameof(endsAt));
        }
        StartsAt = startsAt;
        EndsAt = endsAt;
    }

    public DateTimeOffset StartsAt { get; }

    public DateTimeOffset EndsAt { get; }

    public bool Includes(DateTimeOffset candidateInstant) =>
        candidateInstant >= StartsAt && candidateInstant < EndsAt;
}
```

Get-only properties cannot be set by `with` or object initializers, so the constructor is the only way in. `window.Includes(candidateInstant)` reads as a question.

### Rethrow Without Losing the Stack

Bad (C# fragment):

```csharp
try
{
    await invoiceRepository.SaveAsync(invoice, cancellationToken);
}
catch (Exception ex)
{
    logger.LogError("Save failed");
    throw ex;
}
```

`throw ex;` restarts the stack trace at this line, the log message has no invoice ID or exception, and the broad catch logs cancellations as errors.

Good (C# fragment):

```csharp
try
{
    await invoiceRepository.SaveAsync(invoice, cancellationToken);
}
catch (DbUpdateException saveFailure)
{
    throw new InvoiceSaveException($"Could not save invoice {invoice.Id}.", saveFailure);
}
```

Only the documented persistence failure is caught and translated, the original exception is the `InnerException`, and `OperationCanceledException` passes through untouched. If no translation is needed, do not catch at all; if you must log and rethrow, use `throw;`.

### Async All the Way, with Cancellation

Bad (C# fragment):

```csharp
public async void RefreshPrices()
{
    var prices = priceClient.FetchPricesAsync().Result;
    cache.Store(prices);
}
```

`async void` exceptions crash the process or vanish; `.Result` blocks a thread and can deadlock under a synchronization context; nothing can cancel the work.

Good (C# fragment):

```csharp
public async Task RefreshPricesAsync(CancellationToken cancellationToken)
{
    IReadOnlyList<Price> fetchedPrices = await priceClient.FetchPricesAsync(cancellationToken);
    cache.Store(fetchedPrices);
}
```

The caller awaits the task, observes failures, and can cancel. Pass the token to every awaited call that accepts one.

### Named Arguments State the Role

Bad (C# fragment):

```csharp
reportSender.Send(report, true, false);
```

Good (C# fragment):

```csharp
reportSender.Send(report, includeDrafts: true, notifyOwner: false);
```

Named arguments make each flag's role visible and survive parameter reordering. When flags combine into modes, replace them with an enum.

### Exhaustive Switch Expressions

Bad (C# fragment):

```csharp
string label = status switch
{
    PaymentStatus.Pending => "Awaiting payment",
    PaymentStatus.Paid => "Paid",
    _ => "",
};
```

`Refunded` and any future status render as a blank label.

Good (C# fragment):

```csharp
string label = paymentStatus switch
{
    PaymentStatus.Pending => "Awaiting payment",
    PaymentStatus.Paid => "Paid",
    PaymentStatus.Refunded => "Refunded",
    _ => throw new ArgumentOutOfRangeException(nameof(paymentStatus), paymentStatus, "Unhandled payment status."),
};
```

Every named member is handled. C# enums can hold unnamed integer values, so the compiler still asks for a discard arm; make it throw with the value instead of returning a placeholder. Treat warning CS8509 (non-exhaustive switch) as an error. For sealed record hierarchies, prefer an abstract base with a private constructor so the set of subtypes is closed.

### Fail at Startup on Bad Configuration

Bad (C# fragment):

```csharp
var smtpHost = configuration["Smtp:Host"] ?? "localhost";
```

A missing production setting silently sends mail to localhost.

Good (C# fragment):

```csharp
public sealed class SmtpOptions
{
    [Required]
    public required string Host { get; init; }

    [Range(1, 65535)]
    public required int Port { get; init; }
}

builder.Services
    .AddOptions<SmtpOptions>()
    .Bind(builder.Configuration.GetSection("Smtp"))
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

The required settings are declared in one place, and the application refuses to start without them. Options classes are configuration bags bound by the framework, so `init` is acceptable here; validation runs at startup instead of in a constructor.

## Implementation Recipe

1. Inspect the target framework, C# language version, nullable setting, analyzers, and `.editorconfig`. Follow .NET naming (`PascalCase` members, `Async` suffix on async methods); the house sentence rule applies to methods, parameters, and calls.
2. Model values with validating constructors and get-only properties; model closed alternatives with enums or closed hierarchies.
3. Choose outcomes: nullable return for absence, a result type for expected domain refusals if the codebase uses one, specific exceptions with inner exceptions for failures.
4. Use `async Task` and `CancellationToken` through every I/O path; dispose resources with `using`.
5. Inject dependencies and `TimeProvider`; validate options at startup.
6. Build with warnings as errors where the repository does, and run analyzers and tests.

## Testing in C#

- Use `[Theory]` with `[InlineData]` (xUnit) or `[TestCase]` (NUnit) for case tables.
- Assert exceptions and their `InnerException` when translation is the contract.
- Use `FakeTimeProvider` for time and real databases (Testcontainers or the repository's harness) for persistence behavior.
- Use `WebApplicationFactory` for HTTP pipeline tests instead of mocking middleware.

## Evidence and Review

Nullable analysis and the compiler prove what the annotations say; they do not prove that `!` is justified, that a catch translates the right exceptions, or that cancellation flows through. Review those paths directly and test them.
