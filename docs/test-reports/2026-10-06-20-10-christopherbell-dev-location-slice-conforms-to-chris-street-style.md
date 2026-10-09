# Location slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 4 of the full Chris Street Style conformance migration; plan docs/implementation-plans/2026-10-06-19-59-christopherbell-dev-location-slice-conforms-to-chris-street-style.md

## Branch
`claude/style-location-20261006` at candidate `d64c12b`

## Pass / Fail

> [!TIP]
> 8 of 8 cases passed on candidate `d64c12b`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Malformed ZIP input returns the same 400 envelope as production 07859a2f | ✅ PASS | Expected exit code 0 |
| 3 | Five-digit ZIP on empty imported data returns the standard 404 envelope | ✅ PASS | Expected status 404 and body containing 'RESOURCE_NOT_FOUND' |
| 4 | ZIP+4 input is normalized and reaches the same 404 lookup (not a 400) | ✅ PASS | Expected status 404 and body containing 'RESOURCE_NOT_FOUND' |
| 5 | Anonymous Census import is rejected before any import work | ✅ PASS | Expected status 403 |
| 6 | ZIP coordinates page renders and loads its page script | ✅ PASS | Expected status 200 and body containing 'js/zip-coordinates.js' |
| 7 | Candidate serves the conformed ZIP page script | ✅ PASS | Expected status 200 and body containing 'lookupFailure.message' |
| 8 | Production 78701 lookup is unaffected (reference: production has imported data) | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:51102/actuator/health/readiness`
2. **Malformed ZIP input returns the same 400 envelope as production 07859a2f**: command `python compare_status_and_body.py http://127.0.0.1:51102/api/location/zip/zip https://www.christopherbell.dev/api/location/zip/zip 400`
3. **Five-digit ZIP on empty imported data returns the standard 404 envelope**: http `GET http://127.0.0.1:51102/api/location/zip/78701`
4. **ZIP+4 input is normalized and reaches the same 404 lookup (not a 400)**: http `GET http://127.0.0.1:51102/api/location/zip/78701-1234`
5. **Anonymous Census import is rejected before any import work**: http `POST http://127.0.0.1:51102/api/location/zip/import/census`
6. **ZIP coordinates page renders and loads its page script**: http `GET http://127.0.0.1:51102/zip-coordinates`
7. **Candidate serves the conformed ZIP page script**: http `GET http://127.0.0.1:51102/js/zip-coordinates.js`
8. **Production 78701 lookup is unaffected (reference: production has imported data)**: command `python -c "import urllib.request,json;r=urllib.request.urlopen(urllib.request.Request('https://www.christopherbell.dev/api/location/zip/78701',headers={'User-Agent':'curl/8.0'}));d=json.loads(r.read());print(r.status,d['payload']);raise SystemExit(0 if d['payload']['zipCode']=='78701' else 1)"`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:51101 (read back with db.getName()); no ZIP data imported |
| Candidate | packaged website.jar at 127.0.0.1:51102, base 07859a2f |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:51102/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-location`
- **Local command:** `python compare_status_and_body.py http://127.0.0.1:51102/api/location/zip/zip https://www.christopherbell.dev/api/location/zip/zip 400` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Local command:** `GET http://127.0.0.1:51102/api/location/zip/78701` in `A:\Projects\christopherbell.dev-worktrees\style-location`
- **Local command:** `GET http://127.0.0.1:51102/api/location/zip/78701-1234` in `A:\Projects\christopherbell.dev-worktrees\style-location`
- **Local command:** `POST http://127.0.0.1:51102/api/location/zip/import/census` in `A:\Projects\christopherbell.dev-worktrees\style-location`
- **Local command:** `GET http://127.0.0.1:51102/zip-coordinates` in `A:\Projects\christopherbell.dev-worktrees\style-location`
- **Local command:** `GET http://127.0.0.1:51102/js/zip-coordinates.js` in `A:\Projects\christopherbell.dev-worktrees\style-location`
- **Local command:** `python -c "import urllib.request,json;r=urllib.request.urlopen(urllib.request.Request('https://www.christopherbell.dev/api/location/zip/78701',headers={'User-Agent':'curl/8.0'}));d=json.loads(r.read());print(r.status,d['payload']);raise SystemExit(0 if d['payload']['zipCode']=='78701' else 1)"` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Candidate identity:** `d64c12b`
- **Cleanup:** Stopped candidate PID 45284 and mongod PID 37776 by process tree; ports 51102 and 51101 have zero listeners; production MongoDB 27017 (PID 5236) untouched; no request was sent to any production write endpoint.

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:51102/actuator/health/readiness
```

### 2. Malformed ZIP input returns the same 400 envelope as production 07859a2f

```text
python compare_status_and_body.py http://127.0.0.1:51102/api/location/zip/zip https://www.christopherbell.dev/api/location/zip/zip 400
```

### 3. Five-digit ZIP on empty imported data returns the standard 404 envelope

```http
GET http://127.0.0.1:51102/api/location/zip/78701
```

### 4. ZIP+4 input is normalized and reaches the same 404 lookup (not a 400)

```http
GET http://127.0.0.1:51102/api/location/zip/78701-1234
```

### 5. Anonymous Census import is rejected before any import work

```http
POST http://127.0.0.1:51102/api/location/zip/import/census
```

### 6. ZIP coordinates page renders and loads its page script

```http
GET http://127.0.0.1:51102/zip-coordinates
```

### 7. Candidate serves the conformed ZIP page script

```http
GET http://127.0.0.1:51102/js/zip-coordinates.js
```

### 8. Production 78701 lookup is unaffected (reference: production has imported data)

```text
python -c "import urllib.request,json;r=urllib.request.urlopen(urllib.request.Request('https://www.christopherbell.dev/api/location/zip/78701',headers={'User-Agent':'curl/8.0'}));d=json.loads(r.read());print(r.status,d['payload']);raise SystemExit(0 if d['payload']['zipCode']=='78701' else 1)"
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: db8a039d-554f-4db9-bf77-b6fabf6d26e0
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791335471
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
Date: Wed, 07 Oct 2026 01:10:11 GMT
Connection: close

