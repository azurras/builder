# Rust

Follow the repository's Rust edition, `rustfmt`, `clippy` configuration, and error-handling crates. This guide applies the shared rules and the [principles](jane-street-principles.md) to Rust. Rust is the mainstream language closest to OCaml: enums with data, exhaustive `match`, `Option` and `Result`, and immutability by default are built in. The style's job in Rust is mostly to avoid escaping those guarantees: no `unwrap` on fallible input, no wildcard arms on domain enums, no newtype-free primitives where swaps are dangerous, and no locks held across `.await`.

The Rust examples in this guide were reviewed but not compiled in the Builder environment. Compile and test them with the target repository's toolchain before relying on them.

## Idioms at a Glance

| Prefer | Avoid | Why |
|---|---|---|
| `Result<T, E>` with `?` and a domain error type | `unwrap()` and `expect()` on input, I/O, or parsing | Failures stay values the caller handles |
| Error enums that implement `std::error::Error` and expose `source()` | `String` errors or `Box<dyn Error>` in library APIs | Callers can match on outcomes and see causes |
| `expect("reason the invariant holds")` only for true invariants | Bare `unwrap()` | The panic message explains the broken assumption |
| Enums with data for states | Structs with several `bool` and `Option` fields | Illegal combinations cannot be built |
| `match` that names every variant | `_ =>` arms on domain enums | Adding a variant fails compilation where it matters |
| Newtypes (`struct UserId(u64)`) with `TryFrom` for validation | Bare `u64` and `String` for IDs, emails, and amounts | Swaps fail to compile; only validated values exist |
| Private fields and constructor functions | `pub` fields on types with invariants | Outside code cannot break the invariant |
| Borrowed parameters (`&str`, `&[T]`) for read-only input | Taking `String` or `Vec<T>` and cloning to satisfy the borrow checker | Ownership matches intent; fewer copies |
| Iterators with named intermediate bindings | Index loops with manual bounds | No off-by-one errors; the data flow is visible |
| `Drop` and scoped guards for cleanup | Manual cleanup calls on each path | Cleanup runs on every exit, including `?` |
| Short lock scopes; no guard held across `.await` | Holding a `Mutex` guard while awaiting I/O | Avoids deadlocks and non-`Send` futures |
| `#[must_use]` on results callers must not ignore | Silently droppable important values | The compiler warns when the value is ignored |
| `unsafe` blocks with a `// SAFETY:` comment stating the invariant | Unexplained `unsafe` | Reviewers can check the claimed invariant |

## Smells Reviewers Flag

- `unwrap()` outside tests and examples; `expect("")` with no explanation.
- `_ =>` on an enum the crate owns.
- `.clone()` added to make the borrow checker quiet, with no reasoning about ownership.
- `pub` fields on a type whose constructor validates.
- Functions that take `String` but only read it.
- `Rc<RefCell<T>>` or `Arc<Mutex<T>>` spread across the codebase instead of a clear owner.
- A `MutexGuard` alive across an `.await`.
- `as` casts between numeric types that can truncate or wrap silently (use `try_from`).
- `Box<dyn Error>` returned from a library's public API.
- `#[allow(clippy::...)]` with no reason.

## Good and Bad Pairs

### Parse with `Result`, Not `unwrap`

Bad (Rust fragment):

```rust
fn load_port(config_text: &str) -> u16 {
    config_text.trim().parse().unwrap()
}
```

Bad input crashes the process with a message that does not say which setting was wrong, and reserved ports are accepted.

Good (Rust example):

```rust
use std::fmt;
use std::num::ParseIntError;

#[derive(Debug)]
pub enum PortParseError {
    NotANumber(ParseIntError),
    Reserved(u16),
}

impl fmt::Display for PortParseError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            PortParseError::NotANumber(_) => write!(formatter, "port is not a number from 0 to 65535"),
            PortParseError::Reserved(port_number) => {
                write!(formatter, "port {port_number} is reserved; use 1024 or higher")
            }
        }
    }
}

impl std::error::Error for PortParseError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            PortParseError::NotANumber(cause) => Some(cause),
            PortParseError::Reserved(_) => None,
        }
    }
}

pub fn parse_port_from(port_text: &str) -> Result<u16, PortParseError> {
    let port_number: u16 = port_text.trim().parse().map_err(PortParseError::NotANumber)?;
    if port_number < 1024 {
        return Err(PortParseError::Reserved(port_number));
    }
    Ok(port_number)
}
```

Each failure is a variant the caller can match, the parse error is kept as the source, and the message says what a valid value looks like. Crates such as `thiserror` generate the `Display` and `Error` code; use them if the repository does.

Check: `"8080"` parses; `"80"` is `Reserved(80)`; `"http"` and `"70000"` are `NotANumber` with a source.

### Newtypes Make Validated Values Distinct

Bad (Rust fragment):

```rust
fn send_welcome(user_id: u64, account_id: u64, email: String) { ... }
```

