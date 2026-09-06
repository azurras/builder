# Registration

Maintain `docs/spokes/repos.md` with one section per repository. Re-registering the same slug updates that section. Record factual local path, remote, default branch, purpose, status, guardrails, and notes; preserve other entries.

## Workflow

1. Discover the active Builder root with `git rev-parse --show-toplevel` and verify origin with `git remote get-url origin`. Supported authoritative roots are `C:\Users\Christopher\Developer\builder` on Windows and `/Users/cbell/Developer/builder` on macOS; origin is `https://github.com/azurras/builder.git`. Do not require the macOS path on Windows.
2. Inspect the target repository read-only to establish its actual local path, remote, and default branch. Record access gaps rather than inventing values. Registration does not authorize source changes or deployment.
3. Record repository purpose and guardrails, including branch policy, validation, ownership, and direct-push rules.
4. Run the helper with the verified hub root explicitly. Review only the intended registry section change, update hub indexes, and validate hub state.
5. Use the [phase finalizer](../../maintain-builder-hub/references/phase-finalization.md) with the registry and intended related files; routine registration does not require a new continuity artifact.

## PowerShell Example

```powershell
$builderRoot = git rev-parse --show-toplevel
python .agents/skills/manage-spoke-repositories/scripts/manage_spoke_repositories.py register --root $builderRoot --name 'Example Repo' --path 'A:\Projects\example' --remote 'https://github.com/org/example.git' --default-branch main --purpose 'Describe the repository responsibility'
```

Replace the example values with inspected facts. On macOS, invoke the same helper with the discovered root and native paths; the helper is platform-independent.
