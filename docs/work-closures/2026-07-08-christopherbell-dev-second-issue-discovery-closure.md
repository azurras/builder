# christopherbell.dev Second Issue Discovery Closure

- Status: completed
- Work record: `docs/work/2026-07-08-christopherbell-dev-second-issue-discovery.md`
- Spoke repo: `C:\Users\Christopher\Developer\christopherbell.dev`
- GitHub repo: `azurras/christopherbell.dev`
- Audit worktree: `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\issue-audit-20260709` at `origin/main` commit `d5ac7aba`

## Completed Scope

Found another round of 20 concrete bugs/enhancements and created concise GitHub issues for each one. The issues are open in `azurras/christopherbell.dev` as #1122 through #1141.

## Created Issues

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

## Validation

- Verified there were no open issues before creation.
- Verified there were no open PRs before creating the new issue round.
- Refreshed the spoke remote and audited latest `origin/main` in a detached worktree.
- Confirmed the live domain returned 404 for sampled public routes.
- Created all 20 issues through `gh issue create` and captured their URLs.

## Known Gaps

No source changes were made in the spoke repo. The audit worktree remains available for follow-up implementation planning.
