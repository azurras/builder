# Test Report Template

Copy this skeleton and fill each section as [report content](report.md) describes. Do not leave placeholders; write `None` or the explicit gap instead. See the [complete example](example.md).

````markdown
# <Change>: Test Report

## Story/Issue
<Issue or request, with a link>

## Branch
`<branch>` at `<short sha>`

## Pass / Fail

> [!TIP]
> **<N> of <N> passed** on candidate `<short sha>`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | <Case name> | ✅ PASS | <One-line reason> |

## Test Cases
1. **<Case name>:** <the behavior, endpoint or flow exercised>.

## App / Environment

| Setting | Value |
|---|---|
| App | <name> |
| Runtime | <profile, configuration, database or fixtures> |

## Local Run Details
- **Local command:** `<exact command>`
- **Working directory:** <path or checkout>
- **Logs:** <location>
- **Cleanup:** <what was stopped or removed>

## Data Sent

### 1. <Case name>

```text
<actual request, input or arguments>
```

## Response Received

### 1. <Case name>

```text
<actual response, exit status or output>
```

## Evidence
- <command, timestamp, screenshot or log excerpt>

## Bugs / Follow-ups
None.

## Document Status
complete

## Project
<slug>
````
