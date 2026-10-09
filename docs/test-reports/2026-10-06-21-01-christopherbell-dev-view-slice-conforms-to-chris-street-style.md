# View slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 8 of the full Chris Street Style conformance migration; plan docs/implementation-plans/2026-10-06-20-56-christopherbell-dev-view-slice-conforms-to-chris-street-style.md

## Branch
`claude/style-view-20261006` at candidate `94bd5cc`

## Pass / Fail

> [!TIP]
> 4 of 4 cases passed on candidate `94bd5cc`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Every public view route returns the same status as production | ✅ PASS | Expected exit code 0 |
| 3 | Login page keeps its noindex robots meta | ✅ PASS | Expected status 200 and body containing 'noindex,nofollow' |
| 4 | WFL favorites page keeps its canonical social URL | ✅ PASS | Expected status 200 and body containing 'https://www.christopherbell.dev/wfl/favorites' |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:49182/actuator/health/readiness`
2. **Every public view route returns the same status as production**: command `python view_route_sweep.py http://127.0.0.1:49182 https://www.christopherbell.dev`
3. **Login page keeps its noindex robots meta**: http `GET http://127.0.0.1:49182/login`
4. **WFL favorites page keeps its canonical social URL**: http `GET http://127.0.0.1:49182/wfl/favorites`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:49181 (read back with db.getName()) |
| Candidate | packaged website.jar at 127.0.0.1:49182, base 1d1516f9 |
| Baseline | production www.christopherbell.dev, read-only GET requests during the run |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:49182/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-view`
- **Local command:** `python view_route_sweep.py http://127.0.0.1:49182 https://www.christopherbell.dev` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Local command:** `GET http://127.0.0.1:49182/login` in `A:\Projects\christopherbell.dev-worktrees\style-view`
- **Local command:** `GET http://127.0.0.1:49182/wfl/favorites` in `A:\Projects\christopherbell.dev-worktrees\style-view`
- **Candidate identity:** `94bd5cc`
- **Cleanup:** Stopped candidate PID 52608 and mongod PID 49508 by process tree; both ports have zero listeners; production MongoDB 27017 untouched.

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:49182/actuator/health/readiness
```

### 2. Every public view route returns the same status as production

```text
python view_route_sweep.py http://127.0.0.1:49182 https://www.christopherbell.dev
```

### 3. Login page keeps its noindex robots meta

```http
GET http://127.0.0.1:49182/login
```

### 4. WFL favorites page keeps its canonical social URL

```http
GET http://127.0.0.1:49182/wfl/favorites
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: 2f42d729-a9d3-4385-a8be-e10593d477ed
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791338517
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
Date: Wed, 07 Oct 2026 02:00:57 GMT
Connection: close

{"status":"UP"}
```

### 2. Every public view route returns the same status as production

<details><summary>43 lines</summary>

```text
exit code: 0
--- stdout ---
/: candidate 200, production 200 (same)
/blog: candidate 200, production 200 (same)
/photos: candidate 200, production 200 (same)
/photos/usage: candidate 200, production 200 (same)
/software-handoff-kit: candidate 410, production 410 (same)
/software-handoff-kit/preview: candidate 410, production 410 (same)
/back-office: candidate 200, production 200 (same)
/command-center: candidate 200, production 200 (same)
/shared: candidate 200, production 200 (same)
/music: candidate 200, production 200 (same)
/report: candidate 200, production 200 (same)
/thebell: candidate 200, production 200 (same)
/thebell/tony: candidate 200, production 200 (same)
/login: candidate 200, production 200 (same)
/forgot-password: [REDACTED] 200, production 200 (same)
/reset-password: [REDACTED] 200, production 200 (same)
/signup: candidate 200, production 200 (same)
/void/login: candidate 200, production 200 (same)
/void/signup: candidate 200, production 200 (same)
/survive: candidate 200, production 200 (same)
/site-monitor: candidate 200, production 200 (same)
/canes-box-tracker: candidate 200, production 200 (same)
/vin-decoder: candidate 200, production 200 (same)
/zip-coordinates: candidate 200, production 200 (same)
/void: candidate 200, production 200 (same)
/void/explore: candidate 200, production 200 (same)
/void/topic/music: candidate 200, production 200 (same)
/void/topic/%20%20: candidate 400, production 400 (same)
/profile: candidate 200, production 200 (same)
/messages: candidate 200, production 200 (same)
/notifications: candidate 200, production 200 (same)
/u/no-such-user-for-style-check: candidate 404, production 404 (same)
/p/no-such-post-for-style-check: candidate 404, production 404 (same)
/wfl: candidate 200, production 200 (same)
/wfl/favorites: candidate 200, production 200 (same)
/wfl/top-liked: candidate 200, production 200 (same)
/wfl/top-rated: candidate 308, production 308 (same)
/wfl/restaurants/no-such-restaurant: candidate 404, production 404 (same)
/no-such-page-for-style-check: candidate 404, production 404 (same)
/api/no-such-api-for-style-check: candidate 403, production 403 (same)
40 of 40 routes match production
```

</details>

### 3. Login page keeps its noindex robots meta

<details><summary>93 lines</summary>

```text
HTTP 200 
X-Request-Id: 2e68beb8-fbfd-41db-8f62-0c4d4a9f0c39
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791338525
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
Date: Wed, 07 Oct 2026 02:01:05 GMT
Connection: close

