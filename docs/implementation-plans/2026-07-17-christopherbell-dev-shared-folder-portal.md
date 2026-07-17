# christopherbell.dev Shared Folder Portal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to execute this plan task by task with review checkpoints.

**Goal:** Add an authenticated shared-drive experience over `A:\Shared`, with independent read/write permissions, large resumable uploads, safe previews, original downloads, progressive media fallback, recycle/audit administration, and production-safe Windows operation.

**Architecture:** The Spring Boot application remains the policy and HTTP boundary. It resolves every user path beneath a configured root, reads current account permissions from MongoDB, streams originals, owns upload/recycle/audit metadata, and admits one transcode job. A separate WinSW-managed `LocalService` worker consumes validated job files and is the only process allowed to invoke pinned ffprobe/FFmpeg binaries. The existing privileged website service identity remains unchanged for Command Center compatibility.

**Tech Stack:** Java 25, Spring Boot 4.1, Spring Security, Thymeleaf, vanilla JavaScript, MongoDB, Gradle/JUnit/Mockito, Node test runner, PowerShell/Pester, WinSW, NTFS ACLs, ffprobe, and FFmpeg fragmented MP4 output.

## Document Status

`ready-for-execution`

## Objective

Deliver the approved shared-folder portal without exposing host paths, buffering complete large files in the JVM, weakening existing authentication, granting media tools the website's system privileges, or disrupting the live site on port 8080.

## Goals

- Serve `/shared` as a data-free shell whose protected APIs require effective `SHARED_FOLDER_READ` or `SHARED_FOLDER_WRITE`.
- Preserve `USER`, `MOD`, and `ADMIN`; ADMIN always has both effective shared permissions, and WRITE implies READ.
- Allow administrators to grant/revoke permissions, inspect audit history, and restore or purge recycled items in Back Office.
- Support safe browsing, downloads, ranges, previews, mutations, and resumable uploads up to 10 GB by default.
- Play compatible media directly and progressively transcode unsupported decodable media through an isolated worker.
- Bound cache, disk reserve, retention, concurrency, request size, and rate limits.
- Verify on a non-8080 port, then deploy and prove production behavior including Command Center regressions.

## Inputs

- Spec: `docs/specs/2026-07-17-christopherbell-dev-shared-folder-portal.md`
- Work record: `docs/work/2026-07-17-christopherbell-dev-shared-folder-portal.md`
- Spoke: `A:\Projects\christopherbell.dev`
- Planning source: refreshed `origin/main` at `9108f9cb936aa80eb10f235210c6b101e16496c4`
- WinSW service-account contract: `NT AUTHORITY\LocalService` in `<serviceaccount>` and `<priority>belownormal</priority>` from the official WinSW v3 configuration reference.

## Branch

- Base: refreshed `origin/main`
- Branch: `codex/shared-folder-portal`
- Worktree: create a clean isolated worktree under `A:\Projects\christopherbell.dev-worktrees\shared-folder-portal`; do not modify or clean the divergent primary checkout.

## Non-Goals

- No public or anonymous file links.
- No literal FTP/SFTP/WebDAV protocol endpoint.
- No per-file ACL model, sharing invitations, quotas, archive extraction, office-document rendering, or collaborative editing.
- No execution of uploaded content or inline rendering of active/unknown formats.
- No mutation of source media during inspection or transcoding.
- No change to the existing production website service account or Command Center privilege model.
- No more than one active transcode job in version one.

## Assumptions

- `A:\Shared` and `A:\Shared-System` can be created as distinct NTFS roots.
- MongoDB remains available to the Spring application; filesystem content remains the listing source of truth.
- The production host supports the existing pinned WinSW build and the built-in `NT AUTHORITY\LocalService` account.
- A verified Windows FFmpeg distribution can be pinned with URL, version, and SHA-256 before production installation.
- A chunk size of 8 MiB is acceptable while the complete file remains capped at 10 GB.
- Fragmented MP4 with H.264 video and AAC audio is the first compatible derivative profile; audio-only inputs use fragmented M4A/AAC.

## Open Questions

None.

## Global Constraints

- Use test-driven development: add the focused failing test before each production edit and record the expected RED cause.
- Refresh `origin/main` immediately before worktree creation and re-inspect line ranges if upstream changed.
- Never use an absolute client path. Decode once, normalize a relative path, reject empty segments where not allowed, canonicalize existing ancestors, reject reparse points, and prove the resolved target remains beneath the configured root immediately before access or mutation.
- Never follow symbolic links, junctions, mount points, or other reparse points in the visible tree.
- Load shared-folder permissions from the current account record for each protected request; do not place them in the long-lived JWT.
- Never construct shell command strings from filenames. Pass fixed executable/argument arrays and validated job JSON only.
- Keep the website on port 8080 untouched until alternate-port prod-profile verification and the Builder test report pass.
- Commit and push each logical spoke checkpoint, then complete independent review, CI, merge, production verification, Builder closure, and session memory.

## Task Breakdown

### Task 1 - Add independent account permissions and Back Office administration

Sequence / dependencies:

- Runs first because every shared API depends on a fresh effective-capability decision.
- Keep role hierarchy behavior unchanged and avoid JWT migration.

#### Code Edit 1.1

- File: `website/src/test/java/dev/christopherbell/account/AccountServiceTest.java`
- Lines: after 349
- Action: add

Proposed:

```java
@Test
void sharedFolderStateCannotBecomeWriteOnly() {
  var account = accountService.updateSharedFolderPermissions(
      accountId, new SharedFolderPermissionUpdate(true, true));
  assertThat(account.permissions()).containsExactlyInAnyOrder(
      SHARED_FOLDER_READ, SHARED_FOLDER_WRITE);

  account = accountService.updateSharedFolderPermissions(
      accountId, new SharedFolderPermissionUpdate(false, false));
  assertThat(account.permissions()).isEmpty();

  assertThatThrownBy(() -> accountService.updateSharedFolderPermissions(
      accountId, new SharedFolderPermissionUpdate(false, true)))
      .isInstanceOf(InvalidRequestException.class);
}

@Test
void adminAlwaysReceivesEffectiveReadAndWrite() {
  account.setRole(Role.ADMIN);
  account.setPermissions(Set.of());
  assertThat(sharedFolderAccess.effectivePermissions(account))
      .containsExactlyInAnyOrder(SHARED_FOLDER_READ, SHARED_FOLDER_WRITE);
}
```

Verification:

- Run `gradlew.bat :website:test --tests "*AccountServiceTest*"`.
- Expected RED: permission types and update method do not exist.

#### Code Edit 1.1a

- File: `website/src/main/java/dev/christopherbell/account/model/AccountPermission.java`
- Lines: 1
- Action: add

Proposed:

```java
package dev.christopherbell.account.model;

public enum AccountPermission {
  SHARED_FOLDER_READ,
  SHARED_FOLDER_WRITE
}
```

Verification:

- The enum is independent of `Role`; no change is made to role hierarchy or JWT authorities.

#### Code Edit 1.1b

- File: `website/src/main/java/dev/christopherbell/account/model/dto/SharedFolderPermissionUpdate.java`
- Lines: 1
- Action: add

Proposed:

```java
package dev.christopherbell.account.model.dto;

import jakarta.validation.constraints.NotNull;

public record SharedFolderPermissionUpdate(
    @NotNull Boolean read,
    @NotNull Boolean write) {}
```

Verification:

- Missing/null fields return 400; `{read:false,write:true}` returns 400 as an invalid write-only state.
- The Back Office sends `{true,true}` when WRITE is enabled and `{false,false}` when READ is removed.

#### Code Edit 1.2

- File: `website/src/main/java/dev/christopherbell/account/model/Account.java`
- Lines: 75-78
- Action: replace

Current:

```java
  private Role role;
  private Set<String> followingIds;
```

Proposed:

```java
  private Role role;
  @Builder.Default
  private Set<AccountPermission> permissions = new HashSet<>();
  private Set<String> followingIds;
```

Verification:

- Add `AccountPermission.java` at lines 1-7 with `SHARED_FOLDER_READ` and `SHARED_FOLDER_WRITE`.
- Existing MongoDB documents deserialize with an empty set and no role field changes.

#### Code Edit 1.3

- File: `website/src/main/java/dev/christopherbell/account/AccountService.java`
- Lines: after 352
- Action: add

Proposed:

```java
public AccountDetail updateSharedFolderPermissions(
    String accountId, SharedFolderPermissionUpdate request) {
  Account account = accountRepository.findById(accountId)
      .orElseThrow(() -> new ResourceNotFoundException("Account not found."));
  if (!request.read() && request.write()) {
    throw new InvalidRequestException("Shared-folder write requires read.");
  }
  EnumSet<AccountPermission> next = EnumSet.noneOf(AccountPermission.class);
  if (request.read()) next.add(SHARED_FOLDER_READ);
  if (request.write()) next.add(SHARED_FOLDER_WRITE);
  account.setPermissions(next);
  return accountMapper.toAccount(accountRepository.save(account));
}
```

Verification:

- Add immutable request validation and map permissions through `AccountDetail`.
- Re-run focused account tests and verify WRITE-only input is normalized to READ+WRITE.

#### Code Edit 1.3a

- File: `website/src/main/java/dev/christopherbell/account/model/dto/AccountDetail.java`
- Lines: 40-41
- Action: replace

Current:

```java
  private Role role;
  private AccountStatus status;
```

Proposed:

```java
  private Role role;
  @Builder.Default
  private Set<AccountPermission> permissions = new HashSet<>();
  private AccountStatus status;
```

Verification:

- Add required imports and prove MapStruct maps stored permissions for admin account lists and `/me` without exposing them through the public `AccountProfile` DTO.
- Frontend effective access checks use `role === 'ADMIN'` OR stored permission, preserving ADMIN defaults even when the stored set is empty.

#### Code Edit 1.4

- File: `website/src/main/java/dev/christopherbell/account/AccountController.java`
- Lines: after 424
- Action: add

Proposed:

```java
@PatchMapping(
    value = V20260717 + "/{accountId}/shared-folder-permissions",
    consumes = MediaType.APPLICATION_JSON_VALUE,
    produces = MediaType.APPLICATION_JSON_VALUE)
@PreAuthorize("@permissionService.hasAuthority('ADMIN')")
public ResponseEntity<Response<AccountDetail>> updateSharedFolderPermissions(
    @PathVariable String accountId,
    @Valid @RequestBody SharedFolderPermissionUpdate request) {
  return ResponseEntity.ok(Response.<AccountDetail>builder()
      .payload(accountService.updateSharedFolderPermissions(accountId, request))
      .success(true)
      .build());
}
```

Verification:

- Add controller tests for ADMIN success, non-admin 403, invalid body 400, revocation, and ADMIN effective invariants.
- Record a permission-change audit event without storing the request body.

#### Code Edit 1.5

- File: `website/src/main/resources/static/js/back-office.js`
- Lines: after 341
- Action: add

Proposed:

```javascript
const shared = new Set(user.permissions ?? []);
renderSharedFolderPermissions({
  read: user.role === 'ADMIN' || shared.has('SHARED_FOLDER_READ'),
  write: user.role === 'ADMIN' || shared.has('SHARED_FOLDER_WRITE'),
  disabled: user.role === 'ADMIN'
});

const saveSharedFolderPermissions = async ({ read, write }) => {
  await api.accounts.updateSharedFolderPermissions(user.id, {
    read: read || write,
    write
  });
  await refreshUsers();
};
```

Verification:

- Update `api.js`, `back-office-users.js`, the Back Office template, and JS tests.
- Assert disabling READ also disables WRITE, enabling WRITE enables READ, and ADMIN controls are checked/disabled.

### Task 2 - Establish configuration, access policy, and safe path resolution

Sequence / dependencies:

- Depends on Task 1 permission types.
- Creates the only path-resolution boundary used by later tasks.

#### Code Edit 2.1

- File: `website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderPathResolverTest.java`
- Lines: 1
- Action: add

Proposed:

```java
@TempDir Path temp;

@Test
void resolvesOnlyOrdinaryDescendants() throws Exception {
  Path root = Files.createDirectory(temp.resolve("shared"));
  Files.createDirectories(root.resolve("music/live"));
  var resolver = new SharedFolderPathResolver(root);
  assertThat(resolver.existing("music/live")).isEqualTo(root.resolve("music/live"));
  assertThatThrownBy(() -> resolver.existing("../secret"))
      .isInstanceOf(UnsafeSharedPathException.class);
  assertThatThrownBy(() -> resolver.existing(root.toString()))
      .isInstanceOf(UnsafeSharedPathException.class);
}

@Test
void rejectsAnyReparsePointOrLinkInTheChain() throws Exception {
  // Create a supported test link/junction fixture or mock BasicFileAttributes.
  assertThatThrownBy(() -> resolver.existing("linked/outside.txt"))
      .isInstanceOf(UnsafeSharedPathException.class);
}
```

Verification:

- Run the focused test; expected RED is the missing resolver.
- Include Windows-specific integration coverage for a junction when permissions allow creation.

#### Code Edit 2.2

- File: `website/src/main/java/dev/christopherbell/sharedfolder/fs/SharedFolderPathResolver.java`
- Lines: 1
- Action: add

Proposed:

```java
public final class SharedFolderPathResolver {
  private final Path root;

  public Path existing(String raw) {
    Path relative = parseRelative(raw);
    Path candidate = root.resolve(relative).normalize();
    requireBeneathRoot(candidate);
    walkExistingSegmentsWithoutLinksOrReparsePoints(candidate);
    return candidate;
  }

  public Path newChild(String parent, String name) {
    Path safeParent = existing(parent);
    validateSingleWindowsName(name);
    Path child = safeParent.resolve(name).normalize();
    requireBeneathRoot(child);
    return child;
  }
}
```

Verification:

- Cover dot segments, encoded separators, absolute/UNC/drive paths, ADS colons, reserved DOS names, trailing dots/spaces, NUL/control characters, case variants, missing ancestors, and race rechecks.

#### Code Edit 2.3

- File: `website/src/main/java/dev/christopherbell/configuration/SharedFolderProperties.java`
- Lines: 1
- Action: add

Proposed:

```java
@Validated
@ConfigurationProperties("app.shared-folder")
public record SharedFolderProperties(
    Path root, Path systemRoot,
    @NotNull @DataSizeMin(bytes = 1) DataSize maxUpload,
    @NotNull @DataSizeMin(bytes = 1) DataSize uploadChunk,
    @NotNull @DataSizeMin(bytes = 1) DataSize minimumFreeSpace,
    @NotNull @DataSizeMin(bytes = 1) DataSize transcodeCacheLimit,
    @NotNull @DurationMin(seconds = 1) Duration recycleRetention,
    @NotNull @DurationMin(seconds = 1) Duration auditRetention,
    boolean enabled) {}
```

