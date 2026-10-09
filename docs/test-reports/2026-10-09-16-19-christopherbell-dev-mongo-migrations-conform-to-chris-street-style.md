# Mongo migrations conform to Chris Street Style: Test Report

## Story/Issue
Slice 18f of the style migration ([plan](../implementation-plans/2026-10-09-16-11-christopherbell-dev-mongo-migrations-conform-to-chris-street-style.md)): the migration runner, durable records, cutover ledger and every migration's effect are unchanged

## Branch
``claude/style-mongo-migration-20261009` at candidate `6b0da31a`` at candidate `6b0da31`

## Pass / Fail

> [!TIP]
> 4 of 4 cases passed on candidate `6b0da31`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | A fresh database reaches readiness: the runner applied migrations V001 to V015 and the domain preflight passed (either failing throws at startup) | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Startup log has no ERROR lines and no migration or preflight failure | ✅ PASS | Expected exit code 0 |
| 3 | Migrated lunch collections serve the public What's for Lunch page | ✅ PASS | Expected status 200 and body containing "What's For Lunch" |
| 4 | Create mig_a through the API and log in (account collection migrated by V008 and V015) | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **A fresh database reaches readiness: the runner applied migrations V001 to V015 and the domain preflight passed (either failing throws at startup)**: http `GET http://127.0.0.1:62501/actuator/health/readiness`
2. **Startup log has no ERROR lines and no migration or preflight failure**: command `python -c "import sys;t=open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-607b2289da284b19a8108bc1f9953371/candidate.out.log',encoding='utf-8',errors='replace').read().splitlines();e=[l for l in t if ' ERROR ' in l or 'Migration ' in l and 'failed' in l or 'preflight' in l.lower() and ' WARN ' in l];print('matching lines:',len(e));sys.exit(1 if e else 0)"`
3. **Migrated lunch collections serve the public What's for Lunch page**: http `GET http://127.0.0.1:62501/wfl`
4. **Create mig_a through the API and log in (account collection migrated by V008 and V015)**: command `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:62501 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad mig_a`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod |
| Candidate | packaged website.jar at 127.0.0.1:62501, commit 6b0da31a |
| Checksums | git diff shows no change to any 64-character checksum constant |
| Credentials | one disposable USER; password generated and never recorded; token file deleted |
| Coverage limit | the already-applied path on restart needs the same database twice; MongoMigrationRunnerTest covers it, and production's restart on deploy proves it against real durable records |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:62501/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-mongo-migration`
- **Local command:** `python -c "import sys;t=open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-607b2289da284b19a8108bc1f9953371/candidate.out.log',encoding='utf-8',errors='replace').read().splitlines();e=[l for l in t if ' ERROR ' in l or 'Migration ' in l and 'failed' in l or 'preflight' in l.lower() and ' WARN ' in l];print('matching lines:',len(e));sys.exit(1 if e else 0)"` in `A:\Projects\christopherbell.dev-worktrees\style-mongo-migration`
- **Local command:** `GET http://127.0.0.1:62501/wfl` in `A:\Projects\christopherbell.dev-worktrees\style-mongo-migration`
- **Local command:** `python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:62501 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad mig_a` in `A:\Projects\christopherbell.dev-worktrees\style-mongo-migration`
- **Candidate identity:** `6b0da31`
- **Cleanup:** Candidate and mongod stopped; disposable database root removed; token file deleted

## Data Sent

### 1. A fresh database reaches readiness: the runner applied migrations V001 to V015 and the domain preflight passed (either failing throws at startup)

```http
GET http://127.0.0.1:62501/actuator/health/readiness
```

### 2. Startup log has no ERROR lines and no migration or preflight failure

```text
python -c "import sys;t=open(r'C:/Users/Christopher/AppData/Local/Temp/christopherbell-test-mongo-607b2289da284b19a8108bc1f9953371/candidate.out.log',encoding='utf-8',errors='replace').read().splitlines();e=[l for l in t if ' ERROR ' in l or 'Migration ' in l and 'failed' in l or 'preflight' in l.lower() and ' WARN ' in l];print('matching lines:',len(e));sys.exit(1 if e else 0)"
```

### 3. Migrated lunch collections serve the public What's for Lunch page

