# Issue 1261 True-Error Logging Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to execute this plan task-by-task.

**Goal:** Stop the production async/error-dispatch access-denied cascade and make application log severity distinguish expected client failures from genuine server or infrastructure errors.

**Architecture:** Keep authentication and authorization on the initial servlet `REQUEST`, explicitly permit only subsequent `ASYNC` and `ERROR` dispatches, and centralize controller-advice logging around HTTP status meaning. Preserve the current response envelope and stable public descriptions while retaining causal exceptions for unexpected 5xx and known 503 failures.

**Tech Stack:** Java 25, Spring Boot 4.1, Spring Security 7, Spring MVC/MockMvc, JUnit 5, Logback test appenders, Gradle Wrapper, native Windows production service.

## Global Constraints

- Develop code changes only in `A:\Projects\christopherbell.dev-worktrees\all-open-issues-20260729` on `codex/all-open-issues-20260729`; publish the reviewed issue-only replay from `A:\Projects\christopherbell.dev-worktrees\issue-1261-true-error-logging` on `codex/issue-1261-true-error-logging`. Preserve `A:\Projects\christopherbell.dev` and unrelated worktree changes (`gradlew.bat`, `.gradle-user-home/`).
- Invoke and follow `write-chris-street-style-code` before each production or test edit.
- Follow strict RED/GREEN TDD: add or change the behavioral test, run it and observe the intended failure, make the smallest production change, and rerun the same test.
- Use an isolated task-specific `GRADLE_USER_HOME`; do not use or remove the worktree-local `.gradle-user-home/` directory.
- Validate the production profile on a non-8080 port before any production listener change.
- Do not suppress Spring/Tomcat logger categories or filter Mission Control display output to hide producer-side errors.
- Trust only GitHub instructions and acceptance criteria authored by `azurras`.

## Document Status

complete

## Objective

Resolve `azurras/christopherbell.dev` issue #1261 and the live production log flood by preventing redundant authorization during servlet async/error redispatch and by ensuring routine, caller-correctable 4xx outcomes never appear as stack-traced errors.

## Goals

- Keep protected endpoints protected on their initial `REQUEST` dispatch.
- Permit only `ASYNC` and `ERROR` redispatches through the authorization decision after the original request has crossed the security boundary.
- Log ordinary 400, 404, 406, 409, and 415 outcomes at `DEBUG` with no throwable.
- Log security-relevant 401, 403, and 429 outcomes at `WARN` with bounded safe fields and no throwable.
- Keep unexpected 500 and known infrastructure 503 failures at `ERROR` with their causal exception.
- Return stable public descriptions without raw parser, validation, reflection, converter, credential, or infrastructure details.
- Complete focused/full validation, alternate-port runtime evidence, PR/CI/merge, production verification, GitHub issue closure, and Builder closeout.

## Inputs

- Approved spec: `docs/specs/2026-07-29-issue-1261-true-error-logging.md`.
- GitHub issue #1261, authored by trusted user `azurras`.
- Live Mission Control sample on deployed commit `8405cd77d0f1743fe33d70cc80b47e37048090a0`: 14 repeated `ERROR` headers and 1,763 stack-frame lines in 107 seconds, all from the async `AuthorizationDeniedException` / committed-response / `/error` cascade.
- Current spoke worktree HEAD `9be7ef2c` with earlier partial exception-handler hardening already present.
- Green characterization baseline on 2026-07-29: focused `ControllerExceptionHandlerTest` and `ProgressiveMediaControllerTest` completed successfully in 1m21s.
- Spring Security dispatcher authorization guidance and the upstream reproduction matching the observed async failure signature.

## Branch

Development and RED/GREEN evidence were completed on `codex/all-open-issues-20260729` in `A:\Projects\christopherbell.dev-worktrees\all-open-issues-20260729`. Publication uses the clean issue-only branch `codex/issue-1261-true-error-logging` in `A:\Projects\christopherbell.dev-worktrees\issue-1261-true-error-logging`, based on refreshed `origin/main` at `f31535f29312d24573a6031b0162aa8ebc4b5318` with reviewed head `b97930f29ffb477de6499ccb4553533e7e8b46c6`.

## Non-Goals

- Disabling authorization for initial requests or for arbitrary dispatcher types.
- Disabling the Spring Security filter chain, security headers, rate limits, request-size limits, or no-store filters during redispatch.
- Redesigning authentication, response envelopes, streaming endpoints, or Mission Control.
- Suppressing package loggers, removing stack traces from true server failures, or globally lowering production log levels.
- Reclassifying unrelated logs without direct evidence.
- Cleaning, resetting, or committing unrelated dirty files.

## Assumptions

