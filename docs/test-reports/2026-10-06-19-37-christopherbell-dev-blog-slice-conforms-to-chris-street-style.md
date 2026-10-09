# Blog slice conforms to Chris Street Style: Test Report

## Story/Issue
Slice 2 of the full Chris Street Style conformance migration; plan docs/implementation-plans/2026-10-06-19-31-christopherbell-dev-blog-slice-conforms-to-chris-street-style.md

## Branch
`claude/style-blog-20261006` at candidate `2acb67a`

## Pass / Fail

> [!TIP]
> 7 of 7 cases passed on candidate `2acb67a`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Candidate readiness on isolated MongoDB test | ✅ PASS | Expected status 200 and body containing '"UP"' |
| 2 | Blog post list returns the configured (empty) posts | ✅ PASS | Expected status 200 and body containing '"posts":[]' |
| 3 | Absent valid post ID returns the standard 404 envelope | ✅ PASS | Expected status 404 and body containing 'RESOURCE_NOT_FOUND' |
| 4 | Malformed post ID returns the standard 400 envelope | ✅ PASS | Expected status 400 and body containing 'REQUEST_ERROR' |
| 5 | Candidate serves the conformed blog component | ✅ PASS | Expected status 200 and body containing 'this.renderPosts(blogPostsFromResponse(postsResponse))' |
| 6 | List, 404 and 400 responses are byte-identical to production 0202b97b | ✅ PASS | Expected exit code 0 |
| 7 | Blog page has the blog mount and its app script inside body (line-ending independent) | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Candidate readiness on isolated MongoDB test**: http `GET http://127.0.0.1:56078/actuator/health/readiness`
2. **Blog post list returns the configured (empty) posts**: http `GET http://127.0.0.1:56078/api/blog/v1/posts`
3. **Absent valid post ID returns the standard 404 envelope**: http `GET http://127.0.0.1:56078/api/blog/v1/posts/00000000-0000-0000-0000-000000000000`
4. **Malformed post ID returns the standard 400 envelope**: http `GET http://127.0.0.1:56078/api/blog/v1/posts/not-a-uuid`
5. **Candidate serves the conformed blog component**: http `GET http://127.0.0.1:56078/js/components/blog.js`
6. **List, 404 and 400 responses are byte-identical to production 0202b97b**: command `python -c "`
7. **Blog page has the blog mount and its app script inside body (line-ending independent)**: command `python -c "`

## App / Environment

| Setting | Value |
|---|---|
| Profile | test |
| Database | test on a fresh disposable mongod 8.3 at 127.0.0.1:56077 (read back with db.getName()) |
| Candidate | packaged website.jar at 127.0.0.1:56078 |
| Baseline | production serving 0202b97b, fetched during the run |

## Local Run Details
- **Local command:** `GET http://127.0.0.1:56078/actuator/health/readiness` in `A:\Projects\christopherbell.dev-worktrees\style-blog`
- **Local command:** `GET http://127.0.0.1:56078/api/blog/v1/posts` in `A:\Projects\christopherbell.dev-worktrees\style-blog`
- **Local command:** `GET http://127.0.0.1:56078/api/blog/v1/posts/00000000-0000-0000-0000-000000000000` in `A:\Projects\christopherbell.dev-worktrees\style-blog`
- **Local command:** `GET http://127.0.0.1:56078/api/blog/v1/posts/not-a-uuid` in `A:\Projects\christopherbell.dev-worktrees\style-blog`
- **Local command:** `GET http://127.0.0.1:56078/js/components/blog.js` in `A:\Projects\christopherbell.dev-worktrees\style-blog`
- **Local command:** `python -c "` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Local command:** `python -c "` in `C:\Users\Christopher\AppData\Local\Temp\claude\A--Projects-builder\bc02e5cc-a8b4-4d99-84a5-e48233135236\scratchpad`
- **Candidate identity:** `2acb67a`
- **Cleanup:** Stopped candidate PID 33032 and mongod PID 82748 by process tree; ports 56078 and 56077 have zero listeners; production MongoDB 27017 (PID 5236) untouched; secrets were process-scoped.

## Data Sent

### 1. Candidate readiness on isolated MongoDB test