`send_welcome(account_id, user_id, raw_input)` compiles, and the email was never checked.

Good (Rust fragment):

```rust
pub struct EmailAddress(String);

#[derive(Debug)]
pub struct InvalidEmailAddress {
    pub rejected_value: String,
}

impl TryFrom<String> for EmailAddress {
    type Error = InvalidEmailAddress;

    fn try_from(raw_email: String) -> Result<Self, Self::Error> {
        let trimmed_email = raw_email.trim();
        let has_local_and_domain = trimmed_email
            .split_once('@')
            .is_some_and(|(local_part, domain)| !local_part.is_empty() && domain.contains('.'));
        if has_local_and_domain {
            Ok(EmailAddress(trimmed_email.to_owned()))
        } else {
            Err(InvalidEmailAddress { rejected_value: raw_email })
        }
    }
}

impl EmailAddress {
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

fn send_welcome_to(user_id: UserId, email_address: &EmailAddress) { ... }
```

The tuple field is private outside its module, so the only way to get an `EmailAddress` is through validation. `UserId` and `AccountId` newtypes make the swap a compile error. The email rule here is deliberately simple; use the real requirement.

### Enums Instead of Flag Combinations

Bad (Rust fragment):

```rust
struct Download {
    is_complete: bool,
    is_failed: bool,
    bytes_received: u64,
    error_message: Option<String>,
}
```

`is_complete` and `is_failed` can both be true, and `error_message` can be set on a successful download.

Good (Rust fragment):

```rust
enum Download {
    InProgress { bytes_received: u64, total_bytes: Option<u64> },
    Complete { file_path: PathBuf },
    Failed { reason: DownloadFailure },
}

fn status_line_for(download: &Download) -> String {
    match download {
        Download::InProgress { bytes_received, total_bytes: Some(total_bytes) } => {
            format!("{bytes_received} of {total_bytes} bytes")
        }
        Download::InProgress { bytes_received, total_bytes: None } => format!("{bytes_received} bytes"),
        Download::Complete { file_path } => format!("Saved to {}", file_path.display()),
        Download::Failed { reason } => format!("Failed: {reason}"),
    }
}
```

Each variant holds only its own data, and the `match` names every case. Adding `Paused` stops compilation here until someone decides what to show.

### Do Not Hold a Lock Across `.await`

Bad (async Rust fragment):

```rust
let mut cached_prices = price_cache.lock().unwrap();
let fresh_price = price_client.fetch_price(&symbol).await?;
cached_prices.insert(symbol, fresh_price);
```

Every other task that needs the cache waits for a network call. With `std::sync::Mutex`, the future is not `Send` and cannot be spawned on a multi-threaded runtime.

Good (async Rust fragment):

```rust
let fresh_price = price_client.fetch_price(&symbol).await?;
{
    let mut cached_prices = price_cache.lock().expect("price cache mutex poisoned by an earlier panic");
    cached_prices.insert(symbol, fresh_price);
}
```

The remote call happens without the lock, and the guard lives only for the insert. The `expect` message explains why a panic here means an earlier bug.

### Borrow What You Only Read

Bad (Rust fragment):

```rust
fn greeting(name: String) -> String {
    format!("Hello, {name}")
}

let message = greeting(user.display_name.clone());
```

The function only reads `name`, so the caller is forced to clone.

Good (Rust fragment):

```rust
fn greeting_for(display_name: &str) -> String {
    format!("Hello, {display_name}")
}

let greeting_message = greeting_for(&user.display_name);
```

The signature says the function borrows, and the call reads as a sentence.

## Implementation Recipe

1. Inspect the edition, MSRV, `clippy` lints, and the repository's error crates. Follow Rust naming (`snake_case`, `UpperCamelCase` types); the house sentence rule applies to functions, parameters, and calls.
2. Model states as enums and validated values as newtypes with private fields and `TryFrom` or `new` constructors.
3. Return `Result` from fallible functions; give libraries typed errors with `source()`, and keep `unwrap` for tests and proven invariants with `expect` messages.
4. Choose ownership deliberately: borrow for reading, take ownership to store or consume, and avoid clones that hide a design problem.
5. In async code, own spawned tasks (`JoinSet`, join handles), propagate cancellation, and keep lock scopes free of `.await`.
6. Run `cargo fmt`, `cargo clippy` with the repository's settings, and `cargo test`.

## Testing in Rust

- Put unit tests in `#[cfg(test)]` modules next to the code and integration tests under `tests/`.
- Match on error variants with `assert!(matches!(result, Err(PortParseError::Reserved(80))))`.
- Use `insta` or similar snapshot tools when the repository does, and read every snapshot diff.
- Use property tests (`proptest`) for parsers and round trips when the input space is large.

## Evidence and Review

The compiler proves memory safety and exhaustiveness; it does not prove that errors carry context, that `expect` messages are true, or that a newtype's constructor validates the real rule. Review those by reading the code and testing the rejected inputs.
