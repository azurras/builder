# Deepen Chris Street Style Examples and Language Guides

## Plan Format
task-contract-v1

## Document Status
ready-for-execution

## Objective
Make write-chris-street-style-code explain what Jane Street-inspired style means in depth, give many more paired good and bad examples, and give each supported language its own deep guide of idioms, smells, and good/bad pairs, while the shared rules stay language-neutral.

## Goals
- Add a principles reference that explains each Jane Street-derived principle: what it means, why it matters, how it looks in any language, the smells that violate it, and a short good/bad pair.
- Grow the cross-language example catalogue from 8 to roughly 20 pairs covering boolean blindness, illegal states, exhaustiveness, stringly-typed data, units, swappable IDs, guard clauses, clever expressions, hidden time/globals, swallowed failures, lying comments, retries/idempotency, stale async state, and test evidence; add a catalogue index.
- Deepen the Java, JavaScript/TypeScript, and Python guides with idiom tables, smell checklists, and several good/bad pairs each, including Spring and TypeScript specifics used by the christopherbell-dev spoke.
- Add dedicated guides for Go, Rust, C#, OCaml, SQL (including document stores), and Shell/PowerShell, each with idioms, smells, and good/bad pairs.
- Keep SKILL.md concise: route to every new reference, add a short summary of the style, and keep rules, modes, and authority limits unchanged.

## Inputs
- User request 2026-10-04: more good/bad examples, more verbosity on Jane Street style, broad across languages but deep within each.
- Inspected all current skill files at main 7134e7f: SKILL.md, agents/openai.yaml, and the ten references.
- Prior plan [Explicit Chris Street coding standard](2026-10-04-explicit-chris-street-coding-standard.md) and the christopherbell-dev style audit report (Java/Spring, MongoDB, JavaScript, PowerShell/Pester).
- Verified sources: Effective ML Revisited (Yaron Minsky, 2011) headings: use uniform interfaces, make illegal states unrepresentable, code for exhaustiveness, open few modules, make common errors obvious; "What if writing tests was a joyful experience?" (James Somers, 2023) on expect tests; plus the four sources already cited.
- Local toolchains: Python 3.12, Node 24, JDK 25, bash, PowerShell 7. Go, Rust, .NET, and OCaml are not installed.

## Branch
Builder main through commit-push-builder-main under the existing publication policy; publish this plan before implementation and the verified skill afterwards.

## Non-Goals
Changing the ten mandatory rules, modes, authority limits, or skill name; application changes; installing toolchains; claiming an official Jane Street style manual.

## Assumptions
Language guides adapt shared rules and never contradict them. Examples are original. Target repositories' versions and formatters still govern.

## Open Questions
None. Kotlin, Swift, C/C++, Ruby, and PHP stay in the adaptation map; dedicated guides can follow on request.

## Task Breakdown

### Task 1 - Add the principles reference and route it
Dependencies: None; inspection complete.
Files: .agents/skills/write-chris-street-style-code/SKILL.md; new references/jane-street-principles.md beside the existing references; references/sources-and-adaptation.md.
Symbols: SKILL.md intro and Required Reference Selection table; principle sections; Primary Sources list.
Inspection: Read SKILL.md routing table and every reference at 7134e7f; verified source headings listed in Inputs.
Required skill: write-chris-street-style-code before writing code-bearing examples.
Behavior: A reader learns what each principle means, why, how to apply it in any language, and how to spot a violation.
Invariants: Attribute only verified source claims; label house additions as house rules; keep SKILL.md concise and mandatory rules unchanged.
Boundary/API: Skill name, frontmatter, and implicit invocation unchanged; every new reference reachable from a routing row.
Effects and failures: Documentation only.
Tests and evidence: Link/anchor check, frontmatter check, SkillDiscoveryTests, semantic review.
Verification: Scratch link checker over the skill folder; python -B .agents/tests/test_skill_consolidation.py SkillDiscoveryTests.

### Task 2 - Expand the cross-language example catalogue
Dependencies: Task 1 defines principle names that examples link to.
Files: references/good-and-bad-examples.md.
Symbols: Catalogue index; existing sections 1-8 kept with anchors; new numbered sections.
Inspection: Read the current eight examples and their inbound anchor links from java.md, javascript.md, python.md.
Required skill: write-chris-street-style-code.
Behavior: Each pair names the defect, the counterexample, the correction, and the check that proves it.
Invariants: Existing anchors that other files link to stay valid; complete examples are labeled and runnable; fragments and pseudocode are labeled.
Boundary/API: Language-specific pairs live in language guides; this file stays cross-language.
Effects and failures: Documentation only; example checks run in the scratchpad.
Tests and evidence: Run every example labeled complete in Python, Node, or Java with valid and invalid inputs.
Verification: Native runs in scratch files; anchor check.

