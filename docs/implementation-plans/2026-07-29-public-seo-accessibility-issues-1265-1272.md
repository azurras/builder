# Public SEO and Accessibility Issues 1265-1272 Implementation Plan

## Document Status

complete

## Objective

Resolve #1265-#1272 by making crawler policy explicit, returning resource-specific public metadata and true 404s, generating the sitemap from current public data, correcting WFL and The Bell markup, eliminating ambiguous button behavior, and adding standard authentication autocomplete metadata.

## Goals

- Render `noindex,nofollow` for authentication, private, and administrative shells without marking public content private.
- Render a non-indexable 404 page without a home-page canonical, while preserving HTTP 404 for unknown routes and missing dynamic resources.
- Render canonical, resource-specific metadata for active profiles, active posts, and existing restaurants.
- Give `/wfl/top-rated` its own canonical and keep `/wfl/favorites` out of indexing and sitemap discovery.
- Build valid sitemap documents from an explicit public-route registry plus active profiles/posts and existing restaurants, with deterministic ordering, canonical escaping, and 50,000-URL splitting.
- Give both The Bell pages one H1, one main landmark, logical headings, and hardened new-tab links.
- Require explicit button types in static and dynamically rendered controls.
- Add `name` and standard `autocomplete` tokens to login, signup, forgot-password, and reset-password fields.

## Inputs

- Campaign spec: `docs/specs/2026-07-29-complete-christopherbell-dev-issues-1258-1307.md`.
- GitHub issues #1265-#1272, authored by `azurras`, with zero comments or attachments.
- Merged baseline `origin/main` at `e393687d10c40b856f35d669c25bf3ea65c5c083`.
- Batch 1 production is healthy and its seven issues are closed.
- Mandatory test-first execution and `chris-street-style` before code edits.

## Branch

Execute on `codex/issues-1265-1272-20260729` in `A:\Projects\christopherbell.dev-worktrees\issues-1265-1272-20260729`, based on `origin/main` at `e393687d`.

## Non-Goals

- Redesigning page visual styles or JavaScript application behavior beyond required server-rendered metadata.
- Indexing authentication-only resources, WFL favorites, messages, reports, Shared Folder, Music, Back Office, or Command Center.
- Publishing API endpoints in the sitemap.
- Adding a separate addressable blog-detail route; the current blog is one aggregate public page and remains one registered sitemap URL.
- Replacing Spring MVC, Thymeleaf, Mongo repositories, or the existing social-preview fragment.

## Assumptions

- Active accounts have public `/u/{username}` pages; suspended/deleted accounts must be excluded and return 404.
- Posts are eligible only while `expiresOn` is strictly after the injected clock instant; TTL cleanup lag must not expose expired URLs.
- Every persisted WFL restaurant has a public profile route and is sitemap-eligible.
- The sitemap protocol limit is 50,000 URLs per document; `/sitemap.xml` may be a `urlset` for one page or a `sitemapindex` pointing at numbered shards when the limit is exceeded.
- Existing post preview resolution remains the authority for `/p/{postId}` metadata and expiration-aware 404 behavior.

## Open Questions

None.

## Task Breakdown

### Task 1 - Centralize indexing policy and repair WFL/404 rules (#1265, #1266, #1268)

Sequence / dependencies:
- Runs first because dynamic pages and sitemap generation must consume the same public/private classification.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: private/auth/admin shells render `noindex,nofollow`; top-rated is canonical and indexable; favorites is self-canonical but non-indexable; every 404 is non-indexable and never canonicalizes to home.
  - Invariants: public pages remain indexable; HTTP status ownership stays in controllers/error handling; social metadata remains escaped by Thymeleaf.
  - Boundary/API: a small view-indexing helper owns model keys and the shared social fragment emits the robots tag.
  - Effects and failures: indexing metadata is response-only; absent model metadata means public/indexable; missing dynamic resources fail with 404 rather than a generic 200 shell.
  - Tests and evidence: add failing rendered-route tests for every private route, WFL modes, unknown HTML, and vanished post before changing controllers/templates.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/view/ViewIndexingPolicy.java`
- Lines: before 1
- Action: add

Proposed:
```java
public final class ViewIndexingPolicy {
  public static final String ROBOTS = "robotsContent";
  public static final String NO_INDEX = "noindex,nofollow";

