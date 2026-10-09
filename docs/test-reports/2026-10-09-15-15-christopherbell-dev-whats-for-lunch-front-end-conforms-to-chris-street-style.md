# Whats for Lunch front end conforms to Chris Street Style: Test Report

## Story/Issue
Slice 17g of the style migration ([plan](../implementation-plans/2026-10-09-15-07-christopherbell-dev-whats-for-lunch-front-end-conforms-to-chris-street-style.md)): the picks, list and restaurant pages render and respond to clicks as before

## Branch
``claude/style-lunch-js-20261009` at candidate `89bed8e2`` at candidate `89bed8e`

## Pass / Fail

> [!TIP]
> 1 of 1 cases passed on candidate `89bed8e`. The browser walk-through below matched production where compared; its only console errors were expected.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:61676/actuator/health/readiness`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test (monthly OpenStreetMap import disabled) |
| Database | test on a fresh disposable mongod |
| Candidate | packaged website.jar at 127.0.0.1:61676, commit 89bed8e2 |
| Browser | Claude desktop built-in browser, anonymous viewer |
| Coverage limit | pick cards, votes, favorites, sessions and deletion need restaurants, which only an ADMIN or a live import can create; whats-for-lunch-vote and session-recovery tests cover those controllers |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:61676/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-lunch-js`
- **Candidate identity:** `89bed8e`
- **Cleanup:** Candidate and mongod stopped; disposable database root removed

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:61676/actuator/health/readiness
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: a7fd3cb2-5552-4bf1-af54-71abdd23053f
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791576924
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/vnd.spring-boot.actuator.v3+json
Transfer-Encoding: chunked
Date: Fri, 09 Oct 2026 20:14:24 GMT
Connection: close

{"status":"UP"}
```

## Browser Walk-through
Browser walk-through in the Claude desktop built-in browser, anonymous viewer (no token in localStorage), candidate 89bed8e2 at 127.0.0.1:61676. Values were read from the DOM with the browser's JavaScript inspector. The same filter sequence was repeated on production `/wfl` (read-only requests only) for comparison.

| Page and action | Observed on the candidate | Production |
|---|---|---|
| `/wfl` loads | Title "CB \| What's For Lunch?", heading "What's For Lunch?", freshness "Not yet imported" with 393 covered cities, location panel selected, ZIP form shown | Location panel selected on load |
| Click the Filters tab | Filters selected; 16 cuisine checkboxes and the clear button shown | Filters selected |
| Click the Session tab | Session selected | Not repeated |
| Check one cuisine, then click clear | 1 checked before, 0 after; nearby picks reload and return to the location panel, because the browser has no location | 0 checked after; returns to the location panel |
| Submit the ZIP "12" | The input reports invalid and the form stays | Not repeated |
| Submit the ZIP 78701 | "The request is invalid." shown with "Using ZIP 78701"; the disposable database has no imported ZIP coordinates, so the server answers 400 | Not repeated: production has ZIP data |
| `/wfl/top-liked` | Title "CB \| Top 10 Liked Restaurants", list mode `top-liked`, freshness shown | Not repeated |
| Console errors | Two: the browser pane's own permissions policy blocking geolocation (the page asks for location on load, as production does), and the deliberate 400 from the ZIP 78701 request. No script errors | Not read |

## Evidence
- Case 1 started 2026-10-09T15:14:24-05:00, took 32 ms, candidate `89bed8e`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