### Task 3 - Deepen the Java, JavaScript/TypeScript, and Python guides
Dependencies: Task 2 for cross-links.
Files: references/java.md; references/javascript.md; references/python.md.
Symbols: Idioms table, smells checklist, good/bad pairs, recipe, evidence sections.
Inspection: Read the three current guides; style audit report shows Spring, Mongo, exception-cause, and interruption concerns in the spoke.
Required skill: write-chris-street-style-code.
Behavior: Each guide gives concrete native good and bad code for naming, state, validation, errors, resources, concurrency, testing, and framework use.
Invariants: Respect supported versions; mark version-dependent features; preserve existing recipe content.
Boundary/API: Unchanged file names so routing stays stable.
Effects and failures: Documentation only.
Tests and evidence: Compile Java examples with javac 25; run JavaScript with Node 24 and TypeScript via Node type stripping (syntax only, not type-checked); run Python examples.
Verification: Native runs in scratch files.

### Task 4 - Add Go, Rust, C#, OCaml, SQL, and Shell/PowerShell guides
Dependencies: Task 1 routing pattern.
Files: new references/go.md, rust.md, csharp.md, ocaml.md, sql.md, shell.md; update references/language-adaptation.md and references/templates-and-configuration.md to point at them.
Symbols: Per-guide idioms, smells, recipe, good/bad pairs; adaptation mechanism map rows.
Inspection: Existing java.md structure is the pattern; templates guide holds current shell and SQL fragments.
Required skill: write-chris-street-style-code.
Behavior: Readers of those languages get the same depth as Java/Python.
Invariants: Examples whose compiler is unavailable are labeled as not compiled here; shell and SQL examples are executed.
Boundary/API: New rows in the SKILL.md routing table.
Effects and failures: Documentation only.
Tests and evidence: Run bash and PowerShell examples; run SQL through Python sqlite3; review Go/Rust/C#/OCaml carefully and disclose they were not compiled.
Verification: Native runs; link check.

### Task 5 - Validate and publish
Dependencies: Tasks 1-4.
Files: changed skill files; docs/session-memory/2026-10-04-builder.md; generated indexes; this plan's status.
Symbols: Validation section; dated entry.
Inspection: Final diff, staged paths, origin/main before publication.
Behavior: Reviewed skill and delivery record are on origin main.
Invariants: Preserve unrelated changes; never force push.
Boundary/API: Builder memory, hub, and commit helpers.
Effects and failures: Commit and push; a failed push keeps the commit for push-only recovery.
Tests and evidence: Full checks above, hub refresh, diff check, remote readback.
Verification: python .agents/skills/maintain-builder-hub/scripts/maintain_builder_hub.py refresh --root .; git diff --check; publisher dry run and publish; git ls-remote origin refs/heads/main.

## Code Changes
Skill documentation and original code-bearing examples only.

## Files and Modules
The write-chris-street-style-code folder; this plan; dated Builder memory; generated indexes.

## Unit Testing
Reuse SkillDiscoveryTests; native example runs exercise valid and rejected inputs. No phrase-matching tests.

## Local Testing
Runtime verification does not apply: Builder has no runnable application and this change is instructions plus isolated examples. Examples run in the scratchpad with native toolchains.

## Validation
Pending implementation.

## Rollback or Recovery
Revert the publication commit through a reviewed follow-up commit; retain a local commit if push fails and retry with push-only.

## Risks
Longer references cost context: keep SKILL.md short and load only the guides in scope. Uncompiled Go/Rust/C#/OCaml examples could contain errors: keep them small, review them, and disclose. Over-prescription: guides defer to repository conventions.

## Completion Criteria
- Principles reference, about 20 cross-language pairs, three deepened guides, and six new guides exist and are routed.
- All locally runnable examples pass their checks; unverifiable ones are labeled.
- Links, anchors, frontmatter, SkillDiscoveryTests, hub check, and diff check pass.
- Plan, skill, and memory are pushed and remote readback matches.