{"status":"UP"}
```

### 2. Malformed ZIP input returns the same 400 envelope as production 07859a2f

```text
exit code: 0
--- stdout ---
candidate 400 {'messages': [{'code': 'INVALID_REQUEST', 'description': 'The request is invalid.'}], 'payload': None, 'requestId': None, 'success': False}
production 400 {'messages': [{'code': 'INVALID_REQUEST', 'description': 'The request is invalid.'}], 'payload': None, 'requestId': None, 'success': False}
```

### 3. Five-digit ZIP on empty imported data returns the standard 404 envelope

```text
HTTP 404 
X-Request-Id: 2f29c242-622a-4cd3-824b-475c7b337075
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791335472
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Content-Length: 146
Date: Wed, 07 Oct 2026 01:10:12 GMT
Connection: close

{"messages":[{"code":"RESOURCE_NOT_FOUND","description":"The requested resource was not found."}],"payload":null,"requestId":null,"success":false}
```

### 4. ZIP+4 input is normalized and reaches the same 404 lookup (not a 400)

```text
HTTP 404 
X-Request-Id: 75470103-faf9-405d-a317-42870081b68c
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791335472
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Content-Length: 146
Date: Wed, 07 Oct 2026 01:10:12 GMT
Connection: close

{"messages":[{"code":"RESOURCE_NOT_FOUND","description":"The requested resource was not found."}],"payload":null,"requestId":null,"success":false}
```

### 5. Anonymous Census import is rejected before any import work

```text
HTTP 403 
X-Request-Id: 29bc5421-52b5-40e4-b92a-27e61cb2c336
Set-Cookie: [REDACTED]
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: application/json
Transfer-Encoding: chunked
Date: Wed, 07 Oct 2026 01:10:12 GMT
Connection: close