  private ViewIndexingPolicy() {}

  public static void noIndex(Model model) {
    model.addAttribute(ROBOTS, NO_INDEX);
  }
}
```

Verification:
- `./gradlew.bat :website:test --tests '*ViewControllerTest'`

#### Code Edit 1.2
- File: `website/src/main/resources/templates/fragments/social-preview.html`
- Lines: 4-28
- Action: replace

Current:
```html
<th:block th:fragment="socialPreview(title, description, url, image, imageAlt)">
  <meta name="description" th:content="${description}" />
  <link rel="canonical" th:href="${url}" />
```

Proposed:
```html
<th:block th:fragment="socialPreview(title, description, url, image, imageAlt)">
  <meta name="description" th:content="${description}" />
  <meta th:if="${robotsContent != null}" name="robots" th:content="${robotsContent}" />
  <link th:if="${url != null}" rel="canonical" th:href="${url}" />
```

Verification:
- `./gradlew.bat :website:test --tests '*ViewControllerTest'`

#### Code Edit 1.3
- File: `website/src/main/java/dev/christopherbell/view/account/AccountViewController.java`
- Lines: 19-79
- Action: replace

Current:
```java
@GetMapping(value = "/profile")
public String getProfilePage(HttpServletRequest request) {
  return "profile.html";
}
```

Proposed:
```java
@GetMapping(value = "/profile")
public String getProfilePage(Model model) {
  ViewIndexingPolicy.noIndex(model);
  return "profile.html";
}
```

Apply the same explicit helper call to `/login`, `/signup`, `/forgot-password`, `/reset-password`, `/void/login`, `/void/signup`, `/messages`, `/notifications`, `/report`, `/shared`, `/music`, `/back-office`, and `/command-center`.
Companion literal locations are `ContentViewController.java` lines 54-99 and `VoidViewController.java` lines 56-84.

Verification:
- `./gradlew.bat :website:test --tests '*ViewControllerTest'`

#### Code Edit 1.4
- File: `website/src/main/java/dev/christopherbell/view/wfl/WhatsForLunchViewController.java`
- Lines: 26-51
- Action: replace

Current:
```java
model.addAttribute("socialTitle", "CB | Favorite Restaurants");
model.addAttribute("listMode", "favorites");
```

Proposed:
```java
model.addAttribute("socialTitle", "CB | Favorite Restaurants");
model.addAttribute("socialUrl", PUBLIC_ROOT + "/wfl/favorites");
ViewIndexingPolicy.noIndex(model);
model.addAttribute("listMode", "favorites");
```

Also set `socialUrl` to `PUBLIC_ROOT + "/wfl/top-rated"` in the public top-rated mode.

Verification:
- `./gradlew.bat :website:test --tests '*ViewControllerTest'`

#### Code Edit 1.5
- File: `website/src/main/resources/templates/wfl-list.html`
- Lines: 5-12
- Action: replace

Current:
```html
<th:block th:replace="~{fragments/social-preview :: socialPreview(${socialTitle}, ${listDescription}, 'https://www.christopherbell.dev/wfl', ...)}"></th:block>
```

Proposed:
```html
<th:block th:replace="~{fragments/social-preview :: socialPreview(${socialTitle}, ${listDescription}, ${socialUrl}, ...)}"></th:block>
```

The 404 and vanished templates must include `<meta name="robots" content="noindex,nofollow" />`; the generic 404 must omit canonical/Open Graph URL metadata rather than point to `/`.
Companion literal locations are `templates/error/404.html` lines 1-12 and `templates/post-vanished.html` lines 1-10.

Verification:
- `./gradlew.bat :website:test --tests '*ViewControllerTest' --tests '*ControllerExceptionHandlerTest'`

#### Code Edit 1.6
- File: `website/src/test/java/dev/christopherbell/view/ViewControllerTest.java`
- Lines: 1-300
- Action: add

Proposed:
```java
@ParameterizedTest
@ValueSource(strings = {"/login", "/signup", "/forgot-password", "/reset-password",
    "/profile", "/messages", "/notifications", "/report", "/shared", "/music",
    "/back-office", "/command-center", "/void/login", "/void/signup"})
