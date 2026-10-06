# Photo slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 1 of the full Chris Street Style conformance migration; plan docs/implementation-plans/2026-10-05-20-06-christopherbell-dev-photo-slice-conforms-to-chris-street-style.md

## Branch
`claude/style-photo-20261005` at candidate `190cfc0`

## Pass / Fail

> [!TIP]
> 6 of 6 cases passed on candidate `190cfc0`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Gallery API returns configured photos | ✅ PASS | Expected status 200 and body containing '"The River Walk - San Antonio"' |
| 3 | Photography usage page renders | ✅ PASS | Expected status 200 and body containing 'Photography Usage' |
| 4 | Candidate serves the conformed gallery component | ✅ PASS | Expected status 200 and body containing 'renderGallery(galleryImagesFromResponse(galleryResponse))' |
| 5 | Candidate gallery JSON is byte-identical to production baseline ef15adc0 | ✅ PASS | Expected exit code 0 |
| 6 | Photography page renders with gallery mount and app script inside body (rerun without shell path rewriting) | ✅ PASS | Expected status 200 and body containing 'js/app.js"></script>\n</body>' |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:49770/actuator/health/readiness`
2. **Gallery API returns configured photos**: http `GET http://127.0.0.1:49770/api/photo/v1`
3. **Photography usage page renders**: http `GET http://127.0.0.1:49770/photos/usage`
4. **Candidate serves the conformed gallery component**: http `GET http://127.0.0.1:49770/js/components/gallery.js`
5. **Candidate gallery JSON is byte-identical to production baseline ef15adc0**: command `python -c "a=open('photo-baseline-prod.json','rb').read();b=open('photo-candidate.json','rb').read();print(len(a),len(b),'identical' if a==b else 'DIFFERENT');raise SystemExit(0 if a==b else 1)"`
6. **Photography page renders with gallery mount and app script inside body (rerun without shell path rewriting)**: http `GET http://127.0.0.1:49770/photos`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:49769 (read back with db.getName()) |
| Candidate | packaged website.jar at 127.0.0.1:49770 |
| Baseline | production /api/photo/v1 serving ef15adc0, captured 2026-10-05 before the run |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:49770/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-photo`
- **Local command:** `GET http://127.0.0.1:49770/api/photo/v1` in `A:\Projects\christopherbell.dev-worktrees\style-photo`
- **Local command:** `GET http://127.0.0.1:49770/photos/usage` in `A:\Projects\christopherbell.dev-worktrees\style-photo`
- **Local command:** `GET http://127.0.0.1:49770/js/components/gallery.js` in `A:\Projects\christopherbell.dev-worktrees\style-photo`
- **Local command:** `python -c "a=open('photo-baseline-prod.json','rb').read();b=open('photo-candidate.json','rb').read();print(len(a),len(b),'identical' if a==b else 'DIFFERENT');raise SystemExit(0 if a==b else 1)"` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Local command:** `GET http://127.0.0.1:49770/photos` in `A:\Projects\christopherbell.dev-worktrees\style-photo`
- **Candidate identity:** `190cfc0`
- **Cleanup:** Stopped candidate PID 33260 and mongod PID 45188 by process tree; ports 49770 and 49769 have zero listeners; production MongoDB 27017 (PID 5236) untouched; secrets were process-scoped.

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:49770/actuator/health/readiness
```

### 2. Gallery API returns configured photos

```http
GET http://127.0.0.1:49770/api/photo/v1
```

### 3. Photography usage page renders

```http
GET http://127.0.0.1:49770/photos/usage
```

### 4. Candidate serves the conformed gallery component

```http
GET http://127.0.0.1:49770/js/components/gallery.js
```

### 5. Candidate gallery JSON is byte-identical to production baseline ef15adc0

```text
python -c "a=open('photo-baseline-prod.json','rb').read();b=open('photo-candidate.json','rb').read();print(len(a),len(b),'identical' if a==b else 'DIFFERENT');raise SystemExit(0 if a==b else 1)"
```

### 6. Photography page renders with gallery mount and app script inside body (rerun without shell path rewriting)

```http
GET http://127.0.0.1:49770/photos
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: 964dc1b1-0fd7-43d6-9161-f76dc5f76f59
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791249358
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
Date: Tue, 06 Oct 2026 01:14:58 GMT
Connection: close

