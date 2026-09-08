# 2026-07-25 - christopherbell-dev Session Memory

Website development and production-delivery history. Repository paths, guardrails, reviews, and snapshots are dated evidence; verify current configuration before execution.

## Reading and Updating This Record

This file records work and events for this project on this date. Append same-day progress, decisions, reviews, blockers, publication and closure here; use a separate file for each other date. Sources with no date in their filename are grouped by their last recorded Git change date in the original corpus; that is archival provenance, not a claim that every described event occurred that day. Plans and runtime reports remain separate evidence documents. Imported instructions and statuses are historical evidence, not current operating policy; current AGENTS.md and skills take precedence. Use the source navigation or search for an issue, date, or topic rather than loading the entire history.

## Imported Source Navigation

- [docs/spokes/state.md](#source-docs-spokes-state-md)
- [docs/session-memory/2026-07-25-approve-all-open-issue-campaign-spec.md](#source-docs-session-memory-2026-07-25-approve-all-open-issue-campaign-spec-md)
- [docs/session-memory/2026-07-25-authorize-autonomous-issue-campaign-continuation.md](#source-docs-session-memory-2026-07-25-authorize-autonomous-issue-campaign-continuation-md)
- [docs/session-memory/2026-07-25-browser-security-issues-1125-1130.md](#source-docs-session-memory-2026-07-25-browser-security-issues-1125-1130-md)
- [docs/session-memory/2026-07-25-plan-github-automation-issues-1144-1150.md](#source-docs-session-memory-2026-07-25-plan-github-automation-issues-1144-1150-md)
- [docs/session-memory/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md](#source-docs-session-memory-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md)
- [docs/session-memory/2026-07-25-public-content-issues-1131-1137.md](#source-docs-session-memory-2026-07-25-public-content-issues-1131-1137-md)
- [docs/session-memory/2026-07-25-public-delivery-issues-1122-1124-1138.md](#source-docs-session-memory-2026-07-25-public-delivery-issues-1122-1124-1138-md)
- [docs/session-memory/2026-07-25-start-all-open-issue-campaign.md](#source-docs-session-memory-2026-07-25-start-all-open-issue-campaign-md)
- [docs/specs/2026-07-25-complete-all-open-christopherbell-dev-issues.md](#source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md)
- [docs/spoke-reviews/2026-07-25-browser-security-issues-1125-1130.md](#source-docs-spoke-reviews-2026-07-25-browser-security-issues-1125-1130-md)
- [docs/spoke-reviews/2026-07-25-github-automation-issues-1144-1150.md](#source-docs-spoke-reviews-2026-07-25-github-automation-issues-1144-1150-md)
- [docs/spoke-reviews/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md](#source-docs-spoke-reviews-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md)
- [docs/spoke-reviews/2026-07-25-public-content-issues-1131-1137.md](#source-docs-spoke-reviews-2026-07-25-public-content-issues-1131-1137-md)
- [docs/spoke-reviews/2026-07-25-public-delivery-issues-1122-1124-1138.md](#source-docs-spoke-reviews-2026-07-25-public-delivery-issues-1122-1124-1138-md)
- [docs/spoke-updates/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md](#source-docs-spoke-updates-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md)
- [docs/spoke-updates/2026-07-25-public-content-issues-1131-1137.md](#source-docs-spoke-updates-2026-07-25-public-content-issues-1131-1137-md)
- [docs/work/2026-07-25-complete-all-open-christopherbell-dev-issues.md](#source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md)

<a id="source-docs-spokes-state-md"></a>
## Undated archive | spokes | Spoke Repository State

Original source: `docs/spokes/state.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `49cece0697fbc0674489f69cd75ec14aa102fd09650658037cfe69fb5ab7b6b1`.

<!-- migrated-source: docs/spokes/state.md -->
<a id="source-docs-spokes-state-md--spoke-repository-state"></a>
### Spoke Repository State

Snapshot: 2026-07-25 15:12 Central Daylight Time

<a id="source-docs-spokes-state-md--christopherbelldev"></a>
#### christopherbell.dev

- Path: `A:\Projects\christopherbell.dev`
- Registered remote: `https://github.com/azurras/christopherbell.dev.git`
- Branch: `main`
- HEAD: `6457e88a`
- Origin: `https://github.com/azurras/christopherbell.dev.git`
- Status:
```text
M  .gitattributes
M  .github/workflows/ci.yml
A  .superpowers/sdd/progress.md
A  .superpowers/sdd/task-3-report.md
A  .superpowers/sdd/task-4-report.md
A  .superpowers/sdd/task-4-review-fix-design.md
A  .superpowers/sdd/task-4-review-fix-plan.md
A  .superpowers/sdd/task-5-report.md
A  .superpowers/sdd/task-6-report.md
A  .superpowers/sdd/task-7-report.md
A  Makefile
M  README.md
M  build.gradle.kts
M  cbell-lib/build.gradle.kts
M  cbell-lib/src/main/java/dev/christopherbell/libs/api/APIVersion.java
M  cbell-lib/src/main/java/dev/christopherbell/libs/api/controller/ControllerExceptionHandler.java
M  docs/operations/mongodb-backup-restore.md
A  docs/operations/windows-production.md
A  docs/superpowers/plans/2026-07-12-wsl-production-tool-retirement.md
A  docs/superpowers/specs/2026-07-11-native-windows-production-deployment-design.md
A  docs/superpowers/specs/2026-07-12-wsl-production-tool-retirement-design.md
M  gradle/wrapper/gradle-wrapper.properties
M  gradlew
MM gradlew.bat
A  ops/production/windows/config/app.env.example
A  ops/production/windows/config/deploy.example.json
A  ops/production/windows/config/media-tools-manifest.json
A  ops/production/windows/modules/Production.AutoDeploy.psm1
A  ops/production/windows/modules/Production.Common.psm1
A  ops/production/windows/modules/Production.Deploy.psm1
A  ops/production/windows/modules/Production.Install.psm1
A  ops/production/windows/modules/Production.Operations.psm1
A  ops/production/windows/modules/Production.Sensors.psm1
A  ops/production/windows/modules/Production.SharedFolder.psm1
A  ops/production/windows/modules/Production.SharedFolderWorker.psm1
A  ops/production/windows/prod.ps1
A  ops/production/windows/service/ChristopherBellDev.xml
A  ops/production/windows/service/ChristopherBellMediaWorker.xml
A  ops/production/windows/service/Start-ChristopherBellDev.ps1
A  ops/production/windows/service/Start-SharedFolderMediaWorker.ps1
A  ops/production/windows/tests/Production.AutoDeploy.Tests.ps1
A  ops/production/windows/tests/Production.Command.Tests.ps1
A  ops/production/windows/tests/Production.Common.Tests.ps1
A  ops/production/windows/tests/Production.Deploy.Tests.ps1
A  ops/production/windows/tests/Production.Install.Tests.ps1
A  ops/production/windows/tests/Production.Operations.Tests.ps1
A  ops/production/windows/tests/Production.Security.Integration.Tests.ps1
A  ops/production/windows/tests/Production.Sensors.Tests.ps1
A  ops/production/windows/tests/Production.SharedFolderWorker.Tests.ps1
A  prod.cmd
M  website/build.gradle.kts
M  website/src/main/java/dev/christopherbell/Application.java
M  website/src/main/java/dev/christopherbell/account/AccountController.java
M  website/src/main/java/dev/christopherbell/account/AccountService.java
M  website/src/main/java/dev/christopherbell/account/README.md
M  website/src/main/java/dev/christopherbell/account/model/Account.java
A  website/src/main/java/dev/christopherbell/account/model/AccountPermission.java
M  website/src/main/java/dev/christopherbell/account/model/README.md
M  website/src/main/java/dev/christopherbell/account/model/dto/AccountDetail.java
M  website/src/main/java/dev/christopherbell/account/model/dto/README.md
A  website/src/main/java/dev/christopherbell/account/model/dto/SharedFolderPermissionUpdate.java
M  website/src/main/java/dev/christopherbell/admin/README.md
M  website/src/main/java/dev/christopherbell/admin/activity/AdminActivityService.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/CommandCenterAccessService.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/CommandCenterConfiguration.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/CommandCenterController.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/CommandCenterProperties.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/action/CommandCenterActionService.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/action/CommandCenterActionType.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/action/CommandExecutor.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/action/SimulatedCommandExecutor.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/action/WindowsCommandExecutor.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/logs/CommandCenterLogService.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProvider.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/CommandCenterMetricsService.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/CommandCenterSamplingLifecycle.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/CpuTemperatureSensorClient.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/HostMetricsProvider.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureClient.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureProvider.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/NvidiaMetricsProvider.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/OshiHostMetricsProvider.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/PowerShellCpuTemperatureProbe.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java
A  website/src/main/java/dev/christopherbell/admin/commandcenter/model/CommandCenterSnapshot.java
M  website/src/main/java/dev/christopherbell/configuration/README.md
M  website/src/main/java/dev/christopherbell/configuration/RateLimitProperties.java
A  website/src/main/java/dev/christopherbell/configuration/SchedulingConfiguration.java
A  website/src/main/java/dev/christopherbell/configuration/SharedFolderConfiguration.java
A  website/src/main/java/dev/christopherbell/configuration/SharedFolderMediaProperties.java
A  website/src/main/java/dev/christopherbell/configuration/SharedFolderProperties.java
M  website/src/main/java/dev/christopherbell/configuration/filter/RateLimitFilter.java
A  website/src/main/java/dev/christopherbell/configuration/filter/RequestPayloadTooLargeException.java
M  website/src/main/java/dev/christopherbell/configuration/filter/RequestSizeLimitFilter.java
M  website/src/main/java/dev/christopherbell/configuration/security/README.md
M  website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java
A  website/src/main/java/dev/christopherbell/sharedfolder/README.md
A  website/src/main/java/dev/christopherbell/sharedfolder/audit/MongoSharedFolderAuditSink.java
A  website/src/main/java/dev/christopherbell/sharedfolder/audit/SharedFolderAuditCommand.java
A  website/src/main/java/dev/christopherbell/sharedfolder/audit/SharedFolderAuditEvent.java
A  website/src/main/java/dev/christopherbell/sharedfolder/audit/SharedFolderAuditFilter.java
A  website/src/main/java/dev/christopherbell/sharedfolder/audit/SharedFolderAuditQueryService.java
A  website/src/main/java/dev/christopherbell/sharedfolder/audit/SharedFolderAuditRecorder.java
A  website/src/main/java/dev/christopherbell/sharedfolder/audit/SharedFolderAuditRepository.java
A  website/src/main/java/dev/christopherbell/sharedfolder/audit/SharedFolderAuditSink.java
A  website/src/main/java/dev/christopherbell/sharedfolder/fs/JnaWindowsSharedFolderNativeBridge.java
A  website/src/main/java/dev/christopherbell/sharedfolder/fs/LinuxSharedFolderMountMetadata.java
A  website/src/main/java/dev/christopherbell/sharedfolder/fs/NioSharedFolderFileSystemBoundary.java
A  website/src/main/java/dev/christopherbell/sharedfolder/fs/PortableSharedFolderPrivateBoundary.java
A  website/src/main/java/dev/christopherbell/sharedfolder/fs/RootedNioSharedFolderFileSystemBoundary.java
A  website/src/main/java/dev/christopherbell/sharedfolder/fs/SharedFolderFileSystemBoundary.java
A  website/src/main/java/dev/christopherbell/sharedfolder/fs/SharedFolderMountMetadata.java
A  website/src/main/java/dev/christopherbell/sharedfolder/fs/SharedFolderPathResolver.java
A  website/src/main/java/dev/christopherbell/sharedfolder/fs/SharedFolderReadResource.java
A  website/src/main/java/dev/christopherbell/sharedfolder/fs/UnsafeSharedPathException.java
A  website/src/main/java/dev/christopherbell/sharedfolder/fs/WindowsSharedFolderMutationBoundary.java
A  website/src/main/java/dev/christopherbell/sharedfolder/fs/WindowsSharedFolderNativeBridge.java
A  website/src/main/java/dev/christopherbell/sharedfolder/fs/WindowsSharedFolderReadBoundary.java
A  website/src/main/java/dev/christopherbell/sharedfolder/maintenance/MongoSharedFolderMaintenanceLeaseStore.java
A  website/src/main/java/dev/christopherbell/sharedfolder/maintenance/SharedFolderMaintenanceHostLock.java
A  website/src/main/java/dev/christopherbell/sharedfolder/maintenance/SharedFolderMaintenanceLease.java
A  website/src/main/java/dev/christopherbell/sharedfolder/maintenance/SharedFolderMaintenanceLeaseDocument.java
A  website/src/main/java/dev/christopherbell/sharedfolder/maintenance/SharedFolderMaintenanceLeaseStore.java
A  website/src/main/java/dev/christopherbell/sharedfolder/maintenance/SharedFolderMaintenanceService.java
A  website/src/main/java/dev/christopherbell/sharedfolder/media/MediaCacheKeys.java
A  website/src/main/java/dev/christopherbell/sharedfolder/media/MediaJob.java
A  website/src/main/java/dev/christopherbell/sharedfolder/media/MediaJobRepository.java
A  website/src/main/java/dev/christopherbell/sharedfolder/media/MediaJobStatus.java
A  website/src/main/java/dev/christopherbell/sharedfolder/media/MediaOutputProfile.java
A  website/src/main/java/dev/christopherbell/sharedfolder/media/MediaPlaybackDescriptor.java
A  website/src/main/java/dev/christopherbell/sharedfolder/media/MediaPlaybackMode.java
A  website/src/main/java/dev/christopherbell/sharedfolder/media/MediaPlaybackService.java
A  website/src/main/java/dev/christopherbell/sharedfolder/media/MediaSourceBoundary.java
A  website/src/main/java/dev/christopherbell/sharedfolder/media/MediaStorage.java
A  website/src/main/java/dev/christopherbell/sharedfolder/media/MediaWorkerJobDescriptor.java
A  website/src/main/java/dev/christopherbell/sharedfolder/media/ProgressiveMediaController.java
A  website/src/main/java/dev/christopherbell/sharedfolder/media/ProgressiveMediaStreamer.java
A  website/src/main/java/dev/christopherbell/sharedfolder/model/SharedDirectoryEntry.java
A  website/src/main/java/dev/christopherbell/sharedfolder/model/SharedDirectoryEntryType.java
A  website/src/main/java/dev/christopherbell/sharedfolder/model/SharedDirectoryResponse.java
A  website/src/main/java/dev/christopherbell/sharedfolder/model/SharedFolderCreateFolderRequest.java
A  website/src/main/java/dev/christopherbell/sharedfolder/model/SharedFolderDeleteRequest.java
A  website/src/main/java/dev/christopherbell/sharedfolder/model/SharedFolderMoveRequest.java
A  website/src/main/java/dev/christopherbell/sharedfolder/model/SharedFolderPreviewKind.java
A  website/src/main/java/dev/christopherbell/sharedfolder/model/SharedFolderPreviewResponse.java
A  website/src/main/java/dev/christopherbell/sharedfolder/model/SharedFolderRenameRequest.java
A  website/src/main/java/dev/christopherbell/sharedfolder/recycle/SharedFolderRecycleEntry.java
A  website/src/main/java/dev/christopherbell/sharedfolder/recycle/SharedFolderRecycleItem.java
A  website/src/main/java/dev/christopherbell/sharedfolder/recycle/SharedFolderRecyclePage.java
A  website/src/main/java/dev/christopherbell/sharedfolder/recycle/SharedFolderRecycleRepository.java
A  website/src/main/java/dev/christopherbell/sharedfolder/recycle/SharedFolderRecycleService.java
A  website/src/main/java/dev/christopherbell/sharedfolder/recycle/SharedFolderRecycleState.java
A  website/src/main/java/dev/christopherbell/sharedfolder/security/SharedFolderAccessService.java
A  website/src/main/java/dev/christopherbell/sharedfolder/service/SharedFolderAccountMutationLimiter.java
A  website/src/main/java/dev/christopherbell/sharedfolder/service/SharedFolderBrowserService.java
A  website/src/main/java/dev/christopherbell/sharedfolder/service/SharedFolderByteRangeResource.java
A  website/src/main/java/dev/christopherbell/sharedfolder/service/SharedFolderContentPolicy.java
A  website/src/main/java/dev/christopherbell/sharedfolder/service/SharedFolderDownloadService.java
A  website/src/main/java/dev/christopherbell/sharedfolder/service/SharedFolderMutationRecovery.java
A  website/src/main/java/dev/christopherbell/sharedfolder/service/SharedFolderMutationRecoveryRepository.java
A  website/src/main/java/dev/christopherbell/sharedfolder/service/SharedFolderMutationRecoveryState.java
A  website/src/main/java/dev/christopherbell/sharedfolder/service/SharedFolderMutationService.java
A  website/src/main/java/dev/christopherbell/sharedfolder/service/SharedFolderObservedItemTokens.java
A  website/src/main/java/dev/christopherbell/sharedfolder/service/SharedFolderPreviewService.java
A  website/src/main/java/dev/christopherbell/sharedfolder/service/SharedFolderRangeNotSatisfiableException.java
A  website/src/main/java/dev/christopherbell/sharedfolder/upload/SharedFolderUploadChunkProof.java
A  website/src/main/java/dev/christopherbell/sharedfolder/upload/SharedFolderUploadCompleteRequest.java
A  website/src/main/java/dev/christopherbell/sharedfolder/upload/SharedFolderUploadCreateRequest.java
A  website/src/main/java/dev/christopherbell/sharedfolder/upload/SharedFolderUploadFinalizationState.java
A  website/src/main/java/dev/christopherbell/sharedfolder/upload/SharedFolderUploadService.java
A  website/src/main/java/dev/christopherbell/sharedfolder/upload/SharedFolderUploadSession.java
A  website/src/main/java/dev/christopherbell/sharedfolder/upload/SharedFolderUploadSessionRepository.java
A  website/src/main/java/dev/christopherbell/sharedfolder/upload/SharedFolderUploadState.java
A  website/src/main/java/dev/christopherbell/sharedfolder/upload/SharedFolderUploadStatus.java
A  website/src/main/java/dev/christopherbell/sharedfolder/web/SharedFolderAdminController.java
A  website/src/main/java/dev/christopherbell/sharedfolder/web/SharedFolderNoStoreFilter.java
A  website/src/main/java/dev/christopherbell/sharedfolder/web/SharedFolderReadController.java
A  website/src/main/java/dev/christopherbell/sharedfolder/web/SharedFolderWriteController.java
M  website/src/main/java/dev/christopherbell/view/README.md
M  website/src/main/java/dev/christopherbell/view/content/ContentViewController.java
A  website/src/main/resources/application-deploy-smoke.yml
M  website/src/main/resources/application-local.yml
M  website/src/main/resources/application-prod.yml
A  website/src/main/resources/application-test.yml
M  website/src/main/resources/application.yml
A  website/src/main/resources/lib/cpu-temperature.ps1
M  website/src/main/resources/static/css/README.md
M  website/src/main/resources/static/css/main.css
M  website/src/main/resources/static/js/README.md
M  website/src/main/resources/static/js/app.js
M  website/src/main/resources/static/js/back-office.js
A  website/src/main/resources/static/js/command-center.js
M  website/src/main/resources/static/js/components/nav.js
M  website/src/main/resources/static/js/lib/README.md
M  website/src/main/resources/static/js/lib/api.js
A  website/src/main/resources/static/js/lib/back-office-shared-folder.js
M  website/src/main/resources/static/js/lib/back-office-users.js
A  website/src/main/resources/static/js/lib/command-center.js
A  website/src/main/resources/static/js/lib/shared-folder-streaming.js
A  website/src/main/resources/static/js/lib/shared-folder-worker-runtime.js
A  website/src/main/resources/static/js/lib/shared-folder.js
M  website/src/main/resources/static/js/lib/util.js
A  website/src/main/resources/static/js/shared-folder.js
A  website/src/main/resources/static/shared-folder-auth-sw.js
M  website/src/main/resources/templates/back-office.html
A  website/src/main/resources/templates/command-center.html
A  website/src/main/resources/templates/shared-folder.html
M  website/src/test/java/dev/christopherbell/account/AccountControllerTest.java
M  website/src/test/java/dev/christopherbell/account/AccountServiceTest.java
M  website/src/test/java/dev/christopherbell/admin/AdminActivityServiceTest.java
A  website/src/test/java/dev/christopherbell/admin/commandcenter/CommandCenterAccessServiceTest.java
A  website/src/test/java/dev/christopherbell/admin/commandcenter/CommandCenterComponentWiringTest.java
A  website/src/test/java/dev/christopherbell/admin/commandcenter/CommandCenterControllerTest.java
A  website/src/test/java/dev/christopherbell/admin/commandcenter/CommandCenterPropertiesTest.java
A  website/src/test/java/dev/christopherbell/admin/commandcenter/action/CommandCenterActionServiceTest.java
A  website/src/test/java/dev/christopherbell/admin/commandcenter/action/WindowsCommandExecutorTest.java
A  website/src/test/java/dev/christopherbell/admin/commandcenter/logs/CommandCenterLogServiceTest.java
A  website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProviderTest.java
A  website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/CommandCenterMetricsServiceTest.java
A  website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/CommandCenterSamplingLifecycleTest.java
A  website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureClientTest.java
A  website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/LibreHardwareCpuTemperatureProviderTest.java
A  website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/NvidiaMetricsProviderTest.java
A  website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/PowerShellCpuTemperatureProbeTest.java
A  website/src/test/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisionerTest.java
AA website/src/test/java/dev/christopherbell/configuration/MongoProfileConfigurationTest.java
M  website/src/test/java/dev/christopherbell/configuration/RateLimitFilterTest.java
M  website/src/test/java/dev/christopherbell/configuration/RequestSizeLimitFilterTest.java
A  website/src/test/java/dev/christopherbell/configuration/SchedulingConfigurationTest.java
M  website/src/test/java/dev/christopherbell/configuration/SecurityConfigTest.java
A  website/src/test/java/dev/christopherbell/configuration/SharedFolderPropertiesTest.java
A  website/src/test/java/dev/christopherbell/configuration/security/SharedFolderWorkerStaticResourceTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderAccessServiceTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderAccountMutationLimiterTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderAuditCommandTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderAuditPersistenceTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderAuditQueryServiceTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderAuditRecorderTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderLeaseClaimRepositoryTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderMaintenanceServiceTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderMutationServiceTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderNoStoreFilterTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderPathResolverTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderReadControllerTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderReadServiceTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderRecycleServiceTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderSecurityIntegrationTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderUploadServiceTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderWriteControllerTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/fs/NioSharedFolderFileSystemBoundaryTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/fs/PortableSharedFolderPrivateBoundaryTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/fs/WindowsSharedFolderBoundarySpringWiringTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/fs/WindowsSharedFolderMutationBoundaryTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/fs/WindowsSharedFolderNativeJnaIntegrationTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/fs/WindowsSharedFolderReadBoundaryTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/maintenance/MongoSharedFolderMaintenanceLeaseStoreTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/maintenance/SharedFolderMaintenanceHostLockTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/maintenance/SharedFolderMaintenanceLeaseTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/media/MediaPlaybackServiceTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/media/MediaStorageTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/media/ProgressiveMediaControllerTest.java
A  website/src/test/java/dev/christopherbell/sharedfolder/media/ProgressiveMediaStreamerTest.java
M  website/src/test/java/dev/christopherbell/view/ViewControllerTest.java
M  website/src/test/js/a11y-markup.test.js
A  website/src/test/js/back-office-shared-folder.test.js
M  website/src/test/js/back-office-users.test.js
A  website/src/test/js/command-center.test.js
M  website/src/test/js/nav-messages-link.test.js
A  website/src/test/js/shared-folder-page-initialization.test.js
A  website/src/test/js/shared-folder-streaming.test.js
A  website/src/test/js/shared-folder-worker-runtime.test.js
A  website/src/test/js/shared-folder.test.js
```

<!-- /migrated-source: docs/spokes/state.md -->

<a id="source-docs-session-memory-2026-07-25-approve-all-open-issue-campaign-spec-md"></a>
## 2026-07-25 | session-memory | 2026-07-25 - Approve All Open Issue Campaign Spec

Original source: `docs/session-memory/2026-07-25-approve-all-open-issue-campaign-spec.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `ef11eab7108c037b179214389da8d8b88daf9922771a7421ee898b6a5e4df25e`.

<!-- migrated-source: docs/session-memory/2026-07-25-approve-all-open-issue-campaign-spec.md -->
<a id="source-docs-session-memory-2026-07-25-approve-all-open-issue-campaign-spec-md--2026-07-25---approve-all-open-issue-campaign-spec"></a>
### 2026-07-25 - Approve All Open Issue Campaign Spec

<a id="source-docs-session-memory-2026-07-25-approve-all-open-issue-campaign-spec-md--1530---approve-all-open-issue-campaign-spec"></a>
#### 15:30 - Approve All Open Issue Campaign Spec

<a id="source-docs-session-memory-2026-07-25-approve-all-open-issue-campaign-spec-md--request"></a>
##### Request
Continue after the user approved the proposed seven-batch design for completing every open christopherbell.dev issue.

<a id="source-docs-session-memory-2026-07-25-approve-all-open-issue-campaign-spec-md--project-context"></a>
##### Project Context
The GitHub inventory contains 58 open issues: #1122-#1141, #1143-#1151, and #1153-#1181. The earlier count of 60 was arithmetic error; #1142 and #1152 were already closed. Builder has no open issues.

<a id="source-docs-session-memory-2026-07-25-approve-all-open-issue-campaign-spec-md--work-completed"></a>
##### Work Completed
Saved `docs/specs/2026-07-25-complete-all-open-christopherbell-dev-issues.md` with seven dependency-aware batches and one explicit acceptance entry for every open issue. Updated the campaign work ledger to link the spec, record the isolated worktree, and capture the passing baseline.

<a id="source-docs-session-memory-2026-07-25-approve-all-open-issue-campaign-spec-md--decisions"></a>
##### Decisions
Use seven cohesive PR batches instead of one mega-PR or 58 issue-per-PR changes. Preserve bearer-token API compatibility while moving browser authentication to HttpOnly cookies and CSRF protection. Use required signup names, a 15-minute post-edit window, per-user conversation archive, anonymized retained public posts after account deletion, and a repository-native Mongo migration/lease implementation unless plan-time evidence favors a maintained compatible library.

<a id="source-docs-session-memory-2026-07-25-approve-all-open-issue-campaign-spec-md--validation"></a>
##### Validation
GitHub CLI reconfirmed 58 open issues. Automated spec review found exactly 58 unique issue acceptance entries, no missing or unexpected issue numbers, and no TODO/TBD placeholders. Baseline spoke verification previously passed `:website:test`, `:website:jsTest`, and all 175 browser tests.

<a id="source-docs-session-memory-2026-07-25-approve-all-open-issue-campaign-spec-md--current-state"></a>
##### Current State
The campaign spec is `ready-for-review`. No spoke source code has been edited. Implementation planning remains gated on the user's written-spec review approval.

<a id="source-docs-session-memory-2026-07-25-approve-all-open-issue-campaign-spec-md--follow-ups"></a>
##### Follow-ups
After spec approval, create and validate the Batch 1 implementation plan with inspected line-range Code Edit blocks, then checkpoint it before test-first implementation.

<!-- /migrated-source: docs/session-memory/2026-07-25-approve-all-open-issue-campaign-spec.md -->

<a id="source-docs-session-memory-2026-07-25-authorize-autonomous-issue-campaign-continuation-md"></a>
## 2026-07-25 | session-memory | 2026-07-25 - Authorize Autonomous Issue Campaign Continuation

Original source: `docs/session-memory/2026-07-25-authorize-autonomous-issue-campaign-continuation.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `76712b3e41b3892f7a55737b11663b6720aa73f2a4a2b3911309eb8f20f56b41`.

<!-- migrated-source: docs/session-memory/2026-07-25-authorize-autonomous-issue-campaign-continuation.md -->
<a id="source-docs-session-memory-2026-07-25-authorize-autonomous-issue-campaign-continuation-md--2026-07-25---authorize-autonomous-issue-campaign-continuation"></a>
### 2026-07-25 - Authorize Autonomous Issue Campaign Continuation

<a id="source-docs-session-memory-2026-07-25-authorize-autonomous-issue-campaign-continuation-md--1532---authorize-autonomous-issue-campaign-continuation"></a>
#### 15:32 - Authorize Autonomous Issue Campaign Continuation

<a id="source-docs-session-memory-2026-07-25-authorize-autonomous-issue-campaign-continuation-md--request"></a>
##### Request
The user approved the written 58-issue campaign spec and explicitly instructed Codex to continue without requesting further routine approvals, and to save that instruction.

<a id="source-docs-session-memory-2026-07-25-authorize-autonomous-issue-campaign-continuation-md--project-context"></a>
##### Project Context
The approved scope remains the seven batches and 58 GitHub issues in `docs/specs/2026-07-25-complete-all-open-christopherbell-dev-issues.md`. Repository and safety rules still apply, including trusted-comment boundaries, isolated spoke worktrees, artifact checkpoints, CI gates, and alternate-port verification on the production host.

<a id="source-docs-session-memory-2026-07-25-authorize-autonomous-issue-campaign-continuation-md--work-completed"></a>
##### Work Completed
Changed the campaign spec to `ready-for-execution`, recorded the approval and autonomous-continuation instruction in the spec and work ledger, and created an ad-hoc user-memory update note at `C:\Users\Christopher\.codex\memories\extensions\ad_hoc\notes\2026-07-25T153143-autonomous-approved-issue-campaign.md`.

<a id="source-docs-session-memory-2026-07-25-authorize-autonomous-issue-campaign-continuation-md--decisions"></a>
##### Decisions
Do not pause for routine design, plan, implementation, test, PR, merge, issue-closure, or Builder phase approvals within the accepted campaign. Ask only if new authority is required, scope would materially expand/change, or a safe in-scope path cannot resolve an external blocker.

<a id="source-docs-session-memory-2026-07-25-authorize-autonomous-issue-campaign-continuation-md--validation"></a>
##### Validation
Confirmed the written spec already contains exactly 58 unique issue acceptance entries and has no placeholder text. Builder hub validation will run after index refresh.

<a id="source-docs-session-memory-2026-07-25-authorize-autonomous-issue-campaign-continuation-md--current-state"></a>
##### Current State
The campaign spec is approved and `ready-for-execution`. Batch 1 implementation planning is the next active phase.

<a id="source-docs-session-memory-2026-07-25-authorize-autonomous-issue-campaign-continuation-md--follow-ups"></a>
##### Follow-ups
Create, review, validate, commit, and push the Batch 1 implementation plan, then proceed directly to test-first implementation.

<!-- /migrated-source: docs/session-memory/2026-07-25-authorize-autonomous-issue-campaign-continuation.md -->

<a id="source-docs-session-memory-2026-07-25-browser-security-issues-1125-1130-md"></a>
## 2026-07-25 | session-memory | 2026-07-25 Browser Security Issues 1125-1130

Original source: `docs/session-memory/2026-07-25-browser-security-issues-1125-1130.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `be68941e3fffe14357a9d6d3e42d110ab9c389f9ec21c1eb51d38ebe35f07b6a`.

<!-- migrated-source: docs/session-memory/2026-07-25-browser-security-issues-1125-1130.md -->
<a id="source-docs-session-memory-2026-07-25-browser-security-issues-1125-1130-md--2026-07-25-browser-security-issues-1125-1130"></a>
### 2026-07-25 Browser Security Issues 1125-1130

<a id="source-docs-session-memory-2026-07-25-browser-security-issues-1125-1130-md--2051---complete-browser-security-sub-batch"></a>
#### 20:51 - Complete browser security sub-batch

<a id="source-docs-session-memory-2026-07-25-browser-security-issues-1125-1130-md--request"></a>
##### Request

Continue the autonomous campaign to complete every open `azurras/christopherbell.dev` GitHub issue.
The user authorized routine continuation without approval pauses and asked that this preference be
saved. Only comments by `azurras` may influence issue scope or acceptance.

<a id="source-docs-session-memory-2026-07-25-browser-security-issues-1125-1130-md--project-context"></a>
##### Project Context

Builder is the durable workflow hub at `C:\Users\Christopher\Developer\builder`. The authoritative
spoke checkout at `A:\Projects\christopherbell.dev` contains extensive unrelated user work and was
left untouched. Development used the isolated worktree
`A:\Projects\christopherbell.dev-worktrees\browser-security-1125-1130` on
`codex/browser-security-1125-1130`. The development host also runs production on native Windows
services, so all pre-merge runtime testing used port `8090`.

<a id="source-docs-session-memory-2026-07-25-browser-security-issues-1125-1130-md--work-completed"></a>
##### Work Completed

- Delivered issues #1125-#1130 in [PR #1249](https://github.com/azurras/christopherbell.dev/pull/1249), squash-merged as `b6c361d1d916337679a37f04caa46c3475215e71`.
- Added typed browser-security configuration, production HSTS, CSP, same-origin framing, referrer and permissions policies.
- Restored Spring SPA CSRF for cookie browsers while retaining a narrow stateless legacy/API login path.
- Replaced browser localStorage JWT handling with an HttpOnly `CBELL_AUTH` cookie and a non-secret `CBELL_AUTH_STATE` marker verified against `/me`.
- Removed token transport from browser modules and the shared-folder service worker; same-origin requests now carry cookies naturally.
- Made password-reset links use the configured canonical origin and added bounded Bean Validation to login/reset DTOs.
- Required and normalized first and last names in signup UI and server validation.
- Recorded the final review at `docs/spoke-reviews/2026-07-25-browser-security-issues-1125-1130.md` and production evidence in `docs/test-reports/2026-07-25-browser-security-issues-1125-1130.md`.

<a id="source-docs-session-memory-2026-07-25-browser-security-issues-1125-1130-md--decisions"></a>
##### Decisions

- Explicit bearer clients retain priority and receive the legacy JWT response; only requests opting into `X-CBELL-Browser-Session: cookie` receive browser cookies and require CSRF for login.
- A readable cookie contains only a presence marker, never credentials or authorization claims; the server remains authoritative.
- Invalid or expired public credentials continue anonymously so browser logout and stale-session cleanup can complete.
- Production trusts the configured canonical reset origin and ignores forwarded host/protocol values.

<a id="source-docs-session-memory-2026-07-25-browser-security-issues-1125-1130-md--validation"></a>
##### Validation

- Observed RED evidence before implementation for cookie auth, CSRF, localStorage removal, signup names, and worker cookie forwarding.
- Focused post-review Java: 74 cases passed.
- Full Java: 108 suites, 999 tests, 0 failures, 3 skipped.
- Full JavaScript after rebase: 195/195 passed; `node --check` passed all 22 changed JavaScript files; `git diff --check` passed.
- PR #1249 passed Windows, macOS, Ubuntu, Dependency Review, and CodeQL for Actions, Java/Kotlin, and JavaScript/TypeScript.
- Live port-8090 matrix passed, the process was stopped, and production port 8080 stayed healthy.
- Native auto-deploy switched production from PID `50708` to PID `26680`; the public site remained `200` and now emits the complete HTTPS security policy.
- Production login/CSRF/validation/logout probes returned the planned `400`/`403`/`200` results and Secure cookie-clearing attributes.
- A pre-deployment signed-in Chrome `/shared` session redirected to `/login?redirect=%2Fshared` after refresh, proving fail-closed migration from the removed localStorage JWT. No console errors appeared.

<a id="source-docs-session-memory-2026-07-25-browser-security-issues-1125-1130-md--current-state"></a>
##### Current State

- Issues #1125-#1130 are closed automatically by the merged PR.
- The isolated worktree is clean at `98099a40`; `origin/main` is `b6c361d1d916337679a37f04caa46c3475215e71`.
- Production is healthy on port `8080`, PID `26680`.
- Chrome is waiting at the login page with the intended `/shared` return target because the storage migration requires one fresh login.
- The campaign has 41 open issues remaining.

<a id="source-docs-session-memory-2026-07-25-browser-security-issues-1125-1130-md--follow-ups"></a>
##### Follow-ups

- After the user completes the one-time fresh login, confirm authenticated `/shared` access under the new cookie session.
- Select the next dependency-aware issue batch and continue the full Builder delivery loop.

<!-- /migrated-source: docs/session-memory/2026-07-25-browser-security-issues-1125-1130.md -->

<a id="source-docs-session-memory-2026-07-25-plan-github-automation-issues-1144-1150-md"></a>
## 2026-07-25 | session-memory | 2026-07-25 - Plan GitHub Automation Issues 1144-1150

Original source: `docs/session-memory/2026-07-25-plan-github-automation-issues-1144-1150.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `e440ad761bc77d2f92d5cff54d5f78e8298ff66ae0779a0ad4faa582a980ee4c`.

<!-- migrated-source: docs/session-memory/2026-07-25-plan-github-automation-issues-1144-1150.md -->
<a id="source-docs-session-memory-2026-07-25-plan-github-automation-issues-1144-1150-md--2026-07-25---plan-github-automation-issues-1144-1150"></a>
### 2026-07-25 - Plan GitHub Automation Issues 1144-1150

<a id="source-docs-session-memory-2026-07-25-plan-github-automation-issues-1144-1150-md--request"></a>
#### Request

Continue the approved campaign to complete every open `azurras/christopherbell.dev` issue without routine approval pauses, beginning with the GitHub automation portion of Batch 1.

<a id="source-docs-session-memory-2026-07-25-plan-github-automation-issues-1144-1150-md--work-completed"></a>
#### Work Completed

- Created `docs/implementation-plans/2026-07-25-github-automation-issues-1144-1150.md` for issues #1144-#1150.
- Defined artifact-native RED/GREEN coverage for Gradle caching, failed-run diagnostics, CodeQL, Dependency Review, Dependabot grouping, and stale-policy permissions and windows.
- Split the broader deployment/configuration batch so this independent automation work can be reviewed, rolled back, merged, and closed as one coherent pull request.
- Updated the central work ledger with the ready plan.

<a id="source-docs-session-memory-2026-07-25-plan-github-automation-issues-1144-1150-md--decisions"></a>
#### Decisions

- Execute inline without subagents, consistent with the user's autonomous campaign authorization.
- Keep each GitHub automation concern in its native configuration file and add a Node built-in filesystem contract test rather than introducing an npm dependency.
- Preserve console test output while adding JUnit XML for artifact collection.
- Use current supported major action tags verified from official action documentation.
- Parse YAML into structured Jackson trees in JUnit rather than relying on formatting-sensitive Node regular expressions; include the checkout step shown by the official Dependency Review installation contract.

<a id="source-docs-session-memory-2026-07-25-plan-github-automation-issues-1144-1150-md--validation"></a>
#### Validation

- `validate_implementation_plan.py` passed.
- Placeholder scan and `git diff --check` passed.
- Execution-readiness review found no blockers. Residual risk is limited to GitHub-hosted feature availability and action behavior, which the pull request checks must prove.
- After remote main advanced, the baseline was refreshed at `ea2ba7ea4c4ab1b71f172a29dd994e8375507675`: `:website:test` and all 176 `jsTest` cases passed. The reviewed plan was updated before implementation to use parsed YAML assertions and the current README insertion line.
- Full trusted issue-body intake corrected the stale contract before production edits: workflow-level permissions are empty, the job receives only issue and pull-request writes, assigned and milestone issues are directly exempt, and `pinned`/`roadmap` protection labels cover action/stale's lack of native pin-metadata support.
- Final diff review made `jackson-dataformat-yaml` an explicit test dependency so the parsed-YAML contract does not rely on Springdoc's transitive classpath.
- PR #1241 proved that GitHub default setup rejects advanced-workflow SARIF uploads. The corrective design preserves all three default-setup languages in the checked-in matrix, builds Java manually, and only then switches default setup off through GitHub's supported API.

<a id="source-docs-session-memory-2026-07-25-plan-github-automation-issues-1144-1150-md--completion"></a>
#### Completion

- Implemented and pushed commits `0b7c117f` and `86e7442d` on `codex/github-automation-1144-1150`.
- Merged PR [#1241](https://github.com/azurras/christopherbell.dev/pull/1241) as squash commit `88144134290e5f690c048cb4945db531b8ef17c9`.
- GitHub closed #1144, #1145, #1146, #1147, #1148, #1149, and #1150 at merge time.
- Created and verified repository labels `pinned` and `roadmap` for stale-policy protection.
- Switched CodeQL from default setup to the checked-in advanced workflow through the supported repository API after preserving Actions, Java/Kotlin, and JavaScript/TypeScript coverage.

<a id="source-docs-session-memory-2026-07-25-plan-github-automation-issues-1144-1150-md--final-validation"></a>
#### Final Validation

- RED: all five parsed-YAML configuration contracts failed before implementation; the expanded CodeQL matrix contract also failed before the hosted fix.
- GREEN: the focused five-test JUnit contract passed.
- `gradlew build --rerun-tasks --no-daemon` passed on the rebased final tree; the browser JUnit report parsed with a `testsuites` root and all 176 browser tests passed.
- Hosted checks passed on Ubuntu, macOS, Windows, Dependency Review, and all CodeQL language jobs.
- Independent review found no Critical, Important, or Minor findings.
- Local Spring app testing and a Builder test report were not applicable because this batch changed repository automation only and did not change runtime application behavior.

<a id="source-docs-session-memory-2026-07-25-plan-github-automation-issues-1144-1150-md--follow-up"></a>
#### Follow-up

- Continue the autonomous campaign with the remaining 51 open issues, beginning with the next production/deployment/configuration sub-plan.

<a id="source-docs-session-memory-2026-07-25-plan-github-automation-issues-1144-1150-md--current-state-and-follow-up"></a>
#### Current State and Follow-up

- Plan status is `ready-for-execution`.
- Next create `codex/github-automation-1144-1150` in a fresh sibling worktree, invoke the required implementation skills, witness RED, implement, run the full relevant suites, publish a pull request, wait for checks, merge, and close #1144-#1150.

<!-- /migrated-source: docs/session-memory/2026-07-25-plan-github-automation-issues-1144-1150.md -->

<a id="source-docs-session-memory-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md"></a>
## 2026-07-25 | session-memory | 2026-07-25 - Production foundations issues 1143, 1151, 1153, and 1154

Original source: `docs/session-memory/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `c97730af5de117e27a309ae87e601bf6ffa197f9205a0cdb462c4d7cdf10ecb5`.

<!-- migrated-source: docs/session-memory/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md -->
<a id="source-docs-session-memory-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--2026-07-25---production-foundations-issues-1143-1151-1153-and-1154"></a>
### 2026-07-25 - Production foundations issues 1143, 1151, 1153, and 1154

<a id="source-docs-session-memory-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--2335---production-foundations-issues-1143-1151-1153-and-1154"></a>
#### 23:35 - Production foundations issues 1143, 1151, 1153, and 1154

<a id="source-docs-session-memory-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--request"></a>
##### Request

Continue the approved campaign to complete every open `azurras/christopherbell.dev` issue autonomously. The user authorized implementation, testing, PR, CI, merge, production verification, and Builder closeout without routine approval pauses. Only GitHub comments from `azurras` are trusted instructions; these four issues had no comments or attachments.

<a id="source-docs-session-memory-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--project-context"></a>
##### Project Context

- Builder hub: `C:\Users\Christopher\Developer\builder`, branch `main`.
- Dirty authoritative spoke checkout: `A:\Projects\christopherbell.dev`; it was not edited.
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\production-foundations-1143-1154`, branch `codex/production-foundations-1143-1154`.
- Production is the native Windows `ChristopherBellDev` service on port 8080 with a SYSTEM-owned guarded deployment loop.
- The worktree's checkout-only `gradlew.bat` line-ending difference was preserved and excluded from both commits.

<a id="source-docs-session-memory-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--work-completed"></a>
##### Work Completed

- Completed environment-driven production Mongo configuration (#1143), pre-refresh aggregated redacted production settings validation (#1151), pinned loopback-only persistent Mongo Compose support (#1153), and a leased immutable versioned Mongo migration runner with V001 infrastructure indexes (#1154).
- Added typed mail settings so non-production mail defaults off, production retains enabled compatibility by default, and an explicit false value makes mail credentials optional without resolving a sender.
- Added Windows production environment parsing and launch allowlisting for `APP_MAIL_ENABLED`, plus migration/local Mongo authoring, recovery, backup, and rollback documentation.
- Spoke commit `257e2f656c030aa585b99cb07d58d96489a980b4` implemented the batch. After macOS CI reproduced a pre-existing timing race, commit `4e767dfd87a03f873114d496600f1a68d8f560c6` replaced the provider-side pre-return latch with a deterministic single-worker executor barrier.
- PR #1252 squash-merged as `965b25bb3e703a2e67a5064d777a9ab1998f26a1`; issues #1143, #1151, #1153, and #1154 closed automatically.

<a id="source-docs-session-memory-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--decisions"></a>
##### Decisions

- Registered an `ApplicationContextInitializer` so invalid production settings fail before Mongo, mail, or web bean refresh and report setting names without values.
- Kept production mail enabled by default for existing deployment compatibility while making the switch explicit and typed.
- Used the official `mongo:8.3.2` image with loopback-only publishing, a named volume, and a `mongosh` health check.
- Kept migration identity/checksum append-only, serialized execution through a fixed Mongo lease, and failed closed on checksum drift or incomplete records.
- Fixed the macOS CI race at its synchronization boundary instead of rerunning CI: a queued executor barrier cannot complete until the timed-out provider wrapper has executed its `finally` completion marker.

<a id="source-docs-session-memory-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--validation"></a>
##### Validation

- Witnessed focused Java compilation RED and 6-of-25 Pester RED, then 32 focused Java passes.
- Missing-settings packaged start exited 1 before port 8090 bound and emitted one redacted report naming Mongo URI, JWT, sender, and Resend settings.
- Disposable database `christopherbell_foundations_test_20260725230000` passed first start and restart at HTTP 200, retained exactly one APPLIED V001 record and both indexes, then was dropped after exact-name and production-inequality guards.
- Final local suite: 1,030 Java tests with zero failures and three existing skips; 199 JavaScript tests passed; 247 Pester tests with 243 passed, zero failed, and four environment/privilege skips; diff checks passed.
- The exact timing test and all 12 owning command-center metrics tests passed after the deterministic repair; the full 1,030-test suite passed again.
- PR checks passed on Ubuntu, macOS, Windows, Dependency Review, and CodeQL for Actions, Java/Kotlin, and JavaScript/TypeScript.
- Guarded production deployment changed the Java listener from PID 29012 to 30976. `/` remained 200; readiness briefly returned 503 during initialization, then reached 200.
- Read-only production Mongo inspection proved exactly one APPLIED V001 record with checksum `aec77e3e8cf68bf8d67f239ee0e842fbdad26ea9766ab04cbc3d74dd9ad93876`, both named indexes, and a released ownerless epoch-expired migration lease.
- The deployed command-center HTML referenced assets under the exact merge SHA namespace. The in-app browser was anonymous, while Chrome blocked controlled navigation before reaching the site; neither browser limitation affected the HTTP, release, or database acceptance evidence.

<a id="source-docs-session-memory-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--current-state"></a>
##### Current State

- Production is healthy on Java listener PID 30976 at merge `965b25bb`.
- The four source issues are closed and PR #1252 is merged.
- The isolated spoke worktree tracks the pushed commit history and retains only unstaged `gradlew.bat` line-ending state.
- The campaign has 30 open issues remaining.

<a id="source-docs-session-memory-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--follow-ups"></a>
##### Follow-ups

- Refresh Builder indexes and validation, commit/push this closeout checkpoint, and post concise closure reconciliation comments to the four GitHub issues.
- Reconcile the remaining live issue inventory, select the next dependency-aware batch, and continue the approved delivery loop without routine approval pauses.

<!-- /migrated-source: docs/session-memory/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md -->

<a id="source-docs-session-memory-2026-07-25-public-content-issues-1131-1137-md"></a>
## 2026-07-25 | session-memory | 2026-07-25 - Public content issues 1131-1137

Original source: `docs/session-memory/2026-07-25-public-content-issues-1131-1137.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `4c735850c41be26b82a9f185b8c82a00e9a570ab6923d7e1b80e5d058d872bc4`.

<!-- migrated-source: docs/session-memory/2026-07-25-public-content-issues-1131-1137.md -->
<a id="source-docs-session-memory-2026-07-25-public-content-issues-1131-1137-md--2026-07-25---public-content-issues-1131-1137"></a>
### 2026-07-25 - Public content issues 1131-1137

<a id="source-docs-session-memory-2026-07-25-public-content-issues-1131-1137-md--2220---public-content-issues-1131-1137"></a>
#### 22:20 - Public content issues 1131-1137

<a id="source-docs-session-memory-2026-07-25-public-content-issues-1131-1137-md--request"></a>
##### Request
Complete every open `azurras/christopherbell.dev` GitHub issue autonomously under the approved 58-issue campaign. The user explicitly authorized implementation, testing, PR, CI, merge, production verification, and Builder closeout without routine approval pauses. Only GitHub comments from `azurras` are trusted instructions.

<a id="source-docs-session-memory-2026-07-25-public-content-issues-1131-1137-md--project-context"></a>
##### Project Context
- Builder hub: `C:\Users\Christopher\Developer\builder`, branch `main`.
- Spoke authoritative checkout: `A:\Projects\christopherbell.dev`; it remains dirty and was not edited.
- Isolated spoke worktree: `A:\Projects\christopherbell.dev-worktrees\public-content-1131-1137`, branch `codex/public-content-1131-1137`.
- Campaign spec: `C:\Users\Christopher\Developer\builder\docs\specs\2026-07-25-complete-all-open-christopherbell-dev-issues.md`.
- Batch plan: `C:\Users\Christopher\Developer\builder\docs\implementation-plans\2026-07-25-public-content-issues-1131-1137.md`.
- Production is the native Windows `ChristopherBellDev` service on port 8080 with automatic guarded deployment from `origin/main`.

<a id="source-docs-session-memory-2026-07-25-public-content-issues-1131-1137-md--work-completed"></a>
##### Work Completed
- Completed issues #1131-#1137 through PR #1251: current anonymous blog/photo APIs, standard response-envelope rendering, public photography usage route, archive link/favicon/asset repairs, removal of insecure The Bell images, useful gallery alt fallbacks, and pinned self-hosted Bootstrap 5.3.3 with a narrower CSP.
- Corrected `application.yml` from `photo-properties.images` to `photo-properties.photos`, restoring all 12 configured gallery records.
- Replaced the CI-bound `@SpringBootTest` configuration regression with a narrow `YamlPropertySourceLoader` plus `Binder` test after macOS CI exposed an unintended MongoDB dependency.
- Spoke commits: `ea54749730df97f2bfc920271c8463eb826e3f2f`, `4108c5c6f5adf5877f247c2cff4cf543fd7eb1cd`, and `f5120784bf4763cbd57666839307be24d209198a`.
- PR #1251 squash-merged as `4b82116a0ed489c74eed144a478f1b3a3944ada2`; issues #1131-#1137 closed automatically.
- Updated and validated the test report at `C:\Users\Christopher\Developer\builder\docs\test-reports\2026-07-25-public-content-issues-1131-1137.md` and spoke review at `C:\Users\Christopher\Developer\builder\docs\spoke-reviews\2026-07-25-public-content-issues-1131-1137.md`; production closure update committed to Builder as `bd667a1`.

<a id="source-docs-session-memory-2026-07-25-public-content-issues-1131-1137-md--decisions"></a>
##### Decisions
- Kept public access GET-only: anonymous GETs are permitted while equivalent POST requests remain denied.
- Used the repository's existing response helper shapes and safe text DOM construction rather than adding a parallel API client or HTML injection path.
- Reused the Bootstrap WebJar already compatible with the Gradle application and pinned it exactly to 5.3.3; no new CDN trust was added.
- Treated configured `n/a` photo descriptions as missing so a meaningful photo name becomes the alt fallback.
- Narrowed the configuration test to the binding boundary it owns; no full app context or external database is required.

<a id="source-docs-session-memory-2026-07-25-public-content-issues-1131-1137-md--validation"></a>
##### Validation
- Focused public-content Java suite: 29 passed.
- Focused Node suite: 4 passed after witnessed RED failures; full JavaScript suite: 199 passed.
- Authoritative local command `gradlew.bat :website:cleanTest :website:check --no-daemon --no-watch-fs --max-workers=1 --console=plain`: passed in 1m32s after the CI harness fix, with 1,003 Java tests, 0 failures, 3 skipped, plus `bootJar` and sensor runtime verification.
- PR checks passed on Ubuntu, macOS, Windows, Dependency Review, and all CodeQL analyses; post-merge main CI Build and CodeQL passed.
- Automatic production deployment changed the Java listener from PID 26680 to 29012. Production HTTPS returned 200 for every target page, API, and WebJar asset; both APIs exposed configured data; all four POST boundary probes returned 403.
- Deployed browser checks rendered all 12 gallery images with correct alt partitioning, the usage warning, the configured blog post, and Tony's three images with zero warning/error console entries.
- Builder test-report quality and hub-state validation passed; only known legacy-plan warnings remain.

<a id="source-docs-session-memory-2026-07-25-public-content-issues-1131-1137-md--current-state"></a>
##### Current State
- Builder was clean after pushing `bd667a1` before this memory entry.
- The isolated spoke worktree tracks its pushed branch and has only the known checkout-only `gradlew.bat` LF-to-CRLF difference, which is absent from all commits.
- Production is healthy on port 8080 at merge `4b82116a`.
- The controlled Chrome tab still redirects `/shared` to `/login?redirect=%2Fshared` despite the user reporting sign-in, so authenticated browser verification may require signing in within that specific controlled tab when an authenticated issue needs it.

<a id="source-docs-session-memory-2026-07-25-public-content-issues-1131-1137-md--follow-ups"></a>
##### Follow-ups
- Commit and push this memory checkpoint, generate exact closure text for #1131-#1137, and reconcile Builder work records.
- Inventory the remaining open GitHub issues against the campaign spec, select the next coherent batch, create a fresh isolated worktree, and continue the full delivery loop without requesting routine approval.

<a id="source-docs-session-memory-2026-07-25-public-content-issues-1131-1137-md--2222---public-content-issues-1131-1137"></a>
#### 22:22 - Public content issues 1131-1137

<a id="source-docs-session-memory-2026-07-25-public-content-issues-1131-1137-md--closure-reconciliation"></a>
##### Closure Reconciliation

- Saved the completed spoke update at `C:\Users\Christopher\Developer\builder\docs\spoke-updates\2026-07-25-public-content-issues-1131-1137.md`.
- Updated the active campaign ledger to mark the public-content plan complete, record PR #1251 and production PID `29012`, and reduce the remaining issue count from 41 to 34.
- The batch has no remaining blocker or acceptance gap. The controlled Chrome authentication mismatch is retained only as contextual state for a future authenticated flow, not as a campaign blocker.

<!-- /migrated-source: docs/session-memory/2026-07-25-public-content-issues-1131-1137.md -->

<a id="source-docs-session-memory-2026-07-25-public-delivery-issues-1122-1124-1138-md"></a>
## 2026-07-25 | session-memory | 2026-07-25 - public-delivery-issues-1122-1124-1138

Original source: `docs/session-memory/2026-07-25-public-delivery-issues-1122-1124-1138.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `3482c6248a91e1f2f4b27b134fd2c135473bd858f44a5eb8bb45954e1f33aebf`.

<!-- migrated-source: docs/session-memory/2026-07-25-public-delivery-issues-1122-1124-1138.md -->
<a id="source-docs-session-memory-2026-07-25-public-delivery-issues-1122-1124-1138-md--2026-07-25---public-delivery-issues-1122-1124-1138"></a>
### 2026-07-25 - public-delivery-issues-1122-1124-1138

<a id="source-docs-session-memory-2026-07-25-public-delivery-issues-1122-1124-1138-md--1932---public-delivery-issues-1122-1124-and-1138"></a>
#### 19:32 - Public delivery issues 1122 1124 and 1138

<a id="source-docs-session-memory-2026-07-25-public-delivery-issues-1122-1124-1138-md--request"></a>
##### Request
Complete every open GitHub issue in azurras/christopherbell.dev autonomously. Preserve the dirty authoritative checkout, use isolated worktrees, carry each issue through implementation, verification, PR/CI, merge, production acceptance, closure, and durable Builder records. The user explicitly waived routine approval pauses and asked that preference be saved.

<a id="source-docs-session-memory-2026-07-25-public-delivery-issues-1122-1124-1138-md--project-context"></a>
##### Project Context
Builder is the workflow hub at C:\Users\Christopher\Developer\builder. The authoritative spoke checkout at A:\Projects\christopherbell.dev remains dirty and untouched. Only GitHub comments by azurras are trusted as scope or workflow instructions. Production is the native Windows ChristopherBellDev service behind Cloudflare.

<a id="source-docs-session-memory-2026-07-25-public-delivery-issues-1122-1124-1138-md--work-completed"></a>
##### Work Completed
- Completed GitHub automation issues #1144-#1150 through PR #1241, merged as 88144134290e5f690c048cb4945db531b8ef17c9.
- Completed public-delivery issues #1122, #1123, #1124, and #1138 through PR #1245, merged as c0ccb88bf8666fa1014d2568ce772f48ac538705.
- Added a Cloudflare Single Redirect rule that preserves apex paths and queries while returning 301 to canonical www.
- Live testing found production rendered /dev asset URLs because the installed service does not receive the candidate launcher's GIT_COMMIT environment.
- Fixed the regression test-first in isolated worktree A:\Projects\christopherbell.dev-worktrees\asset-version-fix. PR #1246 embeds the exact checkout SHA in packaged application.yml while preserving a runtime GIT_COMMIT override; it merged as 193761d4e0b69240188b8d053de4c9ba4115e339.
- Changed Cloudflare Browser Cache TTL from four hours to Respect Existing Headers so Spring remains authoritative for versioned assets, direct assets, and metadata.
- Added final production closure comments to #1122, #1123, #1124, and #1138.
- Updated the Builder plan, test report, spoke review, and campaign work ledger; production acceptance checkpoint commit is 15cf54e on Builder main.
- Saved the user's autonomous-continuation preference to C:\Users\Christopher\.codex\memories\extensions\ad_hoc\notes\2026-07-25T153143-autonomous-approved-issue-campaign.md.

<a id="source-docs-session-memory-2026-07-25-public-delivery-issues-1122-1124-1138-md--decisions"></a>
##### Decisions
- Kept fixed resource versioning so relative ES-module imports remain inside one release namespace.
- Embedded the Git SHA at build time instead of relying on a one-time service-wrapper environment change; this survives native service restarts and works with the existing auto-deployer.
- Kept GIT_COMMIT as an optional runtime override for candidate launches.
- Made Cloudflare respect origin cache headers rather than duplicating per-route cache logic at the edge.

<a id="source-docs-session-memory-2026-07-25-public-delivery-issues-1122-1124-1138-md--validation"></a>
##### Validation
- Test-first regression failed against origin/main because packaged application.yml used ${GIT_COMMIT:dev}; all seven focused PublicDeliveryConfigurationTest tests passed after the fix.
- gradlew.bat --no-daemon clean build passed all 21 tasks in 4 minutes 53 seconds.
- Independent review found no merge blocker. An isolated JAR without GIT_COMMIT served SHA-versioned CSS; /dev CSS did not resolve.
- PR #1246 passed Windows, macOS, Linux, Dependency Review, CodeQL Actions, Java/Kotlin, and JavaScript/TypeScript checks.
- Production HTML uses exact namespace /193761d4e0b69240188b8d053de4c9ba4115e339/.
- Versioned CSS returns 200 with public max-age=31536000 immutable; direct CSS returns 200 with public max-age=3600; robots.txt returns 200 with no-cache.
- Liveness and readiness return 200 with detail-free UP bodies; aggregate health returns 403.
- Apex /blog?utm_source=codex returns 301 to the identical www path and query.
- Builder index refresh completed and hub validation passed with only known legacy-plan warnings.

<a id="source-docs-session-memory-2026-07-25-public-delivery-issues-1122-1124-1138-md--current-state"></a>
##### Current State
- Builder main is clean after commit 15cf54e before this memory entry.
- The asset-version worktree is clean at local branch codex/fix-production-asset-version; its remote branch was deleted by merged PR #1246.
- Production runs merge 193761d4e0b69240188b8d053de4c9ba4115e339.
- Issues #1122-#1124, #1138, and #1144-#1150 are closed. Forty-seven open issues remain, beginning with #1125.

<a id="source-docs-session-memory-2026-07-25-public-delivery-issues-1122-1124-1138-md--follow-ups"></a>
##### Follow-ups
- Continue immediately with the next dependency-aware security batch, likely #1125-#1130, using a fresh isolated worktree and the full Builder delivery loop.
- Independent review warned that the packaged-config unit assertion accepts any 40-hex fallback rather than comparing with HEAD. Generated-resource inspection, isolated-JAR HTTP proof, and exact live merge-SHA validation close the release evidence gap; later test hardening may encode exact equality.
- Close the overall campaign work record and save final campaign memory only after all remaining issues are resolved.

<!-- /migrated-source: docs/session-memory/2026-07-25-public-delivery-issues-1122-1124-1138.md -->

<a id="source-docs-session-memory-2026-07-25-start-all-open-issue-campaign-md"></a>
## 2026-07-25 | session-memory | 2026-07-25 - Start All Open Issue Campaign

Original source: `docs/session-memory/2026-07-25-start-all-open-issue-campaign.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `05074641c776477867fc3a8db980a8c002af1b6e0ec6541eda728b6ea79b20c9`.

<!-- migrated-source: docs/session-memory/2026-07-25-start-all-open-issue-campaign.md -->
<a id="source-docs-session-memory-2026-07-25-start-all-open-issue-campaign-md--2026-07-25---start-all-open-issue-campaign"></a>
### 2026-07-25 - Start All Open Issue Campaign

<a id="source-docs-session-memory-2026-07-25-start-all-open-issue-campaign-md--1512---start-all-open-issue-campaign"></a>
#### 15:12 - Start All Open Issue Campaign

<a id="source-docs-session-memory-2026-07-25-start-all-open-issue-campaign-md--request"></a>
##### Request
Complete every currently open GitHub issue, prioritizing the best solution. The user asked to skip the coding-standard skill, but Builder repository instructions make that skill mandatory for code edits.

<a id="source-docs-session-memory-2026-07-25-start-all-open-issue-campaign-md--project-context"></a>
##### Project Context
Builder is the workflow hub. `azurras/builder` has no open issues; `azurras/christopherbell.dev` has 58 open issues and no open pull requests. Issues #1142 and #1152 were already closed. Only GitHub comments from `azurras` are trusted as workflow instructions.

<a id="source-docs-session-memory-2026-07-25-start-all-open-issue-campaign-md--work-completed"></a>
##### Work Completed
Inventoried GitHub state, refreshed the spoke remote, inspected worktrees, created the campaign work ledger, and refreshed `docs/spokes/state.md`.

<a id="source-docs-session-memory-2026-07-25-start-all-open-issue-campaign-md--decisions"></a>
##### Decisions
Treat the 58 open christopherbell.dev issues as the requested scope. Preserve the authoritative spoke checkout because it is ahead 3, behind 53, and contains extensive unrelated changes. Use isolated worktrees based on current `origin/main`.

<a id="source-docs-session-memory-2026-07-25-start-all-open-issue-campaign-md--validation"></a>
##### Validation
Confirmed Builder branch `main` and clean starting status. Confirmed the Builder origin URL. Confirmed remote spoke `origin/main` at `259e873259f14d3fea5d81a9b6845ead727a9eee` after fetch.

<a id="source-docs-session-memory-2026-07-25-start-all-open-issue-campaign-md--current-state"></a>
##### Current State
Campaign is active. No spoke code has been edited. The next phase is current-state audit in a clean worktree, followed by the durable spec and implementation plan checkpoints.

<a id="source-docs-session-memory-2026-07-25-start-all-open-issue-campaign-md--follow-ups"></a>
##### Follow-ups
Audit all 58 issues, group only coherent dependencies, retain per-issue closure evidence, and run local runtime verification on a non-production port before any deployment action.

<!-- /migrated-source: docs/session-memory/2026-07-25-start-all-open-issue-campaign.md -->

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md"></a>
## 2026-07-25 | specs | Complete All Open christopherbell.dev Issues

Original source: `docs/specs/2026-07-25-complete-all-open-christopherbell-dev-issues.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `925f13ede47165138d0f8258c77d587de8cdb04db737c2c22913ea27933729fe`.

<!-- migrated-source: docs/specs/2026-07-25-complete-all-open-christopherbell-dev-issues.md -->
<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--complete-all-open-christopherbelldev-issues"></a>
### Complete All Open christopherbell.dev Issues

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--document-status"></a>
#### Document Status

complete

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--purpose"></a>
#### Purpose

Close every GitHub issue that was open in `azurras/christopherbell.dev` at the 2026-07-25 campaign inventory by validating current behavior, implementing the unmet contract, proving it locally, passing required CI, merging through pull requests, and recording issue-specific closure evidence.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--completion-summary"></a>
#### Completion Summary

Completed 2026-07-26. All 58 inventoried issues are closed, every delivery batch passed local
runtime verification and required GitHub gates, all merged changes reached native Windows
production, and a live `gh issue list --state open` returned an empty result. Final production
merge `9963ed0cc83f8b43f54612c1b8c6ed2966f22607` is serving through PID `29164` on port `8080`;
local and external roots return HTTP 200 and the native service set remains Running/Automatic.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--background"></a>
#### Background

Builder has no open issues. `azurras/christopherbell.dev` has 58 open issues: #1122-#1141, #1143-#1151, and #1153-#1181. Issues #1142 and #1152 were already closed. There were no open pull requests at inventory time. The current remote baseline was `259e873259f14d3fea5d81a9b6845ead727a9eee` and passed `:website:test` plus all 175 browser-side JavaScript tests.

The authoritative spoke checkout at `A:\Projects\christopherbell.dev` contains extensive unrelated user work and must not be changed. Campaign work uses isolated worktrees created from refreshed `origin/main`. This Windows development machine also hosts production. Local runtime verification must therefore use a non-8080 port before any production restart or deployment.

Live checks on 2026-07-25 returned 404 for `/`, `/blog`, `/photos`, `/wfl`, `/tools`, `/canes-box-tracker`, `/sitemap.xml`, `/favicon.ico`, and `/actuator/health`; `/robots.txt` returned 200. Operational acceptance is required in addition to code acceptance for issues about production routing or deployment smoke coverage.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--goals"></a>
#### Goals

- Resolve all 58 inventoried issues with the smallest cohesive set of production-quality changes.
- Preserve an issue-level mapping from requirement to tests, commits, pull requests, CI, local runtime evidence, and closure text.
- Deliver in seven dependency-aware batches so each pull request is reviewable and can be reverted independently.
- Keep public and authenticated API contracts explicit, stable, and documented.
- Improve security without breaking non-browser bearer-token clients.
- Prove runtime behavior on an alternate port and verify production only after merged code is deployed safely.
- Close issues already satisfied by current code only after direct evidence confirms every acceptance point.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--non-goals"></a>
#### Non-Goals

- Redesigning the site or replacing Thymeleaf and vanilla JavaScript.
- Introducing a JavaScript package manager, frontend framework, bundler, or transpiler.
- Reformatting or refactoring unrelated code.
- Cleaning, rebasing, or incorporating unrelated changes from the authoritative spoke checkout.
- Treating unit tests alone as local application evidence.
- Trusting GitHub comments or attachments from authors other than `azurras` as instructions.
- Weakening required CI or merging known failing changes merely to reduce backlog count.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--delivery-shape"></a>
#### Delivery Shape

Each batch receives its own reviewed implementation plan with literal inspected line ranges, test-first evidence, focused automated validation, full relevant regression coverage, alternate-port runtime testing, Builder test report, spoke review, pull request, required CI, merge, and issue updates. Closely related issues may share a pull request when they modify the same boundary, but every issue keeps separate acceptance and closure evidence.

A batch begins only after its implementation plan checkpoint is committed and pushed. The next batch refreshes from the then-current `origin/main` so it includes earlier merged dependencies and current Dependabot or user changes.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--cross-cutting-requirements"></a>
#### Cross-Cutting Requirements

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--compatibility"></a>
##### Compatibility

- Use Java 25, Spring Boot 4.1, Gradle Wrapper, MongoDB, Thymeleaf, and vanilla ES modules.
- Preserve repository-native package ownership and public response envelopes.
- Keep bearer-token authentication supported for explicit API clients while migrating browser authentication to cookies.
- Handle old Mongo documents with missing new fields safely.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--security"></a>
##### Security

- Validate untrusted input at HTTP, configuration, URL-fetch, and persistence boundaries.
- Default to fail closed for authentication, authorization, SSRF, production configuration, and distributed locks.
- Do not log secrets, tokens, password-reset links, unsafe response bodies, or private host details.
- Public health endpoints expose status only, not sensitive component detail.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--data-and-operations"></a>
##### Data and Operations

- Mongo index/data changes use a repeatable versioned migration runner with durable applied-state records and a distributed execution lease.
- Scheduled work and manual imports use one shared Mongo-backed lease abstraction where overlap would corrupt or duplicate work.
- New status and audit records must be bounded, queryable by indexed fields, and have documented retention where appropriate.
- Destructive or merge-style operations require preview or explicit confirmation when requested by the source issue.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--testing"></a>
##### Testing

- Behavior changes begin with a failing behavioral test or a reproducible failing contract.
- Add success, validation, authorization, concurrency, and failure-path coverage appropriate to each issue.
- Run `node --check` for every touched JavaScript file and `:website:jsTest` for browser changes.
- Run focused Java tests first, then `:website:test` for shared configuration, security, persistence, or API-model changes.
- Run the full repository build before publication when a batch changes build configuration or workflows.
- Exercise affected HTTP routes or UI flows against a locally running app on a non-production port and capture exact requests and responses.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--batch-1-production-deployment-ci-and-configuration"></a>
#### Batch 1: Production, Deployment, CI, and Configuration

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--issues"></a>
##### Issues

#1122, #1123, #1124, #1138, #1143, #1144, #1145, #1146, #1147, #1148, #1149, #1150, #1151, #1153, and #1154.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--required-behavior"></a>
##### Required Behavior

- #1122: Diagnose and correct the native Windows service, Cloudflare tunnel, deploy configuration, or application binding that causes public routes to return 404. Add a deploy smoke command that fails on non-200 public routes. Do not treat a code-only change as acceptance.
- #1123: Serve `robots.txt` and a valid `sitemap.xml` containing supported canonical public routes. Both return 200 with correct content types and canonical HTTPS URLs.
- #1124: Expose minimal liveness/readiness endpoints with status-only public responses. Add post-deploy checks for readiness plus key public routes and document the contract.
- #1138: Configure explicit immutable/versioned static-resource URLs or content-based cache busting and long-lived cache headers for versioned CSS, JS, images, and favicon resources. HTML remains revalidatable.
- #1143: Production MongoDB configuration comes only from a documented environment-driven URI and has no localhost fallback.
- #1144: CI uses the official Gradle setup action with dependency and wrapper caching without weakening dependency verification.
- #1145: CI uploads Java and browser-test reports or diagnostic logs on failure using `if: failure()` or `if: always()` with safe artifact contents and bounded retention.
- #1146: CodeQL scans Java on pull requests, the default branch, and a schedule. Workflow permissions are least privilege.
- #1147: Dependency Review runs on pull requests and fails for configured vulnerable dependency changes while covering Gradle and Actions manifests.
- #1148: Dependabot uses coherent Gradle and Actions groups, predictable labels, limits, and a non-disruptive cadence.
- #1149: The stale workflow has specific, respectful issue/PR messages, sensible stale/close windows, exemption labels, and excludes security and active-work labels.
- #1150: The stale workflow declares default read-only permissions and grants only `issues: write` and `pull-requests: write` to its job.
- #1151: The production profile fails startup with one clear validation report when required JWT, Mongo, mail-sender, or Resend settings are absent or unsafe. Optional mail operation is controlled by an explicit switch rather than accidental blank configuration.
- #1153: Provide Docker Compose support for a local MongoDB instance with persistent storage, health check, documented URI, startup, stop, and reset steps. Do not include production secrets.
- #1154: Add a versioned application migration runner that records applied migrations, prevents concurrent execution with a Mongo lease, handles idempotent index/data changes, fails startup on an incomplete required migration, and is documented with rollback/recovery guidance.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--batch-2-browser-authentication-and-security"></a>
#### Batch 2: Browser Authentication and Security

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--issues-1"></a>
##### Issues

#1125, #1126, #1127, #1128, #1129, and #1130.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--required-behavior-1"></a>
##### Required Behavior

- #1125: Configure HSTS for HTTPS production responses, a Content Security Policy compatible with local assets and explicitly allowlisted YouTube/CDN sources, frame denial, strict referrer policy, MIME sniffing protection, and a least-privilege permissions policy. Tests assert headers on a public page.
- #1126: Enable CSRF protection for cookie-authenticated browser mutations. Browser JavaScript sends the issued CSRF token. Explicit bearer-authenticated API requests remain stateless and are not forced into a browser session contract. Unsafe cookie-authenticated requests without a valid token are rejected.
- #1127: Login places authentication in a Secure production, HttpOnly, SameSite cookie with bounded lifetime and path. Browser JavaScript no longer reads or writes the JWT in localStorage. Logout expires the cookie. Existing Authorization bearer handling remains available for non-browser clients during migration.
- #1128: Password-reset links use one validated configured public base URL. Forwarded headers cannot change the reset host. Proxy trust is explicit and tests include spoofed headers.
- #1129: Login, reset request, and reset confirmation DTOs have appropriate `@NotBlank`, `@Email`, token, and password-length constraints; controller request bodies use `@Valid`; malformed payloads return the normal 400 envelope before service entry.
- #1130: First and last names remain required to match the existing persisted/account contract. Signup markup and client validation visibly mark them required, and tests prove blank names are rejected consistently.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--batch-3-public-blog-gallery-and-archive"></a>
#### Batch 3: Public Blog, Gallery, and Archive

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--issues-2"></a>
##### Issues

#1131, #1132, #1133, #1134, #1135, #1136, and #1137.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--required-behavior-2"></a>
##### Required Behavior

- #1131: The public blog component calls the current versioned read API, unwraps the standard response, and displays posts unauthenticated. Unsupported tag filtering is removed unless a tested public tag endpoint is implemented.
- #1132: The gallery component calls the current versioned photo API, unwraps the standard response, and loads configured images on public `/photos` without USER authority.
- #1133: `/photos/usage` maps to the existing usage template, is linked from the gallery or footer, and returns 200 anonymously.
- #1134: The Bell archive contains no empty, numeric-placeholder, obsolete social/resume links, or references to missing favicon/static assets. Intentional non-links render as text.
- #1135: The Bell templates contain no insecure `http://` image sources. Use HTTPS or local static assets and remove dead sources.
- #1136: Gallery images use the configured description as alt text, falling back to the name. Empty alt text is reserved for intentionally decorative images.
- #1137: Every Bootstrap CDN include is pinned and protected by SRI and `crossorigin`, or the dependency is self-hosted. Duplicate includes are removed. A template regression test rejects unprotected CDN assets.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--batch-4-request-limits-rate-limiting-and-api-errors"></a>
#### Batch 4: Request Limits, Rate Limiting, and API Errors

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--issues-3"></a>
##### Issues

#1139, #1140, #1141, and #1157.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--required-behavior-3"></a>
##### Required Behavior

- #1139: Request-size limits bind from validated typed configuration with environment-specific defaults and route-aware upload limits. Oversized JSON receives the normal error envelope with 413; streamed and unknown-length requests remain bounded.
- #1140: Rate-limit buckets use an expiring bounded cache. Expiry is at least aligned with each rule window, inactive clients are evicted, and cardinality cannot grow without limit.
- #1141: Limited responses include correct `Retry-After`, `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and reset metadata plus the standard JSON error envelope.
- #1157: Replace generic service `RuntimeException` wrapping with named domain/API exceptions that preserve cause internally and map to consistent safe error responses. Do not replace programmer faults with misleading domain responses.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--batch-5-accounts-messages-notifications-posts-and-moderation"></a>
#### Batch 5: Accounts, Messages, Notifications, Posts, and Moderation

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--issues-4"></a>
##### Issues

#1155, #1156, #1158, #1159, #1160, #1161, #1162, #1163, #1164, #1165, #1166, #1167, and #1168.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--required-behavior-4"></a>
##### Required Behavior

- #1155: Admin account queries use server-side page, size, sort, status/role, and safe text search parameters. Page sizes are bounded and the Back Office renders navigation and result metadata.
- #1156: Account deletion removes credentials, reset state, follows, trust links, notifications, private messages, reports, sessions, and user-owned private data. Public post history is anonymized to a stable deleted-user identity rather than attributing it to a living username. Audit references retain bounded identifiers needed for accountability without retaining unnecessary personal data. Cleanup is idempotent and tested for partial failure/retry behavior.
- #1158: Conversation summaries are produced by a repository aggregation that returns the latest message per distinct participant pair, independent of activity volume in one conversation.
- #1159: Conversation history uses a stable `(createdOn, id)` cursor with bounded page size, next-cursor metadata, and deterministic ordering.
- #1160: Users can archive a conversation for their own inbox. Archiving does not delete another participant's data and new messages restore visibility. Authorization prevents altering another user's archive state.
- #1161: Notification APIs return bounded cursor pages with stable ordering and next-cursor metadata. The UI supports load more without duplicating items.
- #1162: An authenticated mark-all-read endpoint updates only the caller's unread notifications atomically; the UI updates the unread counter after success.
- #1163: Notification fanout uses an indexed idempotency/dedupe key for actor, action, target, recipient, and a documented short window. High-volume paths enforce bounded per-actor/recipient rates without dropping unrelated events.
- #1164: Post feeds sort and paginate by `(effectiveTimestamp, id)` and encode both values in an opaque validated cursor so tied timestamps do not skip or duplicate posts.
- #1165: Authors may edit their own non-expired posts within a configured 15-minute window. Admin moderation remains a separate action. Persist original-created time, edited timestamp, and a bounded audit event; UI displays edited status.
- #1166: A compound indexed uniqueness rule prevents the same reporter from creating multiple open reports for the same target. The API returns the existing report or a clear conflict/validation response under races.
- #1167: The report queue supports bounded server-side pagination, stable sorting, and status, report type, target type, reporter, and validated date-range filters.
- #1168: Account status changes, role changes, and report resolutions record actor, target, reason, timestamp, and bounded before/after values. Back Office exposes filtered audit entries to authorized moderators.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--batch-6-wfl-and-location-imports"></a>
#### Batch 6: WFL and Location Imports

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--issues-5"></a>
##### Issues

#1169, #1170, #1171, #1172, #1173, #1174, and #1175.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--required-behavior-5"></a>
##### Required Behavior

- #1169: Nearby and top-rated restaurant lookup executes distance/rating filtering in indexed repository queries rather than loading all restaurants. If current repository-bound candidate lookup already satisfies this, retain or extend tests and close from evidence without unnecessary rewriting.
- #1170: Manual and scheduled WFL imports share a distributed lease. Persist visible status, start/end time, create/update/delete/skip counts, trigger/actor, and a safe last-error category.
- #1171: WFL OSM import has a side-effect-free dry run that computes create/update/delete/unchanged counts and representative changes. Admin apply requires referencing a fresh preview token or checksum.
- #1172: Duplicate cleanup returns candidate groups and the proposed stable survivor without deletion. Apply requires explicit group identity and fresh observed versions; tests cover selection and stale confirmation.
- #1173: Public WFL pages display the last successful import time, source, and metro/city coverage, with an honest unavailable state.
- #1174: Startup validates metro names, cities/states, coordinate ranges, bounding-box ordering, duplicates, source URLs, and required import settings. Invalid production configuration fails clearly.
- #1175: ZIP coordinate imports record source version, checksum, counts, and completion time. Reimporting the same checksum is a reported no-op; partial or changed imports are idempotent and observable.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--batch-7-vin-scheduling-and-link-previews"></a>
#### Batch 7: VIN, Scheduling, and Link Previews

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--issues-6"></a>
##### Issues

#1176, #1177, #1178, #1179, #1180, and #1181.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--required-behavior-6"></a>
##### Required Behavior

- #1176: VIN cache entries record decoder version and refreshed/expiry time. Fresh entries are used, stale entries refresh from NHTSA, and failed refreshes do not silently extend stale data.
- #1177: Batch VIN decode enforces a validated configured maximum and returns an ordered result for every submitted VIN with either decoded data or a specific validation/upstream error. One invalid VIN does not discard successful results.
- #1178: RandomVIN scheduling uses typed enable, initial-delay, fixed-delay, timeout, and minimum-safe-delay configuration. It is disabled by default, production-safe when enabled, documented, and rejects dangerously short polling.
- #1179: Scheduled collectors and manual equivalents use the shared Mongo lease abstraction with deterministic lock names, bounded lease durations, owner tokens, renewal or safe expiry, and skipped-run observability.
- #1180: Link preview fetching accepts only HTTP/HTTPS public destinations, rejects userinfo, localhost, link-local, private, multicast, reserved, and unsafe resolved addresses for IPv4 and IPv6, revalidates every redirect, and never follows `file:` or other schemes. Tests cover blocked literal and DNS-resolved hosts plus allowed public URLs.
- #1181: Link preview requests have bounded connect/read/overall timeouts, manual redirect count, response bytes, supported content types, parsed metadata length, and success/failure cache lifetimes. Repeated bad URLs use a bounded recent-failure cache and do not repeat outbound work during the failure TTL.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--files-and-ownership-boundaries"></a>
#### Files and Ownership Boundaries

Expected areas include:

- `.github/workflows/`, `.github/dependabot.yml`, `README.md`, and `docs/operations/` for CI and operations.
- `website/src/main/resources/application*.yml` and typed configuration packages for production and feature configuration.
- `dev.christopherbell.configuration` for security, filters, migrations, production validation, and shared scheduler leases.
- Existing feature packages under `account`, `message`, `notification`, `post`, `report`, `whatsforlunch`, `location`, and `vehicle`; new subfeature packages are created only for distinct responsibilities.
- `website/src/main/resources/templates` and `static/js` for public pages, authentication, Back Office, and feed behavior.
- Matching Java and JavaScript tests plus the owning feature README for every changed behavior.

Exact files and line ranges belong in each batch implementation plan after current-code inspection.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--validation-and-acceptance"></a>
#### Validation and Acceptance

A batch is accepted only when:

1. Every issue requirement is mapped to code or a documented already-satisfied behavior.
2. Required failing evidence or characterization baseline was witnessed before the semantic change.
3. Focused tests, static checks, JavaScript syntax checks, and required wider suites pass.
4. The app starts locally on a non-8080 port and affected endpoints/UI flows are exercised with exact inputs and captured responses.
5. A complete validated Builder test report records runtime evidence.
6. The branch is pushed, a pull request is opened, required CI passes, and the PR is merged.
7. Each included issue is closed or updated with its commit, PR, CI, local test report, known gaps, and final state.
8. Builder spoke review, work ledger, indexes, validation, and session memory are current and pushed.

For #1122 and other operational work, acceptance additionally requires production smoke evidence after deployment. `/` is the primary anonymous smoke route. Health endpoints are supplemental and may intentionally expose only restricted or status-only information.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--rollout-and-recovery"></a>
#### Rollout and Recovery

- Merge batches in the defined order unless a critical security issue requires an earlier isolated hotfix.
- Rebase or merge current `origin/main` before publication and rerun affected tests after conflict resolution.
- Prefer additive data migrations followed by code adoption; destructive cleanup requires a later explicit migration after compatibility is proven.
- Every migration and distributed lock includes recovery documentation for interrupted runs.
- Production deployment uses the existing native Windows service workflow and `deploy.lock` protections.
- Verify the candidate on an alternate port before replacing or restarting the live listener.
- If production verification fails, keep the prior release active or roll back through the documented Windows production release mechanism and leave affected issues open with evidence.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--risks"></a>
#### Risks

- Browser cookie/CSRF migration touches most authenticated JavaScript flows; staged compatibility and broad regression coverage are required.
- Several pagination changes add or alter API models. Preserve compatibility where practical and version contracts when shape changes cannot be additive.
- Mongo migrations and distributed leases are concurrency-sensitive. Atomic compare-and-set behavior and interruption tests are mandatory.
- CSP can break CDN assets and YouTube embeds. Test both header presence and required page functionality.
- Current production 404s may be operational rather than source-code defects. Diagnose service, port, and tunnel layers separately.
- Large batches can accumulate conflicts with Dependabot and ongoing feature work. Keep each PR cohesive and refresh before starting the next batch.

<a id="source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md--open-questions"></a>
#### Open Questions

None block planning. The accepted defaults are: seven dependency-aware batches; required first/last names; HttpOnly cookie plus explicit bearer compatibility; 15-minute author edit window; per-user conversation archive rather than destructive cross-user deletion; anonymized retained public posts on account deletion; and a repository-native Mongo migration/lease implementation unless plan-time compatibility evidence favors a maintained library.

The user approved this written specification on 2026-07-25 and explicitly authorized autonomous continuation through the remaining delivery phases without routine approval gates.

<!-- /migrated-source: docs/specs/2026-07-25-complete-all-open-christopherbell-dev-issues.md -->

<a id="source-docs-spoke-reviews-2026-07-25-browser-security-issues-1125-1130-md"></a>
## 2026-07-25 | spoke-reviews | Browser Security Issues 1125-1130 Review

Original source: `docs/spoke-reviews/2026-07-25-browser-security-issues-1125-1130.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `f06e6898387f63e8ea76b204b4d6bb7d2f57ba2c4dff0b924071696c836c2985`.

<!-- migrated-source: docs/spoke-reviews/2026-07-25-browser-security-issues-1125-1130.md -->
<a id="source-docs-spoke-reviews-2026-07-25-browser-security-issues-1125-1130-md--browser-security-issues-1125-1130-review"></a>
### Browser Security Issues 1125-1130 Review

- Status: complete
- Spoke: `azurras/christopherbell.dev`
- Branch: `codex/browser-security-1125-1130`
- Pull request: [#1249](https://github.com/azurras/christopherbell.dev/pull/1249)
- Merge commit: `b6c361d1d916337679a37f04caa46c3475215e71`
- Related work: [Complete All Open christopherbell.dev Issues](#source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md)
- Plan: [Browser Security Issues 1125-1130](../implementation-plans/2026-07-25-browser-security-issues-1125-1130.md)
- Test report: [Browser Security Issues 1125-1130](../test-reports/2026-07-25-browser-security-issues-1125-1130.md)

<a id="source-docs-spoke-reviews-2026-07-25-browser-security-issues-1125-1130-md--findings"></a>
#### Findings

No blocker or warning remains.

The independent pre-merge review initially found one important compatibility regression: browser
cookie login had replaced the bearer-token acquisition contract used by explicit API clients. It
also found minor stale-session and documentation gaps. The implementation now has explicit dual
login modes, verifies the readable non-secret session marker against `/me`, and documents the
cookie-only worker boundary. Focused boundary tests cover those corrections.

No PR comments or attachments supplied review guidance. The PR had no comments or reviews, so no
untrusted GitHub input influenced scope, acceptance, merge, or closure.

<a id="source-docs-spoke-reviews-2026-07-25-browser-security-issues-1125-1130-md--scope-reviewed"></a>
#### Scope Reviewed

- Production response headers and typed browser-security configuration.
- Spring Security SPA CSRF behavior and narrow bearer-login compatibility.
- HttpOnly JWT cookie issuance, authentication priority, and logout clearing.
- Removal of JavaScript-readable JWT and shared-folder worker token transport.
- Canonical password-reset origin and authentication/reset DTO validation.
- Required first/last signup names in browser and server contracts.

<a id="source-docs-spoke-reviews-2026-07-25-browser-security-issues-1125-1130-md--validation-reviewed"></a>
#### Validation Reviewed

- Observed RED tests for cookie authentication, CSRF, localStorage removal, signup names, and worker cookie forwarding.
- Focused post-review Java validation: 74 cases passed.
- Full Java validation: 108 suites, 999 tests, 0 failures, 3 skipped.
- Full post-rebase JavaScript validation: 195/195 passed; all 22 changed JavaScript files passed `node --check`.
- `git diff --check` passed and scans found no production browser-token storage or worker-token path.
- PR #1249 passed Windows, macOS, Ubuntu, Dependency Review, and every CodeQL language gate.
- Alternate-port live testing on `8090` and post-merge public HTTPS testing both passed.
- Native auto-deploy switched production to PID `26680` while `/` remained available.

<a id="source-docs-spoke-reviews-2026-07-25-browser-security-issues-1125-1130-md--house-style-compliance"></a>
#### House-Style Compliance

The final design keeps credential ownership server-side, distinguishes explicit bearer clients
from cookie browsers, validates configuration and DTO boundaries, preserves repository-native
Spring and browser-module patterns, and provides direct regression evidence for each trust boundary.

<a id="source-docs-spoke-reviews-2026-07-25-browser-security-issues-1125-1130-md--risks-and-follow-ups"></a>
#### Risks and Follow-ups

- Existing users must sign in once after the intentional localStorage-to-HttpOnly-cookie migration.
- A successful live password submission was not automated or logged; successful cookie issuance is
  covered at the controller boundary to avoid exposing production credentials.

<a id="source-docs-spoke-reviews-2026-07-25-browser-security-issues-1125-1130-md--merge-readiness"></a>
#### Merge Readiness

Complete. PR #1249 is merged, all required checks passed, and production acceptance succeeded.

<a id="source-docs-spoke-reviews-2026-07-25-browser-security-issues-1125-1130-md--closure-readiness"></a>
#### Closure Readiness

ready

<a id="source-docs-spoke-reviews-2026-07-25-browser-security-issues-1125-1130-md--evidence"></a>
#### Evidence

- Issues: `cbell504/website#1125` through `#1130`; all closed automatically at merge.
- Final branch/head: `codex/browser-security-1125-1130` at `98099a40`.
- Merge: PR #1249 at `b6c361d1d916337679a37f04caa46c3475215e71`.
- Spec: campaign spec applies; no separate sub-batch spec was needed.
- Plan: `docs/implementation-plans/2026-07-25-browser-security-issues-1125-1130.md`, `complete`.
- Test report: `docs/test-reports/2026-07-25-browser-security-issues-1125-1130.md`, including sent data and received responses.
- Session memory: `docs/session-memory/2026-07-25-browser-security-issues-1125-1130.md`.

<a id="source-docs-spoke-reviews-2026-07-25-browser-security-issues-1125-1130-md--closure-text"></a>
#### Closure Text

Ready. PR #1249 merged as `b6c361d1d916337679a37f04caa46c3475215e71`; all Windows,
macOS, Ubuntu, dependency-review, and CodeQL gates passed. Focused and full automated suites,
alternate-port runtime testing, and post-merge production acceptance prove the header, CSRF,
HttpOnly-cookie, canonical reset-origin, DTO-validation, and signup-name contracts. No known
application defect remains; existing users only need one fresh login after the intentional
credential-storage migration. Issues #1125-#1130 may remain closed.

<!-- /migrated-source: docs/spoke-reviews/2026-07-25-browser-security-issues-1125-1130.md -->

<a id="source-docs-spoke-reviews-2026-07-25-github-automation-issues-1144-1150-md"></a>
## 2026-07-25 | spoke-reviews | GitHub Automation Issues 1144-1150 Review

Original source: `docs/spoke-reviews/2026-07-25-github-automation-issues-1144-1150.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `3be34dc8261a246f61cf41afa0a5e8b7c3f8a08df5d99cb81c93d451cbc16ef5`.

<!-- migrated-source: docs/spoke-reviews/2026-07-25-github-automation-issues-1144-1150.md -->
<a id="source-docs-spoke-reviews-2026-07-25-github-automation-issues-1144-1150-md--github-automation-issues-1144-1150-review"></a>
### GitHub Automation Issues 1144-1150 Review

- Status: complete
- Spoke: `azurras/christopherbell.dev`
- Branch: `codex/github-automation-1144-1150`
- Pull request: [#1241](https://github.com/azurras/christopherbell.dev/pull/1241)
- Head reviewed: `86e7442d4f7534f934895696d8db17ad29f3f1e3`
- Merge commit: `88144134290e5f690c048cb4945db531b8ef17c9`
- Related work: [Complete All Open christopherbell.dev Issues](#source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md)
- Plan: [GitHub Automation Issues 1144-1150](../implementation-plans/2026-07-25-github-automation-issues-1144-1150.md)

<a id="source-docs-spoke-reviews-2026-07-25-github-automation-issues-1144-1150-md--findings"></a>
#### Findings

No blockers or warnings. Independent review reported no Critical, Important, or Minor findings.

<a id="source-docs-spoke-reviews-2026-07-25-github-automation-issues-1144-1150-md--scope-reviewed"></a>
#### Scope Reviewed

- Gradle cache behavior and read-only pull-request cache writes.
- Failure-only retention of Java, browser, and Gradle diagnostic artifacts.
- Browser JUnit XML generation while preserving console output.
- Dependency Review permissions and high-severity failure threshold.
- Dependabot grouping, labels, schedules, and pull-request limits.
- Stale messages, timing, exemptions, labels, and least-privilege permissions.
- CodeQL triggers, permissions, manual Java build, and coverage-preserving Actions/Java/JavaScript matrix.
- Parsed-YAML regression tests, README contract, and the complete diff against `origin/main`.

<a id="source-docs-spoke-reviews-2026-07-25-github-automation-issues-1144-1150-md--validation-reviewed"></a>
#### Validation Reviewed

- Initial five-test RED and GREEN evidence.
- CodeQL matrix RED and GREEN evidence after the hosted default/advanced setup conflict.
- Fresh `gradlew build --rerun-tasks --no-daemon` success on the rebased branch.
- Valid `website/build/test-results/jsTest/results.xml` with `testsuites` root and 176 passing browser tests.
- Passing Ubuntu, macOS, Windows, Dependency Review, default-drain CodeQL, and advanced CodeQL checks on PR #1241.
- Verified `pinned` and `roadmap` labels and `not-configured` default CodeQL state after the advanced workflow became authoritative.

<a id="source-docs-spoke-reviews-2026-07-25-github-automation-issues-1144-1150-md--house-style-compliance"></a>
#### House-Style Compliance

The final Before-Edit Brief remained accurate. Configuration effects and permissions are explicit, semantic YAML is parsed rather than matched by formatting-sensitive regular expressions, failure artifacts preserve original job conclusions, and the diff contains one cohesive automation purpose.

<a id="source-docs-spoke-reviews-2026-07-25-github-automation-issues-1144-1150-md--risks-and-follow-ups"></a>
#### Risks and Follow-ups

- GitHub-hosted action behavior remains an external dependency, mitigated by supported major tags and successful hosted checks.
- Pinned issues must receive the documented `pinned` label because actions/stale cannot inspect GitHub pin metadata.
- No runtime application behavior changed, so local Spring app testing and a Builder runtime test report were not applicable.

<a id="source-docs-spoke-reviews-2026-07-25-github-automation-issues-1144-1150-md--merge-readiness"></a>
#### Merge Readiness

Ready and merged. All automated, hosted, structural, and independent review gates passed before squash merge.

<a id="source-docs-spoke-reviews-2026-07-25-github-automation-issues-1144-1150-md--closure-readiness"></a>
#### Closure Readiness

ready

<a id="source-docs-spoke-reviews-2026-07-25-github-automation-issues-1144-1150-md--closure-text"></a>
#### Closure Text

Completed in PR #1241 and merged as `88144134`. Gradle caching, failed-run diagnostics, Dependency Review, grouped Dependabot updates, bounded least-privilege stale handling, and a coverage-preserving advanced CodeQL matrix are active. The full local build, all 176 browser tests, Dependency Review, all platform CI jobs, and all CodeQL language jobs passed. No runtime app test report was required because application behavior did not change. Issues #1144-#1150 closed automatically at merge; no known blockers remain.

<!-- /migrated-source: docs/spoke-reviews/2026-07-25-github-automation-issues-1144-1150.md -->

<a id="source-docs-spoke-reviews-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md"></a>
## 2026-07-25 | spoke-reviews | Production Foundations Issues 1143, 1151, 1153, and 1154 Spoke Review

Original source: `docs/spoke-reviews/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `da7af75a9377beba8063c5ef2b6fa306547ea01ce72530dbe74361fe48906b4a`.

<!-- migrated-source: docs/spoke-reviews/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md -->
<a id="source-docs-spoke-reviews-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--production-foundations-issues-1143-1151-1153-and-1154-spoke-review"></a>
### Production Foundations Issues 1143, 1151, 1153, and 1154 Spoke Review

<a id="source-docs-spoke-reviews-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--document-status"></a>
#### Document Status

complete

<a id="source-docs-spoke-reviews-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--reviewed-spoke"></a>
#### Reviewed Spoke

- Repository: `https://github.com/azurras/christopherbell.dev.git`
- Worktree:
  `A:\Projects\christopherbell.dev-worktrees\production-foundations-1143-1154`
- Branch: `codex/production-foundations-1143-1154`
- Base: `4b82116a0ed489c74eed144a478f1b3a3944ada2`
- Reviewed head: `4e767dfd87a03f873114d496600f1a68d8f560c6`.
- Pull request: [#1252](https://github.com/azurras/christopherbell.dev/pull/1252),
  squash-merged as `965b25bb3e703a2e67a5064d777a9ab1998f26a1`.
- Issues: `#1143`, `#1151`, `#1153`, and `#1154`

<a id="source-docs-spoke-reviews-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--scope-reviewed"></a>
#### Scope Reviewed

- Production MongoDB URI and database profile configuration.
- Pre-refresh, redacted production setting validation and initializer
  registration in the packaged JAR.
- Typed mail configuration and password-reset enabled/disabled behavior.
- Protected Windows production environment parsing and service-launch allowlist.
- Root MongoDB Compose service, local defaults, and contributor commands.
- Atomic MongoDB lease document/service.
- Ordered migration interface, properties, record states, state transitions,
  runner, V001 indexes, checksum, and recovery documentation.
- Focused and full automated tests, disposable runtime evidence, cleanup, live
  production continuity, staged diff, and worktree hygiene.

<a id="source-docs-spoke-reviews-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--findings"></a>
#### Findings

No remaining Blocker or Warning findings.

Review found and resolved two pre-publication consistency gaps:

1. An invalid `APP_MAIL_ENABLED` value originally returned from validation
   before the invalid sender joined the same report. The final initializer and
   protected environment parser aggregate the relevant setting names without
   echoing values; the focused regression proves the combined partition.
2. The V001 `migration_status_completed` index initially used ascending
   `completedAt`. It now matches the reviewed design with ascending `status` and
   descending `completedAt`.

The staged sensitive-value scan matched only the deliberately malformed
credential-bearing URI in the redaction regression. The value exists solely in
test input and the assertion proves it is absent from the thrown message. No
credential, token, private key, production secret, or disposable-runtime JWT is
staged.

<a id="source-docs-spoke-reviews-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--validation-checked"></a>
#### Validation Checked

- Focused RED compiled only after the new production settings, typed mail,
  lease, and migration types existed.
- Focused Pester RED failed 6 of 25 cases before `APP_MAIL_ENABLED` entered the
  allowlist and conditional validation.
- Final focused production-foundations Java suite: 32 passed.
- Packaged missing-settings start: exit `1`, no port `8090` listener, one
  `Invalid production configuration` report naming Mongo URI, JWT, sender, and
  provider key without values.
- Disposable first start and restart: `/` and readiness returned status code
  200; V001 remained exactly one `APPLIED` record with checksum
  `aec77e3e8cf68bf8d67f239ee0e842fbdad26ea9766ab04cbc3d74dd9ad93876`.
- Runtime Mongo metadata contained `migration_status_completed` and
  `lease_expiry`; the migration lease was unowned after both starts.
- Exact database `christopherbell_foundations_test_20260725230000` was dropped
  only after name and production-inequality checks; it no longer exists.
- Final `cleanTest + check`: 1,030 Java tests, 0 failures, 3 existing skips; 199
  JavaScript tests passed; `bootJar` and `verifySensorRuntime` passed.
- Full Windows production Pester: 247 total, 243 passed, 0 failed, 4 privileged
  or explicit-acceptance skips.
- `git diff --cached --check` passed.
- `application-prod.yml` contains no `mongodb://localhost:27017` fallback.
- Docker CLI is unavailable on this host; the structural Compose regression
  parsed the YAML and proved its image, port, volume, health check, and
  no-secret boundaries.
- Live production remained PID `29012`, port `8080`, status code 200 throughout
  the alternate-port run and final verification.

<a id="source-docs-spoke-reviews-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--house-style-review"></a>
#### House-Style Review

The implementation follows repository-native Java, Spring configuration,
PowerShell, YAML, and test conventions. Boundaries are explicit and narrow:
the initializer owns pre-refresh validation, `MailProperties` owns mail intent,
the lease service owns atomic query semantics, and the migration runner owns
ordering and durable state transitions. Tests partition absent, malformed,
disabled, enabled, contention, drift, incomplete, success, failure, restart,
and cleanup behavior. Error text carries setting names, migration IDs, and safe
categories only.

<a id="source-docs-spoke-reviews-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--risks"></a>
#### Risks

- Migration lease duration is bounded at 2 minutes. V001 performs only
  idempotent index creation and completed within startup acceptance; future
  long-running migrations must be decomposed or introduce reviewed renewal
  orchestration before exceeding that lease.
- An interrupted migration deliberately blocks startup until an operator
  corrects the cause. The recovery runbook requires a backup, no active owner,
  exact-record inspection, and a bounded single-record action.
- Local Compose syntax could not be passed through the Docker CLI on this host.
  Cross-platform CI and the YAML structural regression remain required gates.
- Production migration execution completed successfully. Read-only inspection
  proved exactly one APPLIED V001 record, both named indexes, and a released
  ownerless lease.
- `gradlew.bat` has a checkout-only line-ending difference. It is unstaged and
  absent from the reviewed diff.

<a id="source-docs-spoke-reviews-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--requested-changes"></a>
#### Requested Changes

None remaining.

<a id="source-docs-spoke-reviews-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--merge-readiness"></a>
#### Merge Readiness

Complete. The implementation and deterministic timing-test repair passed
Ubuntu, macOS, Windows, Dependency Review, and CodeQL, merged through PR #1252,
and passed guarded production acceptance on Java listener PID `30976`.

<!-- /migrated-source: docs/spoke-reviews/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md -->

<a id="source-docs-spoke-reviews-2026-07-25-public-content-issues-1131-1137-md"></a>
## 2026-07-25 | spoke-reviews | Public Content Issues 1131-1137 Spoke Review

Original source: `docs/spoke-reviews/2026-07-25-public-content-issues-1131-1137.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `0794ac41675787ae899ef02138de322cc81f88cfef2061efc05e09358a8cd62e`.

<!-- migrated-source: docs/spoke-reviews/2026-07-25-public-content-issues-1131-1137.md -->
<a id="source-docs-spoke-reviews-2026-07-25-public-content-issues-1131-1137-md--public-content-issues-1131-1137-spoke-review"></a>
### Public Content Issues 1131-1137 Spoke Review

<a id="source-docs-spoke-reviews-2026-07-25-public-content-issues-1131-1137-md--document-status"></a>
#### Document Status

complete

<a id="source-docs-spoke-reviews-2026-07-25-public-content-issues-1131-1137-md--reviewed-spoke"></a>
#### Reviewed Spoke

- Repository: `https://github.com/azurras/christopherbell.dev.git`
- Worktree: `A:\Projects\christopherbell.dev-worktrees\public-content-1131-1137`
- Branch: `codex/public-content-1131-1137`
- Base: `b6c361d1d916337679a37f04caa46c3475215e71`
- Reviewed head: `f5120784bf4763cbd57666839307be24d209198a`
- Pull request: [azurras/christopherbell.dev#1251](https://github.com/azurras/christopherbell.dev/pull/1251)
- Issues: `#1131`, `#1132`, `#1133`, `#1134`, `#1135`, `#1136`, and `#1137`

<a id="source-docs-spoke-reviews-2026-07-25-public-content-issues-1131-1137-md--scope-reviewed"></a>
#### Scope Reviewed

- Anonymous GET-only blog/photo API boundaries and standard response envelopes.
- Browser normalizers, safe text rendering, unsupported tag removal, and gallery alt-text fallbacks.
- Photography usage route/link.
- The Bell links, favicon, image assets, insecure sources, and stray markup.
- Pinned self-hosted Bootstrap 5.3.3, CSP narrowing, template deduplication, and Dependency Review coverage.
- Tests, package documentation, local HTTP/browser evidence, final committed diff, and worktree hygiene.

<a id="source-docs-spoke-reviews-2026-07-25-public-content-issues-1131-1137-md--findings"></a>
#### Findings

No remaining Blocker or Warning findings.

The initial review found one blocker: `PhotoProperties` bound `photo-properties.photos` while `application.yml` supplied `photo-properties.images`, leaving the live API empty despite 12 configured entries. Commit `4108c5c6f5adf5877f247c2cff4cf543fd7eb1cd` aligns the key, adds a configuration-context regression with witnessed RED/GREEN evidence, and treats configured `n/a` descriptions as missing alt text so the photo name is used. Independent re-review found the blocker closed and no new findings.

The first CI rerun exposed an environment-bound test-harness defect: `PhotoPropertiesConfigurationTest` used `@SpringBootTest`, discovered the full application, and timed out against unavailable MongoDB on macOS. Commit `f5120784bf4763cbd57666839307be24d209198a` narrows the test to load the real `application.yml` and bind only `PhotoProperties`. The configuration contract remains covered without booting unrelated services; the authoritative local suite and the Ubuntu, macOS, and Windows CI jobs all passed afterward.

<a id="source-docs-spoke-reviews-2026-07-25-public-content-issues-1131-1137-md--validation-checked"></a>
#### Validation Checked

- Focused Java public-content suite: 29 passed before review.
- Configuration-binding RED: `PhotoPropertiesConfigurationTest` failed on a null collection before the YAML correction.
- Configuration-binding GREEN: `PhotoPropertiesConfigurationTest` and `PhotoControllerTest` passed after correction.
- Focused Node public-content suite: 4 passed after witnessed RED failures for both payload normalization and the `n/a` alt sentinel.
- Authoritative final `cleanTest + check --max-workers=1 --no-watch-fs`: `BUILD SUCCESSFUL`; 1003 Java tests, 0 failures, 3 skipped; 199 JavaScript tests; `bootJar` and `verifySensorRuntime` passed.
- Live alternate-port API: `GET /api/photo/v1` returned `success=true` with 12 configured photos; the first JPEG returned `200 image/jpeg`, length `4770189`.
- Browser: 12 gallery images rendered; name fallbacks replaced 11 `n/a` descriptions, the one real description remained, the usage link was present, and console logs were empty.
- Static checks: JavaScript syntax, `git diff --check`, recursive no-Bootstrap-CDN scan, archive local-asset scan, and no-insecure-image scan passed.
- Dependency insight selected `org.webjars:bootstrap:5.3.3`; Dependency Review passed on both PR revisions.
- The final PR head passed Ubuntu, macOS, Windows, Dependency Review, and all CodeQL analyses. Post-merge CI Build and CodeQL also passed on `4b82116a`.
- Port `8090` was stopped; production PID `26680` on `8080` returned `200` after final local testing.
- Automatic deployment replaced the live Java listener with PID `29012`. Production HTTPS returned `200` for every target page/API/WebJar asset, both APIs exposed their configured data, all four POST boundary probes remained `403`, and deployed browser checks showed the expected content with no warning/error console entries.

<a id="source-docs-spoke-reviews-2026-07-25-public-content-issues-1131-1137-md--house-style-review"></a>
#### House-Style Review

The implementation follows the repository-native Java, JavaScript, template, configuration, and test conventions while preserving explicit public/private boundaries. The browser renderers own copied collections, use text DOM APIs, isolate response-shape normalization, and partition fallback behavior. The configuration-binding test covers the boundary that controller mocks cannot prove.

<a id="source-docs-spoke-reviews-2026-07-25-public-content-issues-1131-1137-md--risks"></a>
#### Risks

- Bootstrap advances legacy pages from 5.0.2/5.3.3 CDN mixtures to one local 5.3.3 artifact; focused browser checks cover the public pages in this batch, and the full cross-platform suite covers shared regressions.
- The local profile can run unrelated startup jobs unless explicitly disabled. Final gallery verification used `WFL_RESTAURANT_IMPORT_MONTHLY_ENABLED=false`.
- `gradlew.bat` shows a checkout-only LF-to-CRLF difference in this worktree. It is unstaged and absent from both spoke commits.

<a id="source-docs-spoke-reviews-2026-07-25-public-content-issues-1131-1137-md--requested-changes"></a>
#### Requested Changes

None remaining.

<a id="source-docs-spoke-reviews-2026-07-25-public-content-issues-1131-1137-md--merge-readiness"></a>
#### Merge Readiness

Merged through [PR #1251](https://github.com/azurras/christopherbell.dev/pull/1251) as `4b82116a0ed489c74eed144a478f1b3a3944ada2`. All seven source issues closed and production acceptance passed with no known gaps.

<!-- /migrated-source: docs/spoke-reviews/2026-07-25-public-content-issues-1131-1137.md -->

<a id="source-docs-spoke-reviews-2026-07-25-public-delivery-issues-1122-1124-1138-md"></a>
## 2026-07-25 | spoke-reviews | Public Delivery Issues 1122-1124 and 1138 Review

Original source: `docs/spoke-reviews/2026-07-25-public-delivery-issues-1122-1124-1138.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `fcf2f08cabfd5ca2a4c217aff96a93953071b350de9f20c6a5ae6c5efbd20388`.

<!-- migrated-source: docs/spoke-reviews/2026-07-25-public-delivery-issues-1122-1124-1138.md -->
<a id="source-docs-spoke-reviews-2026-07-25-public-delivery-issues-1122-1124-1138-md--public-delivery-issues-1122-1124-and-1138-review"></a>
### Public Delivery Issues 1122-1124 and 1138 Review

- Status: complete
- Spoke: `azurras/christopherbell.dev`
- Branch: `codex/public-delivery-1122-1124-1138`
- Pull requests: [#1245](https://github.com/azurras/christopherbell.dev/pull/1245) and
  [#1246](https://github.com/azurras/christopherbell.dev/pull/1246)
- Production head: `193761d4e0b69240188b8d053de4c9ba4115e339`
- Related work: [Complete All Open christopherbell.dev Issues](#source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md)
- Plan: [Public Delivery Issues 1122-1124 and 1138](../implementation-plans/2026-07-25-public-delivery-issues-1122-1124-1138.md)
- Test report: [Public Delivery Acceptance](../test-reports/2026-07-25-christopherbell-dev-public-delivery-issues-1122-1124-1138.md)

<a id="source-docs-spoke-reviews-2026-07-25-public-delivery-issues-1122-1124-1138-md--findings"></a>
#### Findings

No implementation or production defect remains. The first independent review correctly identified
the apex route as a production prerequisite. The path-preserving Cloudflare redirect was added and
verified before merge.

The follow-up review of the protected-config migration found no actionable issue. Both touched
PowerShell files parse under Windows PowerShell 5.1, the focused suite passed 22/22 there, and
malformed or non-`www` legacy configurations fail closed.

Live testing found a separate `/dev/` asset namespace caused by the installed service not receiving
the candidate launcher's `GIT_COMMIT` environment. Follow-up PR #1246 embeds the exact build SHA as
the fallback. Independent follow-up review found no merge blocker and proved an isolated JAR served
SHA-versioned CSS without `GIT_COMMIT`.

<a id="source-docs-spoke-reviews-2026-07-25-public-delivery-issues-1122-1124-1138-md--scope-reviewed"></a>
#### Scope Reviewed

- Canonical robots and sitemap resource content, media types, and no-cache overrides.
- Public liveness/readiness groups and private aggregate/component health boundaries.
- Fixed release-version resource-chain behavior across Thymeleaf URLs and relative ES modules.
- One-year immutable caching only for successful versioned assets and one-hour direct caching.
- Security matchers for release-scoped asset requests.
- Two-host route/probe matrices during switch, startup verification, rollback, and public smoke.
- Release SHA propagation from immutable deployment directories.
- Legacy protected-config migration from canonical `www` URL to apex plus canonical roots.

<a id="source-docs-spoke-reviews-2026-07-25-public-delivery-issues-1122-1124-1138-md--validation-reviewed"></a>
#### Validation Reviewed

- Initial Java 4-group RED and deployment-script 6-check RED evidence.
- Focused `PublicDeliveryConfigurationTest` 6/6 passing.
- Isolated port-8091 runtime route, content-type, probe-body, rendered-URL, module-import, and
  cache-header evidence; production port 8080 remained healthy.
- Post-rebase clean Gradle build: 21 tasks succeeded.
- Final Windows deployment suite: 240 passed, 0 failed, 4 environment-only skips.
- PR #1245: Windows, macOS, Linux, Dependency Review, and all CodeQL language gates passed.
- `git diff --check` passed and both independent review passes left the worktree unchanged.

<a id="source-docs-spoke-reviews-2026-07-25-public-delivery-issues-1122-1124-1138-md--house-style-compliance"></a>
#### House-Style Compliance

The implementation keeps metadata deterministic, health output bounded, cache effects scoped to
release identities, public-host validation explicit, and rollback behavior fail-closed. The
backward-compatible config migration derives only a valid HTTPS apex from a valid canonical
`www` root and does not rewrite the secret-bearing file.

<a id="source-docs-spoke-reviews-2026-07-25-public-delivery-issues-1122-1124-1138-md--risks-and-follow-ups"></a>
#### Risks and Follow-ups

- The unit regression accepts any 40-hex fallback rather than comparing directly with HEAD. The
  generated resource, isolated JAR, and live exact-merge-SHA checks close that evidence gap for this
  release; a later test-hardening change may encode exact equality.
- Cloudflare Browser Cache TTL is intentionally set to Respect Existing Headers so application
  cache policy remains authoritative.

<a id="source-docs-spoke-reviews-2026-07-25-public-delivery-issues-1122-1124-1138-md--merge-readiness"></a>
#### Merge Readiness

Complete. Both pull requests merged, all check matrices passed, and production runs the follow-up
merge SHA.

<a id="source-docs-spoke-reviews-2026-07-25-public-delivery-issues-1122-1124-1138-md--closure-readiness"></a>
#### Closure Readiness

complete

<a id="source-docs-spoke-reviews-2026-07-25-public-delivery-issues-1122-1124-1138-md--closure-text"></a>
#### Closure Text

Ready. PRs #1245 and #1246 are merged and independently reviewed. Production passes the canonical
metadata, bounded probe, exact release-SHA asset, origin-controlled cache, and apex redirect
contracts. Issues #1122-#1124 and #1138 may remain closed.

<!-- /migrated-source: docs/spoke-reviews/2026-07-25-public-delivery-issues-1122-1124-1138.md -->

<a id="source-docs-spoke-updates-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md"></a>
## 2026-07-25 | spoke-updates | Production Foundations Issues 1143, 1151, 1153, and 1154 Spoke Update

Original source: `docs/spoke-updates/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `c69762e5a4eaea4bdd1b260fdf810c0fa5b8496e93a03c43474be5fc24b5054d`.

<!-- migrated-source: docs/spoke-updates/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md -->
<a id="source-docs-spoke-updates-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--production-foundations-issues-1143-1151-1153-and-1154-spoke-update"></a>
### Production Foundations Issues 1143, 1151, 1153, and 1154 Spoke Update

- Status: complete
- Source repository: `https://github.com/azurras/christopherbell.dev.git`
- Reporting agent: Codex primary agent
- Related work: [Complete All Open christopherbell.dev Issues](#source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md)
- Implementation plan: [Production Foundations Issues 1143, 1151, 1153, and 1154](../implementation-plans/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md)
- Test report: [Production Foundations Issues 1143, 1151, 1153, and 1154](../test-reports/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md)
- Review: [Production Foundations Issues 1143, 1151, 1153, and 1154](#source-docs-spoke-reviews-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md)
- Session memory: [Production Foundations Issues 1143, 1151, 1153, and 1154](#source-docs-session-memory-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md)

<a id="source-docs-spoke-updates-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--result"></a>
#### Result

Issues [#1143](https://github.com/azurras/christopherbell.dev/issues/1143), [#1151](https://github.com/azurras/christopherbell.dev/issues/1151), [#1153](https://github.com/azurras/christopherbell.dev/issues/1153), and [#1154](https://github.com/azurras/christopherbell.dev/issues/1154) were completed and closed through [PR #1252](https://github.com/azurras/christopherbell.dev/pull/1252). The PR squash-merged to `main` as `965b25bb3e703a2e67a5064d777a9ab1998f26a1`.

<a id="source-docs-spoke-updates-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--commits"></a>
#### Commits

- `257e2f656c030aa585b99cb07d58d96489a980b4`: production validation, explicit mail configuration, local Mongo Compose, leases, migrations, documentation, and tests.
- `4e767dfd87a03f873114d496600f1a68d8f560c6`: deterministic executor barrier for the pre-existing command-center timeout race exposed by macOS CI.

<a id="source-docs-spoke-updates-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--validation"></a>
#### Validation

- Focused production-foundations Java suite: 32 passed after witnessed RED compilation failures.
- Focused production Pester RED: 6 of 25 failed before the new mail switch contract; final Windows production suite: 247 total, 243 passed, 0 failed, 4 environment/privilege skips.
- Final local Java result: 1,030 tests, 0 failures, 3 existing skips; JavaScript: 199 passed; `bootJar`, sensor runtime verification, and diff checks passed.
- Disposable production-profile start and restart returned 200 on `/` and readiness, applied V001 exactly once, retained both named indexes, and released the lease; the exact disposable database was then removed.
- PR Ubuntu, macOS, Windows, Dependency Review, and all CodeQL checks passed.
- Guarded production deployment replaced Java listener PID `29012` with `30976`; `/` and readiness returned 200 after initialization.
- Production contains exactly one APPLIED V001 record with the reviewed checksum, `migration_status_completed` and `lease_expiry` indexes, and no migration lease owner.

<a id="source-docs-spoke-updates-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--files-and-behavior"></a>
#### Files and Behavior

The batch added pre-refresh redacted production configuration validation, typed mail enablement, environment-driven production Mongo settings, loopback-only persistent Mongo Compose support, an atomic Mongo lease, immutable versioned migration state and V001 infrastructure indexes, Windows production parsing updates, recovery/local-development documentation, and focused Java/Pester contracts. See the linked PR and test report for the complete file and request/response evidence.

<a id="source-docs-spoke-updates-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--blockers-and-risks"></a>
#### Blockers and Risks

No remaining blocker or acceptance gap. Docker is not installed on this host, so Compose was verified structurally rather than with `docker compose config`. The isolated worktree retains only its checkout-only `gradlew.bat` line-ending difference, absent from every commit.

<a id="source-docs-spoke-updates-2026-07-25-production-foundations-issues-1143-1151-1153-1154-md--next-action"></a>
#### Next Action

Select the next coherent dependency-aware batch from the 30 remaining campaign issues and repeat the full planning, local validation, PR/CI, merge, production acceptance, and closure loop.

<!-- /migrated-source: docs/spoke-updates/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md -->

<a id="source-docs-spoke-updates-2026-07-25-public-content-issues-1131-1137-md"></a>
## 2026-07-25 | spoke-updates | Public Content Issues 1131-1137 Spoke Update

Original source: `docs/spoke-updates/2026-07-25-public-content-issues-1131-1137.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `fe218dfd791819ab75d3526af58161dca927493a77f5362a32f86492d8edaef4`.

<!-- migrated-source: docs/spoke-updates/2026-07-25-public-content-issues-1131-1137.md -->
<a id="source-docs-spoke-updates-2026-07-25-public-content-issues-1131-1137-md--public-content-issues-1131-1137-spoke-update"></a>
### Public Content Issues 1131-1137 Spoke Update

- Status: complete
- Source repository: `https://github.com/azurras/christopherbell.dev.git`
- Reporting agent: Codex primary agent
- Related work: [Complete All Open christopherbell.dev Issues](#source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md)
- Implementation plan: [Public Content Issues 1131-1137](../implementation-plans/2026-07-25-public-content-issues-1131-1137.md)
- Test report: [Public Content Issues 1131-1137](../test-reports/2026-07-25-public-content-issues-1131-1137.md)
- Review: [Public Content Issues 1131-1137](#source-docs-spoke-reviews-2026-07-25-public-content-issues-1131-1137-md)
- Session memory: [Public Content Issues 1131-1137](#source-docs-session-memory-2026-07-25-public-content-issues-1131-1137-md)

<a id="source-docs-spoke-updates-2026-07-25-public-content-issues-1131-1137-md--result"></a>
#### Result

Issues [#1131](https://github.com/azurras/christopherbell.dev/issues/1131) through [#1137](https://github.com/azurras/christopherbell.dev/issues/1137) were completed and closed through [PR #1251](https://github.com/azurras/christopherbell.dev/pull/1251). The PR squash-merged to `main` as `4b82116a0ed489c74eed144a478f1b3a3944ada2`.

<a id="source-docs-spoke-updates-2026-07-25-public-content-issues-1131-1137-md--commits"></a>
#### Commits

- `ea54749730df97f2bfc920271c8463eb826e3f2f`: implement public blog, gallery, archive, and local Bootstrap changes.
- `4108c5c6f5adf5877f247c2cff4cf543fd7eb1cd`: correct the photo configuration key and alt fallback boundary.
- `f5120784bf4763cbd57666839307be24d209198a`: isolate the real-YAML configuration binding regression from MongoDB.

<a id="source-docs-spoke-updates-2026-07-25-public-content-issues-1131-1137-md--validation"></a>
#### Validation

- Focused public-content Java suite: 29 passed.
- Focused Node suite: 4 passed after witnessed RED failures; full JavaScript suite: 199 passed.
- Authoritative local `cleanTest + check`: 1,003 Java tests, 0 failures, 3 skipped; `bootJar` and sensor verification passed.
- PR Ubuntu, macOS, Windows, Dependency Review, and CodeQL checks passed; post-merge `main` CI Build and CodeQL passed.
- Automatic production deployment replaced Java PID `26680` with `29012`.
- Production HTTPS returned `200` for every target page, API, and pinned WebJar asset; both APIs exposed configured content and equivalent POST probes remained `403`.
- Rendered production gallery, usage, blog, and Tony pages matched acceptance with zero warning/error console entries.

<a id="source-docs-spoke-updates-2026-07-25-public-content-issues-1131-1137-md--files-and-behavior"></a>
#### Files and Behavior

The batch updated public blog/photo controllers and security matchers, public browser renderers, the photography usage route, gallery configuration, archive templates/assets, Bootstrap dependency/template delivery, documentation, and focused Java/JavaScript regressions. See the linked PR and test report for the exact file list and request/response evidence.

<a id="source-docs-spoke-updates-2026-07-25-public-content-issues-1131-1137-md--blockers-and-risks"></a>
#### Blockers and Risks

No remaining blocker or known acceptance gap. The isolated worktree retains only its checkout-only `gradlew.bat` line-ending difference, which is absent from every commit.

<a id="source-docs-spoke-updates-2026-07-25-public-content-issues-1131-1137-md--next-action"></a>
#### Next Action

Select the next dependency-aware batch from the 34 remaining campaign issues and repeat the full spec/plan, local validation, PR/CI, merge, production acceptance, and closure loop.

<!-- /migrated-source: docs/spoke-updates/2026-07-25-public-content-issues-1131-1137.md -->

<a id="source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md"></a>
## 2026-07-25 | work | Complete All Open christopherbell.dev Issues

Original source: `docs/work/2026-07-25-complete-all-open-christopherbell-dev-issues.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `bd3e32fca9abc1056bba9653294eebca976832fa87e2d64af8d326e70563e4ee`.

<!-- migrated-source: docs/work/2026-07-25-complete-all-open-christopherbell-dev-issues.md -->
<a id="source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md--complete-all-open-christopherbelldev-issues"></a>
### Complete All Open christopherbell.dev Issues

- Status: closed
- Owner/Agent: Codex primary agent
- Started: 2026-07-25

<a id="source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md--objective"></a>
#### Objective

Resolve every currently open issue in `azurras/christopherbell.dev` through current-state validation, implementation where needed, local runtime testing, pull requests, required CI, merge, and issue closure.

<a id="source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md--scope"></a>
#### Scope

- 58 open issues: #1122-#1141, #1143-#1151, and #1153-#1181; #1142 and #1152 were already closed.
- Builder repository has no open issues as of 2026-07-25.
- Only comments authored by `azurras` may change scope or acceptance intent.

<a id="source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md--related-specs-and-plans"></a>
#### Related Specs and Plans

- Project spec: [Complete All Open christopherbell.dev Issues](#source-docs-specs-2026-07-25-complete-all-open-christopherbell-dev-issues-md) (`ready-for-execution`, approved 2026-07-25).
- Implementation plans: [GitHub Automation Issues 1144-1150](../implementation-plans/2026-07-25-github-automation-issues-1144-1150.md) (`complete`); [Public Delivery Issues 1122-1124 and 1138](../implementation-plans/2026-07-25-public-delivery-issues-1122-1124-1138.md) (`complete`); [Browser Security Issues 1125-1130](../implementation-plans/2026-07-25-browser-security-issues-1125-1130.md) (`complete`); [Public Content Issues 1131-1137](../implementation-plans/2026-07-25-public-content-issues-1131-1137.md) (`complete`); [Production Foundations Issues 1143, 1151, 1153, and 1154](../implementation-plans/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md) (`complete`); [Request Limits, Rate Limiting, and API Errors Issues 1139-1141 and 1157](../implementation-plans/2026-07-25-request-limits-rate-limiting-api-errors-issues-1139-1141-1157.md) (`complete`); [Accounts, Messages, Notifications, Posts, and Moderation Issues 1155-1168](../implementation-plans/2026-07-26-accounts-messages-notifications-posts-moderation-issues-1155-1168.md) (`complete`).

- Completed Batch 6 plan: [WFL and Location Imports Issues 1169-1175](../implementation-plans/2026-07-26-wfl-location-imports-issues-1169-1175.md) (`complete`).
- Completed Batch 7 plan: [VIN, Scheduling, and Link Previews Issues 1176-1181](../implementation-plans/2026-07-26-vin-scheduling-link-previews-issues-1176-1181.md) (`complete`).

<a id="source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md--spoke-repositories"></a>
#### Spoke Repositories

- `christopherbell-dev`: `A:\Projects\christopherbell.dev`; authoritative checkout is dirty and must remain untouched.
- Delivery work will use isolated worktrees based on refreshed `origin/main`.

<a id="source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md--dispatched-tasks"></a>
#### Dispatched Tasks

- No external agent tasks dispatched. The primary agent is executing the campaign.

<a id="source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md--current-state"></a>
#### Current State

- `azurras/builder`: 0 open issues.
- `azurras/christopherbell.dev`: 58 open issues and 0 open pull requests.
- Remote `origin/main`: `ea2ba7ea4c4ab1b71f172a29dd994e8375507675` when the #1144-#1150 implementation worktree was created.
- Authoritative spoke checkout is ahead 3, behind 53, and contains extensive unrelated user changes.
- Isolated campaign worktree: `A:\Projects\christopherbell.dev-worktrees\all-open-issues-20260725` on `codex/all-open-issues-20260725`.
- Baseline `:website:test` and `:website:jsTest` passed; all 175 browser tests passed.
- Seven-batch delivery design was approved by the user and saved as the project spec.
- The user approved the written spec and authorized autonomous continuation without routine phase approval pauses.
- The first Batch 1 sub-plan for #1144-#1150 passed mechanical validation and human execution-readiness review with no blockers.
- A refreshed clean baseline at `ea2ba7e` passed `:website:test` and all 176 browser tests; the plan was strengthened to parse YAML structurally and revalidated before edits.
- PR [#1241](https://github.com/azurras/christopherbell.dev/pull/1241) merged as `88144134290e5f690c048cb4945db531b8ef17c9`; issues #1144-#1150 closed automatically.
- All three CI platforms, Dependency Review, and CodeQL for Actions, Java/Kotlin, and JavaScript/TypeScript passed. GitHub default CodeQL setup was replaced by the checked-in advanced matrix without reducing language coverage.
- The campaign now has 51 open issues remaining.
- Live revalidation for the next sub-batch confirmed that localhost and `www` serve the main pages while the apex hostname returns 404; robots, sitemap, probes, cache headers, and dual-host deployment acceptance need work.
- The public-delivery plan for #1122-#1124 and #1138 is ready for validation and execution on `codex/public-delivery-1122-1124-1138`.
- Public-delivery PR [#1245](https://github.com/azurras/christopherbell.dev/pull/1245) is implemented at `550ae1f36f0c88295eafce4d9bf531772c83149e`; all CI, CodeQL, and Dependency Review gates pass.
- Local port-8091 acceptance proved public metadata, bounded probes, release-scoped asset URLs, and cache headers; 240 of 244 Windows deployment tests pass with four environment-only skips.
- Independent review found no code defects. Merge is held because the apex hostname still returns 404 and would correctly fail the new two-host deployment gate.
- Cloudflare now redirects apex paths and query strings to canonical `www`, and its browser cache
  policy respects origin headers.
- PR #1245 merged as `c0ccb88bf8666fa1014d2568ce772f48ac538705`; follow-up PR #1246 fixed
  the live `/dev/` asset namespace and merged as `193761d4e0b69240188b8d053de4c9ba4115e339`.
- Production runs the exact follow-up merge SHA. SEO metadata, bounded probes, versioned assets,
  cache headers, and apex redirects all pass live acceptance.
- Issues #1122, #1123, #1124, and #1138 are closed. The campaign has 47 open issues remaining.
- Browser-security PR [#1249](https://github.com/azurras/christopherbell.dev/pull/1249) merged as `b6c361d1d916337679a37f04caa46c3475215e71`; all platform, dependency-review, and CodeQL gates passed.
- Production auto-deployed the merge to PID `26680`. Public HTTPS headers, CSRF boundaries, DTO validation, cookie clearing, and fail-closed migration from the old browser JWT session passed live acceptance.
- Issues #1125-#1130 are closed. The campaign has 41 open issues remaining.
- Batch 3 issues #1131-#1137 have no comments or attachments and were revalidated against current main. An isolated worktree was created at `A:\Projects\christopherbell.dev-worktrees\public-content-1131-1137`; the full Java baseline and all 195 browser tests pass.
- Public-content PR [#1251](https://github.com/azurras/christopherbell.dev/pull/1251) merged as `4b82116a0ed489c74eed144a478f1b3a3944ada2`; all platform, dependency-review, and CodeQL gates passed, including the post-merge `main` runs.
- Production auto-deployed the merge to PID `29012`. The public blog, 12-image gallery, usage page, archive repairs, local Bootstrap assets, narrowed CSP, anonymous GET boundaries, and denied POST probes passed live HTTPS and rendered-browser acceptance with zero warning/error console entries.
- Issues #1131-#1137 are closed. The campaign has 34 open issues remaining.
- The four unfinished Batch 1 foundations (#1143, #1151, #1153, and #1154) have no comments or attachments. Their exact issue bodies were revalidated and a fresh worktree was created at `A:\Projects\christopherbell.dev-worktrees\production-foundations-1143-1154` from `origin/main` merge `4b82116a`.
- The first 1,003-test Java baseline had one unrelated command-center timing failure; the complete 12-test owning class passed immediately on isolated rerun. The production-foundations plan records that characterization and requires a clean authoritative suite before publication.
- The production-foundations plan passed mechanical validation and execution-readiness review with no blockers. It selects one redacted pre-refresh settings validator, explicit mail intent, official pinned `mongo:8.3.2` Compose service, and a repository-native immutable migration runner with an atomic lease.
- Production-foundations PR [#1252](https://github.com/azurras/christopherbell.dev/pull/1252) merged as `965b25bb3e703a2e67a5064d777a9ab1998f26a1`; all Ubuntu, macOS, Windows, Dependency Review, and CodeQL gates passed after commit `4e767dfd` replaced a pre-existing command-center timing-test race with a deterministic executor barrier.
- Production auto-deployed the merge from Java listener PID `29012` to `30976`. `/` remained 200, readiness settled to 200, V001 was stored exactly once with the reviewed checksum, both migration indexes exist, and the migration lease is released and ownerless.
- Issues #1143, #1151, #1153, and #1154 are closed. The campaign has 30 open issues remaining.
- Request-boundary PR [#1254](https://github.com/azurras/christopherbell.dev/pull/1254) merged as `ac74bbe30e7392781950bbc1f06f44e196adc46e`; all platform, Dependency Review, and CodeQL gates passed after independent-review commit `fb1f1c55` resolved ordered-expiry, upload-streaming, and rule-identity concerns.
- Production auto-deployed the merge from Java listener PID `20156` to `47288`. `/` remained 200 and readiness settled from 503 to 200.
- Issues #1139, #1140, #1141, and #1157 are closed. The campaign has 26 open issues remaining.
- Live inventory confirmed the exact 26 remaining issues are #1155-#1156 and #1158-#1181. Approved Batch 5 selects #1155, #1156, and #1158-#1168; all 13 are open with no comments or attachments.
- Batch 5 uses clean worktree `A:\Projects\christopherbell.dev-worktrees\accounts-messages-moderation-1155-1168` on `codex/accounts-messages-moderation-1155-1168` from merge `ac74bbe3`. Its baseline `check` passed in 1m39s with 1,173 Java tests, zero failures, and three expected skips.
- The Batch 5 implementation plan passed mechanical validation and execution-readiness review. It uses additive page/cursor APIs, durable idempotent deletion, database-owned dedupe/rate guards, compound cursor indexes, and bounded moderation audit records.
- Batch 5 PR [#1255](https://github.com/azurras/christopherbell.dev/pull/1255) passed all CI and CodeQL gates and merged as `5835a3c2b1dc032413e027568583859b9094ab9d` from final branch head `349ba1c77dd33f2a077750600c7ff3086b31a7b0`.
- Final `:website:check` passed with 1,155 Java tests, zero failures or errors, three expected skips, and 231 JavaScript tests. Independent final review found no actionable findings.
- Native SYSTEM auto-deployment replaced production Java listener PID `47288` with `6624`; `/`, `/back-office`, and the new stable feed returned 200, while protected admin APIs correctly returned 403.
- Issues #1155, #1156, and #1158-#1168 are closed. The campaign has 13 open issues remaining: #1169-#1181.
- Live inventory reconfirmed #1169-#1181 as the exact remaining issues. The approved specification retains two final batches: WFL/location #1169-#1175, then VIN/scheduling/link previews #1176-#1181.
- Batch 6 uses clean worktree `A:\Projects\christopherbell.dev-worktrees\wfl-location-imports-1169-1175` on `codex/wfl-location-imports-1169-1175` from merge `5835a3c2`; baseline `:website:check` passed in 1m46s with all 231 JavaScript tests.
- Batch 6 PR [#1256](https://github.com/azurras/christopherbell.dev/pull/1256) passed all platform, Dependency Review, underlying CodeQL, and aggregate CodeQL gates and merged as `abd2051e76155e5c01137ebec10c2d7550ec3556` from final branch head `a861c4b5d0d751c46e2a8cfab8ec86f17c37d0ae`.
- Final Batch 6 `:website:check` passed 1,170 Java tests with zero failures or errors, three expected skips, 233 JavaScript tests, and sensor-runtime verification. Independent review found no remaining actionable findings.
- Native SYSTEM auto-deployment replaced production Java listener PID `6624` with `41176`; local and external roots/freshness returned 200 while protected WFL operator APIs returned 403.
- Issues #1169-#1175 are closed. The campaign has six open issues remaining, exactly #1176-#1181.
- Final Batch 7 spoke commit `c1e9fc4f` passed 1,200 Java tests, the JavaScript and packaged
  runtime gates, and isolated port-8092 acceptance with V003 migration/index inspection.
- Batch 7 PR [#1257](https://github.com/azurras/christopherbell.dev/pull/1257) passed Ubuntu,
  macOS, Windows, Dependency Review, all CodeQL gates, and squash-merged as
  `9963ed0cc83f8b43f54612c1b8c6ed2966f22607`.
- Native SYSTEM auto-deployment rotated production PID `41176` to `29164`. Local/external roots,
  the VIN page, ordered batch errors, maximum batch rejection, protected boundary, and V003
  production checksum/indexes passed.
- Issues #1176-#1181 are closed. Live GitHub inventory confirms zero open issues remain in
  `azurras/christopherbell.dev`; all 58 campaign issues are complete.

<a id="source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md--blockers"></a>
#### Blockers

None. Docker is unavailable on this native-Mongo host, but the Compose contract passed its checked structural regression and both disposable and production migration acceptance passed. Protected SYSTEM release metadata remains inaccessible to non-elevated sessions by design; production acceptance used listener transition, merged-only endpoint behavior, exact migration evidence, public health, and service state.

<a id="source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md--validation"></a>
#### Validation

- GitHub issue and pull request inventory completed with GitHub CLI and the GitHub connector.
- Builder and spoke Git remotes, branches, worktrees, and status inspected.
- Every delivery batch passed local app testing, a durable test report, required GitHub CI/CodeQL,
  merge, native production acceptance, and issue closure.
- Final live inventory: `[]` for `gh issue list --repo azurras/christopherbell.dev --state open`.

<a id="source-docs-work-2026-07-25-complete-all-open-christopherbell-dev-issues-md--next-steps"></a>
#### Next Steps

None. Resume only for newly opened issues or explicit follow-up work; the 2026-07-25 58-issue
campaign is complete.

<!-- /migrated-source: docs/work/2026-07-25-complete-all-open-christopherbell-dev-issues.md -->

