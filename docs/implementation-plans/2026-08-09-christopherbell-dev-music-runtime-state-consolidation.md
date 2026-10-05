# christopherbell.dev Music Runtime State Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development`
> (recommended) or `superpowers:executing-plans` to implement this plan task-by-task.
> Steps use checkbox (`- [ ]`) syntax for tracking.

## Document Status

`ready-for-execution`

**Goal:** Move queue and radio singleton state into one `music_runtime_state` collection
with two independently versioned documents, retain both old collections for seven days,
and provide a tested bounded reverse-copy operation without dropping any collection.

**Architecture:** One validated `MusicRuntimeStateDocument` envelope represents either the
`queue` or `radio` identity and makes mismatched kind/payload combinations unrepresentable.
A narrow `MusicRuntimeStateStore` owns exact-ID MongoDB reads and saves. Immutable migration
014 converts the two legacy `global` documents before the application becomes ready, while
a separately bounded production command can reverse-copy current destination state if an
application rollback is required.

**Tech Stack:** Java 25, Spring Boot 4.1, Spring Data MongoDB, MongoDB 8.x, JUnit 5,
AssertJ, Mockito, Gradle, PowerShell 7/Windows PowerShell 5.1, Pester, native MongoDB tools.

## Global Constraints

- Work only in an isolated worktree on branch `codex/music-runtime-state-consolidation`
  created from `origin/main` commit `0bcc8a9b83738df9c4adcf076e4be4443090448c` or a
  deliberately refreshed successor reviewed against this plan.
- Preserve unrelated state in `A:\Projects\christopherbell.dev`.
- Invoke `chris-street-style` and `superpowers:test-driven-development` before
  every production-code, test, migration, configuration, or reusable-script edit.
- Do not change public music endpoints, payloads, authorization, playback, or UI behavior.
- Keep queue and radio optimistic-lock versions independent.
- Fail closed on unexpected source count, identity, shape, version, or destination state.
- Do not mutate either legacy source during forward migration.
- Do not add a collection-drop operation in this plan.
- Production cutover requires a verified backup and candidate validation against a clone.
- Keep `music_queue_state` and `music_radio_state` for seven healthy production days.
- A later drop requires a fresh plan, exact preview, restore proof, and explicit approval.
- Keep operational output metadata-only and redact persisted values.

---

## Objective

Deliver the approved non-destructive consolidation cutover through tests, review, pull
request, CI, protected deployment, production verification, and a recorded seven-day
observation boundary. This plan ends with the two legacy collections still present.

## Goals

- Store queue state as `_id: "queue"`, `kind: "QUEUE"`, one queue payload, and its version.
- Store radio state as `_id: "radio"`, `kind: "RADIO"`, one radio payload, and its version.
- Preserve every source logical field and version through migration and reverse conversion.
- Remove broad legacy repositories from the runtime service boundary.
- Make partial or divergent migration destinations block startup.
- Provide a reverse-copy command that requires a stopped writer and verified fresh backup.
- Verify 48 live collections immediately after cutover: 47 original plus the new collection.

## Inputs

- Approved spec: `docs/specs/2026-08-09-christopherbell-dev-music-runtime-state-consolidation.md`
- Prior catalog delivery: PR `azurras/christopherbell.dev#1352`, deployed merge
  `0bcc8a9b83738df9c4adcf076e4be4443090448c`
- Fresh live metadata: 47 collections, 163 indexes, no live-only namespace
- Live source facts: one document in each source, both `_id: "global"`, one `_id` index each
- User decisions: simpler domain model, music runtime first, separate documents, seven days

## Branch

- Repository: `A:\Projects\christopherbell.dev`
- Base: refreshed `origin/main`
- Branch: `codex/music-runtime-state-consolidation`
- Worktree: `A:\Projects\christopherbell.dev-worktrees\music-runtime-state-consolidation`

## Non-Goals

- No other music or website collection is merged.
- No collection is dropped or renamed.
- No dual-write period is introduced.
- No public API or browser asset changes are made.
- No opportunistic repository cleanup or framework abstraction is included.
- The post-soak retirement implementation is not part of this plan.

## Assumptions

- Spring Data MongoDB retains the current `@Version` behavior when an immutable envelope is
  saved through `MongoTemplate.save(entity, collection)`; a real disposable Mongo test must
  witness this before publication.
- The protected deploy stops the production writer before the new binary runs migration 014.
- `New-ProductionBackup` continues to create a non-empty compressed archive, validate it with
  `mongorestore --dryRun`, and write a SHA-256 sidecar.
- The deployed operation scripts remain available while an older release is selected.
- The legacy source collections remain exactly one document each during the observation window.

## Open Questions

None. If the inspected base changes any literal range or interface, update and revalidate this
plan before editing; do not execute against stale ranges.

## Task Breakdown

### Task 1 - Add the validated shared storage representation

Sequence / dependencies:
- First implementation task; create the isolated worktree before executing it.
- Establishes the document and adapter interfaces consumed by Tasks 2 and 3.

Implementation notes:
- Required skill: `chris-street-style` before any code edits; it requires
  `superpowers:test-driven-development` for the new storage behavior.
- Before-Edit Brief:
  - Behavior: queue and radio domain states round-trip through distinct documents in one
    collection while retaining their independent versions.
  - Invariants: only `queue/QUEUE/queue-payload` and `radio/RADIO/radio-payload` are valid;
    version is null or non-negative; payload constructors reapply domain validation.
  - Boundary/API: `MusicRuntimeStateStore` exposes only `findQueue`, `saveQueue`, `findRadio`,
    and `saveRadio`; callers cannot enumerate or cross-read the shared collection.
  - Effects and failures: Mongo reads/writes are owned by the store; malformed persisted data
    throws at construction and infrastructure failures retain their Spring cause.
  - Tests and evidence: `MusicRuntimeStateDocumentTest` is RED because the document does not
    exist, then proves both round trips and invalid mixed payload rejection; a disposable
    Mongo check later proves real optimistic locking.

- [ ] Write `MusicRuntimeStateDocumentTest` first and run it to witness compilation failure.
- [ ] Add the validated document and narrow store until the focused test is green.
- [ ] Remove persistence mapping from the two domain records; retain the broad repository
  interfaces until Task 2 switches their remaining callers so every task boundary compiles.
- [ ] Run the focused document test plus compilation.
- [ ] Commit as `feat: add shared music runtime state storage`.

#### Code Edit 1.1
- File: `website/src/test/java/dev/christopherbell/music/radio/MusicRuntimeStateDocumentTest.java`
- Lines: 1-72
- Action: add

Proposed:
```java
package dev.christopherbell.music.radio;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.Instant;
import java.util.List;
import org.junit.jupiter.api.Test;

class MusicRuntimeStateDocumentTest {
  @Test
  void queueRoundTripPreservesEntriesAndVersion() {
    var entry = new MusicQueueState.Entry(
        "entry-1", "track-1", "token-1", "account-1", Instant.EPOCH);
    var state = new MusicQueueState(MusicQueueState.ID, List.of(entry), 7L);

    var document = MusicRuntimeStateDocument.forQueue(state);

    assertThat(document.id()).isEqualTo(MusicRuntimeStateDocument.QUEUE_ID);
    assertThat(document.kind()).isEqualTo(MusicRuntimeStateDocument.Kind.QUEUE);
    assertThat(document.toQueueState()).isEqualTo(state);
    assertThat(document.version()).isEqualTo(7L);
  }

  @Test
  void radioRoundTripPreservesTimelineAndVersion() {
    var state = new MusicRadioState(
        MusicRadioState.ID, 12, "track-1", "token-1", Instant.EPOCH, 90,
        MusicRadioState.Source.QUEUE, "entry-1", 8L);

    var document = MusicRuntimeStateDocument.forRadio(state);

    assertThat(document.id()).isEqualTo(MusicRuntimeStateDocument.RADIO_ID);
    assertThat(document.kind()).isEqualTo(MusicRuntimeStateDocument.Kind.RADIO);
    assertThat(document.toRadioState()).isEqualTo(state);
    assertThat(document.version()).isEqualTo(8L);
  }

  @Test
  void rejectsMixedIdentityKindAndPayload() {
    var queue = new MusicRuntimeStateDocument.QueuePayload(List.of());
    var radio = new MusicRuntimeStateDocument.RadioPayload(
        1, "track-1", "token-1", Instant.EPOCH, 90,
        MusicRadioState.Source.RADIO, null);

    assertThatThrownBy(() -> new MusicRuntimeStateDocument(
        MusicRuntimeStateDocument.QUEUE_ID,
        MusicRuntimeStateDocument.Kind.QUEUE,
        queue,
        radio,
        0L))
        .isInstanceOf(IllegalArgumentException.class);
    assertThatThrownBy(() -> new MusicRuntimeStateDocument(
        MusicRuntimeStateDocument.RADIO_ID,
        MusicRuntimeStateDocument.Kind.QUEUE,
        queue,
        null,
        0L))
        .isInstanceOf(IllegalArgumentException.class);
  }
}
```

Verification:
- RED: `gradlew.bat --no-daemon :website:test --tests "*MusicRuntimeStateDocumentTest"`
  fails because `MusicRuntimeStateDocument` is absent.
- GREEN: the same command passes all three tests.

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/music/radio/MusicRuntimeStateDocument.java`
- Lines: 1-130
- Action: add

Proposed:
```java
package dev.christopherbell.music.radio;

import java.time.Instant;
import java.util.List;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Version;
import org.springframework.data.mongodb.core.mapping.Document;