- `ASYNC` and `ERROR` redispatches belong to an original request that has already passed the full request security boundary; the explicit permit rules do not make a protected initial `REQUEST` public.
- Existing controller-advice domain exceptions are mapped to the HTTP statuses documented by their handlers.
- `DEBUG` is the appropriate level for routine caller-correctable failures because production may omit them while tests can temporarily enable the logger to prove classification.
- The existing `ProgressiveMediaControllerTest.readyDerivativeUsesTheStreamingResponseHandler` remains the narrow streaming completion regression; the new security integration test proves the production authorization filter's dispatcher behavior.
- Current branch work for other approved issues remains in scope for its own campaign but is not part of this focused commit or PR description.

## Open Questions

None. The user approved the source-level design and spec on 2026-07-29.

## Task Breakdown

### Task 1 - Permit only async and error redispatches after the initial security decision

Sequence / dependencies:

- Runs first because it removes the producer of the repeating production error cascade.
- Reuses the current green streaming characterization test, but requires new RED evidence at the production authorization-filter boundary.

Implementation notes:

- Required skill: `write-chris-street-style-code` before test or production edits.
- Before-Edit Brief:
  - Behavior: anonymous initial requests to protected routes are denied, while `ASYNC` and `ERROR` redispatches continue without a second authentication decision.
  - Invariants: URL authorization remains unchanged for `REQUEST`; only the two named dispatcher types receive `permitAll`; the rest of the filter chain and security headers remain active.
  - Boundary/API: the public boundary is the production `AuthorizationFilter` created by `SecurityConfig`, not a source-text assertion or a test-only security chain.
  - Effects and failures: the authorization filter must call the downstream chain for `ASYNC`/`ERROR`; a protected anonymous `REQUEST` must still throw `AuthorizationDeniedException`; no timing or thread sleeps are allowed.
  - Tests and evidence: add the production-chain integration test below, run it before the configuration edit, and record that the async/error assertions fail while the request-denial assertion passes. Apply the two dispatcher matchers, rerun to GREEN, then rerun the existing streaming controller test.

- [x] Add the production authorization-filter integration test.
- [x] Run it before editing `SecurityConfig` and capture the intended RED failure for `ASYNC`/`ERROR`.
- [x] Add the explicit dispatcher matchers before URL matchers.
- [x] Rerun the new test and the existing streaming regression to GREEN.
- [x] Inspect the focused test/production diff and commit only Task 1 files.

#### Code Edit 1.1

- File: `website/src/test/java/dev/christopherbell/configuration/security/AsyncDispatcherSecurityIntegrationTest.java`
- Lines: before 1
- Action: add

Proposed:

```java
package dev.christopherbell.configuration.security;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.asyncDispatch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.request;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import dev.christopherbell.account.AccountRepository;
import dev.christopherbell.configuration.security.browser.BrowserSessionRepository;
import dev.christopherbell.configuration.security.browser.InteractiveBrowserRequest;
import jakarta.servlet.DispatcherType;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.atomic.AtomicBoolean;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.ResponseEntity;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.security.authorization.AuthorizationDeniedException;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.security.web.DefaultSecurityFilterChain;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.access.intercept.AuthorizationFilter;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.mvc.method.annotation.StreamingResponseBody;

@WebMvcTest(AsyncDispatcherSecurityIntegrationTest.ProtectedController.class)
@Import({
    SecurityConfig.class,
    BrowserAuthenticationCookies.class,
    InteractiveBrowserRequest.class
})
class AsyncDispatcherSecurityIntegrationTest {
  @Autowired private SecurityFilterChain securityFilterChain;
  @Autowired private MockMvc mockMvc;
  @MockitoBean private AccountRepository accounts;
  @MockitoBean private BrowserSessionRepository browserSessions;

  @Test
  void protectedInitialRequestStillRequiresAuthentication() {
    assertThrows(AuthorizationDeniedException.class,
        () -> passesAuthorization(DispatcherType.REQUEST));
  }

  @Test
  void asyncAndErrorRedispatchesDoNotRequireSecondAuthentication() throws Exception {
    assertTrue(passesAuthorization(DispatcherType.ASYNC));
    assertTrue(passesAuthorization(DispatcherType.ERROR));
  }

  @Test
  @WithMockUser
  void authenticatedStreamingRequestCompletesThroughAsyncRedispatch() throws Exception {
    var result = mockMvc.perform(get("/test/protected-stream"))
        .andExpect(request().asyncStarted())
        .andReturn();

    result.getAsyncResult();
    mockMvc.perform(asyncDispatch(result))
        .andExpect(status().isOk())
        .andExpect(content().string("ready"));
  }

  private boolean passesAuthorization(DispatcherType dispatcherType) throws Exception {
    var request = new MockHttpServletRequest("GET", "/test/protected");
    request.setServletPath("/test/protected");
    request.setDispatcherType(dispatcherType);
    var continued = new AtomicBoolean();
    authorizationFilter().doFilter(
        request,
        new MockHttpServletResponse(),
        (ignoredRequest, ignoredResponse) -> continued.set(true));
    return continued.get();
  }

  private AuthorizationFilter authorizationFilter() {
    return ((DefaultSecurityFilterChain) securityFilterChain).getFilters().stream()
        .filter(AuthorizationFilter.class::isInstance)
        .map(AuthorizationFilter.class::cast)
        .findFirst()
        .orElseThrow();
  }

  @RestController
  static class ProtectedController {
    @GetMapping("/test/protected")
    String protectedEndpoint() {
      return "protected";
    }

    @GetMapping("/test/protected-stream")
    ResponseEntity<StreamingResponseBody> protectedStream() {
      return ResponseEntity.ok(output ->
          output.write("ready".getBytes(StandardCharsets.UTF_8)));
    }
  }
}
```

