# Implement Bootstrap WebJar Asset Repair

## Document Status

Complete

## Objective

Repair azurras/christopherbell.dev#1339 by aligning Bootstrap asset references
and anonymous security matchers with packaged Bootstrap 5.3.8, then guard the
dependency/reference contract against future drift.

## Goals

- Serve Bootstrap 5.3.8 CSS and JavaScript anonymously.
- Remove stale 5.3.3 runtime references.
- Preserve GET-only, exact-version static-resource authorization.
- Prove the fix locally, in CI, and in production.

## Inputs

- Spec: docs/specs/2026-08-02-restore-bootstrap-assets-after-webjar-version-bump.md.
- Work: docs/work/2026-08-02-christopherbell-dev-bootstrap-asset-regression.md.
- Issue: azurras/christopherbell.dev#1339.
- Root cause: dependency commit 20290b2f updated only the WebJar dependency;
  production old paths return 404 and actual 5.3.8 paths return 403.

## Branch

- Base: origin/main at 2b40bd860d9e4e05aa18b4dd63e13a390d41208e.
- Branch: codex/issue-1339-bootstrap-assets.
- Worktree: A:\Projects\christopherbell.dev-worktrees\bootstrap-assets-1339.

## Non-Goals

No redesign, CDN, new dependency, Bootstrap upgrade beyond 5.3.8, unrelated
refactor, or authoritative-checkout modification.

## Assumptions

Bootstrap 5.3.8 is the intended pin; Spring Boot serves its versioned WebJar
namespace; JavaScript tests run from repository root; main deploys automatically.

## Open Questions

None.

## Task Breakdown

### Task 1 - Add dependency/reference drift regression coverage

Sequence / dependencies:

First task. Run the new test before production edits and retain the RED output.

Implementation notes:

- Required skill: chris-street-style before any code edits.
- Invoke superpowers:test-driven-development before editing.
- Before-Edit Brief:
  - Behavior: derive the pin from Gradle and reject another Bootstrap version
    embedded in production resources or security sources.
  - Invariants: self-hosting and the CDN prohibition remain enforced.
  - Boundary/API: test-only Node filesystem inspection.
  - Effects and failures: deterministic tracked-file reads; failure names file/reference.
  - Tests and evidence: targeted Node RED before Tasks 2-4 and GREEN after.

#### Code Edit 1.1

- File: website/src/test/js/public-content.test.js
- Lines: after 14
- Action: add

Proposed:

```javascript
function bootstrapVersion() {
  const build = fs.readFileSync('website/build.gradle.kts', 'utf8');
  const dependency = build.match(/implementation\("org\.webjars:bootstrap:([^"]+)"\)/);
  assert.ok(dependency, 'website/build.gradle.kts must pin the Bootstrap WebJar');
  return dependency[1];
}
```

Verification:

- node --test --test-name-pattern="Bootstrap" website/src/test/js/public-content.test.js

#### Code Edit 1.2

- File: website/src/test/js/public-content.test.js
- Lines: 72-84
- Action: replace

Current:

```javascript
test('Bootstrap is self-hosted and no CDN include remains', () => {
  const mainCss = fs.readFileSync('website/src/main/resources/static/css/main.css', 'utf8');
  assert.match(mainCss, /\/webjars\/bootstrap\/5\.3\.3\/css\/bootstrap\.min\.css/);

  for (const file of filesUnder('website/src/main/resources')) {
    if (!/\.(?:css|html)$/i.test(file)) continue;
    assert.doesNotMatch(
      fs.readFileSync(file, 'utf8'),
      /cdn\.jsdelivr\.net\/npm\/bootstrap/i,
      file
    );
  }
});
```

Proposed:

```javascript
test('Bootstrap WebJar references match the packaged dependency', () => {
  const expectedVersion = bootstrapVersion();
  const roots = [
    'website/src/main/resources',
    'website/src/main/java/dev/christopherbell/configuration/security',
  ];

  for (const file of roots.flatMap(filesUnder)) {
    if (!/\.(?:css|html|java|md)$/i.test(file)) continue;
    const source = fs.readFileSync(file, 'utf8');
    for (const match of source.matchAll(/\/webjars\/bootstrap\/([^/]+)\//g)) {
      assert.equal(match[1], expectedVersion, file + ': ' + match[0]);
    }
  }
});

test('Bootstrap is self-hosted and no CDN include remains', () => {
  const mainCss = fs.readFileSync('website/src/main/resources/static/css/main.css', 'utf8');
  assert.ok(mainCss.includes(
    '/webjars/bootstrap/' + bootstrapVersion() + '/css/bootstrap.min.css'
  ));

  for (const file of filesUnder('website/src/main/resources')) {
    if (!/\.(?:css|html)$/i.test(file)) continue;
    assert.doesNotMatch(
      fs.readFileSync(file, 'utf8'),
      /cdn\.jsdelivr\.net\/npm\/bootstrap/i,
      file
    );
  }
});
```

