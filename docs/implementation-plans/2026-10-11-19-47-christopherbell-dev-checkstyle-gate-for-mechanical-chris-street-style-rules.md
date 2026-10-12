# Checkstyle Gate for Mechanical Chris Street Style Rules

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> CI enforces the mechanical Chris Street Style rules on Java code that has already been migrated, so migrated code cannot regress and review can focus on judgment calls.

## Background
The [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md) applied the same mechanical edits to every slice with scratchpad regex scripts:
- single-line `if` bodies became blocks;
- fully qualified names became imports;
- one-line method bodies were split.

Nothing stops new code from reintroducing them. The user asked for item 5: lint rules in the spoke. The [Builder helper plan](2026-10-11-19-10-builder-deploy-aware-merges-and-shared-verification-helpers.md) recorded the matching decisions in the Java guide's Settled Decisions table.

## Goals
- `./gradlew check` runs Checkstyle on main and test Java sources with only the mechanical rules (AC-1).
- Packages whose migration slice has not merged are listed in one suppressions file, and every other file passes (AC-2).
- The migration's remaining slices delete their suppression lines as they land (AC-3).

## Non-Goals

| Not doing | Why |
|---|---|
| A formatter such as Spotless that rewrites files | It would reformat every file at once and conflict with the open migration slices |
| Rules for naming, `Optional`, catch names or status sets | These are judgment calls for review |
| Linting JavaScript, PowerShell or Kotlin | The Java rules are where the migration spent its mechanical effort; the other languages have their own slices |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | `config/checkstyle/checkstyle.xml` enables `NeedBraces` (if, else, for, while, do), `OneStatementPerLine`, `AvoidStarImport`, `RedundantImport`, `UnusedImports` and a fully-qualified-name rule. The Gradle `checkstyle` plugin runs it for `website` and `cbell-lib` main and test sources as part of `check`, and dependency verification metadata covers the new artifacts |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass with suppressions limited to whole packages or files that are named in the umbrella ledger as not yet migrated |
| AC-3 | The umbrella plan's Design tells later slices to remove their suppression lines, and this plan's Implementation Log lists the suppressed set |

## Inputs
- **Request:** "Fix 2, 3, 4, 5, 7", item 5.
- **Inspected at spoke `280b3c61`:**
  - The root and `website` Gradle builds. There is no existing lint.
  - `gradle/verification-metadata.xml` (verify-metadata true).
  - The CI workflows.
  - The umbrella ledger rows 19 to 25.

## Branch
`claude/style-lint-20261011` from spoke `origin/main` `a18b81b2`.

## Assumptions
None.

## Open Questions
None.

## Design
- **Plugin:** the root build applies Gradle's built-in `checkstyle` plugin to every Java subproject. It pins a `toolVersion` whose grammar covers Java 25, sets `maxWarnings = 0`, and takes its configuration from `config/checkstyle` at the root.
- **Fully qualified names:** a `RegexpSinglelineJava` rule flags `java.`, `javax.` or `jakarta.` followed by a package and a type outside `import` and `package` lines, ignoring comments.
- **Suppressions:** `suppressions.xml` lists files by path pattern. Only not-yet-migrated areas qualify, and the measured violations decide the list.
- **Verification metadata:** regenerated with `--write-verification-metadata sha256` for the Checkstyle configurations only. The added components are reviewed as part of this change.

## Expected Changes

| File | Change |
|---|---|
| `build.gradle.kts` | Checkstyle plugin and settings for Java subprojects |
| `config/checkstyle/checkstyle.xml`, `config/checkstyle/suppressions.xml` | New |
| `gradle/verification-metadata.xml` | Checkstyle artifacts |
| `README.md` | Style check section |
| Migrated sources with violations | Mechanical fixes only, when the count is small |

## Task Breakdown

### Task 1 - Checkstyle gate

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | As in Expected Changes |
| **Symbols** | Gradle `checkstyle` extension |
| **Inspection** | Inputs |
| **Behavior** | `check` fails on a mechanical style violation outside suppressed paths |
| **Invariants** | No production behavior changes |
| **Boundary/API** | Build only |
| **Effects and failures** | Violations fail the build with file and line |
| **Tests and evidence** | A deliberate violation in a scratch copy fails the task; the clean tree passes |
| **Verification** | `.\ops\local\Invoke-Gradle.ps1 :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

**Runtime proof not applicable:** the change adds a build-time lint and mechanical source edits without behavior change; the full check, including every test suite, is the proof.

| AC | Check |
|---|---|
| AC-1 | `checkstyleMain` and `checkstyleTest` run under `check`; a planted violation fails |
| AC-2 | Full check |
| AC-3 | Plan and ledger review |

## Rollback or Recovery
Revert the squash-merge commit.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Checkstyle cannot parse Java 25 syntax | Medium | Pin the newest compatible version and measure before suppressing; record the version in the log |
| Suppressions grow into a permanent escape hatch | Low | Only not-yet-migrated paths qualify, and each later slice deletes its lines |

## Implementation Log

### 2026-10-11 - Migrated slices had mechanical misses

- **Change:** The first Checkstyle 14.3.0 run found 875 violations. Of these, 321 were in slices already marked done: music, admin, account, post, configuration, sitemonitor, shared-folder audit and web, and others. The fixes cover every file outside the suppressed slices. NeedBraces and fully qualified names were fixed by a script that edits only the reported lines, bottom-up. One-statement-per-line and unused imports were fixed by a second script, and star imports were expanded to the names `javap` and the sources show each file uses.
- **Reason:** The migration's brace regex handled only single-line `return` and `throw` bodies, and missed `continue`, `break`, assignments, next-line bodies and loops. The gate exists to catch exactly this.
- **Impact:** Expected Changes "Migrated sources with violations" now spans about 110 files instead of a few. The suppressed set is recycle, media, upload, service and package-level shared-folder tests, fs (19d to 19h), architecture tests (20) and `cbell-lib` (21).

### 2026-10-11 - Survive was outside the ledger

- **Change:** The `survive` package and its tests are made to conform here.
- **Reason:** `survive` (PRs #1489 to #1491) arrived after the umbrella plan counted packages, so no ledger row covers it, yet it is first-party code under the "all code" goal.
- **Impact:** The umbrella ledger gains a note that `survive` conformed under this plan.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
