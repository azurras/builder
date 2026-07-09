# 2026-07-08 - create-christopherbell-dev-second-issue-round

## 23:18 - Create christopherbell.dev second issue round

### Request
The user asked for another round of finding issues/enhancements for `christopherbell.dev`, specifically to find 20 items and create concise GitHub issues for each item saying exactly what needs to be done.

### Project Context
The active hub is `C:\Users\Christopher\Developer\builder`. The target spoke is registered at `C:\Users\Christopher\Developer\christopherbell.dev` with remote `https://github.com/azurras/christopherbell.dev.git`. Existing prior rounds had created and closed issues #1090-#1096, #1105-#1109, and #1120. At the start of this request, `gh issue list --repo azurras/christopherbell.dev --state open` returned no open issues and `gh pr list` returned no open PRs.

The main spoke checkout was on branch `codex/pr-1119-ci-fix`, so the audit refreshed `origin/main` and created a separate detached worktree at `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\issue-audit-20260709`, currently at `d5ac7aba` (`Upgrade Spring Boot to 4.1.0`). No spoke source edits were made.

### Work Completed
Created Builder work record `docs/work/2026-07-08-christopherbell-dev-second-issue-discovery.md` and closure record `docs/work-closures/2026-07-08-christopherbell-dev-second-issue-discovery-closure.md`.

Created 20 GitHub issues in `azurras/christopherbell.dev`:

- #1122 Fix production routing so public site pages no longer return 404
- #1123 Add robots.txt and sitemap.xml for public pages
- #1124 Add health/readiness endpoints and a deployment smoke workflow
- #1125 Configure browser security headers in Spring Security
- #1126 Restore CSRF protection for browser state-changing requests
- #1127 Move browser authentication tokens out of localStorage
- #1128 Validate password reset link host instead of trusting forwarded headers
- #1129 Add Bean Validation to login and password reset request DTOs
- #1130 Make signup first and last name requirements match the UI
- #1131 Fix the public blog page API wiring
- #1132 Fix the public photo gallery API wiring
- #1133 Add a route for the photography usage page
- #1134 Repair broken and placeholder links in The Bell archive
- #1135 Remove mixed-content image URLs from The Bell archive
- #1136 Use real gallery alt text from photo metadata
- #1137 Pin or self-host all Bootstrap CDN assets
- #1138 Add cache headers and asset versioning for static resources
- #1139 Make request body size limits configurable
- #1140 Prevent unbounded rate-limit bucket growth
- #1141 Return standard rate-limit response headers

### Decisions
Used authenticated `gh issue create` for issue creation because the local GitHub CLI is installed and authenticated as `azurras`. Did not apply labels because the user asked for concise issues and the current label taxonomy was not needed to complete the request.

Used latest `origin/main` rather than the existing spoke working branch for source evidence. Kept the audit worktree detached to avoid switching or disturbing the main spoke checkout.

### Validation
Ran `gh auth status`, `gh issue list`, and `gh pr list` to confirm authentication and current GitHub state. Refreshed `origin/main` with `git fetch origin main`. Sampled live public routes with `Invoke-WebRequest`; `https://christopherbell.dev/`, `/blog`, `/tools`, `/canes-box-tracker`, `/whatsforlunch`, `/robots.txt`, `/sitemap.xml`, and `/favicon.ico` returned 404. Inspected security config, view controllers, templates, JavaScript components, account/password reset DTOs, rate limiting, and request-size filter code in the detached audit worktree.

### Current State
GitHub issues #1122-#1141 are open. The Builder hub has new work, closure, and session memory artifacts that need index refresh, validation, commit, and push. The spoke audit worktree remains at `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\issue-audit-20260709` for follow-up planning or implementation.

### Follow-ups
Recommended first triage group: #1122 for production availability, #1128 for reset-link host validation, #1125-#1127 for browser security posture, then #1131-#1133 for broken public content pages.