{"timestamp":"2026-10-07T01:10:12.483Z","status":403,"error":"Forbidden","path":"/api/location/zip/import/census"}
```

### 6. ZIP coordinates page renders and loads its page script

<details><summary>134 lines</summary>

```text
HTTP 200 
X-Request-Id: c2fcc6ef-1b1a-4fc7-b000-14bbc2f525a6
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791335472
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
Date: Wed, 07 Oct 2026 01:10:12 GMT
Connection: close

<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="utf-8" />

  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <meta name="author" content="Christopher Bell" />

  

    <meta name="description" content="Look up Census ZIP coordinate origins from christopherbell.dev." />

    

    <link rel="canonical" href="https://www.christopherbell.dev/zip-coordinates" />



    <meta property="og:site_name" content="christopherbell.dev" />

    <meta property="og:locale" content="en_US" />

    <meta property="og:type" content="website" />

    <meta property="og:title" content="CB | ZIP Coordinates" />

    <meta property="og:description" content="Look up Census ZIP coordinate origins from christopherbell.dev." />

    <meta property="og:url" content="https://www.christopherbell.dev/zip-coordinates" />

    <meta property="og:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta property="og:image:secure_url" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta property="og:image:type" content="image/png" />

    <meta property="og:image:width" content="1200" />

    <meta property="og:image:height" content="630" />

    <meta property="og:image:alt" content="The Void preview for christopherbell.dev" />



    <meta name="twitter:card" content="summary_large_image" />

    <meta name="twitter:title" content="CB | ZIP Coordinates" />

    <meta name="twitter:description" content="Look up Census ZIP coordinate origins from christopherbell.dev." />

    <meta name="twitter:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta name="twitter:image:alt" content="The Void preview for christopherbell.dev" />

    <meta name="theme-color" content="#17202a" />

  

  <title>ZIP Coordinates</title>

  <link rel="stylesheet" type="text/css" href="/ed991cd6cda909171e19/css/main.css"/>

</head>

<body class="site-page void-shell-page zip-coordinate-page">

  <div id="nav"></div>

  <main class="site-main zip-coordinate-main" role="main">

    <section class="zip-coordinate-shell" aria-labelledby="zipCoordinateTitle">

      <div class="zip-coordinate-container">

        <header class="zip-coordinate-hero">

          <p class="thread-label">Location signal</p>

          <h1 id="zipCoordinateTitle">ZIP Coordinates</h1>

          <p>Resolve a ZIP code to the imported Census coordinate origin used by site tools.</p>

        </header>



        <div class="zip-coordinate-grid">

          <section class="zip-coordinate-panel" aria-labelledby="zipCoordinateLookupTitle">

            <p class="profile-label">Lookup</p>

            <h2 id="zipCoordinateLookupTitle">Find Coordinates</h2>

            <form id="zipCoordinateForm" class="zip-coordinate-form">

              <label class="form-label" for="zipCoordinateInput">ZIP code</label>

              <div class="input-group input-group-lg">

                <input id="zipCoordinateInput" class="form-control" inputmode="numeric" autocomplete="postal-code" placeholder="78701" />

                <button id="zipCoordinateButton" class="btn btn-primary" type="submit">Lookup</button>

              </div>

              <div class="form-text">Accepts five-digit ZIP codes and ZIP+4 input.</div>

            </form>

            <div id="zipCoordinateAlert" class="alert alert-danger d-none mt-3" role="alert"></div>

          </section>



          <section id="zipCoordinateResult" class="zip-coordinate-panel zip-coordinate-result d-none" aria-live="polite" aria-labelledby="zipCoordinateResultTitle">

            <div class="zip-coordinate-result-header">

              <div>

                <p class="profile-label">Resolved origin</p>

                <h2 id="zipCoordinateResultTitle">Coordinate</h2>

              </div>

              <span id="zipCoordinateCode" class="thread-status-pill is-live">ZIP</span>

            </div>



            <div class="zip-coordinate-summary">

              <div>

                <span>Latitude</span>

                <strong id="zipLatitude">-</strong>

              </div>

              <div>

                <span>Longitude</span>

                <strong id="zipLongitude">-</strong>

              </div>

              <div>

                <span>Source</span>

                <strong id="zipSource">-</strong>

              </div>

              <div>

                <span>Source Year</span>

                <strong id="zipSourceYear">-</strong>

              </div>

            </div>



            <div class="zip-coordinate-output">

              <div class="zip-coordinate-output-header">

                <h3>API URL</h3>

                <button id="copyZipApiButton" class="btn btn-sm btn-outline-light" type="button">Copy</button>

              </div>

              <code id="zipApiUrl"></code>

            </div>



            <div class="zip-coordinate-output">

              <div class="zip-coordinate-output-header">

                <h3>curl</h3>

                <button id="copyZipCurlButton" class="btn btn-sm btn-outline-light" type="button">Copy</button>

              </div>

              <pre><code id="zipCurlOutput"></code></pre>

            </div>

          </section>

        </div>

      </div>

    </section>

  </main>

  <footer id="footer"></footer>

  <script type="module" src="/ed991cd6cda909171e19/js/app.js"></script>

  <script type="module" src="/ed991cd6cda909171e19/js/zip-coordinates.js"></script>

