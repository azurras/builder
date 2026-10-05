# Naming and Readability

This is a mandatory house rule for every language: **code must read like a sentence, and parameter names must complement method/function names**. Apply it to definitions and real calls, not just to the declaration being edited. Use each language's normal casing and syntax.

## Read the Whole Expression

1. Identify the subject: receiver, module, service, or domain object.
2. Choose an operation verb for an action, or a predicate for a question.
3. Name each parameter for its role in that operation. Name caller variables so their actual data fills that role intelligibly.
4. Read the receiver, operation, and arguments aloud. A reader must be able to tell who does what to which data.
5. Inspect ordinary, failure, and boundary calls. Fix confusing names or argument structure before considering the naming work finished.

| Bad | Better | Reason |
|---|---|---|
| `process(a, b)` | `send_invoice_to(invoice, recipient)` | Action and both roles are visible |
| `check(x, d)` | `invoice.isOverdueOn(asOfDate)` | The receiver is the subject and the method asks a question |
| `transfer(x, y, z)` | `transfer(amount, from=sourceAccount, to=destinationAccount)` | Named roles expose direction; illustrative labeled-call syntax |
| `copy(a, b, true)` | `copyFile(sourcePath, destinationPath, ExistingFilePolicy.REPLACE)` | Mode has a domain meaning; inspect the two path arguments |
| `wait(5000)` | `waitForCompletion(timeoutMilliseconds)` | Operation and unit are visible |
| `getUsers()` that writes missing records | `findUsers()` plus `createMissingUsers()` | Names expose distinct effects |

The table illustrates call expressions; the adaptation guide selects valid syntax for the language. For same-type arguments that are easy to swap, use named arguments/labels when supported, a small parameter value that validates the relationship, or distinct role types where warranted. An options object must have a real contract rather than become a bag of unrelated settings.

## Pair Method and Parameter Names

Use these patterns with idiomatic casing:

- `send_invoice_to(invoice, recipient)`: the function supplies the verb and relation; parameters supply the object and destination.
- `load_orders_for(customer_id)`: `customer_id` identifies the input role; the name exposes I/O.
- `is_eligible_for_discount(customer, purchase_date)`: a boolean result answers a stated question.
- `time_window.includes(candidate_instant)`: the receiver provides domain context; the argument supplies the candidate.

At a definition, do not use `x`, `value`, or `arg1` where `recipient`, `customer_id`, or `destination_path` carries essential meaning. At a call, do not hide those roles behind `a`, `b`, or opaque constants. A longer method name does not compensate for meaningless arguments.

Inspect positional compatibility before changing order. Inspect Python keyword calls, Swift argument labels, Kotlin/C# named calls, reflection, and public documentation before renaming parameters. Preserve externally mandated protocol method names and improve internal names and adapters around them.

## Name the Actual Data

- Name identities as identities: `customer_id`, not `customer` when the value is only an ID.
- Name singular items and collections distinctly: `invoice` and `invoices`.
- Expose meaningful representation: `response_text`, `decoded_user_fields`, `validated_user`.
- Include units or use a domain type: `timeout_milliseconds`, `distance_meters`, `amount_in_minor_units`.
- State ownership or scope when relevant: `pending_requests`, `session_subscriptions`, `source_path`.
- Give booleans positive predicates: `is_enabled`, `has_pending_work`, `can_publish`. Prefer `if is_enabled` to double negation.
- Short conventional local names can be clear in a tight mathematical, iteration, or protocol context. Expand them when their domain meaning would otherwise be guessed.

## Introduce a New Variable When Meaning Changes

Parsing, validation, serialization, filtering, aggregation, and conversions often produce a different representation or domain concept. Give each materially different concept its own binding.

Bad illustrative pseudocode:

```text
data = readResponse()
data = parseJson(data)
data = validateOrder(data)
data = sumOrderAmounts(data)
```

Good illustrative pseudocode:

```text
responseText = readResponse()
decodedOrderFields = parseJson(responseText)
validatedOrders = validateOrders(decodedOrderFields)
totalAmountInMinorUnits = sumOrderAmounts(validatedOrders)
```

A running total can remain `total_amount_in_minor_units` as it accumulates. A cursor can remain `next_page_cursor` as it advances. Those updates retain one role. Do not reuse `response_text` to hold a domain object, or `invoices` to hold a numeric total.

## Make Control Flow Readable

Put the normal path in a readable sequence; use guard clauses for independent invalid/early-exit cases. Extract a condition when its domain meaning is important, such as `has_permission_to_publish`, rather than requiring readers to reconstruct a compound boolean repeatedly. Keep a condition inline when it is already simple and clear.

Split a long pipeline or expression at points where meaning changes. Give intermediate values domain names. Prefer explicit branches when a nested conditional, side effect, or error translation makes an expression difficult to trace.

Comments explain intent, an invariant, a surprising constraint, or a compatibility decision. If a comment merely translates an opaque name into English, improve the name. Avoid comments that state guarantees the code does not enforce.

## Naming Review Questions

Read the actual call site and answer: What is the subject? What action or question is expressed? What does each argument represent? Can two arguments be reversed without obvious evidence? Are units and effects clear? Does each variable still hold what its name says? If any answer requires guessing, correct the name or API structure.
