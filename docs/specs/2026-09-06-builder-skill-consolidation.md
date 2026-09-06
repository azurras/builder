# Builder Skill Consolidation

## Document Status
ready-for-execution

## Purpose
Implement the user's approved reduction from 22 discoverable Builder skills to 11, informed by the repository's session history. Preserve operational safeguards and durable evidence while simplifying routing and shared mechanics.

## Requirements
- Six consolidated skills: complete-builder-work (delivery/closure), plan-builder-work (spec/plan/review/validate/optional decision), coordinate-builder-work (start/dispatch/update/close), record-runtime-verification (report/validate), manage-spoke-repositories (register/inspect/snapshot), maintain-builder-hub (check/refresh).
- Retain commit-push-builder-main, verify-local-spring-app, write-jane-street-style-code, review-spoke-work, and save-session-memory as independent skills.
- Retire the old discoverable entrypoints and metadata for the merged capabilities, including standalone save-decision-record. Preserve existing Python CLI paths and the decision template. Record old-to-new routing in a migration reference; preserve historical artifacts.
- Reuse shared dated-Markdown behavior across duplicated save helpers. Preserve file locations, duplicate/overwrite behavior, plan/report validation, and session-memory append semantics.
- Repository inspection is read-only by default in the consolidated interface. Explicit snapshots persist only meaningful state changes and report Git failures rather than treating them as clean.
- Centralize phase finalization: write intended artifacts, refresh indexes, validate, commit only selected files. Preserve separate spec, plan, applicable runtime report, and continuity checkpoints; maintenance does not create its own memory/commit loop.
- Keep runtime evidence distinct from automated tests, production deployment within existing authority, and closure readback before claiming completion.
- Keep independent review and continuity; prefer links to primary evidence over repeating full narratives.
- Update AGENTS.md, README, current skill references, metadata, validators, and regression tests together. Do not modify Superpowers or spoke repositories.

## Evidence and Rationale
The review found 83 session records, 53 runtime reports, 35 spoke reviews, and no decision artifacts. Session history explicitly records phase-commit and runtime-evidence requirements. Five artifact helpers have the same parsed structure after string normalization. The approved design combines discovery entrypoints while retaining specialized references and commands.

## Validation Plan
Characterize legacy artifact commands in temporary directories; test new snapshot read-only/error/idempotency behavior with local Git repositories; check maintenance modes and skill-reference discovery; run full Builder tests, skill metadata validation, hub validation, and independent scenarios before publishing.

## Open Questions
None. The user approved the preceding consolidation proposal and requested implementation.