void privateShellsRenderNoIndex(String route) throws Exception {
  mockMvc.perform(get(route)).andExpect(status().isOk())
      .andExpect(content().string(containsString(
          "name=\"robots\" content=\"noindex,nofollow\"")));
}
```

Add top-rated/favorites canonical assertions, public-route non-noindex assertions, and unknown-route/post-vanished 404 assertions.
Use a Spring Boot MockMvc error-page integration test (rather than only the controller slice) for the unknown-route rendered 404 body; retain the focused controller slice for dynamic-resource status and model assertions.

Verification:
- `./gradlew.bat :website:test --tests '*ViewControllerTest'`

### Task 2 - Resolve dynamic public metadata and true 404s (#1267)

Sequence / dependencies:
- Runs after Task 1 so every missing dynamic resource shares the established 404/indexing contract.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: active profiles, live posts, and existing restaurants return resource-specific title/description/canonical metadata; missing/inactive/expired resources return HTTP 404.
  - Invariants: only public-safe DTO fields enter view models; usernames and IDs are encoded as one path segment; no private account or restaurant operator fields appear in metadata.
  - Boundary/API: domain services remain resource authorities; thin view-preview services translate safe DTOs into bounded metadata records.
  - Effects and failures: view GETs add domain reads; not-found becomes a content-free 404, while persistence/service availability failures remain 5xx.
  - Tests and evidence: first mock valid/missing domain service results in MVC tests, then verify rendered escaping, bounded metadata, and status.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/view/voidroutes/VoidUserSocialPreviewService.java`
- Lines: before 1
- Action: add

Proposed:
```java
@Service
@RequiredArgsConstructor
public class VoidUserSocialPreviewService {
  private final AccountProfileService profiles;

  public VoidUserSocialPreview preview(String username) throws ResourceNotFoundException {
    return VoidUserSocialPreview.from(profiles.getPublicProfile(username));
  }
}
```

Add the analogous restaurant service over `RestaurantService.getRestaurantById`; records must bound and normalize title/description text and expose only safe fields.
The companion addition is `website/src/main/java/dev/christopherbell/view/wfl/RestaurantSocialPreviewService.java` before line 1.

Verification:
- `./gradlew.bat :website:test --tests '*SocialPreview*Test'`

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/account/profile/AccountProfileService.java`
- Lines: 35-48
- Action: replace

Current:
```java
return accountRepository.findByUsername(sanitizedUsername)
    .orElseThrow(() -> new ResourceNotFoundException(...));
```

Proposed:
```java
return accountRepository.findByUsernameAndStatus(sanitizedUsername, AccountStatus.ACTIVE)
    .orElseThrow(() -> new ResourceNotFoundException(...));
