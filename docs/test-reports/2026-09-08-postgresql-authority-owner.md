# PostgreSQL authority owner runtime verification

## Document Status
complete

## Story/Issue
Approved PostgreSQL cutover recovery; [targeted plan](../implementation-plans/2026-09-08-postgresql-authority-owner.md). This report verifies the ownership fix, not completed cutover.

## Branch
`codex/fix-postgresql-authority-owner`, main baseline `39867e9e1f1da44373fda19f82cfb41da08d5129` plus one-line owner-policy correction and runbook clarification.

## App / Environment
Native Windows, Java 25.0.3, website on port 8080, Mongo authoritative. Read-only standalone Java probe invokes compiled FinalizeEvidenceLoader against actual protected authority metadata. No database connection or production fixture writes in this probe.

## Local Run Details
Existing Spring Boot application: `http://127.0.0.1:8080`, managed by ChristopherBellDev. No website restart was performed for this verification.

Elevated hidden PowerShell runs `C:\Users\Christopher\AppData\Local\Temp\cbell-authority-probe-20260908.ps1`, invoking Java with isolated worktree compiled classes and `CutoverAclProbe20260908.java`. Output: `C:\Users\Christopher\AppData\Local\Temp\cbell-authority-probe-20260908.txt`. Probe exited; production service left running.

## Test Cases
1. Existing production readiness remains healthy.
2. Actual protected authority files pass owner and ACL checks after correction.
3. Prior signed evidence passes unchanged integrity checks at its historical lease time.

## Data Sent
HTTP GET `http://127.0.0.1:8080/actuator/health/readiness`, no payload or authorization. Java probe reads C:\ProgramData anchor, application root, authority directory, finalize.properties, authority.key and writer.lock. It calls the evidence loader with a clock one second before the prior lease expiry solely for read-only diagnosis; it does not authorize or invoke finalization.

## Response Received
Readiness HTTP 200, response body `{"status":"UP"}`. Before correction: anchor accepted, five protected nodes rejected, historicalEvidenceAccepted=false. All nodes had BUILTIN\Administrators ownership, only SYSTEM/Administrators full-control ACLs, and no reparse attribute. After correction: productionAnchorAccepted=true, all five nodes accepted=true, historicalEvidenceAccepted=true.

## Pass / Fail
PASS: exact prior rejection resolved without modifying protected files, ACLs, key, signature or lease. PASS: eight existing FinalizeEvidenceLoaderTest cases, including tampering, expired lease and untrusted permissions. New regression tests omitted at user's explicit request.

## Evidence
September 8 live probe outputs above; `:website:test --tests '*FinalizeEvidenceLoaderTest' --console=plain` BUILD SUCCESSFUL, eight passed. `git diff --check` passed. Source inspection confirms PowerShell New-ProtectedProductionAcl sets Administrators ownership; Java already trusted that principal for writes but previously rejected it for ownership.

## Bugs / Follow-ups
Cutover is still ROLLED_BACK before authority. Final CI, merge, approved supported cutover and post-cutover runtime checks remain. This diagnostic does not extend a production lease or prove any PostgreSQL data migration occurred. Automatic deployment remains paused pending PostgreSQL-aware deployment support.
