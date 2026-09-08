# Repository Inspection

Read historical context selectively; reverify path, origin, branch and relevant guardrails before execution.

Run:
python .agents/skills/complete-builder-work/scripts/manage_spoke_repositories.py inspect --path <verified-repository>

Omitting the mode also inspects. It is read-only: no fetch, source modification, memory write or deployment authority. Git failures remain explicit and nonzero.

For authorized persistence use snapshot --path <verified-repository> --root . --project <project>. The helper appends to today's dated memory, skips an identical latest snapshot within that day, and records inspection errors while returning failure. A new date gets its own record. No separate registry or state file is created.