/** Collision-proof queue or radio state stored in the shared Music runtime collection. */
@Document(MusicRuntimeStateDocument.COLLECTION)
public record MusicRuntimeStateDocument(
    @Id String id,
    Kind kind,
    QueuePayload queue,
    RadioPayload radio,
    @Version Long version) {
  public static final String COLLECTION = "music_runtime_state";
  public static final String QUEUE_ID = "queue";
  public static final String RADIO_ID = "radio";

  public MusicRuntimeStateDocument {
    boolean validQueue = QUEUE_ID.equals(id) && kind == Kind.QUEUE
        && queue != null && radio == null;
    boolean validRadio = RADIO_ID.equals(id) && kind == Kind.RADIO
        && queue == null && radio != null;
    if ((!validQueue && !validRadio) || (version != null && version < 0)) {
      throw new IllegalArgumentException("Music runtime state is invalid.");
    }
  }

  public static MusicRuntimeStateDocument forQueue(MusicQueueState state) {
    return new MusicRuntimeStateDocument(
        QUEUE_ID, Kind.QUEUE, new QueuePayload(state.entries()), null, state.version());
  }

  public static MusicRuntimeStateDocument forRadio(MusicRadioState state) {
    return new MusicRuntimeStateDocument(
        RADIO_ID, Kind.RADIO, null, RadioPayload.from(state), state.version());
  }

  public MusicQueueState toQueueState() {
    if (kind != Kind.QUEUE) {
      throw new IllegalStateException("Music runtime state is not queue state.");
    }
    return new MusicQueueState(MusicQueueState.ID, queue.entries(), version);
  }

  public MusicRadioState toRadioState() {
    if (kind != Kind.RADIO) {
      throw new IllegalStateException("Music runtime state is not radio state.");
    }
    return radio.toState(version);
  }

  public enum Kind { QUEUE, RADIO }

  public record QueuePayload(List<MusicQueueState.Entry> entries) {
    public QueuePayload {
      entries = entries == null ? List.of() : List.copyOf(entries);
      new MusicQueueState(MusicQueueState.ID, entries, null);
    }
  }

  public record RadioPayload(
      long stationSequence,
      String trackId,
      String observedToken,
      Instant startedAt,
      double durationSeconds,
      MusicRadioState.Source source,
      String queueEntryId) {
    public RadioPayload {
      new MusicRadioState(
          MusicRadioState.ID, stationSequence, trackId, observedToken, startedAt,
          durationSeconds, source, queueEntryId, null);
    }

    static RadioPayload from(MusicRadioState state) {
      return new RadioPayload(
          state.stationSequence(), state.trackId(), state.observedToken(), state.startedAt(),
          state.durationSeconds(), state.source(), state.queueEntryId());
    }

    MusicRadioState toState(Long version) {
      return new MusicRadioState(
          MusicRadioState.ID, stationSequence, trackId, observedToken, startedAt,
          durationSeconds, source, queueEntryId, version);
    }
  }
}
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MusicRuntimeStateDocumentTest"`

#### Code Edit 1.3
- File: `website/src/main/java/dev/christopherbell/music/radio/MusicRuntimeStateStore.java`
- Lines: 1-48
- Action: add

Proposed:
```java
package dev.christopherbell.music.radio;

import java.util.Optional;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Component;

/** Owns exact-identity persistence for the two independently versioned runtime documents. */
@Component
public final class MusicRuntimeStateStore {
  private final MongoTemplate mongo;

  public MusicRuntimeStateStore(MongoTemplate mongo) {
    this.mongo = mongo;
  }

  public Optional<MusicQueueState> findQueue() {
    return Optional.ofNullable(mongo.findById(
        MusicRuntimeStateDocument.QUEUE_ID,
        MusicRuntimeStateDocument.class,
        MusicRuntimeStateDocument.COLLECTION)).map(MusicRuntimeStateDocument::toQueueState);
  }

  public MusicQueueState saveQueue(MusicQueueState state) {
    return mongo.save(
        MusicRuntimeStateDocument.forQueue(state),
        MusicRuntimeStateDocument.COLLECTION).toQueueState();
  }

  public Optional<MusicRadioState> findRadio() {
    return Optional.ofNullable(mongo.findById(
        MusicRuntimeStateDocument.RADIO_ID,
        MusicRuntimeStateDocument.class,
        MusicRuntimeStateDocument.COLLECTION)).map(MusicRuntimeStateDocument::toRadioState);
  }

  public MusicRadioState saveRadio(MusicRadioState state) {
    return mongo.save(
        MusicRuntimeStateDocument.forRadio(state),
        MusicRuntimeStateDocument.COLLECTION).toRadioState();
  }
}
```

Verification:
- `gradlew.bat --no-daemon :website:compileJava`

#### Code Edit 1.4
- File: `website/src/main/java/dev/christopherbell/music/radio/MusicQueueState.java`
- Lines: 5-10
- Action: replace

Current:
```java
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Version;
import org.springframework.data.mongodb.core.mapping.Document;

/** One optimistic, globally ordered Music queue with no per-user silo. */
@Document("music_queue_state")
```

Proposed:
```java
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Version;

/** One optimistic, globally ordered Music queue with no per-user silo. */
```

Verification:
- `gradlew.bat --no-daemon :website:compileJava`

#### Code Edit 1.5
- File: `website/src/main/java/dev/christopherbell/music/radio/MusicRadioState.java`
- Lines: 4-9
- Action: replace

Current:
```java
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Version;
import org.springframework.data.mongodb.core.mapping.Document;

/** Durable identity and trusted catalog duration for the one global Music station. */
@Document("music_radio_state")
```

Proposed:
```java
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Version;

/** Durable identity and trusted catalog duration for the one global Music station. */
```

Verification:
- `gradlew.bat --no-daemon :website:compileJava`

#### Code Edit 1.6 (sequenced with Task 2)
- File: `website/src/main/java/dev/christopherbell/music/radio/MusicQueueStateRepository.java`
- Lines: 1-5
- Action: delete
- Sequencing: perform this edit in Task 2, after all callers switch; retain unchanged in Task 1.

Current:
```java
package dev.christopherbell.music.radio;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface MusicQueueStateRepository extends MongoRepository<MusicQueueState, String> {}
```

Proposed: delete block in Task 2

Verification:
- `rg -n "MusicQueueStateRepository" website/src/main website/src/test` finds only Task 2
  callers before Task 2 and no matches after Task 2.

#### Code Edit 1.7 (sequenced with Task 2)
- File: `website/src/main/java/dev/christopherbell/music/radio/MusicRadioRepository.java`
- Lines: 1-5
- Action: delete
- Sequencing: perform this edit in Task 2, after all callers switch; retain unchanged in Task 1.

Current:
```java
package dev.christopherbell.music.radio;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface MusicRadioRepository extends MongoRepository<MusicRadioState, String> {}
```

Proposed: delete block in Task 2

Verification:
- `rg -n "MusicRadioRepository" website/src/main website/src/test` finds only Task 2
  callers before Task 2 and no matches after Task 2.

### Task 2 - Route queue and radio services through the narrow store

Sequence / dependencies:
- Runs after Task 1 because the new store must compile before callers switch.

Implementation notes:
- Required skill: `chris-street-style` before any code edits; invoke
  `superpowers:test-driven-development` and record the existing service tests as the green
  characterization baseline for this behavior-preserving dependency refactor.
- Before-Edit Brief:
  - Behavior: queue API results, radio transitions, lease behavior, history idempotency,
    conflict mapping, and queue consumption remain unchanged.
  - Invariants: queue methods can touch only queue state; radio methods can touch only radio
    state; each uses the version returned by its own store operation.
  - Boundary/API: only constructor dependency types and storage method names change; HTTP
    controllers and response types remain untouched.
  - Effects and failures: the store owns Mongo I/O; services retain current conflict and
    domain error translation.
  - Tests and evidence: existing service tests pass before and after; revised doubles model
    the store's complete narrow interface and assertions remain on service results.

