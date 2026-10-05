# C++

Follow the repository's C++ standard, compiler, build system, `clang-format` and `clang-tidy` settings, and error-handling convention (exceptions, `std::expected`, or status codes). This guide applies the shared rules and the [principles](jane-street-principles.md) to C++. Many of the [C guide](c.md)'s concerns still apply at boundaries with C APIs, but C++ can carry the guarantees in its types: RAII owns every resource, constructors establish invariants, `enum class` and `std::variant` model closed states, `std::optional` and `std::expected` make absence and failure visible, and strong types and `std::chrono` stop swapped arguments and unit errors. The style uses those tools and avoids the escape hatches: raw `new` and `delete`, implicit conversions, dangling views, and detached threads.

The C++ examples in this guide were reviewed but not compiled in the Builder environment. Compile them with the target repository's compiler, warnings, and sanitizers before relying on them.

## Idioms at a Glance

| Prefer | Avoid | Why |
|---|---|---|
| RAII types and `std::unique_ptr` from `std::make_unique` | Raw `new` and `delete`; manual cleanup | Every resource is released on every exit, including exceptions |
| The rule of zero: members that manage themselves | Hand-written destructors and copy operations for ordinary classes | Fewer chances to get copying and moving wrong |
| Constructors that establish the invariant, with private data | Public fields or setters on types with invariants; two-phase `init()` | No object exists in an invalid state |
| `explicit` single-argument constructors | Implicit conversions from `int`, `std::string`, or `bool` | Values cannot silently become the wrong type |
| Strong types for IDs and quantities | Several `std::string` or `int` parameters with different roles | Swapped arguments fail to compile |
| `std::chrono` durations and time points | `int timeout` with the unit in a comment | The unit is part of the type |
| `enum class` and `switch` without `default` under `-Wswitch` | Unscoped enums, `int` codes, and placeholder defaults | Names do not leak; new values are reported |
| `std::variant` with `std::visit` for alternatives with data | Flags plus optional members | Each alternative holds exactly its data; a missing handler fails to compile |
| `std::optional` for absence; `std::expected` (C++23) or the repository's exception policy for failure | Sentinel values (`-1`, empty string) and out-parameters with `bool` returns | Outcomes are visible at the call site |
| `std::string_view` and `std::span` parameters for read-only input | Returning views into temporaries; storing views beyond the owner's life | Views never outlive what they point at |
| `std::jthread` with `std::stop_token` (C++20), or threads joined by an owner | Detached threads | Threads stop and are joined when their owner goes away |
| `std::scoped_lock` around short critical sections | Manual `lock`/`unlock`; locks held across callbacks or I/O | No forgotten unlocks or lock-order deadlocks |
| Named algorithms and ranges with named intermediate results | Index loops with manual bounds; dense nested lambdas | Intent is visible and bounds are handled |
| `static_cast` and friends | C-style casts | Each conversion states what it does |
| `-Wall -Wextra -Werror`, `clang-tidy`, AddressSanitizer, UndefinedBehaviorSanitizer, ThreadSanitizer | Default warnings only | Undefined behavior is caught early |

## Smells Reviewers Flag

- `new` or `delete` outside a low-level owning type; `malloc` in C++ code.
- A destructor, copy constructor, or copy assignment written for a class that only holds standard members.
- A non-`explicit` single-argument constructor.
- An `init()` or `setup()` method that must be called after construction.
- `std::string_view` or `std::span` returned from a function or stored in a member without a clear owner.
- A `switch` on an `enum class` with `default:`.
- `std::thread::detach()`.
- Catching `...` or `std::exception` and continuing; throwing values that are not exceptions.
- `using namespace std;` in a header.
- C-style casts, `reinterpret_cast` without a comment, `const_cast` to modify data.
- Output parameters that could be return values.
- Mutable `static` or global state in code that can run on several threads.

## Good and Bad Pairs

### Ownership Belongs to a Type

Bad (C++ fragment):

```cpp
Report* buildReport(const Order& order) {
    Report* report = new Report(order.id());
    report->addLines(order.lines());  // may throw
    return report;
}
```

If `addLines` throws, the report leaks. Callers must also guess whether they own the pointer.