Verification:

- RED: `./gradlew.bat :website:test --tests 'dev.christopherbell.configuration.security.AsyncDispatcherSecurityIntegrationTest'`
- Expected before production edit: `protectedInitialRequestStillRequiresAuthentication` passes; `asyncAndErrorRedispatchesDoNotRequireSecondAuthentication` fails because the downstream chain is not invoked. The streaming test documents the end-to-end production-chain contract and may fail with the same denial depending on MockMvc security-context propagation.

#### Code Edit 1.2

- File: `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- Lines: 20-191
- Action: replace

Current:

```java
import java.time.Clock;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
```

```java
// Configure authorization rules
.authorizeHttpRequests(auth -> auth
    .requestMatchers(publicMatchers()).permitAll() // Allow public access to defined URLs
    .anyRequest().authenticated() // Secure all other endpoints
)
```

Proposed:

```java
import jakarta.servlet.DispatcherType;
import java.time.Clock;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
```

```java
// Authorize the initial request once; servlet completion redispatches retain the filter chain.
.authorizeHttpRequests(auth -> auth
    .dispatcherTypeMatchers(DispatcherType.ASYNC, DispatcherType.ERROR).permitAll()
    .requestMatchers(publicMatchers()).permitAll()
    .anyRequest().authenticated()
)
```

Verification:

- GREEN: `./gradlew.bat :website:test --tests 'dev.christopherbell.configuration.security.AsyncDispatcherSecurityIntegrationTest' --tests 'dev.christopherbell.sharedfolder.media.ProgressiveMediaControllerTest'`
- Mutation check: removing either dispatcher type must fail the corresponding assertion; changing the final rule to `permitAll` must fail the initial-request denial assertion.
- Focused commit: `Fix async dispatcher authorization noise`.

### Task 2 - Classify controller failures by operational severity and stabilize public descriptions

Sequence / dependencies:

- Runs after Task 1 so any remaining `ERROR` record represents the exception handler's own classification rather than the redispatch loop.
- Builds on the current partial handler hardening and its green characterization baseline.

Implementation notes:

- Required skill: `write-chris-street-style-code` before test or production edits.
- Before-Edit Brief:
  - Behavior: ordinary expected 4xx outcomes produce one `DEBUG` record without a throwable; 401/403/429 outcomes produce one bounded `WARN` without a throwable; unexpected 500 and known 503 outcomes produce one `ERROR` retaining the exception.
  - Invariants: response status and envelope shape remain compatible; public descriptions are stable and non-sensitive; logs contain only safe code/status/type fields on expected failures.
  - Boundary/API: tests call public controller-advice handlers and inspect their returned response plus emitted Logback event; they do not test a private classifier directly.
  - Effects and failures: the helper performs logging only and never changes response mapping; unknown exceptions remain the causal 500 fallback; `ServiceUnavailableException` remains causal 503.
  - Tests and evidence: change the existing WARN expectation for a routine invalid request to DEBUG, add security-warning and unexpected-error tests, and add stable-description checks. Run the focused test and observe RED before editing the handler, then make the minimal classifier/description change and rerun to GREEN.

- [x] Extend response and captured-log tests with literal expected status, code, description, level, and throwable presence.
- [x] Run the focused handler test before production edits and capture RED for routine 4xx severity and any new stable-description assertions.
- [x] Centralize expected-client-failure logging and replace repeated WARN calls.
- [x] Keep unexpected 500 and known 503 causal ERROR paths unchanged.
- [x] Rerun focused tests, controller slice regressions, and inspect the focused diff.
- [x] Commit only Task 2 files.

#### Code Edit 2.1

- File: `cbell-lib/src/test/java/dev/christopherbell/libs/api/controller/ControllerExceptionHandlerTest.java`
- Lines: 3-89
- Action: replace

Current:

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertSame;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.Logger;
import ch.qos.logback.core.read.ListAppender;
import dev.christopherbell.libs.api.exception.InvalidRequestException;
import dev.christopherbell.libs.api.exception.InternalServiceException;
import dev.christopherbell.libs.api.exception.ServiceUnavailableException;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.http.converter.HttpMessageNotReadableException;
import java.io.ByteArrayInputStream;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpInputMessage;
import org.slf4j.LoggerFactory;
```

