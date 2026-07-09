# Issue 1120 Spring Boot 4.1 Upgrade

## Document Status

complete

## Objective

Upgrade `azurras/christopherbell.dev` from Spring Boot 3.4.4 to the latest verified Spring Boot release, Spring Boot 4.1.0, and keep the app build/test/runtime path working.

## Goals

- Resolve GitHub issue https://github.com/azurras/christopherbell.dev/issues/1120.
- Update the root Spring Boot Gradle plugin and `cbell-lib` Spring Boot dependency BOM from `3.4.4` to `4.1.0`.
- Update `springdoc-openapi-starter-webmvc-ui` from the Spring Boot 3-compatible `2.8.8` line to `3.0.3`, which Sonatype Central publishes as the current 3.x artifact for Spring Boot 4 usage.
- Verify dependency resolution, Java tests, and a local app HTTP smoke check.

## Inputs

- GitHub issue: https://github.com/azurras/christopherbell.dev/issues/1120
- Latest Spring Boot source: official Spring project/release listing showed Spring Boot `4.1.0` on July 9, 2026.
- Springdoc source: Sonatype Central showed `org.springdoc:springdoc-openapi-starter-webmvc-ui:3.0.3`.
- Baseline command already passed before edits: `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120-baseline'; .\gradlew.bat --no-daemon :website:test`.
- Spoke worktree: `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\issue-1120-spring-boot-4-1`.

## Branch

- Branch: `codex/issue-1120-spring-boot-4-1`
- Base: `origin/main` at `ab42e4cc`
- Worktree: `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\issue-1120-spring-boot-4-1`

## Non-Goals

- Do not refactor application code unless required by Spring Boot 4.1 compile/runtime failures.
- Do not change unrelated dependency versions beyond the Spring Boot upgrade and directly compatible springdoc line.
- Do not touch the dirty primary checkout on branch `codex/pr-1119-ci-fix`.

## Assumptions

- Java 25 remains the intended runtime/toolchain for this repository.
- The app already uses Jakarta servlet/validation APIs, so the Spring Boot 4 migration should not require Java EE package renames.
- `springdoc-openapi-starter-webmvc-ui` 2.x is not appropriate for Spring Boot 4, so the springdoc 3.x update is part of the dependency upgrade rather than unrelated churn.

## Open Questions

None.

## Task Breakdown

### Task 1 - Upgrade Spring Boot dependency coordinates

Sequence / dependencies:
- Runs first after baseline tests because all downstream verification should resolve against Spring Boot 4.1.0.

Implementation notes:
- Change only the root plugin version and `cbell-lib` imported BOM version.
- Leave `io.spring.dependency-management` unchanged unless Gradle resolution fails.

#### Code Edit 1.1
- File: `build.gradle.kts`
- Lines: 4-8
- Action: replace

Current:
```kotlin
plugins {
    id("org.springframework.boot") version "3.4.4" apply false
    id("io.spring.dependency-management") version "1.1.4" apply false
    java
}
```

Proposed:
```kotlin
plugins {
    id("org.springframework.boot") version "4.1.0" apply false
    id("io.spring.dependency-management") version "1.1.4" apply false
    java
}
```

Verification:
- `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:dependencies --configuration runtimeClasspath`

#### Code Edit 1.2
- File: `cbell-lib/build.gradle.kts`
- Lines: 6-10
- Action: replace

Current:
```kotlin
dependencyManagement {
    imports {
        mavenBom("org.springframework.boot:spring-boot-dependencies:3.4.4")
    }
}
```

Proposed:
```kotlin
dependencyManagement {
    imports {
        mavenBom("org.springframework.boot:spring-boot-dependencies:4.1.0")
    }
}
```

Verification:
- `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :cbell-lib:dependencies --configuration runtimeClasspath`

### Task 2 - Align springdoc with Spring Boot 4

Sequence / dependencies:
- Runs after Task 1 because the Spring Boot 4 runtime classpath should not retain the Spring Boot 3-oriented springdoc 2.x starter.

Implementation notes:
- Update only the existing springdoc dependency line.
- Do not add new OpenAPI behavior or properties.

#### Code Edit 2.1
- File: `website/build.gradle.kts`
- Lines: 31-31
- Action: replace

Current:
```kotlin
    implementation("org.springdoc:springdoc-openapi-starter-webmvc-ui:2.8.8")
```

Proposed:
```kotlin
    implementation("org.springdoc:springdoc-openapi-starter-webmvc-ui:3.0.3")
```

Verification:
- `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:dependencyInsight --dependency springdoc-openapi-starter-webmvc-ui --configuration runtimeClasspath`

