# christopherbell.dev Command Center CPU Temperature Selection and Application Commit Test Report

## Document Status

draft

## Story/Issue

Christopher's July 16, 2026 production follow-up reported that CPU temperature
was approximately 68 C while a separate measuring tool showed approximately
34 C, and that Application commit was unavailable in the authenticated command
center.

Related artifacts:

- `docs/specs/2026-07-16-command-center-cpu-temperature-selection-and-commit.md`
- `docs/implementation-plans/2026-07-16-command-center-cpu-temperature-selection-and-commit.md`
- `docs/work/2026-07-12-command-center-cpu-temperature-and-uptime.md`

## Branch

- Spoke worktree:
  `A:\Projects\christopherbell.dev-worktrees\winsw-log-rotation-recovery-merged`
- Branch: `codex/cpu-temperature-selection-and-commit`
- Reviewed implementation commit: `66fa476f`
- Pull request: `https://github.com/azurras/christopherbell.dev/pull/1212`
- Squash merge:
  `013c3d66fd695075d6cee7573b4b366a038ec061`
- Production release:
  `013c3d66fd695075d6cee7573b4b366a038ec061`

## App / Environment

- Windows 11 production desktop running the website, MongoDB, and Cloudflare
  tunnel as native Windows services.
- Production root: `C:\ProgramData\christopherbell.dev`.
- Production endpoint: `http://127.0.0.1:8080/`.
- Public endpoint: `https://www.christopherbell.dev/`.
- CPU: Intel Core i5-13600K.
- CPU sensor provider: LibreHardwareMonitor 0.9.6 through signed PawnIO 2.2.0.0.
- Sensor libraries remained enabled; the acceptance helper did not weaken ACL,
  signature, Defender, or bounded-probe checks.

## Local Run Details

- Added a pure PowerShell selector that prefers `CPU Package`, then `Core Max`,
  then the maximum remaining absolute temperature.
- Excluded sensor names ending in `Distance to TjMax`.
- Kept the public card label generic as `CPU temperature` because fallback
  hardware may not provide a package sensor.
- Added bounded application-side reading of regular, non-symlink
  `release.json` in the active release working directory.
- Required a lowercase 40-character hexadecimal SHA and preserved safe
  unavailable behavior for malformed metadata.
- Changed operational sensor verification to derive both script and library
  hashes from the active `current\app.jar`, preserving rollback compatibility.
- Verified the selector under Windows PowerShell 5.1 with a fixture containing
  package `48 C` and TjMax headroom `66 C`; the selected result was `48 C`.
- Complete local Pester: 85 passed, 0 failed, 2 expected privileged NTFS skips.
- Full Gradle build: success in 32 seconds.
- JavaScript tests: 116 passed.
- `:website:verifySensorRuntime`: passed.
- `git diff --check`: passed.

## Test Cases

| Test case | Result | Evidence |
| --- | --- | --- |
| Root-cause sensor inventory | Pass | Core Average 37.57 C, Core Max 45 C, CPU Package 48 C, actual cores 34-45 C, TjMax-distance values 55-66 C |
| CPU Package preference | Pass | Windows PowerShell 5.1 fixture selected 48 C instead of 66 C headroom |
| TjMax exclusion | Pass | Focused Pester covered package, core-max, fallback, invalid values, and distance-name exclusion |
| Application metadata fallback | Pass | Java tests covered configured commit preference, valid release SHA fallback, invalid/missing metadata, bounds, and symlink rejection |
| Rollback-aware script verification | Pass | Pester derived expected resource hashes from a synthetic active JAR |
| Complete Windows regression | Pass | 85 passed, 0 failed, 2 expected skips |
| Full application regression | Pass | Gradle build and all Java tests passed; JavaScript 116/116 |
| Independent review | Pass | Re-review found no remaining Critical or Important issues |
| GitHub CI and CodeQL | Pass | All seven required checks passed for the amended commit |
| Exact production release | Pass | Active release and `release.json` SHA both equal merge `013c3d66...` |
| Live sensor semantic match | Pass | Website probe 49 C while CPU Package inventory was 50 C |
| Three-window stability | Pass | Samples were 57 C, 47 C, and 44 C; service PID/tree and SCM 7031 record remained stable |
| Probe process bound | Pass | All 18 observations reported 0 accumulated CPU PowerShell probe processes |
| Sensor and Defender gates | Pass | PawnIO running, signature valid, uninstall registered, active threats 0 |
| Local/public website | Pass | Both returned HTTP 200, 3912 bytes, and title `CB \| Home` |
| Authenticated visual cards | Pending | Christopher is hard-refreshing the command center to confirm the displayed CPU and commit cards |

## Data Sent

- Read-only elevated LibreHardwareMonitor inventory of every CPU temperature
  sensor.
- `prod.ps1 verify-startup`, `sensor-status`, `install`, and `auto-install`.
- A guarded deployment request only if the active release did not already
  equal the merged SHA.
- Three direct CPU-temperature verification calls separated by 30-second
  observation windows.
- Read-only service/process/SCM event checks.
- `GET http://127.0.0.1:8080/`.
- `GET https://www.christopherbell.dev/`.

No password, JWT, command-center machine action, restart, shutdown, or reboot
request was sent.

## Response Received

- Initial semantic comparison: direct website probe `49 C`; independently
  opened CPU Package sensor `50 C`.
- Stability samples: `57 C`, `47 C`, and `44 C`.
- Preferred sensor: `CPU Package`,
  `/intelcpu/0/temperature/16`.
- Active application commit:
  `013c3d66fd695075d6cee7573b4b366a038ec061`.
- PawnIO: version `2.2.0.0`, driver `Running`, signature `Valid`.
- Microsoft Defender: zero active WinRing0/PawnIO threats.
- Production services remained Running and Automatic.
- Local and public homepages both returned HTTP 200, 3912 bytes, and
  `<title>CB | Home</title>`.

## Pass / Fail

Automated, review, CI, merge, and native production acceptance result:
**PASS**.

The deployed probe now tracks the preferred absolute CPU Package sensor rather
than thermal headroom, and the active application release metadata contains the
exact merged commit. Final report completion is waiting only for the user's
authenticated visual confirmation that both cards render those values.

## Evidence

- Production acceptance JSON:
  `C:\Users\Christopher\AppData\Local\Temp\cbdev-cpu-temperature-result.json`
- Raw production inventory JSON:
  `C:\Users\Christopher\AppData\Local\Temp\cbdev-cpu-sensor-inventory.json`
- New bundled probe SHA-256:
  `3D863E4917CD10CD4D79485B236B835E4AB727E9FF79A9333FA07332F2D22D76`
- Reviewed commit: `66fa476f`.
- Merged pull request:
  `https://github.com/azurras/christopherbell.dev/pull/1212`.
- Production release:
  `013c3d66fd695075d6cee7573b4b366a038ec061`.
- Pester: 85 passed, 0 failed, 2 skipped.
- JavaScript: 116 passed.
- GitHub checks: CodeQL actions, Java/Kotlin, JavaScript/TypeScript, CodeQL,
  and Windows/macOS/Ubuntu builds all passed.

## Bugs / Follow-ups

- The separate measuring tool may show core average or one idle core while the
  command center intentionally shows CPU Package. Those are different valid
  sensor semantics and may differ under transient load.
- The acceptance helper initially looked for `Name` in normalized inventory
  rows whose label field is `Sensor`; that helper-only defect was corrected
  before final acceptance. The deployed application selector was unaffected.
- Authenticated command-center visual confirmation remains pending from
  Christopher. No production engineering blocker remains.
