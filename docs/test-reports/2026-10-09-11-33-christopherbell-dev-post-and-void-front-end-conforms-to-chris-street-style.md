# Post and Void front end conforms to Chris Street Style: Test Report

## Story/Issue
Slice 16b of the style migration ([plan](../implementation-plans/2026-10-09-11-26-christopherbell-dev-post-and-void-javascript-and-templates-conform-to-chris-stre.md)): the thread, explore and topic pages render and behave as before

## Branch
``claude/style-post-js-20261009` at candidate `3d875c51`` at candidate `3d875c5`

## Pass / Fail

> [!TIP]
> 3 of 3 cases passed on candidate `3d875c5`. The browser walk-through below found all 12 page checks as expected, with no console errors.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Create post_c and post_d through the API and log both in (passwords generated, not recorded) | ✅ PASS | Expected exit code 0 |
| 3 | Build a three-level thread (root, reply, nested reply, deepest reply) with topic #walkthrough | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:53393/actuator/health/readiness`
2. **Create post_c and post_d through the API and log both in (passwords generated, not recorded)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:53393 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad post_c post_d`
3. **Build a three-level thread (root, reply, nested reply, deepest reply) with topic #walkthrough**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post_thread_fixture.py http://127.0.0.1:53393 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post-js-ids.json`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod at 127.0.0.1:53392 |
| Candidate | packaged website.jar at 127.0.0.1:53393, commit 3d875c51 |
| Browser | Claude desktop built-in browser, anonymous viewer |
| Credentials | two disposable USERs used only through the API to build the thread; passwords generated and never recorded; token files deleted |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:53393/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-post-js`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:53393 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad post_c post_d` in `A:\Projects\christopherbell.dev-worktrees\style-post-js`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post_thread_fixture.py http://127.0.0.1:53393 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post-js-ids.json` in `A:\Projects\christopherbell.dev-worktrees\style-post-js`
- **Candidate identity:** `3d875c5`
- **Cleanup:** Candidate and mongod stopped; disposable database root removed; token files deleted

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:53393/actuator/health/readiness
```

### 2. Create post_c and post_d through the API and log both in (passwords generated, not recorded)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:53393 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad post_c post_d
```

### 3. Build a three-level thread (root, reply, nested reply, deepest reply) with topic #walkthrough

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post_thread_fixture.py http://127.0.0.1:53393 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/post-js-ids.json
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: d38585c4-49eb-4c4a-8a26-05ec80857218
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791563586
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
Date: Fri, 09 Oct 2026 16:32:06 GMT
Connection: close

{"status":"UP"}
```

### 2. Create post_c and post_d through the API and log both in (passwords generated, not recorded)

```text
exit code: 0
--- stdout ---
post_c create 201 login 200
post_d create 201 login 200
```

### 3. Build a three-level thread (root, reply, nested reply, deepest reply) with topic #walkthrough

```text
exit code: 0
--- stdout ---
{"root": "d00bc0b0-b822-424c-bc95-4e2f56278ce0", "reply": "e71f3078-053f-4322-a687-12f7bae35666", "nested": "8a9bdb96-8dac-4294-ad2b-ed3ed1b1ddfd", "deepest": "905031ea-d5be-4202-8d79-7e79e174e14b"}
```

## Browser Walk-through
Browser walk-through in the Claude desktop built-in browser, anonymous viewer (no token in localStorage), candidate 3d875c51 at 127.0.0.1:53393. Values read from the DOM with the browser's JavaScript inspector after each page loaded.

| Page and action | Observed | Expected |
|---|---|---|
| /p/{nested} (second-level reply) | Hero "Post", meta "@post_c · 1 reply", status pill "Live" with class is-live, reply pill "1 reply" | Same as before |
| /p/{nested} context cards | root card "@post_c / Root of the walk-through thread #walkthrough"; parent card "@post_d / First-level reply from post_d" | Both cards filled |
| /p/{nested} replies | One reply (the deepest) labelled "Reply depth 1", --thread-depth 0 | Same as before |
| /p/{nested} composer | Visible, "Log in to reply.", textarea and button disabled | Anonymous composer disabled |
| /p/{nested} navigation | Shown; previous and next links and a four-post signal rail | Same as before |
| /p/{root} | No context cards; replies at depth 1, 2, 3 with --thread-depth 0, 1, 2; collapse buttons on the two replies with children | Same as before |
| Collapse the first reply | Only the first reply remains; its button reads "Expand branch", aria-expanded false; reply pill stays "1 reply" | Branch hidden |
| Newest reply with the branch collapsed | All three replies return and both buttons read "Collapse branch" | Branch re-expanded to reach the newest reply |
| Collapse the nested reply, then Expand all | Deepest reply hidden, then all three shown again | Same as before |
| /void/explore | Sections new, fading and revived each render one post with a "#walkthrough" chip linking /void/topic/walkthrough (class void-topic-chip); topics renders the large chip; people renders @post_d and @post_c cards with avatar "P", /u/ links and "Recently active in the Void"; no status text; retry and more hidden; each action row has two buttons | Same as before |
| /void/topic/walkthrough | Title "#walkthrough", one post with its chip, retry and more hidden | Same as before |
| Console errors on the thread, explore and topic pages | None | None |

## Evidence
- Case 1 started 2026-10-09T11:32:06-05:00, took 31 ms, candidate `3d875c5`
- Case 2 started 2026-10-09T11:32:07-05:00, took 641 ms, candidate `3d875c5`
- Case 3 started 2026-10-09T11:32:07-05:00, took 282 ms, candidate `3d875c5`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