Verification:

- RED names 5.3.3 versus 5.3.8; GREEN after Tasks 2-4.

### Task 2 - Align browser resource references with Bootstrap 5.3.8

Sequence / dependencies:

Runs after Task 1 RED; security access follows in Task 3.

Implementation notes:

- Required skill: chris-street-style before any code edits.
- Before-Edit Brief:
  - Behavior: CSS imports and Bootstrap-loading pages request 5.3.8.
  - Invariants: self-hosting, script order, markup, and custom assets stay fixed.
  - Boundary/API: browser resource URLs only.
  - Effects and failures: browsers request packaged paths; Task 3 permits them.
  - Tests and evidence: source-contract GREEN and anonymous HTTP 200.
#### Code Edit 2.1

- File: website/src/main/resources/static/css/main.css
- Lines: 1
- Action: replace

Current:

```css
@import url("/webjars/bootstrap/5.3.3/css/bootstrap.min.css");
```

Proposed:

```css
@import url("/webjars/bootstrap/5.3.8/css/bootstrap.min.css");
```

Verification:

- rg -n "webjars/bootstrap" website/src/main/resources/static/css/main.css
#### Code Edit 2.2

- File: website/src/main/resources/static/dev/feed-harness.html
- Lines: 7
- Action: replace

Current:

```html
  <link href="/webjars/bootstrap/5.3.3/css/bootstrap.min.css" rel="stylesheet">
```

Proposed:

```html
  <link href="/webjars/bootstrap/5.3.8/css/bootstrap.min.css" rel="stylesheet">
```

Verification:

- rg -n "webjars/bootstrap" website/src/main/resources/static/dev/feed-harness.html
#### Code Edit 2.3

- File: website/src/main/resources/templates/back-office.html
- Lines: 410
- Action: replace

Current:

```html
  <script src="/webjars/bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
```

Proposed:

```html
  <script src="/webjars/bootstrap/5.3.8/js/bootstrap.bundle.min.js"></script>
```

Verification:

- rg -n "webjars/bootstrap" website/src/main/resources/templates/back-office.html
#### Code Edit 2.4

- File: website/src/main/resources/templates/forgot-password.html
- Lines: 41
- Action: replace

Current:

```html
  <script src="/webjars/bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
```

Proposed:

```html
  <script src="/webjars/bootstrap/5.3.8/js/bootstrap.bundle.min.js"></script>
```

Verification:

- rg -n "webjars/bootstrap" website/src/main/resources/templates/forgot-password.html
#### Code Edit 2.5

- File: website/src/main/resources/templates/login.html
- Lines: 46
- Action: replace

Current:

```html
  <script src="/webjars/bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
```

Proposed:

```html
  <script src="/webjars/bootstrap/5.3.8/js/bootstrap.bundle.min.js"></script>
```

Verification:

- rg -n "webjars/bootstrap" website/src/main/resources/templates/login.html
#### Code Edit 2.6

- File: website/src/main/resources/templates/messages.html
- Lines: 84
- Action: replace

Current:

```html
  <script src="/webjars/bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
```

Proposed:

```html
  <script src="/webjars/bootstrap/5.3.8/js/bootstrap.bundle.min.js"></script>
```

Verification:

- rg -n "webjars/bootstrap" website/src/main/resources/templates/messages.html
#### Code Edit 2.7

- File: website/src/main/resources/templates/notifications.html
- Lines: 59
- Action: replace

Current:

```html
  <script src="/webjars/bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
```

Proposed:

```html
  <script src="/webjars/bootstrap/5.3.8/js/bootstrap.bundle.min.js"></script>
```

Verification:

- rg -n "webjars/bootstrap" website/src/main/resources/templates/notifications.html
#### Code Edit 2.8

- File: website/src/main/resources/templates/post.html
- Lines: 65
- Action: replace

Current:

```html
  <script src="/webjars/bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
```

Proposed:

```html
  <script src="/webjars/bootstrap/5.3.8/js/bootstrap.bundle.min.js"></script>
```

Verification:

- rg -n "webjars/bootstrap" website/src/main/resources/templates/post.html
#### Code Edit 2.9