```

Add the derived repository method and focused coverage proving suspended profiles are not public.
The companion repository addition is `AccountRepository.java` lines 70-105.

Verification:
- `./gradlew.bat :website:test --tests '*AccountServiceTest' --tests '*AccountProfileServiceTest'`

#### Code Edit 2.3
- File: `website/src/main/java/dev/christopherbell/view/voidroutes/VoidViewController.java`
- Lines: 84-118
- Action: replace

Current:
```java
model.addAttribute("socialUrl", "https://www.christopherbell.dev/u/" + username);
return "user.html";
```

Proposed:
```java
var preview = userPreviews.preview(username);
model.addAttribute("socialTitle", preview.title());
model.addAttribute("socialDescription", preview.description());
model.addAttribute("socialUrl", PUBLIC_ROOT + "/u/" + encode(username));
model.addAttribute("profile", preview.profile());
return "user.html";
```

Apply the same domain-first flow for restaurant pages; map `ResourceNotFoundException` to the non-indexable 404 while leaving other failures unmasked. Preserve the existing expiration-aware post preview flow.
The companion controller location is `WhatsForLunchViewController.java` lines 53-68.

Verification:
- `./gradlew.bat :website:test --tests '*ViewControllerTest'`

#### Code Edit 2.4
- File: `website/src/main/resources/templates/user.html`
- Lines: 1-32
- Action: replace

Current:
```html
<title>User</title>
<h1 id="userHeroTitle">User Feed</h1>
```

Proposed:
```html
<title th:text="${socialTitle}">Void profile</title>
<h1 id="userHeroTitle" th:text="|@${profile.username()}|">@user</h1>
```

Use equivalent server-rendered restaurant name/cuisine/location values and keep client-side mounts for interactive enrichment.
The companion template location is `restaurant.html` lines 1-28.

Verification:
- `./gradlew.bat :website:test --tests '*ViewControllerTest'`

### Task 3 - Generate complete bounded sitemap documents (#1269)

Sequence / dependencies:
- Runs after Tasks 1-2 so eligibility and canonical dynamic routes are settled.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: `/sitemap.xml` represents the current explicit public routes plus active profile/live post/existing restaurant URLs and splits at 50,000 URLs.
  - Invariants: output is valid UTF-8 XML, deterministic and deduplicated; no private route, suspended account, expired post, API route, or favorites route appears.
  - Boundary/API: `PublicRouteRegistry` owns static policy; `PublicSitemapService` owns eligibility, encoding, sorting, splitting, and XML serialization; the controller owns HTTP/cache semantics.
  - Effects and failures: sitemap requests read Mongo/configured content; repository failures remain 5xx and never serve a partial sitemap; no database writes occur.
  - Tests and evidence: start with service tests for route membership, filtering, escaping, ordering, deduplication, and forced small-page splitting, then controller XML parsing tests.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/configuration/PublicRouteRegistry.java`
- Lines: before 1
- Action: add

Proposed:
```java
public final class PublicRouteRegistry {
  public static List<String> paths() {
    return List.of("/", "/blog", "/photos", "/photos/usage", "/void",
        "/void/explore", "/wfl", "/wfl/top-rated", "/thebell", "/thebell/tony",
        "/canes-box-tracker", "/vin-decoder", "/zip-coordinates");
  }
}
```

Verification:
- `./gradlew.bat :website:test --tests '*PublicSitemapServiceTest'`

#### Code Edit 3.2
- File: `website/src/main/java/dev/christopherbell/configuration/PublicSitemapService.java`
- Lines: before 1
- Action: add

Proposed:
```java
@Service
@RequiredArgsConstructor
public class PublicSitemapService {
  static final int MAX_URLS = 50_000;

  public List<SitemapDocument> documents() {
    var urls = Stream.of(staticUrls(), activeProfileUrls(), livePostUrls(), restaurantUrls())
        .flatMap(Function.identity()).distinct().sorted().toList();
    return partitionAndRender(urls, MAX_URLS);
  }
}
```

Use an XML writer, encoded path segments, injected `Clock`, and page-based repository reads; provide a package-private test seam for a smaller URL limit.

Verification:
- `./gradlew.bat :website:test --tests '*PublicSitemapServiceTest'`

#### Code Edit 3.3
- File: `website/src/main/java/dev/christopherbell/account/AccountRepository.java`
- Lines: 90-132
- Action: add