<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="utf-8" />

  <meta name="viewport" content="width=device-width, initial-scale=1" />

  

    <meta name="description" content="Sign in to the Void on christopherbell.dev." />

    <meta name="robots" content="noindex,nofollow" />

    <link rel="canonical" href="https://www.christopherbell.dev/login" />



    <meta property="og:site_name" content="christopherbell.dev" />

    <meta property="og:locale" content="en_US" />

    <meta property="og:type" content="website" />

    <meta property="og:title" content="CB | Login" />

    <meta property="og:description" content="Sign in to the Void on christopherbell.dev." />

    <meta property="og:url" content="https://www.christopherbell.dev/login" />

    <meta property="og:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta property="og:image:secure_url" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta property="og:image:type" content="image/png" />

    <meta property="og:image:width" content="1200" />

    <meta property="og:image:height" content="630" />

    <meta property="og:image:alt" content="The Void preview for christopherbell.dev" />



    <meta name="twitter:card" content="summary_large_image" />

    <meta name="twitter:title" content="CB | Login" />

    <meta name="twitter:description" content="Sign in to the Void on christopherbell.dev." />

    <meta name="twitter:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta name="twitter:image:alt" content="The Void preview for christopherbell.dev" />

    <meta name="theme-color" content="#17202a" />

  

  <title>Login</title>

  <link rel="stylesheet" type="text/css" href="/e112b78388fc69c26955/css/main.css"/>

</head>

<body class="site-page auth-page">

  <div id="nav"></div>

  <main class="auth-shell" role="main">

    <div class="row justify-content-center">

      <div class="col-12 col-md-8 col-lg-6">

        <div class="auth-heading">

          <p class="home-kicker">Welcome back</p>

          <h1>Sign in</h1>

          <p>Get back to posting, profile tools, and the admin bits if you have access.</p>

        </div>

        <div class="card shadow-sm">

          <div class="card-body p-4">

            <div id="loginAlert" class="alert alert-danger d-none" role="alert"></div>

            <form id="loginForm" method="post" novalidate>

              <div class="mb-3">

                <label for="email" class="form-label">Email address</label>

                <input type="email" class="form-control" id="email" name="email" autocomplete="username" placeholder="name@example.com" required />

              </div>

              <div class="mb-3">

                <label for="password" class="form-label">Password</label>

                <input type="password" class="form-control" id="password" name="password" autocomplete="current-password" placeholder="••••••••" required />

                <div class="form-text"><a href="/forgot-password">Forgot password?</a></div>

              </div>

              <div class="d-grid gap-2">

                <button id="loginBtn" type="submit" class="btn btn-primary">Login</button>

                <a class="btn btn-outline-secondary" href="/signup">Sign up</a>

              </div>

            </form>

          </div>

        </div>

      </div>

    </div>

  </main>

  <footer id="footer"></footer>

  <script type="module" src="/e112b78388fc69c26955/js/app.js"></script>

  <script type="module" src="/e112b78388fc69c26955/js/auth/login.js"></script>

  <script src="/webjars/bootstrap/5.3.8/js/bootstrap.bundle.min.js"></script>

  </body>

