# C

Follow the repository's C standard (C99, C11, C17, or C23), compiler, warning flags, formatter, and static analysis. This guide applies the shared rules and the [principles](jane-street-principles.md) to C. C provides almost none of the guarantees the style relies on: no exceptions, no destructors, no bounds checks, no namespaces, and no way to hide a struct's fields except by convention or opaque types. The style therefore moves the guarantees into discipline you can see in the code: every return value is checked, every allocation has one owner and one cleanup path, every buffer travels with its length, invariants live behind opaque types, and the compiler's warnings and sanitizers are part of the build.

The C examples in this guide were reviewed but not compiled in the Builder environment. Compile them with the target repository's compiler, warnings, and sanitizers before relying on them.

## Idioms at a Glance

| Prefer | Avoid | Why |
|---|---|---|
| A status enum returned from every fallible function, with results in out-parameters | Returning `-1`, `0`, or `NULL` with several meanings; ignoring return values | Callers can see and handle each outcome |
| Checking the return of `malloc`, `fopen`, `fwrite`, `fclose`, `snprintf`, and system calls | Assuming success | Failures are reported where they happen |
| One owner per allocation, documented in the function contract | Unclear "who frees this" | No leaks or double frees |
| A single `cleanup:` label that releases everything acquired | Several early returns that each free a different subset | Cleanup is correct on every exit |
| Pointer and length passed together (`const char *text, size_t text_length`) | Pointers whose size the callee must guess | Bounds can be checked |
| `snprintf` with a truncation check; `memcpy` with a checked size | `strcpy`, `strcat`, `sprintf`, `gets` | No silent buffer overflows |
| `size_t` for sizes and counts, with overflow checks before multiplication | `int` for sizes; unchecked `count * size` | No negative sizes or wrapped allocations |
| Opaque structs (`struct time_window;` in the header) with create and destroy functions | Public struct fields for types with invariants | Only the module can build or change a value |
| `enum` for closed states and `switch` without `default`, with `-Wswitch-enum` | `int` state codes and `default:` that hides new values | The compiler reports unhandled cases |
| `const` on everything a function does not modify | Non-`const` pointers to read-only data | The signature tells the caller what may change |
| `static inline` functions | Function-like macros | Arguments are evaluated once and have types |
| Module-prefixed names that read as sentences: `invoice_send_to(invoice, recipient)` | Short global names (`send`, `init`) | No collisions, and calls read clearly without namespaces |
| `-Wall -Wextra -Werror`, AddressSanitizer, UndefinedBehaviorSanitizer, and static analysis in CI | Compiling with default warnings | Many memory and undefined-behavior bugs are caught automatically |

## Smells Reviewers Flag

- A call to a function that can fail whose result is not checked.
- `strcpy`, `strcat`, `sprintf`, `gets`, `scanf("%s")`, or `strncpy` used as if it always terminates the string.
- `malloc(count * sizeof(item))` without an overflow check on `count`.
- A function that returns a pointer without saying who owns it and how to free it.
- Several `return` statements in a function that has acquired more than one resource.
- `int` used for sizes, lengths, or array indexes that come from input.
- A `switch` on an enum with `default:` returning a placeholder.
- Function-like macros that evaluate an argument twice.
- Global mutable variables, especially in code that may run on several threads.
- Casts that silence a warning instead of fixing the type.
- Reading a struct field or array element before checking the pointer or index.

## Good and Bad Pairs

### Bounded Formatting with a Truncation Check

Bad (C fragment):

```c
char greeting[32];
sprintf(greeting, "Hello, %s", display_name);
```

A display name longer than 24 characters writes past the end of `greeting`. This is a memory-safety bug, not a cosmetic one.

Good (C fragment):

```c
enum greeting_status { GREETING_OK, GREETING_TRUNCATED, GREETING_FORMAT_FAILED };

enum greeting_status greeting_format_into(char *greeting_buffer, size_t greeting_buffer_size,
                                          const char *display_name)
{
    int written_length = snprintf(greeting_buffer, greeting_buffer_size, "Hello, %s", display_name);
    if (written_length < 0) {
        return GREETING_FORMAT_FAILED;
    }
    if ((size_t)written_length >= greeting_buffer_size) {
        return GREETING_TRUNCATED;
    }
    return GREETING_OK;
}
```

The buffer travels with its size, `snprintf` never writes past it, and truncation is a distinct outcome the caller must decide about. The name `greeting_format_into(buffer, size, display_name)` says where the result goes.

### One Cleanup Path for Every Exit

Bad (C fragment):

```c
int write_report(const char *path, const struct report *report)
{
    char *text = render_report(report);
    FILE *file = fopen(path, "w");
    if (file == NULL) {
        return -1;
    }
    fputs(text, file);
    fclose(file);
    free(text);
    return 0;
}
```

If `fopen` fails, `text` leaks. If `render_report` returns `NULL`, `fputs` crashes. Write and close failures are ignored, so a full disk reports success.

Good (C fragment):

