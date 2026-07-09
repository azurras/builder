# christopherbell.dev Additional Issue Discovery

## Objective
Create 40 additional concise GitHub issues for azurras/christopherbell.dev, avoiding duplicates from the previous issue discovery batch (#1122-#1141).

## Status
closed

## Owner / Agent Context
Codex acted from the Builder hub at C:\Users\Christopher\Developer\builder and used a detached read-only audit worktree at C:\Users\Christopher\Developer\christopherbell.dev-worktrees\issue-audit-20260709.

## Spoke Repositories
- azurras/christopherbell.dev at C:\Users\Christopher\Developer\christopherbell.dev
- Audit worktree reset to origin/main commit d5ac7aba before this round.

## Completed Scope
Created 40 additional open GitHub issues covering documentation drift, production config, CI/security workflows, account administration, messages, notifications, posts, reporting, moderation, WFL imports, VIN tooling, scheduled collectors, and link preview hardening.

## Created Issues
- #1142 Update project documentation for Spring Boot 4.1 and Java 25 - https://github.com/azurras/christopherbell.dev/issues/1142
- #1143 Use an environment-driven MongoDB URI in production config - https://github.com/azurras/christopherbell.dev/issues/1143
- #1144 Add Gradle dependency caching to CI - https://github.com/azurras/christopherbell.dev/issues/1144
- #1145 Upload test reports from failed CI runs - https://github.com/azurras/christopherbell.dev/issues/1145
- #1146 Add CodeQL scanning for the website project - https://github.com/azurras/christopherbell.dev/issues/1146
- #1147 Add dependency review checks for pull requests - https://github.com/azurras/christopherbell.dev/issues/1147
- #1148 Tune Dependabot grouping and labels - https://github.com/azurras/christopherbell.dev/issues/1148
- #1149 Improve stale workflow messages and exemptions - https://github.com/azurras/christopherbell.dev/issues/1149
- #1150 Set least-privilege permissions on stale workflow - https://github.com/azurras/christopherbell.dev/issues/1150
- #1151 Validate required production settings at startup - https://github.com/azurras/christopherbell.dev/issues/1151
- #1152 Document MongoDB backup and restore procedures - https://github.com/azurras/christopherbell.dev/issues/1152
- #1153 Add Docker Compose support for local MongoDB - https://github.com/azurras/christopherbell.dev/issues/1153
- #1154 Add a migration strategy for Mongo indexes and data changes - https://github.com/azurras/christopherbell.dev/issues/1154
- #1155 Paginate and search the admin account list - https://github.com/azurras/christopherbell.dev/issues/1155
- #1156 Clean up related data when deleting accounts - https://github.com/azurras/christopherbell.dev/issues/1156
- #1157 Replace service RuntimeExceptions with domain API errors - https://github.com/azurras/christopherbell.dev/issues/1157
- #1158 Fix conversation summaries to return latest distinct conversations - https://github.com/azurras/christopherbell.dev/issues/1158
- #1159 Add cursor pagination to conversation history - https://github.com/azurras/christopherbell.dev/issues/1159
- #1160 Add message archive or delete controls - https://github.com/azurras/christopherbell.dev/issues/1160
- #1161 Add notification pagination and load-more support - https://github.com/azurras/christopherbell.dev/issues/1161
- #1162 Add a mark-all-read notification action - https://github.com/azurras/christopherbell.dev/issues/1162
- #1163 Deduplicate and rate-limit notification fanout - https://github.com/azurras/christopherbell.dev/issues/1163
- #1164 Add a stable cursor tie-breaker to post feeds - https://github.com/azurras/christopherbell.dev/issues/1164
- #1165 Add post editing with audit and expiry rules - https://github.com/azurras/christopherbell.dev/issues/1165
- #1166 Prevent duplicate open reports from the same reporter - https://github.com/azurras/christopherbell.dev/issues/1166
- #1167 Add filters and pagination to the report queue - https://github.com/azurras/christopherbell.dev/issues/1167
- #1168 Expand moderation audit logging - https://github.com/azurras/christopherbell.dev/issues/1168
- #1169 Move WFL nearby restaurant lookup to repository-level geospatial queries - https://github.com/azurras/christopherbell.dev/issues/1169
- #1170 Add locking and status for WFL imports - https://github.com/azurras/christopherbell.dev/issues/1170
- #1171 Add a WFL import dry-run preview - https://github.com/azurras/christopherbell.dev/issues/1171
- #1172 Add a WFL duplicate merge preview - https://github.com/azurras/christopherbell.dev/issues/1172
- #1173 Show WFL data freshness on public pages - https://github.com/azurras/christopherbell.dev/issues/1173
- #1174 Validate WFL metro configuration at startup - https://github.com/azurras/christopherbell.dev/issues/1174
- #1175 Make ZIP coordinate imports idempotent and observable - https://github.com/azurras/christopherbell.dev/issues/1175
- #1176 Add TTL and refresh behavior for VIN decode cache entries - https://github.com/azurras/christopherbell.dev/issues/1176
- #1177 Validate VIN batch requests with per-VIN errors - https://github.com/azurras/christopherbell.dev/issues/1177
- #1178 Clean up RandomVIN scheduler configuration - https://github.com/azurras/christopherbell.dev/issues/1178
- #1179 Add distributed locks for scheduled collectors - https://github.com/azurras/christopherbell.dev/issues/1179
- #1180 Harden link preview fetching against SSRF - https://github.com/azurras/christopherbell.dev/issues/1180
- #1181 Cache link preview failures and enforce fetch limits - https://github.com/azurras/christopherbell.dev/issues/1181
## Validation
- Verified open issue range #1142 through #1181 with gh issue list --repo azurras/christopherbell.dev --state open --limit 70 --json number,title,url.
- Confirmed Builder working tree was clean before durable artifact creation.
- Confirmed christopherbell.dev audit worktree was clean after discovery.

## Next Steps
Use the created issue list as the backlog for future spoke implementation rounds. No spoke source files were modified in this discovery-only pass.
