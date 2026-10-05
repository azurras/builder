# OCaml

OCaml is the language Jane Street's public writing describes, so this guide is the reference point for how the principles look when the language supports them fully. Follow the repository's compiler version, `dune` setup, `ocamlformat` profile, and standard library choice (Jane Street's `Base` and `Core`, or the OCaml standard library). Read the [principles](jane-street-principles.md) first; this guide shows them in native form.

The OCaml examples in this guide were reviewed but not compiled in the Builder environment. They assume `Core` unless they say otherwise. Compile and test them with the target repository's toolchain before relying on them.

## Idioms at a Glance

| Prefer | Avoid | Why |
|---|---|---|
| Variants for states, records for data that always coexists | `bool` fields and `option` fields that only make sense together | Illegal states are unrepresentable |
| `match` that names every constructor, with warnings as errors | `_ ->` on domain variants | New constructors fail compilation where they matter |
| An `.mli` per module with an abstract `type t` | Exposing the representation | Invariants live behind `create` and cannot be bypassed |
| `create` returning `t Or_error.t` and `create_exn` for trusted input | Constructors that raise with no `_exn` in the name | The call site shows which operations can raise |
| Labeled arguments (`~source ~destination`) for same-type parameters | Several positional arguments of the same type | Call sites state roles; order does not matter |
| `Or_error.t` or a specific error variant with context | `failwith "error"` and exceptions for expected outcomes | Errors are values with information callers can use |
| `open Core` at most, then qualified names (`String.split`, `Time_ns.now`) | Opening many modules | Readers can tell where a name comes from |
| Type-specific comparison (`Int.equal`, `[@@deriving compare, equal]`) | Polymorphic `=` and `compare` on abstract or functional values | Polymorphic compare can raise or compare representations |
| Expect tests (`let%expect_test`) for behavior | Long chains of boolean assertions | Output shows the behavior; diffs are reviewable |
| Immutable values; `ref` and mutable fields owned by one module | Global mutable state | State changes have one owner |
| `Time_ns.Span.t` and other unit-bearing types | `int` or `float` for durations | Units are in the type |

## Smells Reviewers Flag

- `_ ->` in a match on a variant the codebase owns.
- A record with `is_*` booleans and `option` fields whose validity depends on each other.
- `type t = { ... }` exposed in an `.mli` when the module has invariants.
- A function that raises without `_exn` in its name.
- `failwith` or `assert false` on paths that real input can reach.
- Polymorphic `=` or `compare` on types that are abstract, contain closures, or have a custom equality.
- `open` of several modules at the top of a file.
- Unlabeled `int -> int -> int` or `string -> string -> unit` signatures where the arguments have different roles.
- `Lazy` or top-level effects that run at module initialization.

## Good and Bad Pairs

### Variants Instead of Flags

Bad (OCaml fragment):

```ocaml
type connection =
  { is_connected : bool
  ; session_id : string option
  ; last_error : Error.t option
  }
```

Nothing stops `{ is_connected = true; session_id = None; last_error = Some error }`.

Good (OCaml fragment):

```ocaml
type connection =
  | Connecting of { attempt_number : int }
  | Connected of { session_id : Session_id.t }
  | Disconnected of { reason : Error.t }
```

Each constructor holds only the data that exists in that state. This is the standard example of making illegal states unrepresentable.

### Name Every Case

Bad (OCaml fragment):

```ocaml
let customer_label (status : Payment_status.t) =
  match status with
  | Pending -> "Awaiting payment"
  | Paid -> "Paid"
  | _ -> ""
;;
```

`Refunded` already renders blank, and any new constructor will too.

Good (OCaml fragment):

```ocaml
let customer_label (status : Payment_status.t) =
  match status with
  | Pending -> "Awaiting payment"
  | Paid -> "Paid"
  | Refunded -> "Refunded"
;;
```

With warnings treated as errors, adding `Disputed` makes this a compile error until someone writes its label.

### Abstract Types Guard Invariants

Bad (OCaml fragment, `time_window.mli`):

```ocaml
type t = { starts_at : Time_ns.t; ends_at : Time_ns.t }
```

Callers can build a reversed window directly.

Good (OCaml fragment, `time_window.mli`):

```ocaml
type t

val create : starts_at:Time_ns.t -> ends_at:Time_ns.t -> t Or_error.t
val create_exn : starts_at:Time_ns.t -> ends_at:Time_ns.t -> t
val includes : t -> Time_ns.t -> bool
```

The representation is hidden, so `create` is the only way to make a `t`. The safe version returns `Or_error.t`; the raising version says `_exn`. Labels make the endpoints impossible to swap at the call site: `Time_window.create ~starts_at:market_open ~ends_at:market_close`.

### Labels for Same-Type Arguments

Bad (OCaml fragment):

```ocaml
val transfer : Account_id.t -> Account_id.t -> Money.t -> unit Or_error.t
```

`transfer savings checking amount` and `transfer checking savings amount` both type-check.

Good (OCaml fragment):

```ocaml
val transfer
  :  source:Account_id.t
  -> destination:Account_id.t
  -> amount:Money.t
  -> unit Or_error.t
```

The call `transfer ~source:savings ~destination:checking ~amount` reads as a sentence and cannot be silently reversed.

### Errors Carry Context

Bad (OCaml fragment):

```ocaml
let load_config path =
  try Some (Sexp.load_sexp path |> Config.t_of_sexp) with
  | _ -> None
;;
```

A missing file, a parse error, and a bug in `t_of_sexp` all become `None`.

Good (OCaml fragment):

```ocaml
let load_config ~path =
  Or_error.try_with (fun () -> Sexp.load_sexp path |> Config.t_of_sexp)
  |> Or_error.tag_s ~tag:[%message "Failed to load config" (path : string)]
;;
```

The result is an `Or_error.t` whose error keeps the original exception and adds the path. Callers decide whether a failure is fatal.

### Expect Tests Show Behavior

Bad (OCaml fragment):

```ocaml
let%test _ = String.is_substring (Invoice.render_summary lines) ~substring:"Total"
```

Good (OCaml fragment):

```ocaml
let%expect_test "summary lists each line and the total" =
  print_endline (Invoice.render_summary [ widget_line; gadget_line ]);
  [%expect
    {|
    Widget x2: 5.00
    Gadget x1: 10.00
    Total: 15.00
    |}]
;;
```

The full output is in the test. When behavior changes, the test runner shows a diff that the author accepts only after reading it.

## Implementation Recipe

1. Inspect the compiler version, `dune` flags, warnings-as-errors settings, `ocamlformat` profile, and whether the code uses `Base`, `Core`, or the standard library.
2. Design the `.mli` first: abstract types, labeled arguments, and `Or_error.t` or `_exn` variants.
3. Model states with variants and inline records; avoid `_` in matches on owned variants.
4. Keep effects in `Async` or `Lwt` at the boundary; pass time and randomness in where rules depend on them.
5. Write expect tests for observable behavior and read every diff before promoting it.
6. Build with `dune build @check` and run `dune runtest`.

## Evidence and Review

The type checker proves exhaustiveness and labels; it does not prove that error context is useful, that `_exn` functions are only used on trusted input, or that an expect-test diff was read. Review those directly.