```http
GET http://127.0.0.1:62501/wfl
```

### 4. Create mig_a through the API and log in (account collection migrated by V008 and V015)

```text
python C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad/message_fixture_accounts.py http://127.0.0.1:62501 C:/Users/CHRIST~1/AppData/Local/Temp/claude/A--Projects-builder/bc02e5cc-a8b4-4d99-84a5-e48233135236/scratchpad mig_a
```

## Response Received

### 1. A fresh database reaches readiness: the runner applied migrations V001 to V015 and the domain preflight passed (either failing throws at startup)

```text
HTTP 200 
X-Request-Id: aff3df0b-4672-4be6-856c-3036a5b12fcb
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791580825
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
Date: Fri, 09 Oct 2026 21:19:25 GMT
Connection: close

{"status":"UP"}
```

### 2. Startup log has no ERROR lines and no migration or preflight failure

```text
exit code: 0
--- stdout ---
matching lines: 0
```

### 3. Migrated lunch collections serve the public What's for Lunch page

<details><summary>84 lines</summary>

```text
HTTP 200 
X-Request-Id: d4f10949-5067-42f0-ad87-147fb8676079
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791580825
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/html;charset=UTF-8
Content-Language: en-US
Transfer-Encoding: chunked
Date: Fri, 09 Oct 2026 21:19:25 GMT
Connection: close

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="author" content="Christopher Bell (cbell7@icloud.com)" />
    <meta name="keywords" content="cbell,blog" />
    
    <meta name="description" content="Restaurant picks for the moment when everybody is hungry and nobody has a plan." />
    
    <link rel="canonical" href="https://www.christopherbell.dev/wfl" />

    <meta property="og:site_name" content="christopherbell.dev" />
    <meta property="og:locale" content="en_US" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="CB | What&#39;s For Lunch?" />
    <meta property="og:description" content="Restaurant picks for the moment when everybody is hungry and nobody has a plan." />
    <meta property="og:url" content="https://www.christopherbell.dev/wfl" />
    <meta property="og:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:secure_url" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="The Void preview for christopherbell.dev" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="CB | What&#39;s For Lunch?" />
    <meta name="twitter:description" content="Restaurant picks for the moment when everybody is hungry and nobody has a plan." />
    <meta name="twitter:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />
    <meta name="twitter:image:alt" content="The Void preview for christopherbell.dev" />
    <meta name="theme-color" content="#17202a" />
  

    <title>CB | What's For Lunch?</title>

    <link rel="stylesheet" type="text/css" href="/ba07ef3ecb9fe0381733/css/main.css"/>
    <link rel="stylesheet" type="text/css" href="/ba07ef3ecb9fe0381733/css/whats-for-lunch.css"/>
</head>

<body class="site-page void-shell-page lunch-page lunch-void-page">
    <div id="nav"></div>
    <main class="site-main lunch-void-main" aria-labelledby="lunchTitle">
        <div class="lunch-void-shell">
            <div class="container lunch-void-container">
                <header class="lunch-void-hero">
                    <p class="home-kicker">Decision console</p>
                    <h1 id="lunchTitle">What's For Lunch?</h1>
                    <p>Three signals. One good decision.</p>
                </header>
                <section class="lunch-void-console" aria-label="Lunch decision console">
                    <div id="whats-for-lunch"></div>
                </section>
            </div>
        </div>
    </main>
    <footer id="footer"></footer>
</body>

<script type="module" src="/ba07ef3ecb9fe0381733/js/app.js"></script>
<script type="module" src="/ba07ef3ecb9fe0381733/js/whats-for-lunch.js"></script>

</html>
```

</details>

### 4. Create mig_a through the API and log in (account collection migrated by V008 and V015)

```text
exit code: 0
--- stdout ---
mig_a create 201 login 200
```

## Evidence
- Case 1 started 2026-10-09T16:19:24-05:00, took 46 ms, candidate `6b0da31`
- Case 2 started 2026-10-09T16:19:25-05:00, took 30 ms, candidate `6b0da31`
- Case 3 started 2026-10-09T16:19:25-05:00, took 202 ms, candidate `6b0da31`
- Case 4 started 2026-10-09T16:19:25-05:00, took 500 ms, candidate `6b0da31`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
