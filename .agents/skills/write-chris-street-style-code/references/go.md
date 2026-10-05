# Go

Follow the repository's Go version, `gofmt`, `go vet`, linters (such as `staticcheck` or `golangci-lint`), and module layout. This guide applies the shared rules and the [principles](jane-street-principles.md) to Go. Go already values plain, explicit code, so much of the style is native: errors are values, interfaces are small, and formatting is not debated. The style adds discipline where Go is permissive: errors must carry context and keep their cause, every goroutine needs an owner, enums need exhaustiveness checks, and a struct's zero value must not be an invalid trusted value.

The Go examples in this guide were reviewed but not compiled in the Builder environment. Compile and test them with the target repository's Go toolchain before relying on them.

## Idioms at a Glance

| Prefer | Avoid | Why |
|---|---|---|
| `if err != nil { return ..., fmt.Errorf("load config %s: %w", path, err) }` | `_` for errors, `return err` with no context, `%v` that drops the cause | Errors say what was attempted and still match `errors.Is` and `errors.As` |
| Sentinel or typed errors for outcomes callers handle (`ErrNotFound`) | Returning `nil, nil` for "not found" | Absence is explicit and distinct from success |
| `context.Context` as the first parameter of blocking or I/O calls | Background work with no cancellation | Callers can cancel and set deadlines |
| `defer resource.Close()` after the error check | `defer` before checking the error; ignoring `Close` errors on writes | No nil dereference; failed flushes are reported |
| A goroutine with a clear owner that waits for it (`errgroup`, `sync.WaitGroup`) | `go doWork()` fire-and-forget | Failures and lifetimes are observed |
| The sender closes a channel; receivers never do | Closing from the receiver or from several senders | Prevents panics on send to a closed channel |
| Small interfaces declared by the consumer | Large interfaces declared next to the only implementation | Interfaces describe what a caller needs |
| Named types: `type UserID string`, `time.Duration` | Bare `string` and `int` for IDs and durations | Swaps and unit mistakes become type errors |
| Typed constants starting at `iota + 1` plus an exhaustiveness linter | Raw strings for states; zero value meaning a real state | The zero value is detectably unset |
| Unexported fields with a validating `New...` constructor | Exported fields on types with invariants | Outside packages cannot build invalid values field by field |
| Table-driven tests with named cases | Copy-pasted test functions | Cases read as a specification |
| Explicit dependencies in structs or parameters | Package-level mutable variables and side effects in `init()` | Tests and concurrent callers do not share hidden state |

## Smells Reviewers Flag

- `value, _ := ...` where the discarded value is an error.
- `return err` that passes a low-level error up through several layers with no context.
- `fmt.Errorf("...: %v", err)` where callers need `errors.Is` or `errors.As` (use `%w`).
- `panic` for expected failures such as bad input or missing files.
- `go func() { ... }()` with no `WaitGroup`, `errgroup`, or channel the caller waits on.
- A loop that starts unbounded goroutines for unbounded input.
- `defer` inside a long loop (cleanup waits until the function returns).
- `switch` on a domain enum with a `default` that hides unhandled values.
- `interface{}` or `any` in domain signatures.
- Mutex fields copied by value (`go vet` catches some of these), or locks held across network calls.
- A function named `Get...` that performs network I/O without taking a `context.Context`.

## Good and Bad Pairs

### Errors Carry Context and Keep Their Cause

Bad (Go fragment):

```go
configBytes, _ := os.ReadFile(configPath)
var config Config
json.Unmarshal(configBytes, &config)
return config
```

A missing file and malformed JSON both produce a zero `Config`, and the program starts with settings nobody chose.

Good (Go fragment):

```go
func loadConfigFrom(configPath string) (Config, error) {
	configBytes, err := os.ReadFile(configPath)
	if err != nil {
		return Config{}, fmt.Errorf("read config %s: %w", configPath, err)
	}
	var decodedConfig Config
	if err := json.Unmarshal(configBytes, &decodedConfig); err != nil {
		return Config{}, fmt.Errorf("decode config %s: %w", configPath, err)
	}
	if err := decodedConfig.validate(); err != nil {
		return Config{}, fmt.Errorf("validate config %s: %w", configPath, err)
	}
	return decodedConfig, nil
}
```

Each failure names the stage and the path, `%w` keeps the cause so callers can use `errors.Is(err, fs.ErrNotExist)`, and the decoded value is validated before it is returned.

### Not Found Is an Outcome, Not `nil, nil`

Bad (Go fragment):

```go
func (store *UserStore) FindUser(id string) (*User, error) {
	user, err := store.query(id)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	return user, err
}
```

Callers that only check `err` will dereference a nil user. The comparison with `==` also misses wrapped errors.

Good (Go fragment):

```go
var ErrUserNotFound = errors.New("user not found")

func (store *UserStore) FindUserByID(ctx context.Context, userID UserID) (User, error) {
	row := store.database.QueryRowContext(ctx, "SELECT id, email FROM users WHERE id = $1", userID)
	var foundUser User
	err := row.Scan(&foundUser.ID, &foundUser.Email)
	if errors.Is(err, sql.ErrNoRows) {
		return User{}, fmt.Errorf("user %s: %w", userID, ErrUserNotFound)
	}
	if err != nil {
		return User{}, fmt.Errorf("find user %s: %w", userID, err)
	}
	return foundUser, nil
}
```

Absence is a named error that callers test with `errors.Is(err, ErrUserNotFound)`, infrastructure failure is a different error, and the call is cancellable. Use the placeholder syntax of the repository's SQL driver.

