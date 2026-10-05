# Require the JWT Signing Secret: Test Report

## Story/Issue
Example issue 42: require an explicit JWT secret.

## Branch
`codex/issue-42-require-secret` at `abc1234`

## Pass / Fail

> [!TIP]
> **2 of 2 passed** on candidate `abc1234`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Health with the secret set | ✅ PASS | `/actuator/health` returned 200 `{"status":"UP"}` |
| 2 | Startup without the secret | ✅ PASS | Startup stopped with `JWT_SECRET is required`; the value never appeared |

## Test Cases
1. **Health with the secret set:** the app starts and reports healthy when `JWT_SECRET` is provided.
2. **Startup without the secret:** the app refuses to start when `JWT_SECRET` is absent.

## App / Environment

| Setting | Value |
|---|---|
| App | `example-app` |
| Profile | `local` |
| Base URL | `http://localhost:8081` |
| Environment | `JWT_SECRET=local-test-secret` (case 1 only) |

## Local Run Details
- **Local command:** `./gradlew bootRun --args='--server.port=8081'`
- **Working directory:** the `example-app` checkout at `abc1234`.
- **Logs:** console output, captured below.
- **Cleanup:** app stopped after each case; port 8081 confirmed free.

## Data Sent

### 1. Health with the secret set

```http
GET /actuator/health HTTP/1.1
Host: localhost:8081
```

### 2. Startup without the secret

```text
Local command: ./gradlew bootRun --args='--server.port=8081'
Environment: JWT_SECRET unset
```

## Response Received

### 1. Health with the secret set

```http
HTTP/1.1 200
Content-Type: application/json

{"status":"UP"}
```

### 2. Startup without the secret

```text
Exit code: 1
stderr: java.lang.IllegalStateException: JWT_SECRET is required
```

## Evidence
- `curl -i http://localhost:8081/actuator/health` at 14:02 local time.
- Startup log for case 2 shows the required-secret failure and no secret value.

## Bugs / Follow-ups
None.

## Document Status
complete

## Project
example-app
