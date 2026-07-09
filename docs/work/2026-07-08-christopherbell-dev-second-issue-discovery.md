# christopherbell.dev Second Issue Discovery

- Status: closed
- Owner/agent context: Codex in Builder hub
- Objective: Find another round of 20 concrete bugs/enhancements for `christopherbell.dev` and create concise GitHub issues for each item.
- Spoke repo: `christopherbell.dev` at `C:\Users\Christopher\Developer\christopherbell.dev`, remote `https://github.com/azurras/christopherbell.dev.git`
- Audit worktree: `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\issue-audit-20260709` at `origin/main` commit `d5ac7aba`
- GitHub repo: `azurras/christopherbell.dev`

## Current State

Created 20 open GitHub issues from the audit. The issues cover production routing, SEO/static discovery files, deployment smoke checks, browser security hardening, auth/token handling, password reset host validation, request validation, public blog/photo page regressions, The Bell archive cleanup, gallery accessibility, CDN asset integrity, static caching, request-size configuration, and rate-limit behavior.

## Created Issues

- https://github.com/azurras/christopherbell.dev/issues/1122 - Fix production routing so public site pages no longer return 404
- https://github.com/azurras/christopherbell.dev/issues/1123 - Add robots.txt and sitemap.xml for public pages
- https://github.com/azurras/christopherbell.dev/issues/1124 - Add health/readiness endpoints and a deployment smoke workflow
- https://github.com/azurras/christopherbell.dev/issues/1125 - Configure browser security headers in Spring Security
- https://github.com/azurras/christopherbell.dev/issues/1126 - Restore CSRF protection for browser state-changing requests
- https://github.com/azurras/christopherbell.dev/issues/1127 - Move browser authentication tokens out of localStorage
- https://github.com/azurras/christopherbell.dev/issues/1128 - Validate password reset link host instead of trusting forwarded headers
- https://github.com/azurras/christopherbell.dev/issues/1129 - Add Bean Validation to login and password reset request DTOs
- https://github.com/azurras/christopherbell.dev/issues/1130 - Make signup first and last name requirements match the UI
- https://github.com/azurras/christopherbell.dev/issues/1131 - Fix the public blog page API wiring
- https://github.com/azurras/christopherbell.dev/issues/1132 - Fix the public photo gallery API wiring
- https://github.com/azurras/christopherbell.dev/issues/1133 - Add a route for the photography usage page
- https://github.com/azurras/christopherbell.dev/issues/1134 - Repair broken and placeholder links in The Bell archive
- https://github.com/azurras/christopherbell.dev/issues/1135 - Remove mixed-content image URLs from The Bell archive
- https://github.com/azurras/christopherbell.dev/issues/1136 - Use real gallery alt text from photo metadata
- https://github.com/azurras/christopherbell.dev/issues/1137 - Pin or self-host all Bootstrap CDN assets
- https://github.com/azurras/christopherbell.dev/issues/1138 - Add cache headers and asset versioning for static resources
- https://github.com/azurras/christopherbell.dev/issues/1139 - Make request body size limits configurable
- https://github.com/azurras/christopherbell.dev/issues/1140 - Prevent unbounded rate-limit bucket growth
- https://github.com/azurras/christopherbell.dev/issues/1141 - Return standard rate-limit response headers

## Validation

- `gh issue list --repo azurras/christopherbell.dev --state open --limit 100 --json number,title,url` initially returned no open issues.
- Refreshed `origin/main` and created a detached audit worktree at `d5ac7aba`.
- Checked live public routes with `Invoke-WebRequest`; sampled routes returned 404.
- Inspected current source files for route/API mismatches, security config, static templates, and frontend component wiring.
- Created issues through authenticated `gh issue create`.

## Next Steps

Triage created issues by risk. Suggested first group: #1122, #1128, #1125, #1126, #1127, then user-facing regressions #1131-#1133.