- [ ] Run both existing service tests as the pre-edit characterization baseline.
- [ ] Replace repository dependencies and exact calls in both services.
- [ ] Update service tests to use `MusicRuntimeStateStore` without asserting mocks as output.
- [ ] Delete `MusicQueueStateRepository` and `MusicRadioRepository` after all callers switch.
- [ ] Run both focused test classes and the music package tests.
- [ ] Commit as `refactor: use shared music runtime state store`.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/music/radio/MusicQueueService.java`
- Lines: 21-31
- Action: replace

Current:
```java
  private final MusicQueueStateRepository queues;
  private final MusicCatalog catalog;
  private final MusicAccessService access;
  private final Clock clock;

  public MusicQueueService(
      MusicQueueStateRepository queues,
      MusicCatalog catalog,
      MusicAccessService access,
      Clock clock) {
    this.queues = queues;
```

Proposed:
```java
  private final MusicRuntimeStateStore runtimeState;
  private final MusicCatalog catalog;
  private final MusicAccessService access;
  private final Clock clock;

  public MusicQueueService(
      MusicRuntimeStateStore runtimeState,
      MusicCatalog catalog,
      MusicAccessService access,
      Clock clock) {
    this.runtimeState = runtimeState;
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MusicQueueServiceTest"`

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/music/radio/MusicQueueService.java`
- Lines: 118-125
- Action: replace

Current:
```java
  private MusicQueueState load() {
    return queues.findById(MusicQueueState.ID).orElseGet(MusicQueueState::empty);
  }

  private MusicQueueState save(MusicQueueState state) {
    try {
      return queues.save(state);
```

Proposed:
```java
  private MusicQueueState load() {
    return runtimeState.findQueue().orElseGet(MusicQueueState::empty);
  }

  private MusicQueueState save(MusicQueueState state) {
    try {
      return runtimeState.saveQueue(state);
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MusicQueueServiceTest"`

#### Code Edit 2.3
- File: `website/src/main/java/dev/christopherbell/music/radio/MusicRadioService.java`
- Lines: 30-30
- Action: replace

Current:
```java
  private final MusicRadioRepository states;
```

Proposed:
```java
  private final MusicRuntimeStateStore runtimeState;
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MusicRadioServiceTest"`

#### Code Edit 2.4
- File: `website/src/main/java/dev/christopherbell/music/radio/MusicRadioService.java`
- Lines: 40-55
- Action: replace

Current:
```java
  public MusicRadioService(
      MusicProperties musicProperties,
      MusicRadioProperties radioProperties,
      MusicCatalog catalog,
      MusicRadioRepository states,
      MusicRadioHistoryRepository history,
      MusicQueueService queue,
      MusicRadioSelector selector,
      MusicAccessService access,
      MongoLeaseService leases,
      Clock clock) {
    this.musicProperties = musicProperties;
    this.radioProperties = radioProperties;
    this.catalog = catalog;
    this.states = states;
```

Proposed:
```java
  public MusicRadioService(
      MusicProperties musicProperties,
      MusicRadioProperties radioProperties,
      MusicCatalog catalog,
      MusicRuntimeStateStore runtimeState,
      MusicRadioHistoryRepository history,
      MusicQueueService queue,
      MusicRadioSelector selector,
      MusicAccessService access,
      MongoLeaseService leases,
      Clock clock) {
    this.musicProperties = musicProperties;
    this.radioProperties = radioProperties;
    this.catalog = catalog;
    this.runtimeState = runtimeState;
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MusicRadioServiceTest"`

#### Code Edit 2.5
- File: `website/src/main/java/dev/christopherbell/music/radio/MusicRadioService.java`
- Lines: 82-82
- Action: replace

Current:
```java
        return snapshot(states.findById(MusicRadioState.ID).orElse(null), now);
```

Proposed:
```java
        return snapshot(runtimeState.findRadio().orElse(null), now);
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MusicRadioServiceTest"`

#### Code Edit 2.6
- File: `website/src/main/java/dev/christopherbell/music/radio/MusicRadioService.java`
- Lines: 93-93
- Action: replace

Current:
```java
    MusicRadioState state = states.findById(MusicRadioState.ID).orElse(null);
```

Proposed:
```java
    MusicRadioState state = runtimeState.findRadio().orElse(null);
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MusicRadioServiceTest"`

#### Code Edit 2.7
- File: `website/src/main/java/dev/christopherbell/music/radio/MusicRadioService.java`
- Lines: 129-132
- Action: replace

Current:
```java
        state = states.save(replacement);
      } catch (OptimisticLockingFailureException | DuplicateKeyException contention) {
        return snapshot(states.findById(MusicRadioState.ID).orElse(null), now);
```

Proposed:
```java
        state = runtimeState.saveRadio(replacement);
      } catch (OptimisticLockingFailureException | DuplicateKeyException contention) {
        return snapshot(runtimeState.findRadio().orElse(null), now);
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MusicRadioServiceTest"`

#### Code Edit 2.8
- File: `website/src/test/java/dev/christopherbell/music/radio/MusicQueueServiceTest.java`
- Lines: 24-36
- Action: replace

Current:
```java
    var queues = mock(MusicQueueStateRepository.class);
    var catalog = mock(MusicCatalog.class);
    var access = mock(MusicAccessService.class);
    MusicTrack track = track("song.mp3");
    when(access.requireWrite()).thenReturn(Account.builder().id("writer-1").build());
    when(catalog.findReady(track.id())).thenReturn(Optional.of(track));
    when(queues.findById(MusicQueueState.ID)).thenReturn(Optional.empty());
    when(queues.save(org.mockito.ArgumentMatchers.any())).thenAnswer(invocation -> {
      MusicQueueState state = invocation.getArgument(0);
      return new MusicQueueState(state.id(), state.entries(), 0L);
    });
    var service = new MusicQueueService(
        queues, catalog, access,
```

Proposed:
```java
    var runtimeState = mock(MusicRuntimeStateStore.class);
    var catalog = mock(MusicCatalog.class);
    var access = mock(MusicAccessService.class);
    MusicTrack track = track("song.mp3");
    when(access.requireWrite()).thenReturn(Account.builder().id("writer-1").build());
    when(catalog.findReady(track.id())).thenReturn(Optional.of(track));
    when(runtimeState.findQueue()).thenReturn(Optional.empty());
    when(runtimeState.saveQueue(org.mockito.ArgumentMatchers.any())).thenAnswer(invocation -> {
      MusicQueueState state = invocation.getArgument(0);
      return new MusicQueueState(state.id(), state.entries(), 0L);
    });
    var service = new MusicQueueService(
        runtimeState, catalog, access,
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MusicQueueServiceTest"`

#### Code Edit 2.9
- File: `website/src/test/java/dev/christopherbell/music/radio/MusicQueueServiceTest.java`
- Lines: 50-56
- Action: replace

Current:
```java
    var queues = mock(MusicQueueStateRepository.class);
    when(queues.findById(MusicQueueState.ID))
        .thenReturn(Optional.of(new MusicQueueState(MusicQueueState.ID, java.util.List.of(), 3L)));
    var access = mock(MusicAccessService.class);
    when(access.requireWrite()).thenReturn(Account.builder().id("writer-1").build());
    var service = new MusicQueueService(
        queues, mock(MusicCatalog.class), access, Clock.systemUTC());
```

Proposed:
```java
    var runtimeState = mock(MusicRuntimeStateStore.class);
    when(runtimeState.findQueue())
        .thenReturn(Optional.of(new MusicQueueState(MusicQueueState.ID, java.util.List.of(), 3L)));
    var access = mock(MusicAccessService.class);
    when(access.requireWrite()).thenReturn(Account.builder().id("writer-1").build());
    var service = new MusicQueueService(
        runtimeState, mock(MusicCatalog.class), access, Clock.systemUTC());
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MusicQueueServiceTest"`

#### Code Edit 2.10
- File: `website/src/test/java/dev/christopherbell/music/radio/MusicRadioServiceTest.java`
- Lines: 41-47
- Action: replace

Current:
```java
    var states = mock(MusicRadioRepository.class);
    when(states.findById(MusicRadioState.ID)).thenReturn(Optional.empty());
    when(states.save(any())).thenAnswer(invocation -> invocation.getArgument(0));
    var history = mock(MusicRadioHistoryRepository.class);
    when(history.findTop100ByOrderByStationSequenceDesc()).thenReturn(List.of());

    MusicRadioSnapshot result = service(catalog, states, history, queue, mockSelector()).current();
```

Proposed:
```java
    var runtimeState = mock(MusicRuntimeStateStore.class);
    when(runtimeState.findRadio()).thenReturn(Optional.empty());
    when(runtimeState.saveRadio(any())).thenAnswer(invocation -> invocation.getArgument(0));
    var history = mock(MusicRadioHistoryRepository.class);
    when(history.findTop100ByOrderByStationSequenceDesc()).thenReturn(List.of());

    MusicRadioSnapshot result = service(
        catalog, runtimeState, history, queue, mockSelector()).current();
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MusicRadioServiceTest"`
- `gradlew.bat --no-daemon :website:test --tests "dev.christopherbell.music.*"`

#### Code Edit 2.11
- File: `website/src/test/java/dev/christopherbell/music/radio/MusicRadioServiceTest.java`
- Lines: 71-88
- Action: replace

Current:
```java
    var states = mock(MusicRadioRepository.class);
    when(states.findById(MusicRadioState.ID)).thenReturn(Optional.of(initial));
    when(states.save(any())).thenAnswer(invocation -> invocation.getArgument(0));
    var history = mock(MusicRadioHistoryRepository.class);
    when(history.findTop100ByOrderByStationSequenceDesc()).thenReturn(List.of());
    when(history.existsById("station:1")).thenReturn(true);
    var queue = mock(MusicQueueService.class);
    when(queue.loadForRadio()).thenReturn(MusicQueueState.empty());
    var selector = mockSelector();
    when(selector.select(anyList(), anyList(), anyString())).thenReturn(b, c);

    MusicRadioSnapshot result = service(catalog, states, history, queue, selector).current();

    assertThat(result.stationSequence()).isEqualTo(3);
    assertThat(result.trackId()).isEqualTo(c.id());
    assertThat(result.startedAt()).isEqualTo(NOW.minusSeconds(5));
    assertThat(result.positionSeconds()).isEqualTo(5);
    verify(states, times(2)).save(any());
```

Proposed:
```java
    var runtimeState = mock(MusicRuntimeStateStore.class);
    when(runtimeState.findRadio()).thenReturn(Optional.of(initial));
    when(runtimeState.saveRadio(any())).thenAnswer(invocation -> invocation.getArgument(0));
    var history = mock(MusicRadioHistoryRepository.class);
    when(history.findTop100ByOrderByStationSequenceDesc()).thenReturn(List.of());
    when(history.existsById("station:1")).thenReturn(true);
    var queue = mock(MusicQueueService.class);
    when(queue.loadForRadio()).thenReturn(MusicQueueState.empty());
    var selector = mockSelector();
    when(selector.select(anyList(), anyList(), anyString())).thenReturn(b, c);

    MusicRadioSnapshot result = service(catalog, runtimeState, history, queue, selector).current();

    assertThat(result.stationSequence()).isEqualTo(3);
    assertThat(result.trackId()).isEqualTo(c.id());
    assertThat(result.startedAt()).isEqualTo(NOW.minusSeconds(5));
    assertThat(result.positionSeconds()).isEqualTo(5);
    verify(runtimeState, times(2)).saveRadio(any());
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MusicRadioServiceTest"`

#### Code Edit 2.12
- File: `website/src/test/java/dev/christopherbell/music/radio/MusicRadioServiceTest.java`
- Lines: 92-103
- Action: replace

Current:
```java
  private MusicRadioService service(
      MusicCatalog catalog,
      MusicRadioRepository states,
      MusicRadioHistoryRepository history,
      MusicQueueService queue,
      MusicRadioSelector selector) {
    var leases = mock(MongoLeaseService.class);
    when(leases.tryAcquire(anyString(), anyString(), any(), any())).thenReturn(true);
    when(leases.release(anyString(), anyString())).thenReturn(true);
    return new MusicRadioService(
        musicProperties(), radioProperties(), catalog, states, history, queue, selector,
        mock(MusicAccessService.class), leases, Clock.fixed(NOW, ZoneOffset.UTC));
```

Proposed:
```java
  private MusicRadioService service(
      MusicCatalog catalog,
      MusicRuntimeStateStore runtimeState,
      MusicRadioHistoryRepository history,
      MusicQueueService queue,
      MusicRadioSelector selector) {
    var leases = mock(MongoLeaseService.class);
    when(leases.tryAcquire(anyString(), anyString(), any(), any())).thenReturn(true);
    when(leases.release(anyString(), anyString())).thenReturn(true);
    return new MusicRadioService(
        musicProperties(), radioProperties(), catalog, runtimeState, history, queue, selector,
        mock(MusicAccessService.class), leases, Clock.fixed(NOW, ZoneOffset.UTC));
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MusicRadioServiceTest"`

### Task 3 - Add immutable migration 014 and reverse-fidelity tests

Sequence / dependencies:
- Runs after Tasks 1 and 2 because it uses the target document factories and final runtime
  mapping.

Implementation notes:
- Required skill: `chris-street-style` before any code edits; invoke
  `superpowers:test-driven-development` and witness the migration test fail before adding V014.
- Execution correction from real MongoDB evidence: typed `MongoTemplate` reads and inserts are
  not safe for this migration because conversion can normalize malformed BSON and `@Version`
  initialization resets migrated versions. V014 must validate raw BSON and insert raw target
  documents. An absent legacy version remains absent at rest; the first later store save uses an
  atomic, no-upsert compare-and-set from a missing version to version `0`, and a zero-match is an
  optimistic conflict rather than an overwrite.
- Before-Edit Brief:
  - Behavior: startup copies each present valid legacy queue/radio singleton into its target
    identity, preserving logical payloads and versions while leaving sources intact; zero or one
    document per source is valid because the legacy runtime creates missing state lazily.
  - Invariants: destination is either empty or exactly equivalent; partial, duplicate,
    malformed, extra, or divergent state is rejected before an insert.
  - Boundary/API: immutable `ApplicationMigration` id
    `014-consolidate-music-runtime-state` with checksum
    `11a69bdd4556cfc38060ccdda5075fb9d6bc36f1cc414edd7b26cd61a74b5cbb`.
  - Effects and failures: only the empty destination receives the exact set of present-source
    target documents (possibly none); source reads are explicit by literal namespace; runner
    redaction remains unchanged.
  - Tests and evidence: RED test proves V014 is absent; GREEN tests prove copy fidelity,
    equivalent rerun acceptance, and pre-write refusal for bad source/partial destination.

- [ ] Write V014 tests first and witness RED.
- [ ] Implement raw-BSON preflight, lossless conversion, raw insert, and readback equivalence.
- [ ] Prove nonzero and absent version behavior plus the first-write compare-and-set against a
  disposable, non-production MongoDB instance.
- [ ] Run migration tests and runner regression tests.
- [ ] Later, repeat the proof against a restored production clone before cutover.
- [ ] Commit as `feat: migrate music runtime state`.

#### Code Edit 3.1
- File: `website/src/test/java/dev/christopherbell/configuration/mongo/migration/V014ConsolidateMusicRuntimeStateTest.java`
- Lines: 1-150
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.mongo.migration;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import dev.christopherbell.music.radio.MusicQueueState;
import dev.christopherbell.music.radio.MusicRadioState;
import dev.christopherbell.music.radio.MusicRuntimeStateDocument;
import java.time.Instant;
import java.util.Collection;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Query;

class V014ConsolidateMusicRuntimeStateTest {
  private final MongoTemplate mongo = org.mockito.Mockito.mock(MongoTemplate.class);

  @Test
  void copiesBothValidatedSourcesAndPreservesVersions() {
    var queue = new MusicQueueState(MusicQueueState.ID, List.of(), 4L);
    var radio = radio(9L);
    validSources(queue, radio);
    when(mongo.findAll(MusicRuntimeStateDocument.class, MusicRuntimeStateDocument.COLLECTION))
        .thenReturn(List.of(), List.of(
            MusicRuntimeStateDocument.forQueue(queue),
            MusicRuntimeStateDocument.forRadio(radio)));

    new V014ConsolidateMusicRuntimeState().apply(mongo);

    var inserted = ArgumentCaptor.<Collection<?>>forClass(Collection.class);
    verify(mongo).insert(inserted.capture(), eq(MusicRuntimeStateDocument.COLLECTION));
    assertThat(inserted.getValue()).containsExactlyInAnyOrder(
        MusicRuntimeStateDocument.forQueue(queue),
        MusicRuntimeStateDocument.forRadio(radio));
  }

  @Test
  void acceptsOnlyACompleteEquivalentDestination() {
    var queue = new MusicQueueState(MusicQueueState.ID, List.of(), 4L);
    var radio = radio(9L);
    validSources(queue, radio);
    when(mongo.findAll(MusicRuntimeStateDocument.class, MusicRuntimeStateDocument.COLLECTION))
        .thenReturn(List.of(
            MusicRuntimeStateDocument.forRadio(radio),
            MusicRuntimeStateDocument.forQueue(queue)));

    new V014ConsolidateMusicRuntimeState().apply(mongo);

    verify(mongo, never()).insert(any(Collection.class), eq(MusicRuntimeStateDocument.COLLECTION));
  }

  @Test
  void rejectsPartialDestinationBeforeWriting() {
    var queue = new MusicQueueState(MusicQueueState.ID, List.of(), 4L);
    var radio = radio(9L);
    validSources(queue, radio);
    when(mongo.findAll(MusicRuntimeStateDocument.class, MusicRuntimeStateDocument.COLLECTION))
        .thenReturn(List.of(MusicRuntimeStateDocument.forQueue(queue)));

    assertThatThrownBy(() -> new V014ConsolidateMusicRuntimeState().apply(mongo))
        .isInstanceOf(IllegalStateException.class)
        .hasMessageContaining("destination");
    verify(mongo, never()).insert(any(Collection.class), eq(MusicRuntimeStateDocument.COLLECTION));
  }

  @Test
  void rejectsUnexpectedLegacyCardinalityBeforeWriting() {
    when(mongo.count(any(Query.class), eq(V014ConsolidateMusicRuntimeState.LEGACY_QUEUE)))
        .thenReturn(2L);

    assertThatThrownBy(() -> new V014ConsolidateMusicRuntimeState().apply(mongo))
        .isInstanceOf(IllegalStateException.class)
        .hasMessageContaining("cardinality");
    verify(mongo, never()).insert(any(Collection.class), eq(MusicRuntimeStateDocument.COLLECTION));
  }

  private void validSources(MusicQueueState queue, MusicRadioState radio) {
    when(mongo.count(any(Query.class), eq(V014ConsolidateMusicRuntimeState.LEGACY_QUEUE)))
        .thenReturn(1L);
    when(mongo.count(any(Query.class), eq(V014ConsolidateMusicRuntimeState.LEGACY_RADIO)))
        .thenReturn(1L);
    when(mongo.findById(MusicQueueState.ID, MusicQueueState.class,
        V014ConsolidateMusicRuntimeState.LEGACY_QUEUE)).thenReturn(queue);
    when(mongo.findById(MusicRadioState.ID, MusicRadioState.class,
        V014ConsolidateMusicRuntimeState.LEGACY_RADIO)).thenReturn(radio);
  }

  private MusicRadioState radio(Long version) {
    return new MusicRadioState(
        MusicRadioState.ID, 3, "track-1", "token-1", Instant.EPOCH, 90,
        MusicRadioState.Source.RADIO, null, version);
  }
}
```

Verification:
- RED: focused test fails because `V014ConsolidateMusicRuntimeState` is absent.
- GREEN: `gradlew.bat --no-daemon :website:test --tests "*V014ConsolidateMusicRuntimeStateTest"`

#### Code Edit 3.2
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/V014ConsolidateMusicRuntimeState.java`
- Lines: 1-105
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.mongo.migration;

import dev.christopherbell.music.radio.MusicQueueState;
import dev.christopherbell.music.radio.MusicRadioState;
import dev.christopherbell.music.radio.MusicRuntimeStateDocument;
import java.util.HashMap;
import java.util.List;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Component;

/** Additively consolidates the two legacy Music runtime singleton documents. */
@Component
public final class V014ConsolidateMusicRuntimeState implements ApplicationMigration {
  static final String LEGACY_QUEUE = "music_queue_state";
  static final String LEGACY_RADIO = "music_radio_state";
  private static final String CHECKSUM =
      "11a69bdd4556cfc38060ccdda5075fb9d6bc36f1cc414edd7b26cd61a74b5cbb";

  @Override public String id() { return "014-consolidate-music-runtime-state"; }
  @Override public String checksum() { return CHECKSUM; }
  @Override public String description() { return "Consolidate Music queue and radio runtime state"; }

  @Override
  public void apply(MongoTemplate mongo) {
    var queue = requireLegacy(
        mongo, LEGACY_QUEUE, MusicQueueState.ID, MusicQueueState.class);
    var radio = requireLegacy(
        mongo, LEGACY_RADIO, MusicRadioState.ID, MusicRadioState.class);
    List<MusicRuntimeStateDocument> expected = List.of(
        MusicRuntimeStateDocument.forQueue(queue),
        MusicRuntimeStateDocument.forRadio(radio));
    List<MusicRuntimeStateDocument> existing = destination(mongo);
    if (!existing.isEmpty()) {
      requireEquivalent(existing, queue, radio);
      return;
    }

    mongo.insert(expected, MusicRuntimeStateDocument.COLLECTION);
    requireEquivalent(destination(mongo), queue, radio);
  }

  private static <T> T requireLegacy(
      MongoTemplate mongo, String collection, String id, Class<T> type) {
    if (mongo.count(new Query(), collection) != 1) {
      throw new IllegalStateException("Legacy Music runtime state has unexpected cardinality.");
    }
    T state = mongo.findById(id, type, collection);
    if (state == null) {
      throw new IllegalStateException("Legacy Music runtime state has an unexpected identity.");
    }
    return state;
  }

  private static List<MusicRuntimeStateDocument> destination(MongoTemplate mongo) {
    return mongo.findAll(MusicRuntimeStateDocument.class, MusicRuntimeStateDocument.COLLECTION);
  }

  private static void requireEquivalent(
      List<MusicRuntimeStateDocument> documents,
      MusicQueueState queue,
      MusicRadioState radio) {
    if (documents.size() != 2) {
      throw new IllegalStateException("Music runtime state destination is partial or unexpected.");
    }
    var byId = new HashMap<String, MusicRuntimeStateDocument>();
    for (var document : documents) {
      if (byId.put(document.id(), document) != null) {
        throw new IllegalStateException("Music runtime state destination has duplicate identities.");
      }
    }
    var targetQueue = byId.get(MusicRuntimeStateDocument.QUEUE_ID);
    var targetRadio = byId.get(MusicRuntimeStateDocument.RADIO_ID);
    if (targetQueue == null || targetRadio == null
        || !queue.equals(targetQueue.toQueueState())
        || !radio.equals(targetRadio.toRadioState())) {
      throw new IllegalStateException("Music runtime state destination diverges from its sources.");
    }
  }
}
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*V014ConsolidateMusicRuntimeStateTest" --tests "*MongoMigrationRunnerTest"`

### Task 4 - Teach the collection catalog the migration lifecycle

Sequence / dependencies:
- Runs after Task 3 because the catalog must reflect the final mapped type and manual migration
  owner names.

Implementation notes:
- Required skill: `chris-street-style` before test or documentation edits; invoke
  `superpowers:test-driven-development` for the architecture policy behavior.
- Before-Edit Brief:
  - Behavior: catalog validation recognizes the new active collection and the two intentionally
    retained legacy sources without treating either as an orphan or deletion authorization.
  - Invariants: every mapped/manual owner remains cataloged; `rollback-retained` is source-backed;
    only the expected target document maps to the new collection.
  - Boundary/API: the Markdown catalog remains the source of truth consumed by
    `MongoCollectionCatalogTest` and metadata inventory review.
  - Effects and failures: no database I/O; a stale or undocumented mapping fails the architecture
    test during build.
  - Tests and evidence: the existing expected-size test becomes RED after Tasks 1-3, then passes
    with 52 source-backed names and the new lifecycle vocabulary.

- [ ] Run `MongoCollectionCatalogTest` and witness the expected mapping/count failure.
- [ ] Update lifecycle vocabulary, table rows, provenance, and architecture expectations.
- [ ] Run the focused architecture test and catalog inventory generator tests.
- [ ] Commit as `docs: catalog music runtime state migration`.

#### Code Edit 4.1
- File: `docs/operations/mongodb-collection-catalog.md`
- Lines: 3-8
- Action: replace

Current:
```markdown
This catalog is the source of truth for physical collection ownership in the
`christopherbell` database. Logical groups do not merge storage. A
`legacy-named` entry remains active under its physical name until a separately
approved migration proves compatibility and rollback. `orphan-candidate` and
`system-managed` classify reviewed non-source rows; they are not counted as
source-backed mappings and never authorize cleanup.
```

Proposed:
````markdown
This catalog is the source of truth for physical collection ownership in the
`christopherbell` database. `legacy-named` remains active under a historical
name. `rollback-retained` is source-backed data intentionally preserved during
an approved migration observation window; it never authorizes cleanup.
`orphan-candidate` and `system-managed` classify reviewed non-source rows and
also never authorize cleanup.
````

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MongoCollectionCatalogTest"`

#### Code Edit 4.2
- File: `docs/operations/mongodb-collection-catalog.md`
- Lines: 36-38
- Action: replace

Current:
```markdown
| `music_queue_state` | Music queue state | music and `MusicQueueState` | singleton-state | One global optimistic queue document | `_id` fixed key and optimistic version | user | active |
| `music_radio_history` | Music radio history | music and `MusicRadioHistoryEvent` | event-history | Append-only playback history | Station sequence and occurrence-time indexes | user | active |
| `music_radio_state` | Music radio state | music and `MusicRadioState` | singleton-state | One global optimistic station document | `_id` fixed key and optimistic version | user | active |
```

Proposed:
```markdown
| `music_queue_state` | Legacy Music queue state | music migration and `MusicQueueState` | singleton-state | One immutable rollback copy retained for seven days after cutover | `_id` fixed key and optimistic version | user | rollback-retained |
| `music_radio_history` | Music radio history | music and `MusicRadioHistoryEvent` | event-history | Append-only playback history | Station sequence and occurrence-time indexes | user | active |
| `music_radio_state` | Legacy Music radio state | music migration and `MusicRadioState` | singleton-state | One immutable rollback copy retained for seven days after cutover | `_id` fixed key and optimistic version | user | rollback-retained |
| `music_runtime_state` | Music runtime state | music and `MusicRuntimeStateDocument`; `MusicRuntimeStateStore` | singleton-state | Exactly queue and radio documents with independent optimistic versions | Collision-proof `_id` values `queue` and `radio` | user | active |
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MongoCollectionCatalogTest"`

#### Code Edit 4.3
- File: `docs/operations/mongodb-collection-catalog.md`
- Lines: after 99
- Action: add

Proposed:
```markdown
| `dev.christopherbell.configuration.mongo.migration.V014ConsolidateMusicRuntimeState` | `music_queue_state`, `music_radio_state`, `music_runtime_state` |
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MongoCollectionCatalogTest"`

#### Code Edit 4.4
- File: `docs/operations/mongodb-collection-catalog.md`
- Lines: after 108
- Action: add

Proposed:
```markdown
| `dev.christopherbell.music.radio.MusicRuntimeStateStore` | `music_runtime_state` |
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MongoCollectionCatalogTest"`

#### Code Edit 4.5
- File: `website/src/test/java/dev/christopherbell/architecture/MongoCollectionCatalogTest.java`
- Lines: 44-46
- Action: replace

Current:
```java
  private static final Set<String> VALID_STATUSES = Set.of(
      "active", "legacy-named", "orphan-candidate", "system-managed");
  private static final Set<String> SOURCE_BACKED_STATUSES = Set.of("active", "legacy-named");
```

```java
    assertThat(expected).hasSize(51);
```

Proposed:
```java
  private static final Set<String> VALID_STATUSES = Set.of(
      "active", "legacy-named", "rollback-retained", "orphan-candidate", "system-managed");
  private static final Set<String> SOURCE_BACKED_STATUSES = Set.of(
      "active", "legacy-named", "rollback-retained");
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MongoCollectionCatalogTest"`

#### Code Edit 4.6
- File: `website/src/test/java/dev/christopherbell/architecture/MongoCollectionCatalogTest.java`
- Lines: after 92
- Action: add

Proposed:
```java
      manualOwner("dev.christopherbell.configuration.mongo.migration.V014ConsolidateMusicRuntimeState",
          "music_queue_state", "music_radio_state", "music_runtime_state"),
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MongoCollectionCatalogTest"`

#### Code Edit 4.7
- File: `website/src/test/java/dev/christopherbell/architecture/MongoCollectionCatalogTest.java`
- Lines: after 106
- Action: add

Proposed:
```java
      manualOwner("dev.christopherbell.music.radio.MusicRuntimeStateStore",
          "music_runtime_state"),
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MongoCollectionCatalogTest"`

#### Code Edit 4.8
- File: `website/src/test/java/dev/christopherbell/architecture/MongoCollectionCatalogTest.java`
- Lines: 177-177
- Action: replace

Current:
```java
    assertThat(expected).hasSize(51);
```

Proposed:
```java
    assertThat(expected).hasSize(52);
```

Verification:
- `gradlew.bat --no-daemon :website:test --tests "*MongoCollectionCatalogTest"`

### Task 5 - Add a bounded reverse-copy rollback operation

Sequence / dependencies:
- Runs after Tasks 1-4 because its script targets the final nested destination schema.
- This operation restores current destination state into retained legacy documents; it does
  not drop collections and is used only with the website writer stopped.

Implementation notes:
- Required skill: `chris-street-style` before script, configuration, test, or runbook
  edits; invoke `superpowers:test-driven-development` and read the PowerShell script tests first.
- Execution safety refinement: the confirmed operation acquires the established `deploy.lock`
  before the first writer-state check and holds it through backup, mutation, validation, failure
  wrapping, and disposal. Post-backup failures expose only an allowlisted phase/code and the
  retained archive path while preserving a redacted causal exception.
- Disposable-Mongo tests accept only an explicit credential-free loopback URI on a non-27017
  port. Every Mongo invocation revalidates a canonical, non-reparse, marker-owned data root plus
  OS process start identity, then performs same-connection Mongo startup, `dbPath`, bind, and port
  checks before any fixture reset or mutation.
- Before-Edit Brief:
  - Behavior: `prod.cmd music-runtime-rollback -WhatIf` produces a no-write preview; actual
    reverse copy requires an explicit confirmation switch, stopped website service, and fresh
    verified backup, then returns only bounded metadata.
  - Invariants: exactly two valid destination documents and exactly one retained `global`
    document per source; no wildcard, drop, delete, or database selection input is accepted.
  - Boundary/API: new focused `Production.MusicRuntime.psm1` module exports one operational
    function; command routing passes only `WhatIf` and the confirmation switch.
  - Effects and failures: backup precedes mutation; `mongosh` targets fixed loopback/admin and
    selects fixed `christopherbell`; any check or replace failure stops with the service still
    stopped and preserves the backup/cause.
  - Tests and evidence: RED Pester tests prove the module/command are absent, then GREEN tests
    pressure-test preview, confirmation, service-state, backup ordering, fixed URI, and absence
    of destructive collection commands.

- [ ] Write the new Pester module tests and command-routing test first; witness RED.
- [ ] Add the focused module with exact nested-to-legacy conversion and metadata-only parser.
- [ ] Wire the command and help text; keep preview as the default behavior.
- [ ] Document emergency use and explicitly forbid using it as routine rollback.
- [ ] Run the full production Pester suite under PowerShell 7. Run the new Music runtime,
  command-routing, and operations dependency tests under both PowerShell 7 and Windows
  PowerShell 5.1; preserve the untouched-base PS5-only incompatibility report.
- [ ] Commit as `feat: add bounded music state rollback operation`.

#### Code Edit 5.1
- File: `ops/production/windows/tests/Production.MusicRuntime.Tests.ps1`
- Lines: 1-105
- Action: add

Proposed:
```powershell
BeforeAll {
    $moduleRoot = Join-Path $PSScriptRoot '..\modules'
    Import-Module (Join-Path $moduleRoot 'Production.Common.psm1') -Global -Force
    Import-Module (Join-Path $moduleRoot 'Production.MusicRuntime.psm1') -Force
}

Describe 'Music runtime rollback operation' {
    It 'generates a fixed reverse-copy script without collection deletion' {
        $script = Get-ProductionMusicRuntimeRollbackScript
        $script | Should -Match "getSiblingDB\('christopherbell'\)"
        $script | Should -Match "music_runtime_state"
        $script | Should -Match "music_queue_state"
        $script | Should -Match "music_radio_state"
        $script | Should -Match 'replaceOne'
        $script | Should -Not -Match '\.drop\('
        $script | Should -Not -Match 'deleteMany|dropDatabase|runCommand\(\{\s*drop'
    }

    It 'returns a no-write exact preview with WhatIf' {
        Mock Read-ProductionConfig { throw 'preview must not read protected config' }
        Mock New-ProductionBackup { throw 'preview must not create a backup' }
        Mock Invoke-CheckedProcess { throw 'preview must not invoke mongosh' }

        $preview = Invoke-ProductionMusicRuntimeStateRollback -WhatIf

        $preview.database | Should -Be 'christopherbell'
        $preview.destination | Should -Be 'music_runtime_state'
        $preview.sources | Should -Be @('music_queue_state','music_radio_state')
        $preview.mutates | Should -BeFalse
    }

    It 'requires explicit confirmation before actual execution' {
        { Invoke-ProductionMusicRuntimeStateRollback } |
            Should -Throw '*confirmation*'
    }

    It 'requires the website writer to be stopped before backup or mutation' {
        Mock Read-ProductionConfig { [pscustomobject]@{} }
        Mock Get-Service { [pscustomobject]@{ Status = 'Running' } }
        Mock New-ProductionBackup { throw 'must not run' }

        { Invoke-ProductionMusicRuntimeStateRollback -Confirm } |
            Should -Throw '*stopped*'
        Should -Invoke New-ProductionBackup -Times 0
    }

    It 'backs up before invoking fixed-loopback mongosh and returns metadata only' {
        $script:events = [Collections.Generic.List[string]]::new()
        Mock Read-ProductionConfig {
            [pscustomobject]@{ mongoShellExe='C:\tools\mongosh.exe'; repositoryPath='C:\repo' }
        }
        Mock Get-Service { [pscustomobject]@{ Status = 'Stopped' } }
        Mock New-ProductionBackup {
            [void]$script:events.Add('backup')
            'A:\backups\verified.archive.gz'
        }
        Mock Invoke-CheckedProcess {
            [void]$script:events.Add('mongosh')
            '{"complete":true,"database":"christopherbell","destinationCount":2,"restoredCollections":["music_queue_state","music_radio_state"]}'
        }

        $result = Invoke-ProductionMusicRuntimeStateRollback -Confirm

        $script:events | Should -Be @('backup','mongosh')
        $result.complete | Should -BeTrue
        $result.backup | Should -Be 'A:\backups\verified.archive.gz'
        Should -Invoke Invoke-CheckedProcess -ParameterFilter {
            $FilePath -eq 'C:\tools\mongosh.exe' -and
            $WorkingDirectory -eq 'C:\repo' -and
            $ArgumentList[2] -eq 'mongodb://127.0.0.1:27017/admin'
        }
    }
}
```

Verification:
- RED: Pester cannot import `Production.MusicRuntime.psm1`.
- GREEN: `Invoke-Pester ops/production/windows/tests/Production.MusicRuntime.Tests.ps1 -CI`

#### Code Edit 5.2
- File: `ops/production/windows/modules/Production.MusicRuntime.psm1`
- Lines: 1-175
- Action: add

Proposed:
```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-ProductionMusicRuntimeRollbackScript {
    @'
const target = db.getSiblingDB('christopherbell');
const destination = target.getCollection('music_runtime_state');
const queueSource = target.getCollection('music_queue_state');
const radioSource = target.getCollection('music_radio_state');
const has = (value, key) => Object.prototype.hasOwnProperty.call(value || {}, key);
const safeNumber = (value) => {
  const number = typeof value === 'number'
      ? value
      : value !== null && typeof value === 'object' && typeof value.toNumber === 'function'
          ? value.toNumber()
          : NaN;
  return Number.isFinite(number) ? number : null;
};
const exactCount = (value) => {
  const number = safeNumber(value);
  if (!Number.isSafeInteger(number) || number < 0) {
    throw new Error('music runtime rollback received invalid numeric metadata');
  }
  return number;
};
const validVersion = (value, key) => !has(value, key) ||
    (Number.isSafeInteger(safeNumber(value[key])) && safeNumber(value[key]) >= 0);
const validText = (value, maximum) => typeof value === 'string' &&
    value.length > 0 && value.length <= maximum;
const documents = destination.find({ _id: { $in: ['queue', 'radio'] } }).toArray();
if (documents.length !== 2 || exactCount(destination.countDocuments({})) !== 2) {
  throw new Error('music runtime destination must contain exactly two documents');
}
const queue = documents.find((value) => value._id === 'queue');
const radio = documents.find((value) => value._id === 'radio');
if (!queue || queue.kind !== 'QUEUE' || !queue.queue ||
    (has(queue, 'radio') && queue.radio !== null) ||
    !Array.isArray(queue.queue.entries) || queue.queue.entries.length > 1000 ||
    !validVersion(queue, 'version')) {
  throw new Error('music runtime queue document is invalid');
}
const queueIds = new Set();
for (const entry of queue.queue.entries) {
  if (!validText(entry.id, 100) || !validText(entry.trackId, 128) ||
      !validText(entry.observedToken, 128) || !validText(entry.enqueuedByAccountId, 128) ||
      !(entry.enqueuedAt instanceof Date) || queueIds.has(entry.id)) {
    throw new Error('music runtime queue entry is invalid');
  }
  queueIds.add(entry.id);
}
const sequence = radio && radio.radio ? safeNumber(radio.radio.stationSequence) : null;
const duration = radio && radio.radio ? safeNumber(radio.radio.durationSeconds) : null;
const queueEntryId = radio && radio.radio && has(radio.radio, 'queueEntryId')
    ? radio.radio.queueEntryId
    : null;
if (!radio || radio.kind !== 'RADIO' || !radio.radio ||
    (has(radio, 'queue') && radio.queue !== null) ||
    !Number.isSafeInteger(sequence) || sequence < 1 ||
    !validText(radio.radio.trackId, 128) || !validText(radio.radio.observedToken, 128) ||
    !(radio.radio.startedAt instanceof Date) || duration === null || duration <= 0 ||
    duration > 86400 || !['RADIO', 'QUEUE'].includes(radio.radio.source) ||
    (radio.radio.source === 'QUEUE' && !validText(queueEntryId, 100)) ||
    (radio.radio.source === 'RADIO' && queueEntryId !== null) ||
    !validVersion(radio, 'version')) {
  throw new Error('music runtime radio document is invalid');
}
if (exactCount(queueSource.countDocuments({})) !== 1 ||
    exactCount(queueSource.countDocuments({ _id: 'global' })) !== 1 ||
    exactCount(radioSource.countDocuments({})) !== 1 ||
    exactCount(radioSource.countDocuments({ _id: 'global' })) !== 1) {
  throw new Error('legacy music runtime sources are not exact rollback targets');
}
const queueLegacy = {
  _id: 'global',
  entries: queue.queue.entries,
  _class: 'dev.christopherbell.music.radio.MusicQueueState'
};
if (has(queue, 'version')) queueLegacy.version = queue.version;
const radioLegacy = {
  _id: 'global',
  stationSequence: radio.radio.stationSequence,
  trackId: radio.radio.trackId,
  observedToken: radio.radio.observedToken,
  startedAt: radio.radio.startedAt,
  durationSeconds: radio.radio.durationSeconds,
  source: radio.radio.source,
  queueEntryId: has(radio.radio, 'queueEntryId') ? radio.radio.queueEntryId : null,
  _class: 'dev.christopherbell.music.radio.MusicRadioState'
};
if (has(radio, 'version')) radioLegacy.version = radio.version;
const queueResult = queueSource.replaceOne({ _id: 'global' }, queueLegacy);
if (exactCount(queueResult.matchedCount) !== 1) throw new Error('legacy queue replacement failed');
const radioResult = radioSource.replaceOne({ _id: 'global' }, radioLegacy);
if (exactCount(radioResult.matchedCount) !== 1) throw new Error('legacy radio replacement failed');
if (exactCount(queueSource.countDocuments({ _id: 'global' })) !== 1 ||
    exactCount(radioSource.countDocuments({ _id: 'global' })) !== 1) {
  throw new Error('legacy music runtime readback failed');
}
print(JSON.stringify({
  complete: true,
  database: target.getName(),
  destinationCount: 2,
  restoredCollections: ['music_queue_state', 'music_radio_state']
}));
'@
}

function ConvertFrom-ProductionMusicRuntimeRollback {
    param([Parameter(Mandatory)][string]$Json)
    $value = $Json | ConvertFrom-Json -ErrorAction Stop
    $names = @($value.PSObject.Properties.Name)
    if (@($names | Where-Object {
        $_ -notin @('complete','database','destinationCount','restoredCollections')
    }).Count -ne 0 -or
        $value.complete -ne $true -or
        [string]$value.database -cne 'christopherbell' -or
        [int]$value.destinationCount -ne 2 -or
        [string]::Join([char]0, [string[]]$value.restoredCollections) -cne
            [string]::Join([char]0, [string[]]@('music_queue_state','music_radio_state'))) {
        throw 'Music runtime rollback returned invalid metadata.'
    }
    return $value
}

function Invoke-ProductionMusicRuntimeStateRollback {
    [CmdletBinding()]
    param([switch]$Confirm, [switch]$WhatIf)
    if ($WhatIf) {
        return [pscustomobject][ordered]@{
            database = 'christopherbell'
            destination = 'music_runtime_state'
            sources = @('music_queue_state','music_radio_state')
            mutates = $false
            requiresStoppedWriter = $true
            requiresFreshVerifiedBackup = $true
        }
    }
    if (-not $Confirm) {
        throw 'Music runtime rollback requires explicit confirmation.'
    }
    $config = Read-ProductionConfig
    $service = Get-Service 'ChristopherBellDev' -ErrorAction Stop
    if ($service.Status.ToString() -ne 'Stopped') {
        throw 'ChristopherBellDev must be stopped before Music runtime rollback.'
    }
    $backup = New-ProductionBackup
    $json = Invoke-CheckedProcess `
        -FilePath $config.mongoShellExe `
        -ArgumentList @(
            '--quiet','--norc','mongodb://127.0.0.1:27017/admin','--eval',
            (Get-ProductionMusicRuntimeRollbackScript)) `
        -WorkingDirectory $config.repositoryPath
    $result = ConvertFrom-ProductionMusicRuntimeRollback -Json $json
    $result | Add-Member -NotePropertyName backup -NotePropertyValue $backup
    return $result
}

Export-ModuleMember -Function Get-ProductionMusicRuntimeRollbackScript,Invoke-ProductionMusicRuntimeStateRollback
```

Verification:
- `Invoke-Pester ops/production/windows/tests/Production.MusicRuntime.Tests.ps1 -CI`
- Review generated JS and confirm it contains no `drop`, wildcard namespace, or document output.

#### Code Edit 5.3
- File: `ops/production/windows/prod.ps1`
- Lines: 4-7
- Action: replace

Current:
```powershell
    [ValidateSet('help','install','deploy','status','logs','restart','releases','rollback','backup','mongo-inventory','verify-startup','uninstall','auto-install','auto-deploy','auto-status','auto-remove','sensor-install','sensor-status','sensor-enable','sensor-disable')]
    [string]$Command = 'help',
    [switch]$WhatIf,
    [string]$CloudflareTokenPath
```

Proposed:
```powershell
    [ValidateSet('help','install','deploy','status','logs','restart','releases','rollback','backup','mongo-inventory','music-runtime-rollback','verify-startup','uninstall','auto-install','auto-deploy','auto-status','auto-remove','sensor-install','sensor-status','sensor-enable','sensor-disable')]
    [string]$Command = 'help',
    [switch]$WhatIf,
    [switch]$ConfirmMusicRuntimeRollback,
    [string]$CloudflareTokenPath
```

Verification:
- `Invoke-Pester ops/production/windows/tests/Production.Command.Tests.ps1 -CI`

#### Code Edit 5.4
- File: `ops/production/windows/prod.ps1`
- Lines: 13-15
- Action: replace

Current:
```powershell
foreach ($module in 'Production.Deploy','Production.SharedFolder','Production.Install','Production.Sensors','Production.Operations','Production.AutoDeploy') {
    Import-Module (Join-Path $moduleRoot "$module.psm1") -Force
}
```

Proposed:
```powershell
foreach ($module in 'Production.Deploy','Production.SharedFolder','Production.Install','Production.Sensors','Production.Operations','Production.MusicRuntime','Production.AutoDeploy') {
    Import-Module (Join-Path $moduleRoot "$module.psm1") -Force
}
```

Verification:
- `Invoke-Pester ops/production/windows/tests/Production.Command.Tests.ps1 -CI`

#### Code Edit 5.5
- File: `ops/production/windows/prod.ps1`
- Lines: 17-22
- Action: replace

Current:
```powershell
function Invoke-ProductionCommand {
    param(
        [Parameter(Mandatory)][string]$Command,
        [switch]$WhatIf,
        [string]$CloudflareTokenPath
    )
```

Proposed:
```powershell
function Invoke-ProductionCommand {
    param(
        [Parameter(Mandatory)][string]$Command,
        [switch]$WhatIf,
        [switch]$ConfirmMusicRuntimeRollback,
        [string]$CloudflareTokenPath
    )
```

Verification:
- `Invoke-Pester ops/production/windows/tests/Production.Command.Tests.ps1 -CI`

#### Code Edit 5.6
- File: `ops/production/windows/prod.ps1`
- Lines: after 36
- Action: add

Proposed:
```powershell
        'music-runtime-rollback' = {
            Invoke-ProductionMusicRuntimeStateRollback `
                -Confirm:$ConfirmMusicRuntimeRollback -WhatIf:$WhatIf
        }
```

Verification:
- Add a command test that dotsources `prod.ps1`, mocks
  `Invoke-ProductionMusicRuntimeStateRollback`, invokes the handler with `-WhatIf`, and proves
  the exact switches are forwarded.
- `Invoke-Pester ops/production/windows/tests/Production.Command.Tests.ps1 -CI`

#### Code Edit 5.7
- File: `ops/production/windows/prod.ps1`
- Lines: 52-53
- Action: replace

Current:
```powershell
Invoke-ProductionCommand -Command $Command -WhatIf:$WhatIf `
    -CloudflareTokenPath $CloudflareTokenPath
```

Proposed:
```powershell
Invoke-ProductionCommand -Command $Command -WhatIf:$WhatIf `
    -ConfirmMusicRuntimeRollback:$ConfirmMusicRuntimeRollback `
    -CloudflareTokenPath $CloudflareTokenPath
```

Verification:
- `Invoke-Pester ops/production/windows/tests/Production.Command.Tests.ps1 -CI`

#### Code Edit 5.8
- File: `ops/production/windows/modules/Production.Common.psm1`
- Lines: 519-527
- Action: replace

Current:
```powershell
Usage: prod.cmd <command> [-WhatIf]

Commands: install, deploy, status, logs, restart, releases, rollback, backup,
          mongo-inventory, verify-startup, uninstall, auto-install, auto-deploy,
          auto-status, auto-remove, sensor-install, sensor-status,
          sensor-enable, sensor-disable
```

Proposed:
```powershell
Usage: prod.cmd <command> [-WhatIf]

Commands: install, deploy, status, logs, restart, releases, rollback, backup,
          mongo-inventory, music-runtime-rollback, verify-startup, uninstall,
          auto-install, auto-deploy, auto-status, auto-remove, sensor-install,
          sensor-status, sensor-enable, sensor-disable

music-runtime-rollback previews by default. Actual reverse-copy additionally requires
-ConfirmMusicRuntimeRollback and a stopped ChristopherBellDev service.
```

Verification:
- `pwsh.exe -NoLogo -NoProfile -File ops/production/windows/prod.ps1 help`

#### Code Edit 5.9
- File: `docs/operations/mongodb-migrations.md`
- Lines: after 30
- Action: add

Proposed:
````markdown
### Music runtime-state rollback exception

Migration 014 leaves both legacy collections intact but the new release writes only
`music_runtime_state`. A binary rollback therefore requires reverse-copying the latest queue
and radio state before the prior release starts. With the writer stopped, first preview:

```powershell
.\prod.cmd music-runtime-rollback -WhatIf
```

After confirming the exact database and three namespaces, run the bounded operation with
`-ConfirmMusicRuntimeRollback`. It creates and verifies a fresh full backup before replacing
only the two retained `_id: "global"` documents. It never drops a collection and emits only
metadata. Keep the service stopped if any check fails; use the recorded backup and obtain
approval before a broader production restore.
````

Verification:
- Review the runbook against the command help and Pester behavior.

#### Code Edit 5.10
- File: `ops/production/windows/tests/Production.Command.Tests.ps1`
- Lines: after 124
- Action: add

Proposed:
```powershell
    It 'routes the bounded Music runtime rollback switches' {
        $root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
        $null = . (Join-Path $root 'ops\production\windows\prod.ps1') help
        Mock Invoke-ProductionMusicRuntimeStateRollback { [pscustomobject]@{ complete = $true } }

        $null = Invoke-ProductionCommand `
            -Command 'music-runtime-rollback' `
            -WhatIf `
            -ConfirmMusicRuntimeRollback

        Should -Invoke Invoke-ProductionMusicRuntimeStateRollback -Times 1 -Exactly `
            -ParameterFilter { $WhatIf -and $Confirm }
    }
```

Verification:
- `Invoke-Pester ops/production/windows/tests/Production.Command.Tests.ps1 -CI`

### Task 6 - Close the installed Windows writer-start safety boundary

Sequence / dependencies:
- Runs after Task 5 because it hardens the installed service boundary introduced by the
  schema-direction state machine.
- This is the user-approved scoped follow-on after five Task 5 fix rounds reached the review
  escalation limit. No MongoDB collection mutation is authorized.

Implementation notes:
- Required skill: `chris-street-style` before script or test edits; invoke
  `superpowers:test-driven-development` and preserve Windows PowerShell 5.1 compatibility.
- User-approved post-merge ACL follow-on (2026-08-10): after five Task 6 review rounds, elevated
  disposable evidence exposed an empty installed-file DACL, and the final review then found the
  parent verifier still hid inherited-flag ACEs. Before cutover, both the publisher and pre-import
  launcher must use raw security descriptors requiring exact Builtin Administrators ownership,
  protected DACL, and exactly SYSTEM/Administrators FullControl plus LocalService
  ReadAndExecute/Synchronize OI|CI allow ACEs with no inherited, deny, callback, object, duplicate,
  missing, or extra entry.
- Before-Edit Brief:
  - Behavior: a pre-guard installed service is disabled before publication begins and cannot
    boot or recover until the guarded launcher bundle and parent service directory pass exact
    hash, path, reparse, and ACL validation.
  - Invariants: every publication failure leaves a pre-guard service Disabled; success restores
    Automatic only when the guarded boundary is ready for an explicitly compatible start.
  - Boundary/API: the existing deploy-lock-held writer-start publisher and `prod install`
    lifecycle own the transition; no new public database or collection inputs are added.
  - Effects and failures: a previously running healthy website is restarted and health-checked
    after successful install; an intentionally stopped website remains stopped; failures preserve
    causes and leave the writer stopped/disabled.
  - Tests and evidence: pre-guard staging/first-publication/crash simulations, boot state,
    service-root ACL integration, reinstall running/stopped behavior, and Windows path casing are
    proven on PowerShell 7 and Windows PowerShell 5.1.

- [ ] Write RED tests for pre-guard failure startup type, protected parent directory, reinstall
  lifecycle, and case-insensitive sensor root identity.
- [ ] Disable and verify the pre-guard service before publication, then restore Automatic only
  after the installed guard is fully verified.
- [ ] Protect and verify the canonical non-reparse production/service directory boundary and
  make the installed launcher validate it before JVM startup.
- [ ] Preserve the prior running/stopped state across `prod install`; restart and health-check
  a previously running service under the held deploy lock.
- [ ] Run full PowerShell 7, approved focused PowerShell 5.1, real Windows ACL integration on
  both hosts, parser checks, and a fresh independent review.
- [ ] Commit as `fix: close installed writer start boundary`.

#### Code Edit 6.1
- File: `ops/production/windows/modules/Production.Deploy.psm1`
- Lines: 51-75
- Action: replace

Current:
```powershell
function Ensure-ProductionWriterStartGuardUnderHeldLock {
    # Stops the writer and publishes the guarded launcher bundle.
}
```

Proposed:
```powershell
function Ensure-ProductionWriterStartGuardUnderHeldLock {
    # Disable and verify a pre-guard Automatic service before any publication effect.
    # Publish and validate the complete protected bundle, then restore Automatic only on success.
}
```

Verification:
- Pre-guard staging, first-file, and simulated process-death failures leave the service Disabled.
- A verified bundle restores the intended startup type only after exact readback succeeds.

#### Code Edit 6.2
- File: `ops/production/windows/modules/Production.WriterStart.psm1`
- Lines: 94-220
- Action: replace

Current:
```powershell
function Publish-ProductionWriterStartGuardBundle {
    # Protects staging and bundle files.
}
```

Proposed:
```powershell
function Publish-ProductionWriterStartGuardBundle {
    # Canonicalize and reject reparse traversal, protect/verify the service directory first,
    # publish atomically, and verify the directory plus every installed file and manifest.
}
```

Verification:
- Real Windows ACL assertions prove the expected protected service-directory boundary on both
  supported PowerShell hosts.

#### Code Edit 6.3
- File: `ops/production/windows/service/Start-ChristopherBellDev.ps1`
- Lines: 1-40
- Action: replace

Current:
```powershell
# Verifies the installed launcher files before checking schema direction.
```

Proposed:
```powershell
# Reject reparse traversal and verify the protected service directory and exact installed
# bundle before evaluating schema direction or starting Java.
```

Verification:
- A parent-directory ACL or reparse mismatch fails before JVM launch.

#### Code Edit 6.4
- File: `ops/production/windows/modules/Production.Install.psm1`
- Lines: 184-220
- Action: replace

Current:
```powershell
function Install-ProductionRuntime {
    # Stops an existing website during install.
}
```

Proposed:
```powershell
function Install-ProductionRuntime {
    # Capture prior service state under deploy.lock; after a successful guarded install,
    # restart/health-check only a previously running service and preserve an intentional stop.
}
```

Verification:
- Successful reinstall restores a prior healthy running service and preserves a stopped service.
- Failure leaves the writer stopped/disabled with bounded causal evidence.

#### Code Edit 6.5
- File: `ops/production/windows/modules/Production.Sensors.psm1`
- Lines: 336-347
- Action: replace

Current:
```powershell
[IO.Path]::GetFullPath([string]$config.programDataRoot) -cne $root
```

Proposed:
```powershell
-not [string]::Equals(
    [IO.Path]::GetFullPath([string]$config.programDataRoot),
    $root,
    [StringComparison]::OrdinalIgnoreCase)
```

Verification:
- Canonically identical Windows paths with different casing are accepted.

#### Code Edit 6.6
- File: `ops/production/windows/tests/Production.WriterStart.Tests.ps1`
- Lines: 175-360
- Action: replace

Current:
```powershell
# Bundle publication and launcher-source tests.
```

Proposed:
```powershell
# Pre-guard Disabled-state, crash/failure, boot, protected parent ACL, reparse traversal,
# installed readback, and launcher fail-closed tests.
```

Verification:
- Focused writer-start tests pass under PowerShell 7 and Windows PowerShell 5.1.

#### Code Edit 6.7
- File: `ops/production/windows/tests/Production.Install.Tests.ps1`
- Lines: 1-140
- Action: replace

Current:
```powershell
# Installer structure tests.
```

Proposed:
```powershell
# Reinstall running/stopped/failure lifecycle and real protected-directory ACL tests.
```

Verification:
- Focused install tests pass under PowerShell 7 and Windows PowerShell 5.1.

#### Code Edit 6.8
- File: `ops/production/windows/tests/Production.Sensors.Tests.ps1`
- Lines: 100-170
- Action: replace

Current:
```powershell
# Sensor lock and rollback tests.
```

Proposed:
```powershell
# Add case-insensitive canonical ProgramData-root identity coverage.
```

Verification:
- Focused sensor tests pass under PowerShell 7 and Windows PowerShell 5.1.

### Task 7 - Run full verification, review, publication, and non-destructive cutover

Sequence / dependencies:
- Runs after all code tasks are individually green and committed.
- No implementation edit starts here; any discovered defect returns to RED/GREEN in the
  owning task and receives a fresh focused review.

Implementation notes:
- Required skills at execution: `superpowers:verification-before-completion`,
  `superpowers:requesting-code-review`, `verify-local-spring-app`, `review-spoke-work`, and the
  repository's complete story/issue delivery workflow.
- Before-Edit Brief: not applicable because this task changes no source; it verifies and
  delivers the prior tasks.

- [ ] Use private `GRADLE_USER_HOME` and run focused tests, `:website:test`, and
  `:website:bootJar` with no short outer timeout.
- [ ] Run all production Pester tests under PowerShell 7. Under Windows PowerShell 5.1, run
  `Production.MusicRuntime.Tests.ps1`, `Production.Command.Tests.ps1`, and
  `Production.Operations.Tests.ps1`; do not attribute the separately recorded 85 unrelated
  untouched-base PS5-only incompatibilities to this branch.
- [ ] Perform a whole-diff Jane Street review and an independent code review; fix every blocker.
- [ ] Create a verified native backup and restore it into a disposable database.
- [ ] Capture canonical pre-migration logical digests for the two legacy source documents
  without emitting values.
- [ ] Start the packaged candidate on a non-8080 port against the clone; prove migration 014,
  exactly two target documents, preserved digests/versions, independent optimistic locking,
  queue read/write/remove/reorder, radio transition, queue consumption, readiness, liveness,
  and clean logs.
- [ ] Stop the candidate and run the reverse-copy operation against a separate disposable clone;
  prove the restored legacy logical digests and versions equal the latest destination.
- [ ] Publish a draft PR, run all required CI/dependency/CodeQL checks, address review, and merge.
- [ ] Confirm the protected deploy's candidate-clone validation, verified backup, old-writer stop,
  migration record, exact release, and production PID rotation.
- [ ] Verify local/public health and exact authenticated music API inputs/status/bodies.
- [ ] Run `prod.cmd mongo-inventory`; require 48 live collections, 164 indexes unless the real
  `_id` index total proves another exact value, no live-only namespace, and the two legacy
  namespaces classified as rollback-retained.
- [ ] Save the local test report, spoke update/review, and observation-start evidence in Builder.
- [ ] Keep the hub work `active`; schedule/record the seven-day end timestamp and do not close.

Verification commands:
```powershell
$env:GRADLE_USER_HOME = 'A:\Projects\christopherbell.dev-worktrees\.gradle-music-runtime-state'
.\gradlew.bat --no-daemon :website:test :website:bootJar
pwsh.exe -NoLogo -NoProfile -Command "Invoke-Pester -Path 'ops/production/windows/tests' -CI"
powershell.exe -NoLogo -NoProfile -Command "Import-Module 'A:\Documents\PowerShell\Modules\Pester\5.9.0\Pester.psd1' -Force; Invoke-Pester -Path @('ops/production/windows/tests/Production.MusicRuntime.Tests.ps1','ops/production/windows/tests/Production.Command.Tests.ps1','ops/production/windows/tests/Production.Operations.Tests.ps1') -CI"
.\prod.cmd music-runtime-rollback -WhatIf
.\prod.cmd mongo-inventory
.\prod.cmd verify-startup
```

Expected evidence:
- All Java/Gradle tests, the full PowerShell 7 Pester suite, and the focused Windows
  PowerShell 5.1 Music runtime/command/operations suite pass.
- Disposable Mongo proves real BSON mapping, versions, migration idempotency boundary, and reverse
  conversion fidelity.
- Candidate and production endpoints include URL/port, request input, status, and response body.
- Production retains both source collections and adds exactly one destination collection.

### Task 8 - Observe for seven days and prepare, but do not execute, retirement

Sequence / dependencies:
- Begins only after Task 7 production cutover is healthy.
- Ends at a new user approval gate; collection deletion belongs to a new plan.

Implementation notes:
- No source or database mutation is authorized by this task.
- Record daily readiness/liveness, current release, service state, music API behavior, migration
  status, destination identities/count, optimistic-lock/Mongo errors, and metadata inventory.
- On any state-loss or behavior regression, stop the writer and follow the verified reverse-copy
  rollback procedure; do not start an old binary against stale sources.

- [ ] Record the exact seven-day window start and end in the Builder work record.
- [ ] Collect evidence for at least one real queue mutation/consumption and multiple radio
  transitions during the window.
- [ ] At the end, create a fresh verified backup and restore it into a disposable database.
- [ ] Produce an exact retirement preview with database, literal source names, counts, indexes,
  backup path/SHA-256, restore result, and expected post-drop total 46.
- [ ] Write and validate a separate retirement implementation plan whose only destructive targets
  are `music_queue_state` and `music_radio_state`.
- [ ] Ask the user for explicit approval. Stop without dropping anything if approval is absent.

Verification:
- Builder evidence covers every day and the exact approval preview.
- Production remains at 48 collections until a later approved retirement is executed.

## Code Changes

- Add `MusicRuntimeStateDocument.java`: validated envelope and pure conversions.
- Add `MusicRuntimeStateStore.java`: exact-ID Mongo I/O boundary.
- Remove `@Document` from `MusicQueueState.java` and `MusicRadioState.java`.
- Delete `MusicQueueStateRepository.java` and `MusicRadioRepository.java`.
- Modify `MusicQueueService.java` and `MusicRadioService.java` to use the narrow store.
- Update queue/radio service tests and add document tests.
- Add `V014ConsolidateMusicRuntimeState.java` and focused migration tests.
- Update `MongoCollectionCatalogTest.java` and the collection catalog lifecycle/provenance.
- Add `Production.MusicRuntime.psm1`, its Pester tests, command routing, help, and runbook.
- No drop command or collection-deletion code is added.

## Files and Modules

- Music domain/storage: `website/src/main/java/dev/christopherbell/music/radio/`
- Migration: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/`
- Java tests: corresponding `website/src/test/java/` packages
- Architecture policy: `website/src/test/java/dev/christopherbell/architecture/`
- Windows operations: `ops/production/windows/`
- Runbooks: `docs/operations/mongodb-collection-catalog.md` and
  `docs/operations/mongodb-migrations.md`

## Unit Testing

- Document round trips and mixed-payload rejection.
- Queue/radio service characterization through the new store.
- Migration copy fidelity for all four source-presence combinations, equivalent rerun, duplicate
  source refusal, exact target-membership refusal, divergent destination refusal, and post-insert
  readback.
- Catalog status vocabulary, source-backed coverage, mapped/manual ownership, and exact count.
- PowerShell rollback preview, confirmation, stopped service, backup-before-mutation ordering,
  fixed URI/database/names, allowlisted output, and absence of drop/delete commands.

## Local Testing

- Focused Gradle tests after every RED/GREEN task.
- Full `:website:test` and `:website:bootJar` with a private Gradle home.
- Full Pester under PowerShell 7 plus focused Music runtime/command/operations Pester under
  Windows PowerShell 5.1 using the explicit Pester 5.9 module path.
- Real disposable Mongo cloned from a current verified production backup.
- Packaged candidate on a non-8080 port with exact health and music API evidence.
- Reverse-copy drill against a disposable post-write destination.

## Validation

- Source logical digests and version values equal target values at cutover.
- Queue and radio target versions advance independently under real writes.
- Runtime services never enumerate the shared collection.
- Migration 014 is APPLIED with the exact checksum and no incomplete record.
- Production inventory is exactly 48 collections during retention and has no unowned namespace.
- Current release logs have no mapping, migration, optimistic-lock anomaly, or Mongo failure.

## Rollback or Recovery

- Before live migration: abort deployment; production remains on the old release and sources.
- Candidate failure: destroy only the allowlisted disposable candidate database; preserve backup.
- Live startup failure before new writes: keep writer stopped and follow migration runbook; repair
  forward or use explicitly approved restore.
- Rollback after new writes: stop writer, preview exact reverse-copy, run the confirmed command,
  verify legacy logical digests/versions, then start the prior release.
- Reverse-copy failure: keep writer stopped, preserve the fresh backup and causal evidence, and
  obtain approval before broader restore.
- No rollback step in this plan drops any collection.

## Risks

- Immutable-record `@Version` behavior through `MongoTemplate` could differ from repository
  assumptions. Mitigation: real disposable Mongo conflict test before PR publication.
- A two-document insert is not atomic on standalone MongoDB. Mitigation: preflight empty target,
  reject partial reruns, leave sources intact, and prove recovery on a clone.
- Starting an old release without reverse-copy exposes stale state. Mitigation: explicit runbook,
  bounded command, stopped-writer gate, backup-first sequencing, and deployment evidence.
- Source-backed catalog count changes from 51 to 52. Mitigation: exact architecture assertion and
  provenance; physical count is separately verified as 48.
- PowerShell array comparison can be surprising across hosts. Mitigation: run focused Pester on
  PowerShell 7 and Windows PowerShell 5.1 and use explicit element/count validation if the proposed
  parser comparison fails RED/GREEN review.

## Completion Criteria

- Tasks 1-5 are individually reviewed, committed, and green.
- Full Gradle, full PowerShell 7 Pester, focused Windows PowerShell 5.1 Pester, real disposable
  Mongo, candidate runtime, PR CI, dependency review, CodeQL, merge, protected deployment,
  and production runtime checks pass.
- Production runs the exact merged release with migration 014 APPLIED.
- `music_runtime_state` contains exactly `queue` and `radio` with preserved state and independent
  versions; both legacy collections remain unchanged and cataloged as rollback-retained.
- Builder contains the test report, spoke update, review, and seven-day observation start.
- Work remains active and no collection has been dropped.
- A separate retirement plan and explicit approval remain mandatory before final cleanup/closure.
