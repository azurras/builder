# Repository Inspection

Read historical context selectively; reverify path, origin, branch and relevant guardrails before execution.

Registered spokes come from spokes.json at the Builder root. Run from the Builder root:
python .agents/skills/deliver-change/scripts/manage_spoke_repositories.py list
python .agents/skills/deliver-change/scripts/manage_spoke_repositories.py locate --spoke <slug>
python .agents/skills/deliver-change/scripts/manage_spoke_repositories.py inspect --spoke <slug>

locate prints the resolved path and its source (spokes.local.json, BUILDER_SPOKES_ROOT, or the folder beside Builder) and fails when the checkout is missing or its origin differs from the registry. When a spoke is missing on this machine, clone --spoke <slug> clones its default branch to the resolved path; it refuses an existing path. For a repository that is not registered, use --path <verified-repository> instead of --spoke. To add a spoke, run register --spoke <slug> --name <name> --repository <remote> --description <text> [--default-branch <branch>]; it appends a validated entry to spokes.json and refuses duplicate slugs (including `builder` and standalone project slugs), repositories or checkout folders and local paths.

inspect is the default mode. It is read-only: no fetch, source modification, memory write or deployment authority. Git failures and registry mismatches remain explicit and nonzero.

For authorized persistence use snapshot --spoke <slug> --root . (the memory project defaults to the spoke slug) or snapshot --path <verified-repository> --root . --project <project>, where the project must be active in spokes.json; snapshot refuses any other before inspecting. The helper appends to today's dated memory, skips an identical latest snapshot within that day, and records inspection errors while returning failure. A new date gets its own record. No per-spoke state file is created.