</body>

</html>
```

</details>

### 7. Candidate serves the conformed ZIP page script

<details><summary>123 lines</summary>

```text
HTTP 200 
X-Request-Id: 184eae8a-a298-4ff0-860e-e06d7b5719eb
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791335472
Cache-Control: max-age=3600, public
Last-Modified: Wed, 07 Oct 2026 01:05:45 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 4117
Date: Wed, 07 Oct 2026 01:10:12 GMT
Connection: close

import { API } from './lib/api.js';

import { renderAlert } from './lib/status-message.js';

import { fetchJson } from './lib/util.js';



const hasDocument = typeof document !== 'undefined';

const lookupForm = hasDocument ? document.getElementById('zipCoordinateForm') : null;

const zipInput = hasDocument ? document.getElementById('zipCoordinateInput') : null;

const lookupButton = hasDocument ? document.getElementById('zipCoordinateButton') : null;

const alertBox = hasDocument ? document.getElementById('zipCoordinateAlert') : null;

const resultPanel = hasDocument ? document.getElementById('zipCoordinateResult') : null;



/** Normalize ZIP or ZIP+4 input into the five-digit lookup key the API accepts. */

export function normalizeZipInput(enteredZipCode) {

  const trimmedZipCode = String(enteredZipCode || '').trim();

  if (/^\d{5}$/.test(trimmedZipCode)) return trimmedZipCode;

  if (/^\d{5}-\d{4}$/.test(trimmedZipCode)) return trimmedZipCode.slice(0, 5);

  return '';

}



/** Build a same-origin API URL for display and copy actions. */

export function zipCoordinateApiUrl(origin, zipCode) {

  return `${String(origin || '').replace(/\/$/, '')}${API.location.zipCoordinate(zipCode)}`;

}



/** Build a curl command that exercises the public ZIP coordinate endpoint. */

export function zipCoordinateCurl(origin, zipCode) {

  return `curl '${zipCoordinateApiUrl(origin, zipCode)}'`;

}



function setTextOf(elementId, text) {

  const element = document.getElementById(elementId);

  if (element) element.textContent = text || '-';

}



function showAlert(message) {

  renderAlert(alertBox, message);

}



function hideAlert() {

  alertBox?.classList.add('d-none');

}



function renderCoordinate(coordinate) {

  const zipCode = coordinate?.zipCode || normalizeZipInput(zipInput?.value);

  const apiUrl = zipCoordinateApiUrl(window.location.origin, zipCode);



  setTextOf('zipCoordinateCode', zipCode);

  setTextOf('zipLatitude', coordinate?.latitude == null ? '' : String(coordinate.latitude));

  setTextOf('zipLongitude', coordinate?.longitude == null ? '' : String(coordinate.longitude));

  setTextOf('zipSource', coordinate?.source);

  setTextOf('zipSourceYear', coordinate?.sourceYear == null ? '' : String(coordinate.sourceYear));

  setTextOf('zipApiUrl', apiUrl);

  setTextOf('zipCurlOutput', zipCoordinateCurl(window.location.origin, zipCode));

  resultPanel?.classList.remove('d-none');

}