```http
GET http://127.0.0.1:56078/actuator/health/readiness
```

### 2. Blog post list returns the configured (empty) posts

```http
GET http://127.0.0.1:56078/api/blog/v1/posts
```

### 3. Absent valid post ID returns the standard 404 envelope

```http
GET http://127.0.0.1:56078/api/blog/v1/posts/00000000-0000-0000-0000-000000000000
```

### 4. Malformed post ID returns the standard 400 envelope

```http
GET http://127.0.0.1:56078/api/blog/v1/posts/not-a-uuid
```

### 5. Candidate serves the conformed blog component

```http
GET http://127.0.0.1:56078/js/components/blog.js
```

### 6. List, 404 and 400 responses are byte-identical to production 0202b97b

```text
python -c "
import glob
pairs=[(p,p.replace('blogcmp-prod','blogcmp-cand')) for p in sorted(glob.glob('blogcmp-prod*.json'))]
ok=True
for a,b in pairs:
    same=open(a,'rb').read()==open(b,'rb').read(); ok&=same; print(a[12:],'identical' if same else 'DIFFERENT')
raise SystemExit(0 if ok and len(pairs)==3 else 1)"
```

### 7. Blog page has the blog mount and its app script inside body (line-ending independent)

```text
python -c "
p=open('blog-page.html',encoding='utf-8').read()
mount=p.find('id=\"blog\"'); script=p.find('js/app.js\"></script>'); body_end=p.find('</body>')
print('mount',mount,'script',script,'body_end',body_end)
raise SystemExit(0 if 0<mount<script<body_end else 1)"
```

## Response Received

### 1. Candidate readiness on isolated MongoDB test

```text
HTTP 200 
X-Request-Id: 0bc74ab1-71c3-4ad8-857f-844c8bf3e440
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791333493
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
Date: Wed, 07 Oct 2026 00:37:13 GMT
Connection: close

{"status":"UP"}
```

### 2. Blog post list returns the configured (empty) posts

```text
HTTP 200 
X-Request-Id: 733f4b2c-47e6-4bd0-98f6-71808fe3d128
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791333493
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
Date: Wed, 07 Oct 2026 00:37:13 GMT
Connection: close

{"messages":null,"payload":{"posts":[]},"requestId":null,"success":true}
```

### 3. Absent valid post ID returns the standard 404 envelope

```text
HTTP 404 
X-Request-Id: 7c5ef4cf-eafe-4950-aecd-2342c7c19de2
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791333493
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
Date: Wed, 07 Oct 2026 00:37:13 GMT
Connection: close

{"messages":[{"code":"RESOURCE_NOT_FOUND","description":"The requested resource was not found."}],"payload":null,"requestId":null,"success":false}
```

### 4. Malformed post ID returns the standard 400 envelope

```text
HTTP 400 
X-Request-Id: c1cd49fc-954c-453c-a970-4db47d10e361
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791333493
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
Date: Wed, 07 Oct 2026 00:37:13 GMT
Connection: close

{"messages":[{"code":"REQUEST_ERROR","description":"The request is invalid."}],"payload":null,"requestId":null,"success":false}
```

### 5. Candidate serves the conformed blog component

<details><summary>104 lines</summary>