### Task 3 - Verify and prepare delivery

Sequence / dependencies:
- Runs after dependency edits and any compile/test-driven compatibility fixes.

Implementation notes:
- Run the full website Java test suite.
- Start the local app with a non-production profile/port and exercise at least one HTTP endpoint for the Builder test report.
- If compile/runtime failures reveal required source compatibility changes, inspect the failing file line ranges and update this plan or record the exact follow-up in the closure artifact before editing.

Task-level verification:
- `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:test`
- `$env:SERVER_PORT='8082'; .\gradlew.bat --no-daemon :website:bootRun --args='--spring.profiles.active=local --server.port=8082'`
- `Invoke-WebRequest -UseBasicParsing http://localhost:8082/`

### Task 4 - Migrate public route matchers to Spring Security 7 API

Sequence / dependencies:
- Runs after the first upgraded `:website:test` compile attempt failed because Spring Security 7.1 no longer provides `AntPathRequestMatcher`.

Implementation notes:
- Spring Security's migration docs state that Spring Security 7 uses `PathPatternRequestMatcher` and no longer supports `AntPathRequestMatcher`.
- Keep the existing public URL list and custom single-post matcher unchanged; only replace the removed matcher implementation.

#### Code Edit 4.1
- File: `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- Lines: 12-24
- Action: replace

Current:
```java
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;
import org.springframework.security.web.util.matcher.RequestMatcher;
```

Proposed:
```java
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.security.web.servlet.util.matcher.PathPatternRequestMatcher;
import org.springframework.security.web.util.matcher.RequestMatcher;
```

Verification:
- `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:test`

#### Code Edit 4.2
- File: `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- Lines: 161-199
- Action: replace

Current:
```java
  /**
   * Helper to convert path patterns into {@link AntPathRequestMatcher}s.
   */
  private List<RequestMatcher> publicMatchersList() {
    List<RequestMatcher> matchers = Arrays.stream(PUBLIC_URLS)
        .map(Sec::toMatcher)
        .collect(Collectors.toList());
    // Add a precise matcher for single post GET: /api/posts/{version}/{postId}
    // Excludes reserved paths like "/me" and "/account/**".
    matchers.add(request -> {
      if (!"GET".equalsIgnoreCase(request.getMethod())) return false;
      String prefix = "/api/posts" + APIVersion.V20250914 + "/";
      String path = request.getRequestURI();
      if (!path.startsWith(prefix)) return false;
      String tail = path.substring(prefix.length());
      if (tail.isEmpty()) return false;
      if (tail.contains("/")) return false; // only single segment
      if ("me".equals(tail)) return false;
      if (tail.startsWith("account")) return false;
      return true; // treat as public single-post GET
    });
    return matchers;
  }

  private RequestMatcher[] publicMatchers() {
    return publicMatchersList().toArray(new RequestMatcher[0]);
  }

  private static class Sec {
    static RequestMatcher toMatcher(String spec) {
      // Allow "METHOD:/path" or just "/path"
      if (spec.contains(":")) {
        String[] parts = spec.split(":", 2);
        String method = parts[0];
        String pattern = parts[1];
        return new AntPathRequestMatcher(pattern, method);
      }
      return new AntPathRequestMatcher(spec);
    }
  }
```

Proposed:
```java
  /**
   * Helper to convert path patterns into {@link PathPatternRequestMatcher}s.
   */
  private List<RequestMatcher> publicMatchersList() {
    List<RequestMatcher> matchers = Arrays.stream(PUBLIC_URLS)
        .map(Sec::toMatcher)
        .collect(Collectors.toList());
    // Add a precise matcher for single post GET: /api/posts/{version}/{postId}
    // Excludes reserved paths like "/me" and "/account/**".
    matchers.add(request -> {
      if (!"GET".equalsIgnoreCase(request.getMethod())) return false;
      String prefix = "/api/posts" + APIVersion.V20250914 + "/";
      String path = request.getRequestURI();
      if (!path.startsWith(prefix)) return false;
      String tail = path.substring(prefix.length());
      if (tail.isEmpty()) return false;
      if (tail.contains("/")) return false; // only single segment
      if ("me".equals(tail)) return false;
      if (tail.startsWith("account")) return false;
      return true; // treat as public single-post GET
    });
    return matchers;
  }

  private RequestMatcher[] publicMatchers() {
    return publicMatchersList().toArray(new RequestMatcher[0]);
  }

  private static class Sec {
    static RequestMatcher toMatcher(String spec) {
      // Allow "METHOD:/path" or just "/path"
      if (spec.contains(":")) {
        String[] parts = spec.split(":", 2);
        String method = parts[0];
        String pattern = parts[1];
        return PathPatternRequestMatcher.pathPattern(HttpMethod.valueOf(method), pattern);
      }
      return PathPatternRequestMatcher.pathPattern(spec);
    }
  }
```