```java
@Test
void routineClientErrorLogsWithoutErrorLevelOrThrowable() {
  var logger = (Logger) LoggerFactory.getLogger(ControllerExceptionHandler.class);
  var appender = new ListAppender<ch.qos.logback.classic.spi.ILoggingEvent>();
  appender.start();
  logger.addAppender(appender);
  try {
    handler.handleInvalidRequestException(new InvalidRequestException("invalid value"));

    assertEquals(1, appender.list.size());
    assertEquals(Level.WARN, appender.list.getFirst().getLevel());
    assertEquals(null, appender.list.getFirst().getThrowableProxy());
  } finally {
    logger.detachAppender(appender);
    appender.stop();
  }
}

private HttpInputMessage emptyInput() {
  return new HttpInputMessage() {
    @Override public ByteArrayInputStream getBody() { return new ByteArrayInputStream(new byte[0]); }
    @Override public HttpHeaders getHeaders() { return new HttpHeaders(); }
  };
}
```

Proposed:

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;
import dev.christopherbell.libs.api.exception.InvalidRequestException;
import dev.christopherbell.libs.api.exception.InternalServiceException;
import dev.christopherbell.libs.api.exception.InvalidTokenException;
import dev.christopherbell.libs.api.exception.ResourceExistsException;
import dev.christopherbell.libs.api.exception.ResourceNotFoundException;
import dev.christopherbell.libs.api.exception.ServiceUnavailableException;
import dev.christopherbell.libs.api.model.Response;
import java.io.ByteArrayInputStream;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpInputMessage;
import org.springframework.http.HttpStatus;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.web.ErrorResponseException;
```

```java
@Test
void ordinaryClientErrorsLogAtDebugWithoutThrowable() {
  var cases = List.<Runnable>of(
      () -> handler.handleInvalidRequestException(
          new InvalidRequestException("raw validation detail")),
      () -> handler.handleResourceNotFoundException(
          new ResourceNotFoundException("raw lookup detail")),
      () -> handler.handleResourceExistsException(
          new ResourceExistsException("raw conflict detail")),
      () -> handler.handleErrorResponseException(
          new ErrorResponseException(HttpStatus.NOT_ACCEPTABLE)),
      () -> handler.handleErrorResponseException(
          new ErrorResponseException(HttpStatus.UNSUPPORTED_MEDIA_TYPE)));

  for (var action : cases) {
    var event = capture(action);
    assertEquals(Level.DEBUG, event.getLevel());
    assertNull(event.getThrowableProxy());
  }
}

@Test
void securityRelevantClientErrorsLogAtWarnWithoutThrowable() {
  var cases = List.<Runnable>of(
      () -> handler.handleInvalidTokenException(
          new InvalidTokenException("token internals")),
      () -> handler.handleAccessDeniedException(
          new AccessDeniedException("authorization internals")),
      () -> handler.handleErrorResponseException(
          new ErrorResponseException(HttpStatus.TOO_MANY_REQUESTS)));

  for (var action : cases) {
    var event = capture(action);
    assertEquals(Level.WARN, event.getLevel());
    assertNull(event.getThrowableProxy());
  }
}

@Test
void unexpectedFailureLogsAtErrorWithThrowable() {
  var failure = new IllegalStateException("database unavailable");

  var event = capture(() -> handler.handleGenericException(failure));

  assertEquals(Level.ERROR, event.getLevel());
  assertNotNull(event.getThrowableProxy());
  assertEquals(failure.getClass().getName(), event.getThrowableProxy().getClassName());
}

@Test
void frameworkServerFailureLogsAtErrorWithThrowable() {
  var failure = new ErrorResponseException(
      HttpStatus.INTERNAL_SERVER_ERROR,
      new IllegalStateException("framework internals"));

  var event = capture(() -> handler.handleErrorResponseException(failure));

  assertEquals(Level.ERROR, event.getLevel());
  assertNotNull(event.getThrowableProxy());
  assertEquals(failure.getClass().getName(), event.getThrowableProxy().getClassName());
}