```c
enum report_status { REPORT_OK, REPORT_OUT_OF_MEMORY, REPORT_WRITE_FAILED };

enum report_status report_write_to(const char *report_path, const struct report *report)
{
    enum report_status status = REPORT_WRITE_FAILED;
    char *rendered_report = NULL;
    FILE *report_file = NULL;

    rendered_report = report_render(report);
    if (rendered_report == NULL) {
        status = REPORT_OUT_OF_MEMORY;
        goto cleanup;
    }
    report_file = fopen(report_path, "w");
    if (report_file == NULL) {
        goto cleanup;
    }
    if (fputs(rendered_report, report_file) == EOF) {
        goto cleanup;
    }
    int close_result = fclose(report_file);
    report_file = NULL;
    if (close_result != 0) {
        goto cleanup;
    }
    status = REPORT_OK;

cleanup:
    if (report_file != NULL) {
        fclose(report_file);
    }
    free(rendered_report);
    return status;
}
```

Every resource starts as `NULL`, every failure jumps to one label, and the label releases exactly what was acquired. `fclose` is checked because buffered data is flushed there. The caller can use `errno` for detail after `REPORT_WRITE_FAILED` if the contract documents it. Forward-only `goto` to a cleanup label is the established C idiom for this, not a smell.

### Check Before Multiplying an Allocation Size

Bad (C fragment):

```c
struct order_line *order_lines = malloc(line_count * sizeof *order_lines);
```

A large `line_count` from input wraps the multiplication to a small number. `malloc` succeeds, and later writes overflow the heap.

Good (C fragment):

```c
if (line_count > SIZE_MAX / sizeof(struct order_line)) {
    return ORDER_TOO_MANY_LINES;
}
struct order_line *order_lines = malloc(line_count * sizeof *order_lines);
if (order_lines == NULL) {
    return ORDER_OUT_OF_MEMORY;
}
```

The overflow is rejected as its own outcome before allocating, and allocation failure is checked. `calloc(line_count, sizeof *order_lines)` performs the overflow check itself and zeroes the memory; use it when zeroing is wanted.

### Opaque Types Guard Invariants

Bad (C fragment, `time_window.h`):

```c
struct time_window {
    long long starts_at_seconds;
    long long ends_at_seconds; /* must be greater than starts_at_seconds */
};
```

Any file that includes the header can build a reversed window.

Good (C fragment, `time_window.h`):

```c
struct time_window;

enum time_window_status { TIME_WINDOW_OK, TIME_WINDOW_INVALID_ORDER, TIME_WINDOW_OUT_OF_MEMORY };

enum time_window_status time_window_create(long long starts_at_seconds, long long ends_at_seconds,
                                           struct time_window **created_window);
void time_window_destroy(struct time_window *time_window);
bool time_window_includes(const struct time_window *time_window, long long candidate_seconds);
```

The struct's fields are defined only in `time_window.c`, so `time_window_create` is the only way to make one and it rejects reversed endpoints. Ownership is explicit: whoever receives `created_window` calls `time_window_destroy`. The function names read as sentences with the module as their subject. When heap allocation is too costly, expose the struct but keep the rule that only module functions write its fields, and say so in the header.

### Pointers Travel with Their Lengths

Bad (C fragment):

```c
long sum(int *values);
```

The function cannot know how many values exist, and the non-`const` pointer suggests it may change them.

Good (C fragment):

```c
long long values_sum(const int *values, size_t value_count);
```

The count is part of the contract, `const` promises the values are read only, and the wider return type avoids overflow for realistic counts. The call `values_sum(prices, price_count)` shows both halves of the array together.

### Exhaustive `switch` on Enums

Bad (C fragment):

```c
switch (payment_status) {
case PAYMENT_PENDING: return "Awaiting payment";
case PAYMENT_PAID: return "Paid";
default: return "";
}
```

Good (C fragment):

```c
switch (payment_status) {
case PAYMENT_PENDING:
    return "Awaiting payment";
case PAYMENT_PAID:
    return "Paid";
case PAYMENT_REFUNDED:
    return "Refunded";
}
return NULL; /* Unreachable for valid enum values; callers treat NULL as a defect. */
```

With no `default`, `-Wswitch` (part of `-Wall`) reports any enum value the `switch` does not name. The code after the `switch` handles out-of-range integers, which C allows in an enum variable, as a visible defect rather than a blank label.

## Implementation Recipe

1. Inspect the C standard, compiler, warning flags, sanitizer and analyzer setup, and the project's ownership and error conventions.
2. Write the header first: opaque types, status enums, `const`-correct pointer and length pairs, and a comment for each function stating ownership and failure.
3. Check every fallible call; route every failure through one cleanup path.
4. Validate sizes and indexes before use; check multiplication and addition that feed allocation or indexing.
5. Keep global state out of library code; if threads are involved, document which lock protects what.
6. Build with warnings as errors and run tests under AddressSanitizer and UndefinedBehaviorSanitizer; run the repository's static analyzer.

## Testing in C

- Test each status outcome, not only the success path: allocation failure (with an injectable allocator if the project has one), I/O failure, truncation, and invalid input.
- Run tests under sanitizers in CI; a test that passes without them proves less.
- Fuzz parsers and anything that reads external input (libFuzzer or AFL) when the project supports it.

## Evidence and Review

A clean compile proves very little in C. Review every acquired resource for its release on every path, every buffer write for its bound, and every arithmetic expression that feeds a size. Record sanitizer and analyzer results as evidence.