Good (C++ fragment):

```cpp
std::unique_ptr<Report> buildReportFor(const Order& order) {
    auto report = std::make_unique<Report>(order.id());
    report->addLines(order.lines());
    return report;
}
```

The `unique_ptr` releases the report if an exception escapes and tells callers they own the result. If `Report` is cheap to move, return it by value instead and skip the heap allocation.

### Constructors Establish Invariants; Strong Types Stop Swaps

Bad (C++ fragment):

```cpp
struct TimeWindow {
    std::int64_t startsAtSeconds;
    std::int64_t endsAtSeconds;  // must be after startsAtSeconds
};

void linkCustomerToAccount(const std::string& customerId, const std::string& accountId);
```

Any code can build a reversed window, and the two IDs can be swapped at every call site.

Good (C++ fragment):

```cpp
class TimeWindow {
public:
    TimeWindow(std::chrono::sys_seconds startsAt, std::chrono::sys_seconds endsAt)
        : startsAt_(startsAt), endsAt_(endsAt) {
        if (endsAt_ <= startsAt_) {
            throw std::invalid_argument("TimeWindow end must be after its start");
        }
    }

    bool includes(std::chrono::sys_seconds candidateInstant) const noexcept {
        return candidateInstant >= startsAt_ && candidateInstant < endsAt_;
    }

private:
    std::chrono::sys_seconds startsAt_;
    std::chrono::sys_seconds endsAt_;
};

class CustomerId {
public:
    explicit CustomerId(std::string value) : value_(std::move(value)) {
        if (value_.empty()) {
            throw std::invalid_argument("CustomerId must not be empty");
        }
    }

    const std::string& value() const noexcept { return value_; }

private:
    std::string value_;
};

void linkCustomerToAccount(const CustomerId& customerId, const AccountId& accountId);
```

The window's fields are private and checked once, so every `TimeWindow` is valid, and `timeWindow.includes(candidateInstant)` reads as a question. `std::chrono` time points carry their unit. `CustomerId` and a matching `AccountId` make the swap a compile error, and `explicit` stops a plain string from converting silently. If the codebase does not use exceptions, make the constructor private and add a `static std::expected<TimeWindow, TimeWindowError> create(...)`.

### Units in the Type

Bad (C++ fragment):

```cpp
void setRequestTimeout(int timeout);  // milliseconds

client.setRequestTimeout(30);
```

Good (C++ fragment):

```cpp
void setRequestTimeout(std::chrono::milliseconds requestTimeout);

client.setRequestTimeout(std::chrono::seconds{30});
```

`std::chrono` converts seconds to milliseconds exactly, refuses lossy conversions without an explicit `duration_cast`, and the caller states the unit.

### `std::variant` Instead of Flags

Bad (C++ fragment):

```cpp
struct Download {
    bool isComplete = false;
    bool isFailed = false;
    std::uint64_t bytesReceived = 0;
    std::string errorMessage;
};
```

Good (C++ fragment):

```cpp
struct DownloadInProgress { std::uint64_t bytesReceived; };
struct DownloadComplete { std::filesystem::path filePath; };
struct DownloadFailed { std::string reason; };

using Download = std::variant<DownloadInProgress, DownloadComplete, DownloadFailed>;

template <class... Handlers>
struct Overloaded : Handlers... {
    using Handlers::operator()...;
};

std::string statusLineFor(const Download& download) {
    return std::visit(
        Overloaded{
            [](const DownloadInProgress& inProgress) { return std::to_string(inProgress.bytesReceived) + " bytes"; },
            [](const DownloadComplete& complete) { return "Saved to " + complete.filePath.string(); },
            [](const DownloadFailed& failed) { return "Failed: " + failed.reason; },
        },
        download);
}
```

Each alternative holds only its data. If a `DownloadPaused` alternative is added, `std::visit` fails to compile because no handler accepts it. Do not add a generic `auto` handler; it would hide new alternatives the way `default:` does. The `Overloaded` helper relies on C++20 aggregate deduction; C++17 needs a deduction guide.

### Make Failure Visible with `std::expected`

Bad (C++ fragment):

```cpp
int parsePort(const std::string& portText) {
    return std::stoi(portText);
}
```