</html>
```

</details>

### 4. WFL favorites page keeps its canonical social URL

<details><summary>84 lines</summary>

```text
HTTP 200 
X-Request-Id: 18c16cb5-9472-47a5-9842-b7196089502a
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791338525
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
Date: Wed, 07 Oct 2026 02:01:05 GMT
Connection: close

<!DOCTYPE html>

<html lang="en">



<head>

    <meta charset="utf-8" />

    <meta name="viewport" content="width=device-width, initial-scale=1" />

    <meta name="author" content="Christopher Bell (cbell7@icloud.com)" />

    

    <meta name="description" content="Restaurants you have saved from What&#39;s For Lunch." />

    <meta name="robots" content="noindex,nofollow" />

    <link rel="canonical" href="https://www.christopherbell.dev/wfl/favorites" />



    <meta property="og:site_name" content="christopherbell.dev" />

    <meta property="og:locale" content="en_US" />

    <meta property="og:type" content="website" />

    <meta property="og:title" content="CB | Favorite Restaurants" />

    <meta property="og:description" content="Restaurants you have saved from What&#39;s For Lunch." />

    <meta property="og:url" content="https://www.christopherbell.dev/wfl/favorites" />

    <meta property="og:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta property="og:image:secure_url" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta property="og:image:type" content="image/png" />

    <meta property="og:image:width" content="1200" />

    <meta property="og:image:height" content="630" />

    <meta property="og:image:alt" content="The Void preview for christopherbell.dev" />



    <meta name="twitter:card" content="summary_large_image" />

    <meta name="twitter:title" content="CB | Favorite Restaurants" />

    <meta name="twitter:description" content="Restaurants you have saved from What&#39;s For Lunch." />

    <meta name="twitter:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta name="twitter:image:alt" content="The Void preview for christopherbell.dev" />

    <meta name="theme-color" content="#17202a" />

  



    <title>CB | Favorite Restaurants</title>



    <link rel="stylesheet" type="text/css" href="/e112b78388fc69c26955/css/main.css"/>

</head>



<body class="site-page lunch-page">

    <div id="nav"></div>

    <main class="site-main" role="main">

        <section class="site-hero site-hero-lunch" aria-labelledby="wflListTitle">

            <div class="container">

                <p class="home-kicker">What's For Lunch</p>

                <h1 id="wflListTitle">Favorite Restaurants</h1>

                <p>Restaurants you have saved from What&#39;s For Lunch.</p>

            </div>

        </section>

        <section class="site-content">

            <div class="container">

                <div class="content-panel lunch-panel">

                    <div id="wfl-list" data-list-mode="favorites" data-list-title="Favorite Restaurants"></div>

                </div>

            </div>

        </section>

    </main>

    <footer id="footer"></footer>

</body>



<script type="module" src="/e112b78388fc69c26955/js/app.js"></script>

<script type="module" src="/e112b78388fc69c26955/js/wfl-list.js"></script>



</html>
```

</details>

## Evidence
- Case 1 started 2026-10-06T21:00:57-05:00, took 32 ms, candidate `94bd5cc`
- Case 2 started 2026-10-06T21:00:57-05:00, took 6608 ms, candidate `unknown`
- Case 3 started 2026-10-06T21:01:05-05:00, took 32 ms, candidate `94bd5cc`
- Case 4 started 2026-10-06T21:01:05-05:00, took 30 ms, candidate `94bd5cc`

## Bugs / Follow-ups
- **Native checks on the candidate:** `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` passed in 4m51s. View suites: `ViewControllerTest` 51/51, `RestaurantProfilePageServiceTest` 5/5 and `VoidPostSocialPreviewTest` 3/3. `ModularMonolithArchitectureTest` passed 5/5. JS and Pester suites passed.
- **Route sweep:** all 40 routes matched production. The sweep covered every handler, the 410 retired offer, the 400 invalid topic, the 404s for missing users, posts and restaurants, and the 308 legacy redirect.
- **Harness note:** two follow-up cases had wrong expectations, and both are excluded above:
  - An anonymous unknown `/api/` path gets 403 from security before the not-found handler runs, in both the candidate and production, as the sweep shows.
  - The recorder follows redirects, so the 308 case saw the target page instead; the sweep, which does not follow redirects, confirms the 308.

## Document Status
complete

## Project
christopherbell-dev