{"status":"UP"}
```

### 2. Gallery API returns configured photos

```text
HTTP 200 
X-Request-Id: bc93435a-928b-4055-8720-7ce132016671
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791249358
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
Date: Tue, 06 Oct 2026 01:14:58 GMT
Connection: close

{"messages":null,"payload":{"images":[{"createdOn":null,"description":"n/a","id":"18e1e89a-b739-4dab-9cf9-4d3bebc1f928","name":"The River Walk - San Antonio","path":"/images/photos/IMG_0072.jpeg"},{"createdOn":null,"description":"n/a","id":"3a592438-de79-4842-a0b1-9aed06605486","name":"The Gardens - Denver","path":"/images/photos/IMG_0130.jpeg"},{"createdOn":null,"description":"n/a","id":"8f9fce4e-8093-4e73-a632-aba3e1ee1cf9","name":"The Strip - Las Vegas","path":"/images/photos/IMG_0257.jpeg"},{"createdOn":null,"description":"n/a","id":"15edb715-6483-4a2f-b2fb-0b222c030b79","name":"The Lake - New Orleans","path":"/images/photos/IMG_0390.jpeg"},{"createdOn":null,"description":"n/a","id":"83bc23a3-ffd4-4892-b507-a7e8b1f02915","name":"The Austin Skyline - Austin","path":"/images/photos/IMG_0691.jpeg"},{"createdOn":null,"description":"n/a","id":"12263e26-7e86-4d0d-b034-f879544bbc7f","name":"Parakeet Eats - New Orleans","path":"/images/photos/IMG_0947.jpeg"},{"createdOn":null,"description":"n/a","id":"e7d02bf8-a44d-4d49-8ca4-69353560bff0","name":"The Beach - Miami Beach","path":"/images/photos/IMG_1614.jpeg"},{"createdOn":null,"description":"n/a","id":"84718af6-6621-4a83-93a7-f96235091cce","name":"The Colorado River - Austin","path":"/images/photos/IMG_1666.JPG"},{"createdOn":null,"description":"n/a","id":"224bd926-1937-4a27-96cb-97246b0a88e1","name":"The Austin Skyline 2 - Austin","path":"/images/photos/IMG_1668.JPG"},{"createdOn":null,"description":"n/a","id":"c80bb479-4e2e-4352-928a-f44afe1c163a","name":"NA Miata - Austin","path":"/images/photos/IMG_1350.jpeg"},{"createdOn":null,"description":"The outside view of the building that contains the Tropical Plants from the Denver Botanic Gardens.","id":"9c8f4cb5-33c1-462b-8f15-8a1ea9da4968","name":"Denver Botanic Gardens - Outside Tropical Plants Enclosure","path":"/images/photos/IMG_1854.jpeg"},{"createdOn":null,"description":"n/a","id":"551d3fd2-addc-4b7f-9921-eec9b4c2158c","name":"Denver Botanic Gardens","path":"/images/photos/IMG_1836.jpeg"}]},"requestId":null,"success":true}
```

### 3. Photography usage page renders

<details><summary>75 lines</summary>

```text
HTTP 200 
X-Request-Id: 213a5533-2f3a-48a5-aa14-af7f64280720
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791249359
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
Date: Tue, 06 Oct 2026 01:14:59 GMT
Connection: close

<!DOCTYPE html>

<html lang="en">