Proposed:
```java
Page<Account> findByStatus(AccountStatus status, Pageable pageable);
Page<Post> findByExpiresOnAfter(Instant now, Pageable pageable);
```

Use inherited `RestaurantRepository.findAll(Pageable)` for public restaurant profiles.
The companion post query is added in `PostRepository.java` lines 1-90.

Verification:
- `./gradlew.bat :website:test --tests '*PublicSitemapServiceTest'`

#### Code Edit 3.4
- File: `website/src/main/java/dev/christopherbell/configuration/PublicMetadataController.java`
- Lines: 12-38
- Action: replace

Current:
```java
public ResponseEntity<Resource> sitemap() {
  return metadata("static/sitemap.xml", MediaType.APPLICATION_XML);
}
```

Proposed:
```java
public ResponseEntity<String> sitemap() {
  return xml(sitemaps.root());
}

@GetMapping(value = "/sitemap-{page}.xml", produces = MediaType.APPLICATION_XML_VALUE)
public ResponseEntity<String> sitemapPage(@PathVariable int page) {
  return xml(sitemaps.page(page));
}
```

Permit only GET sitemap root/shard paths and return 404 for invalid shard numbers.
The companion allowlist edit is `SecurityConfig.java` lines 60-110.

Verification:
- `./gradlew.bat :website:test --tests '*PublicDeliveryConfigurationTest' --tests '*PublicMetadataControllerTest'`

#### Code Edit 3.5
- File: `website/src/main/resources/static/sitemap.xml`
- Lines: 1-12
- Action: delete

Current:
```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://www.christopherbell.dev/</loc></url>
  ...
</urlset>
```

Proposed:
```text
Delete the static sitemap. Replace file-based assertions with controller/service XML parsing and explicit public/private/dynamic eligibility assertions.
```

The companion test replacement is `PublicDeliveryConfigurationTest.java` lines 24-60.

Verification:
- `./gradlew.bat :website:test --tests '*PublicDeliveryConfigurationTest' --tests '*PublicSitemapServiceTest'`

### Task 4 - Repair The Bell landmarks, external links, and button semantics (#1270, #1271)

Sequence / dependencies:
- Independent of sitemap data, but runs after route policy so the static accessibility gate can assert all final templates together.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: The Bell pages expose one descriptive H1 inside main and safe new-tab links; every non-submit button declares `type="button"` in templates and generated HTML.
  - Invariants: submit buttons remain submit controls; dialog default buttons retain their intended close/save values; feed action data attributes remain unchanged.
  - Boundary/API: HTML templates and `feed-render.js` are the rendering boundaries; a static JS test rejects future ambiguous markup.
  - Effects and failures: markup-only changes must not trigger form submission or break event delegation.
  - Tests and evidence: add the static failing scan first, then run JS rendering and MVC template suites.

#### Code Edit 4.1
- File: `website/src/main/resources/templates/thebell/index.html`
- Lines: 10-180
- Action: replace

Current:
```html
<h1>The Bell</h1>
...
<h1 style="font-size: 70px;">The Bell</h1>
```

Proposed:
```html
<main class="site-main" role="main">
  <h1>The Bell</h1>
  ...
  <h2>Archive</h2>
</main>
```

Retain one H1 per document, use H2/H3 descendants, and add `rel="noopener noreferrer"` to every `target="_blank"` link.
Apply the same contract to `thebell/tony.html` lines 10-40.

Verification:
- `./gradlew.bat :website:jsTest`

#### Code Edit 4.2
- File: `website/src/main/resources/static/js/lib/feed-render.js`
- Lines: 560-610
- Action: replace

Current:
```html
<button id="replyBtn" class="btn btn-dark">Reply</button>
<button class="post-action post-reply-btn" data-post="${post.id}">
```

Proposed:
```html
<button id="replyBtn" class="btn btn-dark" type="button">Reply</button>
<button class="post-action post-reply-btn" type="button" data-post="${post.id}">
```