`std::stoi` accepts `"80abc"` as 80, throws generic exceptions for other bad input, and the result is an `int` that may not be a valid port.

Good (C++23 fragment):

```cpp
enum class PortParseError { NotANumber, OutOfRange, Reserved };

std::expected<std::uint16_t, PortParseError> parsePortFrom(std::string_view portText) {
    unsigned int parsedNumber = 0;
    const char* textEnd = portText.data() + portText.size();
    auto [parseEnd, parseError] = std::from_chars(portText.data(), textEnd, parsedNumber);
    if (parseError == std::errc::result_out_of_range) {
        return std::unexpected(PortParseError::OutOfRange);
    }
    if (parseError != std::errc{} || parseEnd != textEnd) {
        return std::unexpected(PortParseError::NotANumber);
    }
    if (parsedNumber > 65535) {
        return std::unexpected(PortParseError::OutOfRange);
    }
    if (parsedNumber < 1024) {
        return std::unexpected(PortParseError::Reserved);
    }
    return static_cast<std::uint16_t>(parsedNumber);
}
```

The whole text must be a number, each rejection is a named outcome, and the type of a success is a valid port. `std::from_chars` does not allocate or depend on the locale. Before C++23, use the repository's result type or a specific exception.

### Views Must Not Outlive Their Owner

Bad (C++ fragment):

```cpp
std::string_view fileExtensionOf(std::string_view fileName);

std::string_view extension = fileExtensionOf(directory + "/" + fileName);
useExtension(extension);  // dangling
```

The concatenated string is a temporary destroyed at the end of the full expression, so `extension` points at freed memory.

Good (C++ fragment):

```cpp
const std::string filePath = directory + "/" + fileName;
const std::string_view extension = fileExtensionOf(filePath);
useExtension(extension);
```

The owning string has a name and outlives the view. Use `std::string_view` for parameters; return or store an owning `std::string` unless the view's owner is clearly longer-lived.

### Threads Have Owners That Stop and Join Them

Bad (C++ fragment):

```cpp
std::thread([this] { pollForUpdates(); }).detach();
```

Nothing can stop the thread, and it may run after `this` is destroyed.

Good (C++20 fragment):

```cpp
class UpdatePoller {
public:
    UpdatePoller()
        : pollingThread_([this](std::stop_token stopToken) { pollUntilStopped(stopToken); }) {}

private:
    void pollUntilStopped(std::stop_token stopToken) {
        while (!stopToken.stop_requested()) {
            pollForUpdates();
            std::this_thread::sleep_for(pollInterval);
        }
    }

    std::jthread pollingThread_;
};
```

`std::jthread` requests a stop and joins in its destructor, so the poller's lifetime bounds the thread's lifetime. Declare the `jthread` member last so it is destroyed first, before any members the thread uses. For prompt shutdown, wait on a `std::condition_variable_any` with the stop token instead of sleeping.

## Implementation Recipe

1. Inspect the C++ standard, compiler, `clang-tidy` checks, exception policy, and the project's ownership and error types.
2. Design types first: constructors that establish invariants, `explicit` conversions, strong types for IDs and units, and `enum class` or `std::variant` for states.
3. Express ownership with values and smart pointers; pass read-only input as `const&`, `std::string_view`, or `std::span`; keep views shorter-lived than their owners.
4. Use the project's single error convention consistently: exceptions with specific types, or `std::expected` or status types. Do not mix them at one boundary.
5. Give every thread and asynchronous task an owner that stops and joins it; keep locks short and never call unknown code while holding one.
6. Build with warnings as errors, run `clang-tidy`, and test under AddressSanitizer, UndefinedBehaviorSanitizer, and ThreadSanitizer for concurrent code.

## Testing in C++

- Use the repository's framework (GoogleTest, Catch2, doctest) with parameterized or table tests for cases.
- Test each error outcome and each invariant rejection, not only the success path.
- Run tests under sanitizers in CI.
- Fuzz parsers and decoders when the project supports it.

## Evidence and Review

The compiler proves types, `const`, and some exhaustiveness. It does not prove view lifetimes, thread ownership, or the absence of undefined behavior. Review those directly and record sanitizer and analyzer results.