Verification:

- Add defaults to `application.yml`: 10 GB upload, 8 MiB chunk, 100 GB reserve, 250 GB cache, 30-day recycle, and 180-day audit.
- Point local/test profiles at temporary or build-owned roots; point prod at `A:\Shared` and `A:\Shared-System` through environment variables.

#### Code Edit 2.4

- File: `website/src/main/java/dev/christopherbell/sharedfolder/security/SharedFolderAccessService.java`
- Lines: 1
- Action: add

Proposed:

```java
public void requireRead() {
  Account account = currentActiveApprovedAccount();
  if (!effectivePermissions(account).contains(SHARED_FOLDER_READ)) {
    throw new AccessDeniedException("Shared-folder read access required");
  }
}

public void requireWrite() {
  Account account = currentActiveApprovedAccount();
  if (!effectivePermissions(account).contains(SHARED_FOLDER_WRITE)) {
    throw new AccessDeniedException("Shared-folder write access required");
  }
}
```

Verification:

- Test fresh repository lookup on every call, inactive/unapproved denial, ADMIN defaults, WRITE implication, and immediate revocation with an unchanged JWT.

#### Code Edit 2.5

- File: `cbell-lib/src/main/java/dev/christopherbell/libs/api/APIVersion.java`
- Lines: after 20
- Action: add

Proposed:

```java
public static final String V20260717 = "/2026-07-17";
```

Verification:

- Use `V20260717` for every shared-folder controller mapping and corresponding browser API helper.
- Do not create unversioned shared-folder data or mutation routes.

### Task 3 - Add the portal shell, navigation, listing, metadata, downloads, and safe previews

Sequence / dependencies:

- Depends on Tasks 1-2.
- Completes the read-only vertical slice before mutation work.

#### Code Edit 3.1

- File: `website/src/test/java/dev/christopherbell/view/ViewControllerTest.java`
- Lines: after 157
- Action: add

Proposed:

```java
@Test
void sharedFolderReturnsOnlyTheDataFreeShell() throws Exception {
  mockMvc.perform(get("/shared"))
      .andExpect(status().isOk())
      .andExpect(view().name("shared-folder"))
      .andExpect(content().string(not(containsString("A:\\Shared"))));
}
```

Verification:

- Add SecurityConfig tests proving `/shared` is publicly renderable but every `/api/shared-folder/2026-07-17/**` route requires JWT authentication.
- Expected RED: no shared view mapping/template.

#### Code Edit 3.2

- File: `website/src/main/java/dev/christopherbell/view/content/ContentViewController.java`
- Lines: after 63
- Action: add

Proposed:

```java
@GetMapping("/shared")
public String sharedFolder() {
  return "shared-folder";
}
```

Verification:

- Add `/shared` only to the data-free view allowlist in `SecurityConfig.java` lines 39-89.
- Do not add any `/api/shared-folder` matcher to the public list.

#### Code Edit 3.2a

- File: `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- Lines: 36-40
- Action: replace

Current:

```java
@EnableConfigurationProperties({ClientIpProperties.class, RateLimitProperties.class})
public class SecurityConfig {