Add explicit types to every scanner result; preserve existing explicit submit buttons.
Companion literal template locations are `post.html` line 44, `messages.html` lines 55-61, `music.html` lines 65 and 85, and `void/index.html` lines 47 and 82.

Verification:
- `./gradlew.bat :website:jsTest`

#### Code Edit 4.3
- File: `website/src/test/js/a11y-markup.test.js`
- Lines: 1-90
- Action: add

Proposed:
```javascript
test('templates and generated controls never rely on the default button type', () => {
  for (const source of interactiveMarkupSources()) {
    assert.deepEqual(findButtonsWithoutType(source.text), [], source.path);
  }
});
```

Add assertions for one H1/main per The Bell document and `noopener noreferrer` on all new-tab links.

Verification:
- `./gradlew.bat :website:jsTest`

### Task 5 - Add authentication field identity and autocomplete metadata (#1272)

Sequence / dependencies:
- Runs last because it is markup-only and shares the final rendered-template/browser verification pass.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: browsers/password managers recognize username/email/current-password/new-password/name fields across all four account flows.
  - Invariants: IDs consumed by JavaScript and labels remain unchanged; validation, CSRF, browser-session mode, and request JSON remain unchanged.
  - Boundary/API: standard HTML `name` and `autocomplete` tokens are the only behavior change.
  - Effects and failures: browser autofill becomes deterministic; no server request shape changes because JavaScript still reads existing IDs.
  - Tests and evidence: add failing static/template assertions for exact tokens, then verify rendered pages and a local password-manager-compatible flow.

#### Code Edit 5.1
- File: `website/src/main/resources/templates/login.html`
- Lines: 23-31
- Action: replace

Current:
```html
<input type="email" class="form-control" id="email" required />
<input type="password" class="form-control" id="password" required />
```

Proposed:
```html
<input type="email" class="form-control" id="email" name="email" autocomplete="username" required />
<input type="password" class="form-control" id="password" name="password" autocomplete="current-password" required />
```

Signup uses `email`, `username`, `given-name`, `family-name`, and `new-password`; forgot password uses `email`; both reset password fields use distinct names with `new-password`.
Companion literal locations are `signup.html` lines 23-50, `forgot-password.html` lines 23-27, and `reset-password.html` lines 23-31.

Verification:
- `./gradlew.bat :website:test --tests '*ViewControllerTest'`

#### Code Edit 5.2
- File: `website/src/test/js/a11y-markup.test.js`
- Lines: 1-90
- Action: add

Proposed:
```javascript
test('authentication inputs expose standard password-manager metadata', () => {
  assertAuthField('login.html', 'email', 'username');
  assertAuthField('login.html', 'password', 'current-password');
  assertAuthField('signup.html', 'password', 'new-password');
  assertAuthField('reset-password.html', 'confirmPassword', 'new-password');
});
```

Verification:
- `./gradlew.bat :website:jsTest && ./gradlew.bat :website:test --tests '*ViewControllerTest'`

The companion rendered-template assertions are added in `ViewControllerTest.java` lines 1-300.

## Code Changes

- Add `ViewIndexingPolicy` and dynamic preview services/records.
- Update four view controllers and shared metadata/404/WFL/profile/restaurant templates.
- Add `PublicRouteRegistry`, `PublicSitemapService`, sitemap document model, dynamic repository queries, controller shard endpoints, and security allowlist entries; remove static sitemap XML.
- Repair The Bell templates and all ambiguous template/generated buttons.
- Add standard authentication `name`/`autocomplete` fields.
- Expand MVC, service, repository-boundary, and JavaScript static regression coverage.

## Files and Modules