<head>

    <meta charset="utf-8" />

    <meta name="viewport" content="width=device-width, initial-scale=1" />

    <meta name="author" content="Christopher Bell" />

    <meta name="keywords" content="cbell,photography" />

    

    <meta name="description" content="Photography usage terms for christopherbell.dev." />

    

    <link rel="canonical" href="https://www.christopherbell.dev/photos/usage" />



    <meta property="og:site_name" content="christopherbell.dev" />

    <meta property="og:locale" content="en_US" />

    <meta property="og:type" content="website" />

    <meta property="og:title" content="CB | Photography Usage" />

    <meta property="og:description" content="Photography usage terms for christopherbell.dev." />

    <meta property="og:url" content="https://www.christopherbell.dev/photos/usage" />

    <meta property="og:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta property="og:image:secure_url" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta property="og:image:type" content="image/png" />

    <meta property="og:image:width" content="1200" />

    <meta property="og:image:height" content="630" />

    <meta property="og:image:alt" content="The Void preview for christopherbell.dev" />



    <meta name="twitter:card" content="summary_large_image" />

    <meta name="twitter:title" content="CB | Photography Usage" />

    <meta name="twitter:description" content="Photography usage terms for christopherbell.dev." />

    <meta name="twitter:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta name="twitter:image:alt" content="The Void preview for christopherbell.dev" />

    <meta name="theme-color" content="#17202a" />

  



    <title>CB | Photography Usage</title>



    <link rel="stylesheet" type="text/css" href="/e8a820f9787dd0e3154c/css/main.css"/>

</head>



<body>

    <div id="nav"></div>

    <main role="main" class="container">

        <div class="row">

            <div class="col">

                <h1>Photography Usage</h1>

                <p>Usage of the images on this site is forbidden without written consent from the owner.</p>

            </div>

        </div>

    </main>

    <footer id="footer"></footer>

    <script type="module" src="/e8a820f9787dd0e3154c/js/app.js"></script>

</body>



</html>
```

</details>

### 4. Candidate serves the conformed gallery component

<details><summary>82 lines</summary>

```text
HTTP 200 
X-Request-Id: fb3430c0-b731-4bcc-9b9c-b8f5d419e0ba
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791249359
Cache-Control: max-age=3600, public
Last-Modified: Tue, 06 Oct 2026 01:10:18 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 2392
Date: Tue, 06 Oct 2026 01:14:59 GMT
Connection: close

/**
 * Public photo-gallery component.
 *
 * Fetches configured image metadata and renders content images with meaningful alternatives.
 */
import { API } from '../lib/api.js';
import { fetchJson } from '../lib/util.js';

/** Return a stable owned image collection from the standard API envelope. */
export function galleryImagesFromResponse(response) {
    const images = response?.payload?.images ?? response?.images;
    return Array.isArray(images) ? [...images] : [];
}

/** Content images prefer their description, then name, then an honest generic fallback. */
export function galleryAltText(image) {
    const description = String(image?.description || '').trim();
    const usableDescription = /^n\/a$/i.test(description) ? '' : description;
    return usableDescription || String(image?.name || '').trim() || 'Gallery photo';
}

class PhotoGallery extends HTMLElement {
    connectedCallback() {
        this.renderEmptyGallery();
        this.loadGallery();
    }

    async loadGallery() {
        try {
            const galleryResponse = await fetchJson(API.photos.images);
            this.renderGallery(galleryImagesFromResponse(galleryResponse));
        } catch (error) {
            console.error('Failed to load gallery images', error);
        }
    }

    renderGallery(galleryImages) {
        const galleryRow = this.querySelector('.gallery-row');
        galleryRow.replaceChildren();
        for (const galleryImage of galleryImages) {
            const imageColumn = document.createElement('div');
            imageColumn.className = 'col';
            const imageElement = document.createElement('img');
            imageElement.src = String(galleryImage?.path || '');
            imageElement.className = 'img-fluid rounded';
            imageElement.alt = galleryAltText(galleryImage);
            imageColumn.appendChild(imageElement);
            galleryRow.appendChild(imageColumn);
        }
    }

    renderEmptyGallery() {
        const galleryContainer = document.createElement('div');
        galleryContainer.className = 'container-fluid';
        const galleryRow = document.createElement('div');
        galleryRow.className = 'row row-cols-1 row-cols-sm-1 row-cols-md-2 g-2 gallery-row';
        galleryContainer.appendChild(galleryRow);
        this.replaceChildren(galleryContainer);
    }
}

