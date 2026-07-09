# Example Test Report

## Document Status
complete

## Story/Issue
Example issue 42: require explicit JWT secret.

## Branch
`codex/issue-42-require-secret` at `abc1234`

## App / Environment
- App: `example-app`
- Profile: `local`
- Base URL: `http://localhost:8081`
- Environment: `JWT_SECRET=local-test-secret`

## Local Run Details
- Start command: `JWT_SECRET=local-test-secret ./gradlew bootRun --args='--server.port=8081'`
- App stopped after testing: yes

## Test Cases
- Health endpoint responds after explicit secret is provided.
- App refuses to start when `JWT_SECRET` is absent.

## Data Sent
```http
GET /actuator/health HTTP/1.1
Host: localhost:8081
```

## Response Received
```http
HTTP/1.1 200
Content-Type: application/json

{"status":"UP"}
```

## Pass / Fail
- PASS: health endpoint returned 200 with explicit secret.
- PASS: missing secret startup failed with `JWT_SECRET is required`.

## Evidence
- `curl -i http://localhost:8081/actuator/health`
- Startup log captured required-secret failure.

## Bugs / Follow-ups
None.