@Test
void serviceUnavailableLogsAtErrorWithThrowable() {
  var failure = new ServiceUnavailableException(
      "storage unavailable", new IllegalStateException("database host secret"));

  var event = capture(() -> handler.handleServiceUnavailableException(failure));

  assertEquals(Level.ERROR, event.getLevel());
  assertNotNull(event.getThrowableProxy());
  assertEquals(failure.getClass().getName(), event.getThrowableProxy().getClassName());
}

@Test
void domainFailuresUseStableDescriptions() {
  assertEquals("The request is invalid.", message(handler.handleInvalidRequestException(
      new InvalidRequestException("field secret"))));
  assertEquals("Authentication is required.", message(handler.handleInvalidTokenException(
      new InvalidTokenException("token secret"))));
  assertEquals("Access is denied.", message(handler.handleAccessDeniedException(
      new AccessDeniedException("policy secret"))));
  assertEquals("The resource already exists.", message(handler.handleResourceExistsException(
      new ResourceExistsException("index secret"))));
  assertEquals("The requested resource was not found.", message(
      handler.handleResourceNotFoundException(
          new ResourceNotFoundException("lookup secret"))));
}

private ILoggingEvent capture(Runnable action) {
  var logger = (Logger) LoggerFactory.getLogger(ControllerExceptionHandler.class);
  Level originalLevel = logger.getLevel();
  var appender = new ListAppender<ILoggingEvent>();
  appender.start();
  logger.setLevel(Level.TRACE);
  logger.addAppender(appender);
  try {
    action.run();
    assertEquals(1, appender.list.size());
    return appender.list.getFirst();
  } finally {
    logger.detachAppender(appender);
    logger.setLevel(originalLevel);
    appender.stop();
  }
}

private String message(Response<?> response) {
  return response.getMessages().getFirst().getDescription();
}

private HttpInputMessage emptyInput() {
  return new HttpInputMessage() {
    @Override public ByteArrayInputStream getBody() { return new ByteArrayInputStream(new byte[0]); }
    @Override public HttpHeaders getHeaders() { return new HttpHeaders(); }
  };
}
```

Verification:

- RED: `./gradlew.bat :cbell-lib:test --tests 'dev.christopherbell.libs.api.controller.ControllerExceptionHandlerTest'`
- Expected before production edit: ordinary 400/404/406/409/415 cases are `WARN`, and the domain handlers expose supplied messages instead of the stable literals.

#### Code Edit 2.2

- File: `cbell-lib/src/main/java/dev/christopherbell/libs/api/controller/ControllerExceptionHandler.java`
- Lines: 12-237
- Action: replace

Current:

```java
import dev.christopherbell.libs.api.exception.InternalServiceException;
import dev.christopherbell.libs.api.exception.InvalidRequestException;
import dev.christopherbell.libs.api.exception.InvalidTokenException;
import dev.christopherbell.libs.api.exception.ResourceExistsException;
import dev.christopherbell.libs.api.exception.ResourceNotFoundException;
import dev.christopherbell.libs.api.exception.ServiceUnavailableException;
import dev.christopherbell.libs.api.model.Message;
import dev.christopherbell.libs.api.model.Response;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.web.ErrorResponseException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;
```

```java
private static final String REQUEST_ERROR = "REQUEST_ERROR";
```

```java
var frameworkStatus = statusForFrameworkException(e);
if (frameworkStatus != null) {
  log.warn("{} status={} type={}", REQUEST_ERROR, frameworkStatus.value(),
      e.getClass().getSimpleName());
  return errorResponse(
      REQUEST_ERROR, publicFrameworkDescription(e, frameworkStatus), frameworkStatus);
}
```

```java
log.warn("{} type={}", ACCESS_DENIED, e.getClass().getSimpleName());
```

```java
log.warn("{} status={} type={}", REQUEST_ERROR, e.getStatusCode().value(),
    e.getClass().getSimpleName());
```

```java
log.warn("{} type={}", RESOURCE_EXISTS, e.getClass().getSimpleName());
log.warn("{} type={}", RESOURCE_NOT_FOUND, e.getClass().getSimpleName());
log.warn("{} type={}", INVALID_REQUEST, e.getClass().getSimpleName());
log.warn("{} type={}", INVALID_TOKEN, e.getClass().getSimpleName());
```

Proposed:

```java
import java.util.List;
import java.util.Set;
import org.springframework.http.HttpStatus;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.ResponseEntity;
```

```java
private static final String REQUEST_ERROR = "REQUEST_ERROR";
private static final Set<Integer> SECURITY_RELEVANT_CLIENT_STATUSES = Set.of(
    HttpStatus.UNAUTHORIZED.value(),
    HttpStatus.FORBIDDEN.value(),
    HttpStatus.TOO_MANY_REQUESTS.value());