Verification:
- `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:test --tests dev.christopherbell.configuration.SecurityConfigTest`

### Task 5 - Restore MVC test slice support for Spring Boot 4

Sequence / dependencies:
- Runs after Task 4 because `:website:compileTestJava` then failed on moved `WebMvcTest` and `AutoConfigureMockMvc` classes.

Implementation notes:
- Spring Boot 4 moved MVC test annotations into `org.springframework.boot.webmvc.test.autoconfigure` and ships them through the dedicated `spring-boot-starter-webmvc-test` module.
- Add the MVC test starter, then mechanically replace the old Boot 3 MVC test annotation imports in controller/view tests.

#### Code Edit 5.1
- File: `website/build.gradle.kts`
- Lines: 51-54
- Action: replace

Current:
```kotlin
    // Testing
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.springframework.security:spring-security-test")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
```

Proposed:
```kotlin
    // Testing
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.springframework.boot:spring-boot-starter-webmvc-test")
    testImplementation("org.springframework.security:spring-security-test")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
```

Verification:
- `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:test --tests dev.christopherbell.configuration.SecurityConfigTest`

### Task 6 - Migrate Jackson 2 call sites to Jackson 3 packages

Sequence / dependencies:
- Runs after Spring Boot 4 dependency resolution because Spring Boot 4 manages Jackson 3 packages under `tools.jackson`.

Implementation notes:
- Replace direct `com.fasterxml.jackson` imports with `tools.jackson` imports in production and test code.
- Keep DTO parsing behavior unchanged.
- Replace Jackson 2 APIs removed in Jackson 3 only where compile failures identify them.

#### Code Edit 6.1
- File: `cbell-lib/build.gradle.kts`
- Lines: 13-13
- Action: replace

Current:
```kotlin
    implementation("com.fasterxml.jackson.core:jackson-databind:2.17.1")
```

Proposed:
```kotlin
    implementation("tools.jackson.core:jackson-databind")
```

Verification:
- `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:compileJava :website:compileTestJava`

#### Code Edit 6.2
- File: `cbell-lib/src/main/java/dev/christopherbell/libs/test/TestUtil.java`
- Lines: 4-28
- Action: replace

Current:
```java
import com.fasterxml.jackson.databind.ObjectMapper;

private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper().findAndRegisterModules();
```

Proposed:
```java
import tools.jackson.databind.ObjectMapper;

private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();
```

Verification:
- `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:compileTestJava`

#### Code Edit 6.3
- File: `website/src/main/java/dev/christopherbell/canesboxtracker/OfficialCanesBoxPriceClient.java`
- Lines: 119-121
- Action: replace

Current:
```java
    node.elements().forEachRemaining(child -> prices.addAll(findBoxComboPrices(child)));
```

Proposed:
```java
    node.values().iterator().forEachRemaining(child -> prices.addAll(findBoxComboPrices(child)));
```

Verification:
- `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:compileJava`

### Task 7 - Restore Spring Security 7 and Boot 4 MVC slice behavior

Sequence / dependencies:
- Runs after compile succeeds because the remaining failures were MVC-slice security regressions under Boot 4/Spring Security 7.

Implementation notes:
- Anchor the production JWT filter before Spring Security 7's `AuthorizationFilter`.
- Reuse production public route matchers from test security helpers.
- Keep method-security tests explicit without changing production authorization rules.

#### Code Edit 7.1
- File: `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- Lines: 19-116
- Action: replace

Current:
```java
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

.addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class)
```

Proposed:
```java
import org.springframework.security.web.access.intercept.AuthorizationFilter;