customElements.define('photo-gallery', PhotoGallery);
```

</details>

### 5. Candidate gallery JSON is byte-identical to production baseline ef15adc0

```text
exit code: 0
--- stdout ---
2059 2059 identical
```

### 6. Photography page renders with gallery mount and app script inside body (rerun without shell path rewriting)

<details><summary>80 lines</summary>

```text
HTTP 200 
X-Request-Id: 56f1e9d3-84c8-4099-9507-86fcaceb0797
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791249371
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
Date: Tue, 06 Oct 2026 01:15:11 GMT
Connection: close

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="author" content="Christopher Bell" />
    <meta name="keywords" content="cbell,photography" />
    

    <meta name="description" content="Photography from Christopher Bell." />

    

    <link rel="canonical" href="https://www.christopherbell.dev/photos" />



    <meta property="og:site_name" content="christopherbell.dev" />

    <meta property="og:locale" content="en_US" />

    <meta property="og:type" content="website" />

    <meta property="og:title" content="CB | Photography" />

    <meta property="og:description" content="Photography from Christopher Bell." />

    <meta property="og:url" content="https://www.christopherbell.dev/photos" />

    <meta property="og:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta property="og:image:secure_url" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta property="og:image:type" content="image/png" />

    <meta property="og:image:width" content="1200" />

    <meta property="og:image:height" content="630" />

    <meta property="og:image:alt" content="The Void preview for christopherbell.dev" />



    <meta name="twitter:card" content="summary_large_image" />

    <meta name="twitter:title" content="CB | Photography" />

    <meta name="twitter:description" content="Photography from Christopher Bell." />

    <meta name="twitter:image" content="https://www.christopherbell.dev/images/previews/christopherbell-dev.png" />

    <meta name="twitter:image:alt" content="The Void preview for christopherbell.dev" />

    <meta name="theme-color" content="#17202a" />

  

    <title>CB | Photography</title>

    <link rel="stylesheet" type="text/css" href="/e8a820f9787dd0e3154c/css/main.css"/>
</head>

<body class="site-page photo-page">
    <div id="nav"></div>
    <main class="site-main">
        <section class="site-hero site-hero-photo" aria-labelledby="photoTitle">
            <div class="container">
                <p class="home-kicker">Gallery</p>
                <h1 id="photoTitle">Photo Gallery</h1>
                <p>Places, streets, skylines, and other things worth keeping around.</p>
                <p><a href="/photos/usage">Photography usage</a></p>
            </div>
        </section>
        <section class="site-content">
            <div class="container-fluid gallery-panel" id="gallery"></div>
        </section>
    </main>
    <footer id="footer"></footer>
    <script type="module" src="/e8a820f9787dd0e3154c/js/app.js"></script>
</body>

</html>
```

</details>

## Evidence
- Case 1 started 2026-10-05T20:14:58-05:00, took 31 ms, candidate `190cfc0`
- Case 2 started 2026-10-05T20:14:58-05:00, took 47 ms, candidate `190cfc0`
- Case 3 started 2026-10-05T20:14:59-05:00, took 46 ms, candidate `190cfc0`
- Case 4 started 2026-10-05T20:14:59-05:00, took 32 ms, candidate `190cfc0`
- Case 5 started 2026-10-05T20:14:59-05:00, took 16 ms, candidate `unknown`
- Case 6 started 2026-10-05T20:15:11-05:00, took 31 ms, candidate `190cfc0`

## Bugs / Follow-ups
- **Native checks on `190cfc0`'s content:** `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` passed in 5m03s: 2,215 Java tests, 0 failures or errors, 110 skipped; 382 JS tests passed; Pester suites passed (184, 208, 76). Baseline photo tests before editing passed 3/3, and JS passed 382/382.
- **Harness note:** a first recording of the `/photos` case failed only because Git Bash rewrote the expected text `/js/app.js` into a Windows path. The served page did contain the script. The case was rerun with `MSYS_NO_PATHCONV=1` and passed; the failed artifact is excluded from the cases above.
- **Follow-up (umbrella plan):** configuration key `date-added` never binds to `Photo.createdOn`, so the API always reports `createdOn: null`. Fixing that changes the JSON contract and is left for a separate decision.

## Document Status
complete

## Project
christopherbell-dev