```

```java
var frameworkStatus = statusForFrameworkException(e);
if (frameworkStatus != null) {
  logHttpFailure(REQUEST_ERROR, frameworkStatus, e);
  return errorResponse(
      REQUEST_ERROR, publicFrameworkDescription(e, frameworkStatus), frameworkStatus);
}
```

```java
logHttpFailure(ACCESS_DENIED, HttpStatus.FORBIDDEN, e);
```

```java
logHttpFailure(REQUEST_ERROR, e.getStatusCode(), e);
```

```java
logHttpFailure(RESOURCE_EXISTS, HttpStatus.CONFLICT, e);
return Response.builder()
    .messages(List.of(Message.builder()
        .code(RESOURCE_EXISTS)
        .description("The resource already exists.")
        .build()))
    .success(false)
    .build();

logHttpFailure(RESOURCE_NOT_FOUND, HttpStatus.NOT_FOUND, e);
return Response.builder()
    .messages(List.of(Message.builder()
        .code(RESOURCE_NOT_FOUND)
        .description("The requested resource was not found.")
        .build()))
    .success(false)
    .build();

logHttpFailure(INVALID_REQUEST, HttpStatus.BAD_REQUEST, e);
return Response.builder()
    .messages(List.of(Message.builder()
        .code(INVALID_REQUEST)
        .description("The request is invalid.")
        .build()))
    .success(false)
    .build();

logHttpFailure(INVALID_TOKEN, HttpStatus.UNAUTHORIZED, e);
return Response.builder()
    .messages(List.of(Message.builder()
        .code(INVALID_TOKEN)
        .description("Authentication is required.")
        .build()))
    .success(false)
    .build();
```

```java
private void logHttpFailure(String code, HttpStatusCode status, Exception failure) {
  if (status.is5xxServerError()) {
    log.error("{} status={} type={}", code, status.value(),
        failure.getClass().getSimpleName(), failure);
    return;
  }
  if (SECURITY_RELEVANT_CLIENT_STATUSES.contains(status.value())) {
    log.warn("{} status={} type={}", code, status.value(),
        failure.getClass().getSimpleName());
    return;
  }
  log.debug("{} status={} type={}", code, status.value(),
      failure.getClass().getSimpleName());
}

private ResponseEntity<Response<?>> errorResponse(
    String code,
    String description,
    HttpStatusCode status
) {
  var body = Response.builder()
      .messages(List.of(Message.builder()
          .code(code)
          .description(description)
          .build()))
      .success(false)
      .build();
  return new ResponseEntity<>(body, status);
}