- `website/src/main/java/dev/christopherbell/view/**`
- `website/src/main/java/dev/christopherbell/configuration/Public*`
- Account, post, and restaurant repository/service boundaries.
- `website/src/main/resources/templates/**`, especially shared metadata, error, WFL, dynamic public, The Bell, and auth templates.
- `website/src/main/resources/static/js/lib/feed-render.js`
- `website/src/test/java/dev/christopherbell/view/**`
- `website/src/test/java/dev/christopherbell/configuration/**`
- `website/src/test/js/a11y-markup.test.js`

## Unit Testing

- Witness RED then GREEN for private-route robots metadata, WFL modes, generic/dynamic 404s, active/inactive profiles, existing/missing restaurants, and active/expired posts.
- Test sitemap membership, exclusions, canonical encoding, XML parsing, determinism, deduplication, invalid shard 404, and forced splitting below the production limit.
- Run the static ambiguous-button, The Bell landmark/link, and auth autocomplete gates.
- Run focused view/domain suites after each task and the entire Java/JavaScript suite before runtime testing.

## Local Testing

1. Use external `GRADLE_USER_HOME` and run `./gradlew.bat :website:check :cbell-lib:test --console=plain`.
2. Build the boot JAR, start with `local` profile on port 8093, and set both `SPRING_MONGODB_URI` and `SPRING_MONGODB_DATABASE` to one exact disposable Batch 2 database.
3. Seed one active profile, one suspended profile, one live post, one expired post, and one restaurant only in the disposable database.
4. Verify rendered titles/descriptions/canonicals and 404/noindex behavior with HTTP requests; parse `/sitemap.xml` and confirm only eligible fixtures and public routes appear.
5. Inspect login/signup/reset rendered fields and exercise login/cookie mode to confirm autocomplete additions did not change request/session behavior.
6. Verify The Bell headings/main/new-tab links and button types in rendered/static markup.
7. Stop only the alternate process, confirm port 8093 is free, drop the exact disposable database, and re-check production port 8080/public root/service continuity.

## Validation

- Every acceptance criterion in #1265-#1272 has automated evidence.
- No private route/favorites/inactive profile/expired post appears in sitemap or indexable markup.
- Valid public dynamic resources render specific metadata; invalid resources return non-indexable 404.
- Sitemap XML is canonical, deterministic, valid, bounded, and split-capable.
- All buttons and authentication fields pass static semantic checks.
- Full local gates, alternate-port acceptance, independent review, PR CI/CodeQL/dependency review, merge, production deployment, live verification, issue closure, and Builder artifacts complete.

## Rollback or Recovery

- Revert the Batch 2 merge as one PR if metadata or sitemap behavior regresses; no migration or destructive data change is planned.
- The previous static sitemap can be restored by reverting the controller/service/static-resource commit.
- Runtime fixtures live only in an explicitly named disposable database; stop the exact alternate PID and drop only that database.
- Production deployment retains its release/rollback mechanism; never weaken ProgramData ACLs or stop the 8080 service for local testing.

## Risks

- Large sitemap reads could consume memory; page repository reads, a hard 50,000-URL shard size, deterministic streaming/partitioning, and split tests mitigate this.
- Incorrect route classification could hide public pages or index private ones; one explicit registry and enumerated rendered-route tests mitigate drift.
- Domain lookups on HTML routes add database latency; use indexed ID/username queries and bounded safe metadata.
- Thymeleaf null model values could cause 500s; valid/missing rendered tests cover every dynamic route and mode.
- Static regex checks can miss malformed multiline controls; scan full file contents and include generated template literals.

## Completion Criteria

- The plan executes on the named isolated branch/worktree with no authoritative-checkout edits.
- Focused RED/GREEN evidence and full Java/JavaScript/sensor gates pass.
- Alternate-port runtime report proves exact request, response, sitemap, 404, metadata, semantic markup, cleanup, and production continuity.
- Independent review reports no blocker; PR checks pass and the PR is merged.
- Production serves the merge SHA with expected sitemap/metadata/404 behavior and healthy services.
- #1265-#1272 are closed with spec, plan, commits, test report, CI, production, and session-memory links.