```text
HTTP 200 
X-Request-Id: 0b2819bd-dc61-4430-99aa-e9696149d156
Set-Cookie: [REDACTED]
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9999
X-RateLimit-Reset: 1791333494
Cache-Control: max-age=3600, public
Last-Modified: Wed, 07 Oct 2026 00:32:23 GMT
Accept-Ranges: bytes
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; font-src 'self' data: https://maxcdn.bootstrapcdn.com; img-src 'self' data: blob: https:; connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com; frame-ancestors 'self'; media-src 'self' blob:; worker-src 'self' blob:; form-action 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), geolocation=(), microphone=(), payment=(), usb=()
Content-Type: text/javascript
Content-Length: 2871
Date: Wed, 07 Oct 2026 00:37:14 GMT
Connection: close

/**

 * Public blog-post component.

 *

 * Fetches the versioned read API once and renders configured post text without interpreting HTML.

 */

import { API } from '../lib/api.js';

import { fetchJson } from '../lib/util.js';



/** Return a stable owned post collection from the standard API envelope. */

export function blogPostsFromResponse(response) {

    const posts = response?.payload?.posts ?? response?.posts;

    return Array.isArray(posts) ? [...posts] : [];

}



function appendTextElement(parentElement, tagName, className, text) {

    const textElement = document.createElement(tagName);

    if (className) textElement.className = className;

    textElement.textContent = String(text || '');

    parentElement.appendChild(textElement);

    return textElement;

}



class BlogPosts extends HTMLElement {

    connectedCallback() {

        this.renderEmptyContainer();

        this.loadPosts();

    }



    async loadPosts() {

        try {

            const postsResponse = await fetchJson(API.blog.posts);

            this.renderPosts(blogPostsFromResponse(postsResponse));

        } catch (error) {

            console.error('Failed to load posts', error);

        }

    }



    renderPosts(blogPosts) {

        const postsContainer = this.querySelector('.blogPosts');

        postsContainer.replaceChildren();



        if (blogPosts.length === 0) {

            appendTextElement(

                postsContainer,

                'p',

                'text-center blog-empty-state',

                'No posts have been published yet.'

            );

            return;

        }



        for (const blogPost of blogPosts) {

            postsContainer.appendChild(articleFor(blogPost));

        }

    }



    renderEmptyContainer() {

        const postsContainer = document.createElement('div');

        postsContainer.className = 'blogPosts';

        this.replaceChildren(postsContainer);

    }

}



function articleFor(blogPost) {

    const article = document.createElement('article');

    article.className = 'blogArticle';

    appendTextElement(article, 'h2', 'text-center', blogPost?.title);

    appendTextElement(article, 'h5', 'text-center', `Author: ${blogPost?.author || 'Unknown'}`);

    const publishedOn = blogPost?.createdOn ? new Date(blogPost.createdOn) : null;

    if (publishedOn && !Number.isNaN(publishedOn.getTime())) {

        const publishedOnElement = appendTextElement(

            article,

            'time',

            'd-block text-center',

            publishedOn.toLocaleDateString()

        );

        publishedOnElement.dateTime = publishedOn.toISOString();

    }

    article.appendChild(document.createElement('hr'));

    appendTextElement(article, 'pre', '', blogPost?.contentText);

    return article;

}



customElements.define('blog-posts', BlogPosts);
```

</details>

### 6. List, 404 and 400 responses are byte-identical to production 0202b97b

```text
exit code: 0
--- stdout ---
_api_blog_v1_posts.json identical
_api_blog_v1_posts_00000000-0000-0000-0000-000000000000.json identical
_api_blog_v1_posts_not-a-uuid.json identical
```

### 7. Blog page has the blog mount and its app script inside body (line-ending independent)

```text
exit code: 0
--- stdout ---
mount 2600 script 2777 body_end 2798
```

## Evidence
- Case 1 started 2026-10-06T19:37:13-05:00, took 32 ms, candidate `2acb67a`
- Case 2 started 2026-10-06T19:37:13-05:00, took 31 ms, candidate `2acb67a`
- Case 3 started 2026-10-06T19:37:13-05:00, took 47 ms, candidate `2acb67a`
- Case 4 started 2026-10-06T19:37:13-05:00, took 46 ms, candidate `2acb67a`
- Case 5 started 2026-10-06T19:37:14-05:00, took 30 ms, candidate `2acb67a`
- Case 6 started 2026-10-06T19:37:15-05:00, took 46 ms, candidate `unknown`
- Case 7 started 2026-10-06T19:37:27-05:00, took 32 ms, candidate `unknown`

## Bugs / Follow-ups
- **Native checks on `2acb67a`'s content:** `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` passed in 5m54s: 2,234 Java tests, 0 failures or errors, 110 skipped (blog: controller 4/4, service 6/6); 389 JS tests passed; Pester suites passed (184, 208, 76).
- **Harness note:** a first recording of the `/blog` page check expected LF line endings, but the template is served with CRLF. The page was correct. The check was rerecorded to compare the positions of the mount, script and closing `body` tag, and it passed. The failed artifact is excluded from the cases above.

## Document Status
complete

## Project
christopherbell-dev