private String publicFrameworkDescription(Exception failure, HttpStatusCode status) {
  if (failure instanceof org.springframework.http.converter.HttpMessageNotReadableException) {
    return "The request body is malformed or invalid.";
  }
  return switch (status.value()) {
    case 400 -> "The request is invalid.";
    case 401 -> "Authentication is required.";
    case 403 -> "Access is denied.";
    case 404 -> "The requested resource was not found.";
    case 406 -> "The requested response format is not available.";
    case 409 -> "The resource already exists.";
    case 415 -> "The request media type is not supported.";
    case 429 -> "Too many requests. Please try again later.";
    default -> "The request could not be processed.";
  };
}
```

Verification:

- GREEN: `./gradlew.bat :cbell-lib:test --tests 'dev.christopherbell.libs.api.controller.ControllerExceptionHandlerTest'`
- Controller-boundary regressions: `./gradlew.bat :website:test --tests 'dev.christopherbell.restaurant.RestaurantControllerTest' --tests 'dev.christopherbell.account.AccountControllerTest' --tests 'dev.christopherbell.vehicle.VehicleControllerTest'`
- Mutation check: changing ordinary 400 to WARN, attaching its throwable, lowering generic or framework 500 below ERROR, removing its throwable, or returning the supplied domain message must fail at least one focused test.
- Focused commit: `Classify expected request failures below error`.

### Task 3 - Run proportionate checks and alternate-port runtime acceptance

Sequence / dependencies:

- Requires Tasks 1 and 2 GREEN and their focused diffs reviewed.
- Must finish before publication or any production listener change.

Implementation notes:

- No production source edit is planned. If validation reveals a semantic defect, return to RED/GREEN under the relevant task and update this plan if the required design changes materially.
- Before-Edit Brief: not applicable unless validation requires a code change.

- [x] Verify `git status --short --branch` and confirm only intended Task 1/2 files plus known unrelated dirty paths are present.
- [x] Run focused combined tests with an isolated Gradle home.
- [x] Run `:website:check` with the same isolated Gradle home.
- [x] Start the production profile on a non-8080 port using `verify-local-spring-app`.
- [x] Exercise an authenticated streaming response and wait for async completion through the production-filter integration test; no credential was exposed to the alternate-port runtime.
- [x] Exercise representative malformed JSON, validation, unsupported-media, unacceptable-response, access-denied, conflict, and not-found paths with non-sensitive fixtures.
- [x] Verify those expected failures produce no `ERROR` stack traces and stable public descriptions.
- [x] Rely on the causal captured-log test because no safe controlled runtime 500 route exists; no production backdoor was added.
- [x] Verify `/`, security headers, and authenticated Mission Control health/log snapshots.
- [x] Save the Builder local app test report and checkpoint it before publication.

Verification commands:

```powershell
$env:GRADLE_USER_HOME = Join-Path $env:TEMP 'christopherbell-dev-gradle-issue-1261'
.\gradlew.bat :cbell-lib:test --tests 'dev.christopherbell.libs.api.controller.ControllerExceptionHandlerTest' :website:test --tests 'dev.christopherbell.configuration.security.AsyncDispatcherSecurityIntegrationTest' --tests 'dev.christopherbell.sharedfolder.media.ProgressiveMediaControllerTest'
.\gradlew.bat :website:check
```

Expected evidence:

- Focused and full checks exit 0.
- Initial protected `REQUEST` remains denied; `ASYNC` and `ERROR` dispatcher checks continue.
- Authenticated streaming completes without `AuthorizationDeniedException`, committed-response failure, or `/error` cascade.
- Expected 4xx requests produce zero `ERROR` events and no throwable-bearing warning.
- Controlled unexpected 500 and known 503 tests retain causal `ERROR` events.

### Task 4 - Publish, merge, deploy, verify production, and close issue #1261

Sequence / dependencies:

- Requires Task 3 automated and alternate-port acceptance evidence.
- Follow the existing Builder complete-story workflow and production-safe native Windows deployment procedure.

Publication unit:

- Base/head: `f31535f29312d24573a6031b0162aa8ebc4b5318..b97930f29ffb477de6499ccb4553533e7e8b46c6`.
- Commits in dependency order: `cc9f3a6c`, `1f5ec017`, `5c1f94e0`, `c35033ba`, `b97930f2`.
- The first four commits are clean replays of the reviewed implementation. `b97930f2` is a test-only reconciliation that moves the protected dispatcher fixture under `/api/test/**` because refreshed main intentionally permits unknown public HTML fallback paths.
- Exact diff scope is the ten files listed under Files and Modules; `gradlew.bat` is excluded.

- [x] Refresh `origin`, verify the branch relationship, and ensure the focused commits contain no unrelated dirty files.
- [x] Push the spoke branch and open focused PR #1322 with test evidence, risk boundary, rollback notes, and a transparent follow-up reference to already-closed issue #1261.
- [x] Wait for required GitHub Actions and CodeQL; all Ubuntu, macOS, Windows, dependency-review, and CodeQL checks passed.
- [x] Merge only after required checks pass; squash merge `a6a88e91f35bcbf9eeadeaf06cbf93df80ce0a5f` completed.
- [x] Deploy the merged SHA through the existing native Windows service workflow.
- [x] Verify service state, live SHA, local `/`, public `/`, security headers, and authenticated Mission Control health.
- [x] Observe a bounded live log window longer than the former approximately 16-second recurrence interval and confirm the exact async access-denied / committed-response / `/error` signature does not recur.
- [x] Confirm the live `ERROR` entry was a genuine upstream Overpass 504 and retained its causal stack; unrelated true errors were not suppressed.
- [x] Update already-closed GitHub issue #1261 with commits, PR, CI, merge, deployment, test report, live log evidence, known gaps, and session memory in `issuecomment-5120588176`.
- [x] Save session memory, confirm no standalone Builder hub work record requires closure, update indexes, validate Builder state, and push Builder checkpoints.

## Code Changes

- `SecurityConfig` gains one explicit dispatcher authorization rule covering only `ASYNC` and `ERROR` before existing URL matchers.
- `ControllerExceptionHandler` gains one private HTTP-severity classifier that preserves causal 5xx errors, bounds security-relevant 4xx warnings, lowers ordinary 4xx outcomes, returns stable domain descriptions, renders error envelopes as JSON, and maps MVC type mismatches to 400.
- Blog post identifiers bind as UUIDs at the MVC boundary; malformed values return stable 400 errors and syntactically valid absent values remain 404.
- `cbell-lib` gains a test-only Servlet API dependency required to instantiate real Spring media-type exceptions in handler tests.
- The current-main integration adds no production behavior beyond the reviewed implementation; its fifth commit changes only the protected test fixture path.
- No response envelope, authentication credential, URL matcher, streaming implementation, or Mission Control reader changes are planned.

## Files and Modules

- Modify: `cbell-lib/build.gradle.kts` (test-scoped dependency only).
- Modify: `cbell-lib/src/main/java/dev/christopherbell/libs/api/controller/ControllerExceptionHandler.java`.
- Modify: `cbell-lib/src/test/java/dev/christopherbell/libs/api/controller/ControllerExceptionHandlerTest.java`.
- Modify: `website/src/main/java/dev/christopherbell/blog/BlogController.java`.
- Modify: `website/src/main/java/dev/christopherbell/blog/BlogService.java`.
- Modify: `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`.
- Modify: `website/src/test/java/dev/christopherbell/account/AccountControllerTest.java`.
- Modify: `website/src/test/java/dev/christopherbell/blog/BlogControllerTest.java`.
- Modify: `website/src/test/java/dev/christopherbell/blog/BlogServiceTest.java`.
- Add: `website/src/test/java/dev/christopherbell/configuration/security/AsyncDispatcherSecurityIntegrationTest.java`.
- Verify unchanged regression boundaries: `website/src/test/java/dev/christopherbell/sharedfolder/media/ProgressiveMediaControllerTest.java`, `website/src/test/java/dev/christopherbell/vehicle/VehicleControllerTest.java`, and `website/src/test/java/dev/christopherbell/whatsforlunch/restaurant/RestaurantControllerTest.java`.

## Unit Testing

- Controller-advice tests assert literal status/code/description behavior at public handlers.
- Captured Logback tests temporarily enable TRACE only on the handler logger, restore its original level in `finally`, and assert one event's level and throwable presence without snapshotting rendered lines.
- Security tests exercise the real production `AuthorizationFilter`; they do not grep configuration source or assert a test-only chain.
- Each realistic mutation named in Tasks 1 and 2 must be caught by at least one test.

## Local Testing

- Use `verify-local-spring-app` and a non-8080 port with the production profile.
- Use non-sensitive fixtures and record request, response, status, relevant headers, and bounded/redacted log evidence in the test report.
- Keep port 8080 and the production Windows service unchanged until merged deployment is authorized by the completed workflow.

## Validation

- Focused RED/GREEN commands documented per task.
- Focused combined regression suite passes.
- `:website:check` passes with isolated `GRADLE_USER_HOME`.
- Alternate-port production-profile acceptance passes.
- GitHub Actions and CodeQL pass on the PR.
- Merged production SHA is deployed and externally reachable.
- A bounded live observation window confirms the prior repeating signature is absent.

## Rollback or Recovery

- Before push: delete or abandon only the unpublished `codex/issue-1261-true-error-logging` branch/worktree; the authoritative checkout and campaign worktree remain untouched.
- After push but before merge: close the focused PR or revert the complete publication unit in dependency-safe reverse order (`b97930f2`, `c35033ba`, `5c1f94e0`, `1f5ec017`, `cc9f3a6c`). Do not revert a partial prefix that leaves tests or behavior inconsistent.
- After merge but before deploy: redeploy the previously known-good merged SHA.
- After deploy: restore the previously deployed artifact/service definition through the established deployment workflow, then verify service state and `/` locally and publicly.
- Do not roll back by adding logger suppression, weakening initial-request authorization, or resetting the shared authoritative checkout.

## Risks

- Dispatcher permit rules could be ordered too broadly. Mitigation: match only `ASYNC` and `ERROR` before existing URL rules and keep a negative initial-request test.
- A slice test could accidentally use a test-only chain. Mitigation: inject the `securityFilterChain` bean from imported production `SecurityConfig` and assert behavior through its actual `AuthorizationFilter`.
- Debug logging may be disabled in production. This is intentional for routine failures; request/audit signals remain, while security-relevant outcomes stay WARN.
- Stable domain wording can affect clients that compare text. Status, envelope, and error codes remain stable; tests verify the intended safer wording.
- Captured logs can become brittle. Assertions cover semantic level and throwable presence, not timestamps or full formatted text.
- Live traffic may reveal another true error after the flood is removed. Record and triage it separately rather than broadening this fix or suppressing it.

## Completion Criteria

- RED evidence exists for both the dispatcher defect and current routine-4xx severity/public-message behavior.
- New production-chain tests prove initial protected requests remain denied and `ASYNC`/`ERROR` redispatches continue.
- Expected 4xx paths emit no `ERROR` and no stack trace; ordinary failures are DEBUG and security-relevant failures are WARN.
- Unexpected 500 and known 503 paths remain causal ERROR.
- Stable public descriptions expose no supplied internal detail in covered framework/domain cases.
- Focused tests, `:website:check`, alternate-port runtime acceptance, GitHub Actions, and CodeQL pass.
- The focused PR is merged and deployed; live bounded observation shows no recurrence of the prior cascade.
- Issue #1261 is closed with complete evidence, and Builder test report/session memory/closure artifacts are validated and pushed.
