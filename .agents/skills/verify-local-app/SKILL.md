---
name: verify-local-app
description: Use when verifying any application change locally before creating a pull request, in any language or framework, or when performing authorized runtime verification or deployment.
---

# Verify Local App

Run the application on the local machine and exercise the candidate before creating a pull request, including a draft PR. This applies to any change in an application repository, including code, configuration, dependencies, UI and documentation. Use the repository's native tools and executable entrypoint, regardless of language or framework. Passing unit tests, a build, CI, a remote preview or an already-running older revision do not replace local candidate execution.

For standalone documentation, skills or other work with no runnable application, record the concrete reason application execution does not apply and run appropriate native checks before publication. For a library, exercise the change through a runnable local consumer or integration harness.

Choose verification-only or verification-plus-deployment from existing task authority. Local testing does not authorize production deployment; do not ask again when deployment is already authorized. Planning and review-only requests remain within their scope.

## Preflight Before Tests or Startup

1. Read repository instructions and relevant build, run, test and deployment configuration. Inspect Git state and preserve unrelated work. Identify the candidate revision, required runtime/dependencies, local commands, production processes and resources.
2. Before database-backed tests or startup, verify the effective target, environment overrides and access permissions. Use an isolated test database and an isolated role where the engine supports roles; for embedded databases, verify the owned test-file path and filesystem access. Prevent the candidate from accessing production data. Builder-coordinated MongoDB/PostgreSQL work uses database `test` only, with a PostgreSQL test role isolated from production. Port isolation does not imply data isolation. Never test against live development, staging or production data.
3. If isolation cannot be verified, stop dependent execution and resolve configuration. Treat a run as database-free only when inspected code/configuration proves no connection occurs. Record sanitized evidence without credentials.
4. Never modify database data directly, even in the isolated test database: no shell, client, script, migration or ORM writes outside the application. Perform every add, update and delete through the application's endpoints. When no endpoint covers the needed fixture or cleanup, you may add temporary seed and delete endpoints restricted to the test configuration; remove them before creating the PR and record their use. Direct reads to inspect results are allowed.
5. Isolate enabled jobs, queues, external integrations, files and storage from live state. Use a free non-production port only for applications that listen on a port; use isolated inputs, directories, queues or device settings for other runtimes. Keep production running. Resolve missing dependencies through the supported setup before running the candidate.

## Verify Before Creating the PR

1. Run focused automated checks and repository-required broader validation using the verified test configuration. Build the runnable candidate when required.
2. Start or invoke the application locally with explicit test configuration using its documented command. This may be a web server, desktop application, CLI or worker. Keep the process/session handle, command, working directory, candidate revision/artifact and log location. Start background helpers hidden on Windows unless a visible window was requested or is required for the application being tested.
3. For long-running applications, use a bounded startup deadline and verify meaningful readiness: an expected health response, usable window or successful worker fixture. For short-lived commands, inspect the exit status and expected output or artifact. An arbitrary HTTP response, login redirect or error page is not proof of health.
4. Exercise the changed behavior with representative inputs and relevant regressions. For application documentation-only changes, verify startup and a representative existing flow; execute changed run instructions when relevant. Record the URL/port, CLI invocation, UI action or worker input; sanitized inputs; expected/actual status, output and side effects; and pass/fail results.
5. Stop only candidate processes and helpers owned by this verification session, including on failure. Clean up session-owned fixtures using verified paths, deleting database fixtures through endpoints. Remove temporary seed and delete endpoints, then rerun affected checks. Save runtime evidence with write-test-report when working through Builder, and publish the required report before creating the PR.
6. Confirm the evidence covers the candidate being proposed. After edits affecting behavior, build, configuration or dependencies, rerun the affected checks and local execution before PR creation or updating an existing PR. Reuse unaffected evidence only when its identity and relevance remain verified.
7. Create the PR only after required automated checks, local execution, changed-behavior checks and cleanup pass. Include a concise local verification summary and evidence link. If startup or verification fails or cannot run, resolve the prerequisite and record the blocker; do not open a draft PR to defer proof to CI. If the PR already exists, complete missing local verification before further publication or merge. Verification-only scope ends without production deployment.

## Authorized Deployment

Proceed only when deployment is already authorized and candidate verification passed.

1. Identify the supported deployment pipeline, script or service manager and its protected procedure. Confirm the merged revision/artifact and required CI gates. Do not replace managed deployment with an ad hoc development command or PID kill.
2. Record the current artifact/configuration, tested recovery path, backup prerequisites for data/schema changes and bounded success/failure criteria before mutation. Preserve protected permissions and redact secrets. Resolve unknown deployment or recovery prerequisites first.
3. Let the supported supervisor own process rotation. For a documented unmanaged process, follow its exact stop/start/rollback procedure; port ownership alone is insufficient authority.
4. Verify service/process state, expected listener when applicable, meaningful readiness, deployed identity and changed production behavior through authorized non-destructive checks. Do not write test fixtures into production.
5. On failure, follow the established rollback and verify restoration. Stop repeated restart attempts; report the failed checks and actual recovery state. Request only genuinely missing authority or access.

## Completion Evidence

Record automated results, effective resource isolation, candidate identity, local command/environment, exact runtime inputs and outputs, and cleanup. Identify when local verification passed relative to PR creation. For authorized deployment also record the mechanism/result, production health, deployed identity and any rollback outcome. Never describe missing or failed execution as passing verification.