  private static final String[] PUBLIC_URLS = {
      "/",
```

Proposed:

```java
@EnableConfigurationProperties({
    ClientIpProperties.class, RateLimitProperties.class, SharedFolderProperties.class})
public class SecurityConfig {

  private static final String[] PUBLIC_URLS = {
      "/",
      "/shared",
```

Verification:

- `SecurityConfigTest` proves `/shared` matches publicly and `/api/shared-folder/2026-07-17/entries` does not.
- The shell contains no model data, absolute path, or filesystem content.

#### Code Edit 3.3

- File: `website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderReadControllerTest.java`
- Lines: 1
- Action: add

Proposed:

```java
@Test
void readUserCanListAndRangeDownloadWithoutAbsolutePathLeak() throws Exception {
  givenReadUser();
  mockMvc.perform(get("/api/shared-folder/2026-07-17/entries").queryParam("path", "music"))
      .andExpect(status().isOk())
      .andExpect(jsonPath("$.path").value("music"))
      .andExpect(jsonPath("$.entries[0].name").value("track.flac"))
      .andExpect(content().string(not(containsString("A:\\Shared"))));

  mockMvc.perform(get("/api/shared-folder/2026-07-17/content")
      .queryParam("path", "music/track.flac")
      .header("Range", "bytes=0-3"))
      .andExpect(status().isPartialContent())
      .andExpect(header().string("Accept-Ranges", "bytes"));
}
```

Verification:

- Add denial, stale token, missing file, malformed/multiple range, HEAD, content-disposition, and safe filename tests.

#### Code Edit 3.4

- File: `website/src/main/java/dev/christopherbell/sharedfolder/web/SharedFolderReadController.java`
- Lines: 1
- Action: add

Proposed:

```java
@RequestMapping("/api/shared-folder" + V20260717)
@RestController
@RequiredArgsConstructor
public class SharedFolderReadController {
@GetMapping("/entries")
public SharedDirectoryResponse list(@RequestParam(defaultValue = "") String path) {
  access.requireRead();
  return browser.list(path);
}

@GetMapping("/content")
public ResponseEntity<ResourceRegion> content(
    @RequestParam String path, @RequestHeader HttpHeaders headers) {
  access.requireRead();
  return downloads.open(path, headers.getRange());
}

@GetMapping("/preview")
public ResponseEntity<?> preview(@RequestParam String path) {
  access.requireRead();
  return previews.openSafePreview(path);
}
}
```

Verification:

- Stream from disk; do not call `readAllBytes`.
- Apply `nosniff`, restrictive CSP/sandbox for PDF, escaped UTF-8 text with byte/line caps, no inline SVG/HTML, and attachment disposition for unknown/active types.

#### Code Edit 3.5

- File: `website/src/main/resources/templates/shared-folder.html`
- Lines: 1
- Action: add

Proposed:

```html
<main id="shared-folder-app" data-auth-required="true">
  <nav id="shared-breadcrumbs" aria-label="Shared folder path"></nav>
  <section id="shared-toolbar" aria-label="Folder actions"></section>
  <section id="shared-list" aria-live="polite"></section>
  <section id="shared-preview" hidden></section>
</main>
<script type="module" src="/js/shared-folder.js"></script>
```

Verification:

- Add `shared-folder.js` and focused DOM tests for login redirect, permission denial, breadcrumb navigation, copied internal links, safe text rendering, download, keyboard access, and responsive layout.
- Add the Shared Folder nav item only when `/api/account/me` reports an effective shared read permission.

### Task 4 - Implement conflict-safe mutations and resumable uploads

Sequence / dependencies:

- Depends on the resolver and read portal.
- Complete ordinary mutations before recycle behavior replaces physical delete.

#### Code Edit 4.1

- File: `website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderMutationServiceTest.java`
- Lines: 1
- Action: add

Proposed:

```java
@Test
void mutationRequiresWriteAndMatchingObservedToken() {
  givenReadOnlyUser();
  assertThatThrownBy(() -> mutations.rename("docs/a.txt", "b.txt", token))
      .isInstanceOf(AccessDeniedException.class);

  givenWriteUser();
  assertThatThrownBy(() -> mutations.rename("docs/a.txt", "b.txt", staleToken))
      .isInstanceOf(StaleSharedItemException.class);
}

@Test
void replaceMustBeExplicitAndUsesAtomicMoveWhenSupported() {
  assertThatThrownBy(() -> mutations.move(source, target, token, false))
      .isInstanceOf(SharedItemConflictException.class);
}
```

Verification:

- Expected RED: mutation service does not exist.
- Cover create folder, rename, move, explicit replace, case-only rename, non-empty directory, cross-volume rejection, and race recheck.

#### Code Edit 4.2

- File: `website/src/main/java/dev/christopherbell/sharedfolder/service/SharedFolderMutationService.java`
- Lines: 1
- Action: add

Proposed:

```java
public SharedEntry move(MoveRequest request) {
  access.requireWrite();
  Path source = paths.existing(request.path());
  observedItems.requireMatch(source, request.observed());
  Path target = paths.newChild(request.destination(), request.name());
  conflicts.requireExplicitReplace(target, request.replace());
  paths.recheckForMutation(source, target);
  Files.move(source, target, moveOptions(request.replace()));
  audit.record("MOVE", request.path(), "SUCCESS");
  return entries.describe(target);
}
```

Verification:

- Controllers accept explicit DTOs and return 409 for conflicts/stale observations.
- Every mutation records bounded audit data and never exposes an absolute path.

#### Code Edit 4.3

- File: `website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderUploadServiceTest.java`
- Lines: 1
- Action: add

Proposed:

```java
@Test
void acceptsOrderedIdempotentChunksAndAtomicallyFinalizes() {
  UploadSession session = uploads.create(new UploadCreate("video.mkv", TEN_GB, null));
  uploads.append(session.id(), 0, bytes("first"), sha256("first"));
  uploads.append(session.id(), 0, bytes("first"), sha256("first"));
  assertThat(uploads.status(session.id()).nextOffset()).isEqualTo(5);
  uploads.complete(session.id(), false);
  assertThat(shared.resolve("video.mkv")).hasBinaryContent(bytes("first"));
}

@Test
void rejectsOversizeOutOfOrderHashMismatchAndReserveBreach() {}
```

Verification:

- Expected RED: upload service/session models do not exist.

#### Code Edit 4.4

- File: `website/src/main/java/dev/christopherbell/sharedfolder/upload/SharedFolderUploadService.java`
- Lines: 1
- Action: add

Proposed:

```java
public UploadStatus append(String id, long offset, InputStream body, String digest) {
  access.requireWrite();
  UploadSession session = sessions.requireOwnedActive(id);
  session.requireOffset(offset);
  diskReserve.requireCapacity(session.remainingBytes());
  long written = streamBoundedChunk(body, session.stagingPath(), offset, properties.uploadChunk());
  session.verifyAndAdvance(written, digest);
  sessions.save(session);
  return session.status();
}
```

Verification:

- Store sessions in MongoDB with owner, safe destination, size, offset, digests, expiry, and observed conflict token; store bytes only in private staging.
- Finalize with a same-volume move, explicit replacement, and a final disk/path/token recheck.
- Add create/status/chunk/complete/cancel APIs and browser resume/cancel/progress tests.

#### Code Edit 4.5

- File: `website/src/main/java/dev/christopherbell/configuration/filter/RequestSizeLimitFilter.java`
- Lines: 23-58
- Action: replace

Current:

```java
public class RequestSizeLimitFilter extends OncePerRequestFilter {

  private final long maxSizeBytes;

  public RequestSizeLimitFilter() {
    this(1_000_000L);
  }

  public RequestSizeLimitFilter(long maxSizeBytes) {
    this.maxSizeBytes = maxSizeBytes;
  }

  @Override
  protected void doFilterInternal(HttpServletRequest request,
      HttpServletResponse response,
      FilterChain filterChain) throws ServletException, IOException {
    long contentLength = request.getContentLengthLong();
    if (contentLength > maxSizeBytes) {
      response.setStatus(HttpStatus.PAYLOAD_TOO_LARGE.value());
      return;
    }

    try {
      filterChain.doFilter(new SizeLimitedRequestWrapper(request, maxSizeBytes), response);
    } catch (RequestPayloadTooLargeException e) {
      response.setStatus(HttpStatus.PAYLOAD_TOO_LARGE.value());
    }
  }
```

Proposed:

```java
public class RequestSizeLimitFilter extends OncePerRequestFilter {

  private final long maxSizeBytes;
  private final long sharedUploadChunkMaxSizeBytes;

  public RequestSizeLimitFilter() {
    this(1_000_000L, 8L * 1024 * 1024);
  }

  public RequestSizeLimitFilter(long maxSizeBytes, long sharedUploadChunkMaxSizeBytes) {
    this.maxSizeBytes = maxSizeBytes;
    this.sharedUploadChunkMaxSizeBytes = sharedUploadChunkMaxSizeBytes;
  }

  @Override
  protected void doFilterInternal(HttpServletRequest request,
      HttpServletResponse response,
      FilterChain filterChain) throws ServletException, IOException {
    long limit = request.getRequestURI().startsWith("/api/shared-folder/2026-07-17/uploads/")
        ? sharedUploadChunkMaxSizeBytes : maxSizeBytes;
    long contentLength = request.getContentLengthLong();
    if (contentLength > limit) {
      response.setStatus(HttpStatus.PAYLOAD_TOO_LARGE.value());
      return;
    }
    try {
      filterChain.doFilter(new SizeLimitedRequestWrapper(request, limit), response);
    } catch (RequestPayloadTooLargeException e) {
      response.setStatus(HttpStatus.PAYLOAD_TOO_LARGE.value());
    }
  }
```

Verification:

- Add filter tests for exactly 8 MiB, one byte over, unknown/chunked bodies, and unchanged 1 MiB limits elsewhere.
- Add shared upload/mutation/transcode rules before the global rule in `RateLimitProperties` and test first-match behavior.

#### Code Edit 4.6

- File: `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- Lines: 147-153
- Action: replace

Current:

```java
  /**
   * Configures the request size limiting filter bean.
   */
  @Bean
  public RequestSizeLimitFilter requestSizeLimitFilter() {
    return new RequestSizeLimitFilter();
  }
```

Proposed:

```java
  /**
   * Configures route-aware streaming request limits.
   */
  @Bean
  public RequestSizeLimitFilter requestSizeLimitFilter(
      SharedFolderProperties sharedFolderProperties) {
    return new RequestSizeLimitFilter(
        1_000_000L, sharedFolderProperties.uploadChunk().toBytes());
  }
```

Verification:

- A non-default test property changes the shared upload chunk limit without changing the ordinary request limit.
- Unknown-length request streams still fail as soon as the applicable byte limit is exceeded.

### Task 5 - Add recycle storage, retention, and filtered audit administration

Sequence / dependencies:

- Depends on Task 4 mutation primitives.
- Replaces visible delete with an isolated recoverable move.

#### Code Edit 5.1

- File: `website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderRecycleServiceTest.java`
- Lines: 1
- Action: add

Proposed:

```java
@Test
void deleteMovesItemToPrivateRecycleAndAdminCanRestore() {
  RecycleItem item = recycle.recycle("docs/report.pdf", observed);
  assertThat(shared.resolve("docs/report.pdf")).doesNotExist();
  assertThat(item.originalPath()).isEqualTo("docs/report.pdf");
  assertThat(recycle.restore(item.id(), false).path()).isEqualTo("docs/report.pdf");
}

@Test
void purgeRequiresAdminAndCleanupHonorsThirtyDayRetention() {}
```

Verification:

- Expected RED: recycle service does not exist.
- Cover restore conflict, explicit replace, missing payload, expired metadata, and private-root escape attempts.

#### Code Edit 5.2

- File: `website/src/main/java/dev/christopherbell/sharedfolder/recycle/SharedFolderRecycleService.java`
- Lines: 1
- Action: add

Proposed:

```java
public RecycleItem recycle(String path, ObservedItem observed) {
  access.requireWrite();
  Path source = paths.existing(path);
  observedItems.requireMatch(source, observed);
  RecycleItem item = metadata.create(path, currentAccountId(), Instant.now());
  Path payload = recyclePaths.payload(item.id());
  Files.move(source, payload, StandardCopyOption.ATOMIC_MOVE);
  repository.save(item);
  audit.record("RECYCLE", path, "SUCCESS");
  return item;
}
```

Verification:

- Recycle payloads live only under `A:\Shared-System\recycle`, never in visible listings.
- Scheduled cleanup purges only metadata/payload pairs older than configured retention.

#### Code Edit 5.3

- File: `website/src/main/java/dev/christopherbell/sharedfolder/audit/SharedFolderAuditEvent.java`
- Lines: 1
- Action: add

Proposed:

```java
@Document("shared_folder_audit")
public record SharedFolderAuditEvent(
    @Id String id,
    @Indexed String accountId,
    @Indexed String action,
    String relativePath,
    Long size,
    String outcome,
    String failureCategory,
    String clientIp,
    @Indexed Instant occurredAt,
    @Indexed(expireAfter = "0s") Instant expiresAt) {}
```

Verification:

- Compute `expiresAt = occurredAt + properties.auditRetention()` so the configured 180-day default remains adjustable.
- Add service tests proving bounded paths/categories, no headers/tokens/body/content/absolute paths/tool command lines, and no per-range-event noise.
- Confirm MongoDB creates the zero-second TTL index on `expiresAt` and document actual expiry semantics in tests/docs.

#### Code Edit 5.4

- File: `website/src/main/resources/static/js/back-office.js`
- Lines: after 382
- Action: add

Proposed:

```javascript
const refreshSharedAdministration = async () => {
  const [audit, recycle] = await Promise.all([
    api.sharedFolder.audit(currentAuditFilters),
    api.sharedFolder.recycle()
  ]);
  renderSharedAudit(audit);
  renderRecycleItems(recycle);
};
```

Verification:

- Add Back Office Shared Folder tab/panels with account/action/outcome/date filters, restore, explicit replace, and typed purge confirmation.
- Add controller and JS tests proving ADMIN-only access/actions.

### Task 6 - Implement direct media classification and progressive derivative delivery

Sequence / dependencies:

- Depends on read APIs, access policy, audit, and disk reserve.
- The Spring side creates jobs but never invokes media executables.

#### Code Edit 6.1

- File: `website/src/test/java/dev/christopherbell/sharedfolder/media/MediaPlaybackServiceTest.java`
- Lines: 1
- Action: add

Proposed:

```java
@Test
void compatibleMediaUsesOriginalAndBrowserFailureRequestsFallback() {
  assertThat(media.playback("audio/song.flac").mode()).isEqualTo(DIRECT);
  TranscodeJob job = media.requestFallback("video/source.mkv", VIDEO_MP4);
  assertThat(job.status()).isEqualTo(QUEUED);
  assertThat(job.sourcePath()).isEqualTo("video/source.mkv");
}

@Test
void cacheKeyChangesWhenSourceMetadataOrProfileVersionChanges() {}
```

Verification:

- Expected RED: media service does not exist.
- Cover known browser-compatible container/codec pairs, unknown inspection, native range playback, queue saturation, free-space denial, cache hit, cancellation, and failure isolation.

#### Code Edit 6.2

- File: `website/src/main/java/dev/christopherbell/sharedfolder/media/MediaPlaybackService.java`
- Lines: 1
- Action: add

Proposed:

```java
public PlaybackDescriptor requestFallback(String path, OutputProfile profile) {
  access.requireRead();
  Path source = paths.existingRegularFile(path);
  diskReserve.requireTranscodeCapacity(source);
  String key = cacheKeys.forSource(source, profile, PROFILE_VERSION);
  return cache.findReady(key)
      .map(PlaybackDescriptor::ready)
      .orElseGet(() -> jobs.enqueueValidated(source, key, profile));
}
```

Verification:

- Job descriptors contain schema version, opaque job/cache IDs, canonical source/output paths, source size/mtime, fixed profile enum, and deadline; never raw extra arguments.
- One active job is enforced both in Spring admission and worker locking.

#### Code Edit 6.3

- File: `website/src/main/java/dev/christopherbell/sharedfolder/media/ProgressiveMediaController.java`
- Lines: 1
- Action: add

Proposed:

```java
@GetMapping("/media/jobs/{id}/stream")
public ResponseEntity<StreamingResponseBody> stream(@PathVariable String id) {
  access.requireRead();
  MediaJob job = jobs.requireVisibleToCurrentAccount(id);
  return ResponseEntity.ok()
      .contentType(job.outputProfile().mediaType())
      .header("Cache-Control", "private, no-store")
      .body(output -> progressiveStreamer.copyGrowingFile(job, output));
}
```

Verification:

- Stream completed files with normal range semantics; while growing, stream sequentially with bounded polling and stop on terminal status/client disconnect.
- Prove fragmented MP4 begins playback before completion and document that seeking is limited until ready.

#### Code Edit 6.4

- File: `website/src/main/resources/static/js/shared-folder.js`
- Lines: 1
- Action: add

Proposed:

```javascript
const playMedia = async (entry) => {
  player.src = api.sharedFolder.contentUrl(entry.path);
  player.addEventListener('error', async () => {
    const job = await api.sharedFolder.requestTranscode(entry.path);
    showTranscodeState(job.status);
    player.src = api.sharedFolder.transcodeStreamUrl(job.id);
  }, { once: true });
};
```

Verification:

- Add JS tests for direct success, error fallback, queued/inspecting/transcoding/buffering/ready/failed/canceled/space states, retry, disconnect, and cache reuse.

### Task 7 - Build and harden the isolated LocalService media worker

Sequence / dependencies:

- Depends on Task 6 job contract.
- Must pass unit/Pester isolation tests before any real media tool is installed.

#### Code Edit 7.1

- File: `ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1`
- Lines: 1
- Action: add

Proposed:

```powershell
Describe 'shared-folder media worker' {
  It 'uses LocalService and below-normal priority' {
    [xml]$service = Get-Content $serviceXml
    $service.service.serviceaccount.username | Should -Be 'NT AUTHORITY\LocalService'
    $service.service.priority | Should -Be 'belownormal'
  }

  It 'rejects source and output paths outside configured roots' {
    & $worker -ValidateOnly $badJob
    $LASTEXITCODE | Should -Not -Be 0
  }
}
```

Verification:

- Expected RED: worker/service files do not exist.
- Add fixtures for traversal, reparse points, altered size/mtime, unknown schema/profile, extra fields, expired deadline, and duplicate active lock.

#### Code Edit 7.2

- File: `ops/production/windows/service/ChristopherBellMediaWorker.xml`
- Lines: 1
- Action: add

Proposed:

```xml
<service>
  <id>ChristopherBellMediaWorker</id>
  <name>Christopher Bell Media Worker</name>
  <description>Restricted shared-folder media inspection and transcoding worker</description>
  <executable>%ProgramFiles%\PowerShell\7\pwsh.exe</executable>
  <arguments>-NoLogo -NoProfile -NonInteractive -ExecutionPolicy RemoteSigned -File "%BASE%\Start-SharedFolderMediaWorker.ps1"</arguments>
  <serviceaccount><username>NT AUTHORITY\LocalService</username></serviceaccount>
  <priority>belownormal</priority>
  <startmode>Automatic</startmode>
  <delayedAutoStart>true</delayedAutoStart>
  <onfailure action="restart" delay="10 sec" />
  <logpath>C:\ProgramData\christopherbell.dev\logs</logpath>
  <log mode="roll-by-size"><sizeThreshold>10240</sizeThreshold><keepFiles>14</keepFiles></log>
</service>
```

Verification:

- Validate XML under the repository's pinned WinSW version.
- Verify the worker process identity and priority after installation.

#### Code Edit 7.3

- File: `ops/production/windows/service/Start-SharedFolderMediaWorker.ps1`
- Lines: 1
- Action: add

Proposed:

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$shutdownRequested = $false

while (-not $shutdownRequested) {
  $job = Get-NextValidatedMediaJob -QueueRoot $QueueRoot
  if ($null -eq $job) { Wait-ForQueueSignal -Milliseconds 500; continue }
  Invoke-WithExclusiveWorkerLock {
    Assert-MediaJobRootsAndSourceMetadata $job
    $arguments = New-FixedFfmpegArguments -Job $job
    Invoke-PinnedMediaTool -Arguments $arguments -Deadline $job.deadline
    Complete-MediaJobAtomically $job
  }
}
```

Verification:

- Put validation/argument construction in `Production.SharedFolderWorker.psm1` with pure Pester-testable functions.
- Use `ProcessStartInfo.ArgumentList`, not a command string; redirect bounded logs; kill the process tree on timeout/cancel; write status via temp+atomic rename.
- ffprobe produces bounded JSON only inside the worker; FFmpeg profiles are fixed to fragmented H.264/AAC MP4 or AAC M4A and never inherit client flags.

#### Code Edit 7.4

- File: `ops/production/windows/modules/Production.SharedFolder.psm1`
- Lines: 1
- Action: add

Proposed:

```powershell
$sharedRoot = 'A:\Shared'
$systemRoot = 'A:\Shared-System'
$workerIdentity = 'NT AUTHORITY\LOCAL SERVICE'

New-SharedFolderRuntimeDirectories -SharedRoot $sharedRoot -SystemRoot $systemRoot
Set-SharedFolderAcl -Path $sharedRoot -WebsiteIdentity 'SYSTEM' `
  -WorkerIdentity $workerIdentity -WorkerAccess ReadAndExecute
Set-SharedFolderAcl -Path $systemRoot -WebsiteIdentity 'SYSTEM' `
  -WorkerIdentity $workerIdentity -WorkerWritableChildren @('jobs','staging','cache','logs')
Install-PinnedMediaTools -Manifest $mediaToolManifest
Install-WinSwService -Definition 'ChristopherBellMediaWorker.xml'
```

Verification:

- Extend install/common/security integration tests for idempotence, exact resolved roots, inherited ACL removal, website full control, worker read-only originals, worker-private write roots, and no worker access to config/secrets/deploy/service-control paths.
- Do not grant LocalService modify permission to `A:\Shared` or production configuration.

#### Code Edit 7.5

- File: `ops/production/windows/modules/Production.Install.psm1`
- Lines: 144-171
- Action: replace

Current:

```powershell
function Install-ProductionRuntime {
    [CmdletBinding()]
    param([switch]$WhatIf, [string]$CloudflareTokenPath)
    Assert-Administrator
    $root = 'C:\ProgramData\christopherbell.dev'
    if ($WhatIf) { Write-Output "Would create $root, preserve configuration, verify WinSW, install ChristopherBellDev, and validate cloudflared."; return }
    New-ProductionDirectories $root
    Install-ConfigurationExamples $root
    $config = Read-ProductionConfig (Join-Path $root 'config\deploy.json')
    Read-ProductionEnvironment (Join-Path $root 'config\app.env') | Out-Null
    Protect-ProductionSecrets $root
    Install-CloudflaredService -Executable $config.cloudflaredExe -TokenPath $CloudflareTokenPath
    Set-Service MongoDB -StartupType Automatic
    & sc.exe failure MongoDB reset= 3600 actions= restart/10000/restart/30000 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Failed to configure MongoDB service recovery.' }
    $service = Join-Path $root 'service'
    $binary = Install-WinSwBinary -ServiceRoot $service
    Copy-Item (Join-Path $PSScriptRoot '..\service\ChristopherBellDev.xml') $service -Force
    Copy-Item (Join-Path $PSScriptRoot '..\service\Start-ChristopherBellDev.ps1') $service -Force
    if (-not (Get-Service ChristopherBellDev -ErrorAction SilentlyContinue)) {
        & $binary install | Out-Null
        if ($LASTEXITCODE -ne 0) { throw 'WinSW service installation failed.' }
    }
    & sc.exe config ChristopherBellDev start= auto depend= MongoDB | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Failed to configure the website service.' }
    & sc.exe failure ChristopherBellDev reset= 3600 actions= restart/10000/restart/30000 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Failed to configure website service recovery.' }
}
```

Proposed:

```powershell
function Install-ProductionRuntime {
    [CmdletBinding()]
    param([switch]$WhatIf, [string]$CloudflareTokenPath)
    Assert-Administrator
    $root = 'C:\ProgramData\christopherbell.dev'
    if ($WhatIf) {
        Write-Output "Would install the website runtime and restricted shared media worker under $root."
        return
    }
    New-ProductionDirectories $root
    Install-ConfigurationExamples $root
    $config = Read-ProductionConfig (Join-Path $root 'config\deploy.json')
    Read-ProductionEnvironment (Join-Path $root 'config\app.env') | Out-Null
    Protect-ProductionSecrets $root
    Install-CloudflaredService -Executable $config.cloudflaredExe -TokenPath $CloudflareTokenPath
    Install-WebsiteService -Root $root -Configuration $config
    Install-SharedFolderRuntime -ProductionRoot $root -Configuration $config
}
```

Verification:

- Extract the unchanged MongoDB/website setup into `Install-WebsiteService` with characterization tests before refactoring.
- Import `Production.SharedFolder.psm1`, copy a second renamed WinSW binary beside its matching XML, install/refresh the worker idempotently, and preserve the existing website service identity/configuration.

#### Code Edit 7.6

- File: `ops/production/windows/prod.ps1`
- Lines: 8-10
- Action: replace

Current:

```powershell
Import-Module (Join-Path $moduleRoot 'Production.Common.psm1') -Global -Force
foreach ($module in 'Production.Deploy','Production.Install','Production.Sensors','Production.Operations','Production.AutoDeploy') {
    Import-Module (Join-Path $moduleRoot "$module.psm1") -Force
}
```

Proposed:

```powershell
Import-Module (Join-Path $moduleRoot 'Production.Common.psm1') -Global -Force
foreach ($module in 'Production.Deploy','Production.SharedFolder','Production.Install','Production.Sensors','Production.Operations','Production.AutoDeploy') {
    Import-Module (Join-Path $moduleRoot "$module.psm1") -Force
}
```

Verification:

- `prod.ps1 help`, `install -WhatIf`, existing command dispatch, and all existing module imports remain green.
- `Production.Command.Tests.ps1` proves the shared-folder module loads before `Production.Install` invokes its functions.

### Task 8 - Bound cache, cleanup, audit retention, throttling, and failure behavior

Sequence / dependencies:

- Depends on uploads, recycle, audit, and media worker.
- Consolidates scheduled maintenance and resource-pressure tests.

#### Code Edit 8.1

- File: `website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderMaintenanceServiceTest.java`
- Lines: 1
- Action: add

Proposed:

```java
@Test
void evictsOnlyLeastRecentlyUsedReadyCacheEntriesAboveLimit() {
  cacheFixture.ready("old", GIB_200, t0);
  cacheFixture.ready("new", GIB_100, t1);
  maintenance.run();
  assertThat(cacheFixture.exists("old")).isFalse();
  assertThat(cacheFixture.exists("new")).isTrue();
  assertThat(originals).allMatch(Files::exists);
}

@Test
void reserveFailureStopsNewWorkButPreservesReadsAndDownloads() {}
```

Verification:

- Expected RED: maintenance service does not exist.
- Cover active-job immunity, cache access-time updates, stale staging expiry, recycle retention, audit TTL configuration, and filesystem-unavailable behavior.

#### Code Edit 8.2

- File: `website/src/main/java/dev/christopherbell/sharedfolder/maintenance/SharedFolderMaintenanceService.java`
- Lines: 1
- Action: add

Proposed:

```java
@Scheduled(fixedDelayString = "${app.shared-folder.maintenance-delay:PT15M}")
public void maintain() {
  if (!properties.enabled()) return;
  staging.expireAbandoned();
  recycle.purgeExpired();
  cache.evictLruAbove(properties.transcodeCacheLimit(), jobs.activeCacheKeys());
  jobs.reconcileWorkerStatuses();
}
```

Verification:

- Use a distributed/single-host lock so overlapping schedules cannot run.
- Resolve and verify every deletion target beneath its private root immediately before deletion.

#### Code Edit 8.3

- File: `website/src/main/java/dev/christopherbell/configuration/RateLimitProperties.java`
- Lines: after 34
- Action: add

Proposed:

```java
rules.add(new Rule(
    "shared-upload", 240, Duration.ofMinutes(1),
    List.of("POST", "PUT", "PATCH"),
    List.of("/api/shared-folder/2026-07-17/uploads/**")));
rules.add(new Rule(
    "shared-mutation", 60, Duration.ofMinutes(1),
    List.of("POST", "PUT", "PATCH", "DELETE"),
    List.of("/api/shared-folder/2026-07-17/mutations/**",
        "/api/shared-folder/2026-07-17/recycle/**")));
rules.add(new Rule(
    "shared-transcode", 10, Duration.ofMinutes(1),
    List.of("POST"), List.of("/api/shared-folder/2026-07-17/media/jobs")));
```

Verification:

- Keep the existing IP throttle and add per-account service-level limits for active uploads, queued transcodes, and mutation bursts.
- Test trusted-proxy IP behavior, first-match ordering, 429 bodies, and no throttling regression for progressive/range reads.

### Task 9 - Complete automated verification and documentation

Sequence / dependencies:

- Runs after all feature code and operational scripts.
- Must be green before local runtime testing.

#### Code Edit 9.1

- File: `website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderSecurityIntegrationTest.java`
- Lines: 1
- Action: add

Proposed:

```java
@Test
void permissionsFormASeparateImmediatelyRevocableCapabilityBoundary() {
  String token = tokenFor(USER);
  grantRead(accountId);
  get("/api/shared-folder/2026-07-17/entries", token).expectStatus(200);
  revokeRead(accountId);
  get("/api/shared-folder/2026-07-17/entries", token).expectStatus(403);
  grantWrite(accountId);
  get("/api/shared-folder/2026-07-17/entries", token).expectStatus(200);
  postMutation(token).expectStatus(200);
}
```

Verification:

- Cover anonymous, USER/MOD/ADMIN, inactive/unapproved, read-only/write/admin, CSRF/security headers, direct API access, traversal encodings, and stale JWT.

#### Code Edit 9.2

- File: `docs/operations/windows-production.md`
- Lines: after 260
- Action: add

Proposed:

```markdown
Shared Folder Portal
--------------------

- Visible root: `A:\Shared`
- Private root: `A:\Shared-System`
- Website service: unchanged privileged identity for Command Center
- Media worker: `ChristopherBellMediaWorker` as `NT AUTHORITY\LocalService`
- Recovery: disable shared routes, stop the worker, preserve originals/recycle,
  and restore the prior application/service definitions through `prod.cmd`.
```

Verification:

- Document configuration, ACL intent, pinned tool provenance/checksums, job/cache/recycle layouts, service/log inspection, cleanup, alerts, backup boundaries, update procedure, and rollback.
- Update deploy/config examples and command help without embedding secrets.

#### Code Edit 9.3

- File: `website/build.gradle.kts`
- Lines: after 184
- Action: add

Proposed:

```kotlin
tasks.register("sharedFolderVerification") {
    dependsOn("test")
    description = "Runs shared-folder Java and browser regression coverage"
}
```

Verification:

- Run `gradlew.bat clean test :website:sharedFolderVerification` with an isolated `GRADLE_USER_HOME` if the shared daemon registry is inaccessible.
- Run the repository's complete JS test command, run worker Pester coverage under PowerShell 7, and run installer/operations Pester compatibility coverage under both PowerShell 7 and Windows PowerShell 5.1 where those modules are supported.
- Run `git diff --check`, dependency/security checks, and focused package tests; record exact outputs.

### Task 10 - Perform alternate-port acceptance, review, merge, and production rollout

Sequence / dependencies:

- Runs only after Task 9 passes.
- This is the production safety gate and Builder closeout path.

#### Code Edit 10.1

- File: `ops/production/windows/tests/Production.SharedFolder.Security.Integration.Tests.ps1`
- Lines: 1
- Action: add

Proposed:

```powershell
It 'proves the installed worker privilege boundary' {
  (Get-CimInstance Win32_Service -Filter "Name='ChristopherBellMediaWorker'").StartName |
    Should -Be 'NT AUTHORITY\LocalService'
  Test-PathAsIdentity $worker 'A:\Shared\fixture.mkv' -Read | Should -BeTrue
  Test-PathAsIdentity $worker $productionConfig -Read | Should -BeFalse
  Test-ServiceControlAsIdentity $worker 'ChristopherBellDev' | Should -BeFalse
  Test-ShutdownPrivilegeAsIdentity $worker | Should -BeFalse
}
```

Verification:

- Run only against explicitly confirmed fixture/config paths; do not invoke a real shutdown.
- Confirm worker read/write ACLs, service identity/priority, process tree, executable hashes, and failure isolation.

#### Code Edit 10.2

- File: `docs/test-reports/2026-07-17-christopherbell-dev-shared-folder-portal.md`
- Lines: 1
- Action: add

Proposed:

```markdown
# Shared Folder Portal Local App Test Report

Document Status
---------------
`draft`

Record the exact alternate port, prod-profile command, accounts/capabilities,
requests/UI inputs, status codes, response bodies/headers, screenshots, byte
counts/hashes, progressive playback timestamps, cache reuse, ACL evidence, and
pass/fail results required by the approved spec.
```

Verification:

- Use `verify-local-spring-app`; start on a non-8080 port with controlled temporary visible/private roots first, then an explicitly configured safe production-style fixture root.
- Exercise login, listing, copied link, unauthorized denial, immediate revocation, native FLAC/browser-supported media, MKV fallback, progressive start-before-finish, cache hit, 10 GB policy with smaller configured fixture, resume, conflict, recycle/restore/purge, audit filters, low-space simulation, unavailable FFmpeg, and mobile/desktop UI.
- Record response-body evidence, not only status codes.

#### Code Edit 10.3

- File: `docs/work-closures/2026-07-17-christopherbell-dev-shared-folder-portal.md`
- Lines: 1
- Action: add

Proposed:

```markdown
# christopherbell.dev Shared Folder Portal Closure

Record spoke commits, pull request, CI checks, merge SHA, production release,
alternate-port and production evidence, Builder test report, known gaps,
rollback state, and session-memory link.
```

Verification:

- Request independent code/security review before PR publication; address findings with red-green tests.
- Push `codex/shared-folder-portal`, open a draft PR, monitor required CI, squash-merge only when green, and close/update the source work record.
- Deploy through the existing safe Windows production workflow, preserving port 8080 until candidate verification passes.
- Verify `/`, login, shared read/write/admin flows, one direct media file, one progressive derivative/cache reuse, worker isolation, MongoDB/audit, and Command Center service/power/sensor behavior.
- Save final Builder test report, spoke update/review, closure, and session memory; update indexes, validate hub state, commit, and push Builder `main` at each required artifact checkpoint.

## Code Changes

- Account capability model, fresh access policy, account DTO/API mapping, and Back Office permission controls.
- Shared-folder configuration, path/name/reparse protection, listing, metadata, range downloads, and safe preview services.
- Conflict-token mutations, resumable staged upload sessions, recycle metadata/payloads, audit TTL records, and maintenance.
- Media compatibility decisions, cache/job state, progressive output delivery, and browser playback fallback.
- Restricted PowerShell/WinSW worker, pinned media-tool installation, NTFS ACLs, operational tests, configuration, and documentation.
- Route-aware request-size/rate limits, per-account admission bounds, failure mapping, and security headers.

## Files and Modules

- `website/src/main/java/dev/christopherbell/account/**`: stored permissions, effective capability mapping, and admin update endpoint.
- `website/src/main/java/dev/christopherbell/sharedfolder/**`: access, filesystem, web, uploads, recycle, audit, media, and maintenance packages.
- `website/src/main/java/dev/christopherbell/configuration/**`: typed properties plus request/rate-limit integration.
- `website/src/main/resources/templates/shared-folder.html`, `static/js/shared-folder.js`, Back Office/nav/API JS, and profile YAML.
- `website/src/test/java/dev/christopherbell/sharedfolder/**`, account/config/security/view tests, and `website/src/test/js/**`.
- `ops/production/windows/service/**`, `modules/**`, `tests/**`, deploy/config examples, and Windows operations documentation.
- Builder test report, spoke update/review, work closure, and session memory during execution closeout.

## Unit Testing

- Java: permission invariants, fresh revocation, path/name/reparse defense, conflict tokens, disk streaming, uploads, recycle, audit redaction/TTL, media classification/cache keys/jobs, progressive streaming, maintenance, controllers, headers, error codes, and rate/request limits.
- JavaScript: login/permission gates, navigation, breadcrumbs, links, upload state, conflicts, preview escaping, direct/fallback playback, job states, Back Office invariants, audit filters, and recycle confirmations.
- Pester: service XML, worker schema/path/profile validation, fixed argument arrays, cancellation/timeouts, manifest hashes, installation idempotence, ACLs, identity/priority, and negative privilege checks.
- Full Gradle, JavaScript, Pester, formatting, dependency, and security suites must pass; no focused-test-only completion claim.

## Local Testing

- Use a clean isolated spoke worktree and an isolated `GRADLE_USER_HOME` when necessary.
- Start the Spring application with the prod profile on a non-8080 port and explicit controlled shared/system roots.
- Use real authenticated accounts for no-permission, READ, WRITE, and ADMIN scenarios; prove revocation with the same token.
- Send concrete `GET`, `POST`, `PATCH`, and `DELETE` requests and exercise equivalent browser UI inputs.
- Verify byte ranges, download headers, preview safety, chunk resume, conflicts, recycle recovery, audit filtering, direct playback, progressive start-before-completion, and cache reuse.
- Install/run the worker only after its fixture tests pass; use controlled media fixtures and collect process identity, ACL, status JSON, output growth, duration, and hash/size evidence.
- Save the complete evidence in the Builder test report before production changes.

## Validation

- Automated: complete Java/JS/Pester/security suites green and `git diff --check` clean.
- Runtime: `HTTP 200` data-free `/shared` shell, `401/403` protected API denial, `200` authorized listing, `206 Partial Content` range response, successful streamed upload/mutation/recycle flows, and bounded safe previews.
- Media: direct browser playback when compatible; otherwise a queued worker job whose fragmented output becomes playable before terminal completion and is reused from cache.
- Security: traversal/reparse/ADS/reserved-name tests fail closed; current-account permission revocation is immediate; worker is LocalService and lacks config/service/power privileges.
- Production: public home marker/body evidence, login, shared flows, worker/cache/audit evidence, service health, and unchanged Command Center controls/sensors after safe deployment.
- Delivery: independent review complete, PR checks green, merge and production SHA recorded, source work closed, and Builder artifacts pushed.

## Rollback or Recovery

- Disable shared-folder routes/jobs through configuration, stop and disable `ChristopherBellMediaWorker`, and deploy the prior known-good website release through the existing safe workflow.
- Preserve `A:\Shared` and recycle payloads. Do not delete originals during rollback.
- Restore backed-up service/config files only if deployment changed them; the website service identity itself remains unchanged.
- Treat staging/cache as disposable only after resolving each deletion target beneath `A:\Shared-System` and confirming no active job.
- If a database migration/field causes trouble, tolerate/ignore the additive `permissions` field while running the prior build; no destructive down-migration is required.

## Risks

- **Filesystem escape/race:** Central resolver, no-follow/reparse rejection, Windows-name rules, observed tokens, and immediate pre-operation rechecks.
- **Privileged website exposure:** The website never invokes or parses media; only validated job descriptors cross into the restricted worker.
- **Worker descriptor abuse:** Versioned strict schema, canonical root checks, fixed profiles/arguments, source metadata binding, deadlines, exclusive lock, and bounded output/logs.
- **Large-file memory or disk exhaustion:** Streaming I/O, 8 MiB request cap, 10 GB complete limit, 100 GB reserve, staging expiry, and explicit conflict finalization.
- **Transcode resource contention:** One job, below-normal worker priority, output caps/timeouts, cancellation, and graceful degradation of only fallback playback.
- **Progressive playback portability:** Fragmented MP4/M4A fixture tests in Chrome, sequential growing-file delivery, explicit pre-ready seek limitation, and original-download fallback.
- **Cache/recycle deletion error:** Private roots only, active-job exclusions, LRU/retention tests, and verified resolved paths before removal.
- **Production regression:** Alternate-port prod-profile acceptance, backed-up configs, independent review, required CI, safe deploy lock, and explicit Command Center regression tests.

## Completion Criteria

- Every approved spec acceptance criterion has automated or recorded runtime evidence.
- READ/WRITE/ADMIN behavior, immediate revocation, path containment, large upload semantics, recycle/audit, direct media, progressive fallback/cache, and disk/concurrency limits pass.
- The worker runs as `NT AUTHORITY\LocalService`, media tools never run in the website process, and negative privilege checks pass.
- Full tests, independent review, PR CI, squash merge, safe production deploy, and production verification pass with no port-8080 disruption.
- The Builder test report, source closure/update, spoke review, work closure, and session memory are complete, indexed, validated, committed, and pushed.
