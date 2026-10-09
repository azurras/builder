# Configuration root mail and persistence conform to Chris Street Style: Test Report

## Story/Issue
Slice 18a of the style migration ([plan](../implementation-plans/2026-10-09-15-25-christopherbell-dev-configuration-root-mail-and-persistence-conform-to-chris-str.md)): startup validation, sitemaps and media retention cleanup behave as before

## Branch
``claude/style-config-small-20261009` at candidate `4287ffe6`` at candidate `4287ffe`

## Pass / Fail

> [!TIP]
> 5 of 5 cases passed on candidate `4287ffe`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test (the retention cleanup job is constructed with the application Clock) | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | robots.txt is byte-identical to production (200, text/plain) | ✅ PASS | Expected exit code 0 |
| 3 | sitemap.xml is a URL set listing every one of production's static public URLs | ✅ PASS | Expected exit code 0 |
| 4 | A sitemap shard that does not exist returns 404, as production does | ✅ PASS | Expected status 404 |
| 5 | Candidate log has no ERROR lines | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test (the retention cleanup job is constructed with the application Clock)**: http `GET http://127.0.0.1:52608/actuator/health/readiness`
2. **robots.txt is byte-identical to production (200, text/plain)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_text_body.py http://127.0.0.1:52608/robots.txt https://www.christopherbell.dev/robots.txt`
3. **sitemap.xml is a URL set listing every one of production's static public URLs**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/sitemap_checks.py http://127.0.0.1:52608 https://www.christopherbell.dev`
4. **A sitemap shard that does not exist returns 404, as production does**: http `GET http://127.0.0.1:52608/sitemap-2.xml`
5. **Candidate log has no ERROR lines**: command `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-dda1712588714bb69ceb4eb5965c34dd/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod |
| Candidate | packaged website.jar at 127.0.0.1:52608, commit 4287ffe6 |
| Production | read-only GETs only (robots.txt, sitemap.xml, sitemap-2.xml) |
| Earlier run | a first run on the same candidate was discarded: the shared comparison helper sent Accept: application/json, so both hosts answered robots.txt with the same 406, and production's edge refused Python's default user agent for sitemap.xml. A plain-text comparison helper and an explicit user agent fixed the harness; no application change was made |
| Coverage limit | the production-only initializers run only under the prod profile, which a local candidate must not use; FederationSecretApplicationContextInitializerTest and ProductionSettingsApplicationContextInitializerTest cover them, and ClientIpResolverTest covers forwarded addresses |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:52608/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-config-small`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_text_body.py http://127.0.0.1:52608/robots.txt https://www.christopherbell.dev/robots.txt` in `A:\Projects\christopherbell.dev-worktrees\style-config-small`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/sitemap_checks.py http://127.0.0.1:52608 https://www.christopherbell.dev` in `A:\Projects\christopherbell.dev-worktrees\style-config-small`
- **Local command:** `GET http://127.0.0.1:52608/sitemap-2.xml` in `A:\Projects\christopherbell.dev-worktrees\style-config-small`
- **Local command:** `python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-dda1712588714bb69ceb4eb5965c34dd/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"` in `A:\Projects\christopherbell.dev-worktrees\style-config-small`
- **Candidate identity:** `4287ffe`
- **Cleanup:** Candidate and mongod stopped; disposable database root removed

## Data Sent

### 1. Candidate readiness on isolated MongoDB test (the retention cleanup job is constructed with the application Clock)

```http
GET http://127.0.0.1:52608/actuator/health/readiness
```

### 2. robots.txt is byte-identical to production (200, text/plain)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/compare_text_body.py http://127.0.0.1:52608/robots.txt https://www.christopherbell.dev/robots.txt
```

### 3. sitemap.xml is a URL set listing every one of production's static public URLs

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/sitemap_checks.py http://127.0.0.1:52608 https://www.christopherbell.dev
```

### 4. A sitemap shard that does not exist returns 404, as production does

```http
GET http://127.0.0.1:52608/sitemap-2.xml
```

### 5. Candidate log has no ERROR lines

```text
python -c "import sys;e=[l for l in open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-dda1712588714bb69ceb4eb5965c34dd/candidate.out.log',encoding='utf-8',errors='replace') if ' ERROR ' in l];print('ERROR lines:',len(e));sys.exit(1 if e else 0)"
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test (the retention cleanup job is constructed with the application Clock)

```text
HTTP 200 
X-Request-Id: e63b7a59-99bb-43cb-b00e-0c5e13a52b8e
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791578074
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
Date: Fri, 09 Oct 2026 20:33:34 GMT
Connection: close

{"status":"UP"}
```

### 2. robots.txt is byte-identical to production (200, text/plain)

```text
exit code: 0
--- stdout ---
candidate 200 text/plain 79 bytes
production 200 text/plain 79 bytes
identical
```

### 3. sitemap.xml is a URL set listing every one of production's static public URLs

```text
exit code: 0
--- stdout ---
PASS the candidate sitemap is an XML URL set: 200 application/xml root=urlset urls=15
PASS the candidate lists every one of production's static public URLs: production static=15 missing=[]
```

### 4. A sitemap shard that does not exist returns 404, as production does

```text
HTTP 404 
X-Request-Id: 5190d352-9358-436e-8799-3c38cf09ebf0
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791578076
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Length: 0
Date: Fri, 09 Oct 2026 20:33:36 GMT
Connection: close
```

### 5. Candidate log has no ERROR lines

```text
exit code: 0
--- stdout ---
ERROR lines: 0
```

## Evidence
- Case 1 started 2026-10-09T15:33:34-05:00, took 30 ms, candidate `4287ffe`
- Case 2 started 2026-10-09T15:33:34-05:00, took 343 ms, candidate `4287ffe`
- Case 3 started 2026-10-09T15:33:34-05:00, took 1500 ms, candidate `4287ffe`
- Case 4 started 2026-10-09T15:33:36-05:00, took 31 ms, candidate `4287ffe`
- Case 5 started 2026-10-09T15:33:36-05:00, took 31 ms, candidate `4287ffe`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