### Every Goroutine Has an Owner

Bad (Go fragment):

```go
for _, recipient := range recipients {
	go notifier.Notify(recipient)
}
return nil
```

The function returns before any notification is sent, failures vanish, and a large list starts thousands of goroutines at once.

Good (Go fragment; uses `golang.org/x/sync/errgroup` and Go 1.22 per-iteration loop variables):

```go
func notifyAll(ctx context.Context, recipients []Recipient, notifier Notifier) error {
	notifyGroup, groupContext := errgroup.WithContext(ctx)
	notifyGroup.SetLimit(maxConcurrentNotifications)
	for _, recipient := range recipients {
		notifyGroup.Go(func() error {
			return notifier.Notify(groupContext, recipient)
		})
	}
	return notifyGroup.Wait()
}
```

The group owns the goroutines, bounds concurrency, cancels the rest after the first failure, and returns that failure to the caller. Before Go 1.22, copy `recipient` inside the loop.

### Enums Start at One and Are Checked

Bad (Go fragment):

```go
if order.Status == "canceled" { ... }
```

The stored value is `"cancelled"`; the branch never runs and nothing reports it.

Good (Go fragment):

```go
type OrderStatus int

const (
	OrderStatusOpen OrderStatus = iota + 1
	OrderStatusShipped
	OrderStatusCancelled
)

func customerLabelFor(orderStatus OrderStatus) (string, error) {
	switch orderStatus {
	case OrderStatusOpen:
		return "Open", nil
	case OrderStatusShipped:
		return "Shipped", nil
	case OrderStatusCancelled:
		return "Cancelled", nil
	default:
		return "", fmt.Errorf("unhandled order status %d", orderStatus)
	}
}
```

Starting at `iota + 1` makes the zero value invalid, so an unset status is detectable. The `default` reports the unexpected value instead of hiding it. Go's compiler does not enforce exhaustive switches; enable an `exhaustive` linter if the repository uses one.

### Constructors Guard the Invariant

Bad (Go fragment):

```go
type TimeWindow struct {
	StartsAt time.Time
	EndsAt   time.Time // must be after StartsAt
}
```

Any package can build a reversed window.

Good (Go fragment):

```go
type TimeWindow struct {
	startsAt time.Time
	endsAt   time.Time
}

func NewTimeWindow(startsAt, endsAt time.Time) (TimeWindow, error) {
	if !endsAt.After(startsAt) {
		return TimeWindow{}, fmt.Errorf("time window end %s must be after start %s", endsAt, startsAt)
	}
	return TimeWindow{startsAt: startsAt, endsAt: endsAt}, nil
}

func (window TimeWindow) Includes(candidateTime time.Time) bool {
	return !candidateTime.Before(window.startsAt) && candidateTime.Before(window.endsAt)
}
```

Unexported fields force other packages through `NewTimeWindow`. Go still lets any package write `TimeWindow{}`, so methods must either treat the zero value safely or the package must document that only constructed values are valid. Here a zero window includes nothing, which is safe.

### Defer After the Error Check

Bad (Go fragment):

```go
reportFile, err := os.Create(reportPath)
defer reportFile.Close()
if err != nil {
	return err
}
```

If `Create` fails, the deferred `Close` runs on a nil file. For written files, an ignored `Close` error can hide data that never reached the disk.

Good (Go fragment):

```go
func writeReportTo(reportPath string, reportText string) (err error) {
	reportFile, err := os.Create(reportPath)
	if err != nil {
		return fmt.Errorf("create report %s: %w", reportPath, err)
	}
	defer func() {
		if closeErr := reportFile.Close(); closeErr != nil && err == nil {
			err = fmt.Errorf("close report %s: %w", reportPath, closeErr)
		}
	}()
	if _, err := reportFile.WriteString(reportText); err != nil {
		return fmt.Errorf("write report %s: %w", reportPath, err)
	}
	return nil
}
```

Cleanup is registered only after acquisition succeeds, and a failed close is reported when nothing else failed first.

## Implementation Recipe

1. Inspect the Go version in `go.mod`, the linters, and neighboring package style. Follow Go naming: short receiver names, `MixedCaps`, no `Get` prefix on simple getters. The house sentence rule applies to functions, parameters, and call sites: `store.FindUserByID(ctx, userID)`.
2. Model states with named types and validating constructors; make the zero value either useful or detectably invalid.
3. Return errors with context and `%w`. Use sentinel or typed errors only for outcomes callers act on.
4. Pass `context.Context` first to anything that blocks or does I/O. Give every goroutine an owner who waits for it and observes its error.
5. Keep decisions in plain functions and effects at the edges; inject clocks (`func() time.Time`) when time affects a rule.
6. Run `gofmt`, `go vet`, the repository's linters, and `go test -race` for concurrent code.

## Testing in Go

- Use table-driven tests with `t.Run(testCase.name, ...)` so failures name the case.
- Compare errors with `errors.Is` and `errors.As`, not string matching, unless the message is the contract.
- Use `t.TempDir()` and real files; use `httptest` servers for HTTP clients.
- Use `-race` for anything with goroutines or shared state, and channels or fake clocks instead of `time.Sleep` for ordering.

## Evidence and Review

Read every `if err != nil` branch as carefully as the happy path. Check that each goroutine has an owner and a way to stop. Check that zero values of new types are safe. `go vet` and the compiler prove syntax and some misuse; they do not prove error context, cancellation, or exhaustiveness.