async function copyTextOf(sourceElement, copyButton) {

  if (!sourceElement || !copyButton) return;

  try {

    await navigator.clipboard.writeText(sourceElement.textContent || '');

    const originalLabel = copyButton.textContent;

    copyButton.textContent = 'Copied';

    setTimeout(() => { copyButton.textContent = originalLabel; }, 1200);

  } catch {

    showAlert('Unable to copy text. Please copy it manually.');

  }

}



lookupForm?.addEventListener('submit', async (event) => {

  event.preventDefault();

  hideAlert();

  const zipCode = normalizeZipInput(zipInput?.value);

  if (!zipCode) {

    resultPanel?.classList.add('d-none');

    showAlert('Enter a five-digit ZIP code or ZIP+4.');

    return;

  }



  try {

    if (lookupButton) lookupButton.disabled = true;

    const coordinate = await fetchJson(API.location.zipCoordinate(zipCode));

    renderCoordinate(coordinate);

  } catch (lookupFailure) {

    resultPanel?.classList.add('d-none');

    showAlert(lookupFailure.message || 'ZIP coordinate lookup failed.');

  } finally {

    if (lookupButton) lookupButton.disabled = false;

  }

});



zipInput?.addEventListener('input', () => {

  zipInput.value = zipInput.value.replace(/[^\d-]/g, '').slice(0, 10);

});



if (hasDocument) {

  document.getElementById('copyZipApiButton')?.addEventListener('click', () => {

    copyTextOf(document.getElementById('zipApiUrl'), document.getElementById('copyZipApiButton'));

  });



  document.getElementById('copyZipCurlButton')?.addEventListener('click', () => {

    copyTextOf(document.getElementById('zipCurlOutput'), document.getElementById('copyZipCurlButton'));

  });

}
```

</details>

### 8. Production 78701 lookup is unaffected (reference: production has imported data)

```text
exit code: 0
--- stdout ---
200 {'zipCode': '78701', 'latitude': 30.270569, 'longitude': -97.742589, 'source': 'Census Gazetteer ZCTA', 'sourceYear': 2025}
```

## Evidence
- Case 1 started 2026-10-06T20:10:11-05:00, took 62 ms, candidate `d64c12b`
- Case 2 started 2026-10-06T20:10:11-05:00, took 406 ms, candidate `unknown`
- Case 3 started 2026-10-06T20:10:12-05:00, took 32 ms, candidate `d64c12b`
- Case 4 started 2026-10-06T20:10:12-05:00, took 30 ms, candidate `d64c12b`
- Case 5 started 2026-10-06T20:10:12-05:00, took 31 ms, candidate `d64c12b`
- Case 6 started 2026-10-06T20:10:12-05:00, took 171 ms, candidate `d64c12b`
- Case 7 started 2026-10-06T20:10:12-05:00, took 30 ms, candidate `d64c12b`
- Case 8 started 2026-10-06T20:10:13-05:00, took 266 ms, candidate `unknown`

## Bugs / Follow-ups
- **Native checks on `d64c12b`:** `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` passed in 4m58s. Java: 2,243 tests, 0 failures or errors, 110 skipped. Focused suites: `LocationControllerSecurityTest` 2/2, `LocationControllerTest` 4/4, `ZipCoordinateGazetteerReaderTest` 4/4, `ZipCoordinateServiceTest` 6/6, `RestaurantServiceTest` 62/62 and `ModularMonolithArchitectureTest` 5/5. 390 JS tests passed, and the Pester suites passed.
- **Not exercised at runtime: the ADMIN Census import and re-import.** The application has no supported way to create a local ADMIN. A temporary promotion endpoint was refused by the session's safety classifier, and direct database writes are prohibited. `ZipCoordinateServiceTest` proves the restructured import: create, update, unchanged and stale counts, the saved and deleted rows, the checksum no-op, and that a parse failure writes nothing. Because of this gap, the empty test database returns 404 for real ZIP codes.
- **Post-deploy check:** production returned the `78701` coordinate before the deploy, and the same response is compared after the deploy.

## Document Status
complete

## Project
christopherbell-dev