- File: website/src/main/resources/templates/profile.html
- Lines: 111
- Action: replace

Current:

```html
  <script src="/webjars/bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
```

Proposed:

```html
  <script src="/webjars/bootstrap/5.3.8/js/bootstrap.bundle.min.js"></script>
```

Verification:

- rg -n "webjars/bootstrap" website/src/main/resources/templates/profile.html
#### Code Edit 2.10

- File: website/src/main/resources/templates/reset-password.html
- Lines: 45
- Action: replace

Current:

```html
  <script src="/webjars/bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
```

Proposed:

```html
  <script src="/webjars/bootstrap/5.3.8/js/bootstrap.bundle.min.js"></script>
```

Verification:

- rg -n "webjars/bootstrap" website/src/main/resources/templates/reset-password.html
#### Code Edit 2.11

- File: website/src/main/resources/templates/signup.html
- Lines: 81
- Action: replace

Current:

```html
  <script src="/webjars/bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
```

Proposed:

```html
  <script src="/webjars/bootstrap/5.3.8/js/bootstrap.bundle.min.js"></script>
```

Verification:

- rg -n "webjars/bootstrap" website/src/main/resources/templates/signup.html
#### Code Edit 2.12

- File: website/src/main/resources/templates/user.html
- Lines: 78
- Action: replace

Current:

```html
  <script src="/webjars/bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
```

Proposed:

```html
  <script src="/webjars/bootstrap/5.3.8/js/bootstrap.bundle.min.js"></script>
```

Verification:

- rg -n "webjars/bootstrap" website/src/main/resources/templates/user.html
### Task 3 - Permit the packaged namespace and update security tests

Sequence / dependencies:

Runs after Task 2 so the opened namespace equals the referenced namespace.

Implementation notes:

- Required skill: chris-street-style before any code edits.
- Before-Edit Brief:
  - Behavior: anonymous GETs to 5.3.8 are public static assets.
  - Invariants: only GET and only Bootstrap 5.3.8 are permitted.
  - Boundary/API: Spring Security authorization and authentication-skip matching.
  - Effects and failures: valid resources reach the handler; other paths do not.
  - Tests and evidence: SecurityConfigTest and anonymous local HTTP.

#### Code Edit 3.1

- File: website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java
- Lines: 132
- Action: replace

Current:

```java
      "GET:/webjars/bootstrap/5.3.3/**",
```

Proposed:

```java
      "GET:/webjars/bootstrap/5.3.8/**",
```

Verification:

- .\gradlew.bat :website:test --tests dev.christopherbell.configuration.SecurityConfigTest --no-daemon

#### Code Edit 3.2

- File: website/src/main/java/dev/christopherbell/configuration/security/StaticAssetRequestMatcher.java
- Lines: 17
- Action: replace

Current:

```java
      get("/webjars/bootstrap/5.3.3/**"),
```

Proposed:

```java
      get("/webjars/bootstrap/5.3.8/**"),
```

Verification:

- .\gradlew.bat :website:test --tests dev.christopherbell.configuration.SecurityConfigTest --no-daemon

#### Code Edit 3.3

- File: website/src/test/java/dev/christopherbell/configuration/SecurityConfigTest.java
- Lines: 191-205
- Action: replace

Current:

```java
  @Test
  @DisplayName("Only GET public-content APIs and the pinned Bootstrap WebJar are public")
  void publicContentMatchersAreGetOnly() throws Exception {
    var paths = List.of(
        "/api/blog/v1/posts",
        "/api/blog/v1/posts/post-1",
        "/api/photo/v1",
        "/webjars/bootstrap/5.3.3/css/bootstrap.min.css",
        "/webjars/bootstrap/5.3.3/js/bootstrap.bundle.min.js");

    for (var path : paths) {
      assertTrue(publicMatchers().stream().anyMatch(matcher -> matcher.matches(request("GET", path))));
      assertFalse(publicMatchers().stream().anyMatch(matcher -> matcher.matches(request("POST", path))));
    }
  }
```

Proposed:

```java
  @Test
  @DisplayName("Only GET public-content APIs and the pinned Bootstrap WebJar are public")
  void publicContentMatchersAreGetOnly() throws Exception {
    var paths = List.of(
        "/api/blog/v1/posts",
        "/api/blog/v1/posts/post-1",
        "/api/photo/v1",
        "/webjars/bootstrap/5.3.8/css/bootstrap.min.css",
        "/webjars/bootstrap/5.3.8/js/bootstrap.bundle.min.js");

    for (var path : paths) {
      assertTrue(publicMatchers().stream().anyMatch(matcher -> matcher.matches(request("GET", path))));
      assertFalse(publicMatchers().stream().anyMatch(matcher -> matcher.matches(request("POST", path))));
    }
    assertFalse(publicMatchers().stream().anyMatch(matcher ->
        matcher.matches(request("GET", "/webjars/bootstrap/5.3.3/css/bootstrap.min.css"))));
    assertFalse(publicMatchers().stream().anyMatch(matcher ->
        matcher.matches(request("GET", "/webjars/other/1.0.0/example.js"))));
  }
```

Verification:

- .\gradlew.bat :website:test --tests dev.christopherbell.configuration.SecurityConfigTest --no-daemon

### Task 4 - Synchronize pinned-version documentation

Sequence / dependencies:

Runs after Tasks 2-3 so guidance describes implemented behavior.

Implementation notes:

- Required skill: chris-street-style before editing behavior documentation.
- Before-Edit Brief:
  - Behavior: guidance names 5.3.8 as the served pin.
  - Invariants: self-hosting and least privilege remain unchanged.
  - Boundary/API: documentation only.
  - Effects and failures: no runtime effect; Task 1 scans both READMEs.
  - Tests and evidence: targeted Node test and stale-version search.

#### Code Edit 4.1

- File: website/src/main/java/dev/christopherbell/configuration/security/README.md
- Lines: 28-29
- Action: replace

Current:

```markdown
- The blog list/detail APIs, photo list API, and exact Bootstrap 5.3.3 WebJar paths are public for
  `GET` only.
```

Proposed:

```markdown
- The blog list/detail APIs, photo list API, and exact Bootstrap 5.3.8 WebJar paths are public for
  `GET` only.
```

Verification:

- rg -n --fixed-strings "5.3.3" website/src/main/java/dev/christopherbell/configuration/security

#### Code Edit 4.2

- File: website/src/main/resources/static/css/README.md
- Lines: 25
- Action: replace

Current:

```markdown
- `main.css` imports the pinned, application-served Bootstrap 5.3.3 WebJar once; current templates must not add a second Bootstrap stylesheet or a Bootstrap CDN URL.
```

Proposed:

```markdown
- `main.css` imports the pinned, application-served Bootstrap 5.3.8 WebJar once; current templates must not add a second Bootstrap stylesheet or a Bootstrap CDN URL.
```

Verification:

- rg -n --fixed-strings "5.3.3" website/src/main/resources/static/css

## Code Changes

Dependency-derived Node contract; 5.3.8 resource URLs in CSS/harness/templates;
5.3.8 security matchers and tests; synchronized security/CSS documentation.

## Files and Modules

Website browser resources/templates, configuration security, and Java/Node tests.

## Unit Testing

1. RED targeted Bootstrap Node test.
2. GREEN targeted Bootstrap Node and SecurityConfigTest.
3. .\gradlew.bat :website:jsTest --no-daemon.
4. .\gradlew.bat :website:check --no-daemon --stacktrace.
5. rg stale 5.3.3 across website/src/main and website/src/test.

Use private A:\Temp\christopherbell-bootstrap-1339-gradle.

## Local Testing

Build the packaged JAR; start on a non-8080 port; request /, /login, /signup,
both 5.3.8 assets and obsolete 5.3.3 paths; record request/status/content
type/signature/length; use the in-app browser to verify Bootstrap computed
styling and references; stop only the alternate-port process.

## Validation

RED proves drift, focused/full tests pass, alternate-port CSS/JS return 200
anonymously, old paths do not, browser rendering is restored, required CI passes,
and public production assets/pages pass after deployment.

## Rollback or Recovery

Before merge revert only the branch commit. After merge use a normal revert PR.
If deployment stalls, leave #1339 open and diagnose without weakening ACLs. Do
not merge without equivalent runtime proof.

## Risks

Missed templates are caught by recursive scan; URL/security mismatch by dual
matcher tests and HTTP; broad authorization by exact-version/GET negative tests;
stale production by listener/exact-asset verification; dirty checkout loss by
isolated worktree.

## Completion Criteria

All edits implemented without unrelated changes; no stale 5.3.3 reference;
focused Node/Java, jsTest, and website:check pass; alternate-port browser/runtime
passes; Builder test report is saved/validated/pushed; PR/CI/merge complete;
production serves 5.3.8 assets with 200; issue #1339 closes; Builder closure and
session memory are indexed, validated, and pushed.