.addFilterBefore(jwtAuthenticationFilter, AuthorizationFilter.class)
```

Verification:
- `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:test --tests dev.christopherbell.configuration.JwtAuthenticationFilterTest`

#### Code Edit 7.2
- File: `website/src/test/java/dev/christopherbell/configuration/security/ControllerSliceSecurityTestConfig.java`
- Lines: after 1
- Action: add

Current:
```java
// file does not exist
```

Proposed:
```java
@TestConfiguration
@EnableWebSecurity
public class ControllerSliceSecurityTestConfig {
  // Test-only MVC slice filter chain using production public matchers and a bridge for @WithMockUser.
}
```

Verification:
- `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:test --tests dev.christopherbell.account.AccountControllerTest`

#### Code Edit 7.3
- File: `website/src/test/java/dev/christopherbell/configuration/security/ControllerSliceMethodSecurityTestConfig.java`
- Lines: after 1
- Action: add

Current:
```java
// file does not exist
```

Proposed:
```java
@TestConfiguration
@EnableWebSecurity
@EnableMethodSecurity
public class ControllerSliceMethodSecurityTestConfig extends ControllerSliceSecurityTestConfig {
}
```

Verification:
- `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:test --tests dev.christopherbell.canesboxtracker.CanesBoxTrackerControllerTest --tests dev.christopherbell.location.LocationControllerTest --tests dev.christopherbell.whatsforlunch.restaurant.RestaurantControllerMemberSecurityTest`

## Code Changes

- `build.gradle.kts`: replace Spring Boot Gradle plugin version `3.4.4` with `4.1.0`.
- `cbell-lib/build.gradle.kts`: replace Spring Boot dependency BOM `3.4.4` with `4.1.0`.
- `website/build.gradle.kts`: replace springdoc starter `2.8.8` with `3.0.3`.
- `website/build.gradle.kts`: add `spring-boot-starter-webmvc-test` for Boot 4 MVC slice tests.
- `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`: replace removed Spring Security `AntPathRequestMatcher` usage with `PathPatternRequestMatcher`.
- `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`: anchor the custom JWT filter before Spring Security 7 `AuthorizationFilter`.
- `cbell-lib` and `website` Java sources/tests: migrate Jackson imports to `tools.jackson` packages and replace Jackson 2 APIs removed in Jackson 3.
- `website/src/test/java/dev/christopherbell/configuration/security/*`: add Boot 4 MVC-slice security helpers for controller tests.
- `website/src/test/java/**`: update moved Boot 4 MVC test annotation imports from `org.springframework.boot.test.autoconfigure.web.servlet` to `org.springframework.boot.webmvc.test.autoconfigure`.

## Files and Modules

- `build.gradle.kts`
- `cbell-lib/build.gradle.kts`
- `website/build.gradle.kts`
- `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- `website` Spring Boot app module
- `cbell-lib` shared library module

## Unit Testing

- Baseline already passed before edits: `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120-baseline'; .\gradlew.bat --no-daemon :website:test`.
- After edits, run: `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:test`.
- Dependency resolution checks:
  - `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:dependencyInsight --dependency spring-boot --configuration runtimeClasspath`
  - `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:dependencyInsight --dependency springdoc-openapi-starter-webmvc-ui --configuration runtimeClasspath`

## Local Testing

- Start the app locally from the issue worktree with `local` profile and an alternate port, for example: `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; $env:SERVER_PORT='8082'; .\gradlew.bat --no-daemon :website:bootRun --args='--spring.profiles.active=local --server.port=8082'`.
- Exercise `GET http://localhost:8082/`; `GET http://localhost:8082/actuator/health` is protected by app security and returns 403 for anonymous smoke requests.
- Stop the local process after the smoke check unless it is needed for additional verification.

## Validation

- Spring Boot version resolves to `4.1.0` in the Gradle classpath.
- Springdoc starter resolves to `3.0.3`.
- `:website:test` passes after the upgrade.
- Local app starts on an alternate port and returns `200 OK` for the public home route.
- Pull request is opened and issue #1120 is closed only after implementation and test evidence are recorded.

## Rollback or Recovery

- Revert the three dependency version edits to restore Spring Boot `3.4.4` and springdoc `2.8.8` if Spring Boot 4.1 has incompatible runtime behavior that cannot be fixed safely in this issue.
- If the PR is opened but fails CI, leave issue #1120 open and update the GitHub thread with the failing check and next required compatibility fix.

## Risks

- Spring Boot 4.1 pulls Spring Framework 7 and Jackson 3, which can expose runtime incompatibilities not caught by compilation.
- Third-party starters can lag Spring Boot major versions; springdoc is upgraded to the 3.x line to reduce that risk.
- MongoDB-backed behavior is mostly covered by mocked tests here; local smoke testing does not prove production Mongo connectivity.

## Completion Criteria

- Dependency edits are committed on `codex/issue-1120-spring-boot-4-1`.
- Automated tests pass after the upgrade.
- Local runtime smoke check passes and is saved in a Builder test report.
- PR is created, verified, and merged or the issue is updated with a clear blocked state.
- Builder work record, implementation plan, test report, closure, indexes, validation, and session memory are saved.
