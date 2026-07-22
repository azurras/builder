# Templates and Code-Bearing Configuration Guidance

Apply this reference to executable templates, build and deployment configuration, workflow definitions, framework configuration, query templates, and configuration that controls runtime behavior. Repository-native rendering, schema, formatting, and security mechanisms take precedence.

## Table of Contents

- [Decision guide](#decision-guide)
- [Keep logic at the right boundary](#keep-logic-at-the-right-boundary)
- [Escaping and trust](#escaping-and-trust)
- [Stable rendering contracts](#stable-rendering-contracts)
- [Configuration as an interface](#configuration-as-an-interface)
- [Defaults and failure](#defaults-and-failure)
- [Secrets and operational effects](#secrets-and-operational-effects)
- [Testing](#testing)
- [Good and bad](#good-and-bad)
- [Review checklist](#review-checklist)

## Decision Guide

| Need | Prefer | Avoid |
|---|---|---|
| Presentation condition | Small obvious branch in the template | Nested business rules and data transformation |
| Repeated rendering rule | Tested view-model/helper or component | Copy-pasted expressions across templates |
| Untrusted output | Framework-native escaping for the correct context | Raw HTML/string concatenation |
| Script/test hook | Stable semantic or `data-*` selector | Incidental DOM nesting or visible copy |
| Required configuration | Typed/schema-validated startup input | Late `null` failures deep in execution |
| Optional configuration | Explicit defaults documented at the key | Ambient fallback spread across modules |
| Environment variation | One validated configuration model | Branching on environment in many files |
| Secret | Secret provider/environment reference with redaction | Literal value in repository or logs |

## Keep Logic at the Right Boundary

- Keep templates responsible for presentation, small visibility choices, iteration, and safe formatting.
- Move domain decisions, authorization, non-trivial aggregation, and reusable transformations into tested source code or a view model.
- Keep simple formatting local when extraction would obscure rather than clarify.
- Avoid invoking remote services, database queries, or mutable operations during rendering.
- Make partials and components accept narrow, named inputs instead of ambient global context.
- Treat build, workflow, and deployment expressions as code when they contain conditions, sequencing, or effects.

A template branch is acceptable when a reviewer can state its complete rule immediately. If the rule needs its own examples or can affect multiple renderers, move it to a testable boundary.

## Escaping and Trust

- Use framework-native automatic escaping by default.
- Identify the output context: HTML text, attribute, URL, JavaScript, CSS, SQL, and shell contexts require different handling.
- Use raw/unescaped output only when the value comes from a reviewed sanitizer that guarantees the exact output context.
- Keep authorization outside presentation hiding; a hidden control is not an enforcement boundary.
- Validate URLs and protocols before rendering attacker-controlled links.
- Quote shell and query values through native parameter mechanisms, not template interpolation.
- Treat included templates and generated fragments as untrusted unless their production path is controlled.

Security rules override aesthetic consistency. Do not weaken escaping or validation to preserve legacy markup.

## Stable Rendering Contracts

- Preserve semantic HTML, accessibility names, focus order, keyboard behavior, and form labels.
- Give JavaScript and tests stable semantic selectors or explicit `data-*` hooks when no accessible query exists.
- Avoid coupling scripts to child position, styling classes, or user-visible copy unless that is the actual contract.
- Keep IDs unique and deterministic when consumers rely on them.
- Treat emails, feeds, and externally consumed markup as compatibility surfaces.
- Make empty, loading, error, and unavailable states explicit; do not render malformed partial data as success.

## Configuration as an Interface

Configuration has callers, compatibility, defaults, validation, and failure behavior like any other API.

- Define the accepted keys, types, units, ranges, and combinations.
- Validate at startup, build, deployment, or command entry before work begins.
- Use schemas or typed configuration facilities already present in the repository.
- Reject unknown keys when typos would be dangerous; tolerate them only when forward compatibility requires it.
- Name units in keys or use typed duration/size formats.
- Keep environment-specific values separate from invariant configuration structure.
- Version persisted or externally supplied configuration formats when incompatible changes are possible.
- Preserve ordering only when the consuming tool treats it as semantic.

## Defaults and Failure

- Put explicit defaults next to the configuration definition and cover them with tests.
- Use no default for required secrets, identities, destructive targets, or security-sensitive policy.
- Fail early with a message that identifies the safe key and violated constraint.
- Distinguish missing, empty, malformed, unsupported, and inaccessible values when remediation differs.
- Do not silently fall back from a secure or production mode to a weaker mode.
- Preserve original parser or provider context for diagnostics while redacting sensitive values.

Explicit defaults should be safe, unsurprising, and stable. A default that depends on the current directory, machine, locale, or time is an effect and must be visible.

## Secrets and Operational Effects

- Reference secrets through the repository's approved provider or environment mechanism.
- Never write real secret values into examples, fixtures, snapshots, logs, or error output.
- Mark commands or workflows that deploy, publish, delete, restart, or mutate external systems as effects with clear conditions.
- Pin action, image, plugin, and dependency versions according to repository security policy.
- Give jobs least privilege and narrow token permissions.
- Make retry, timeout, concurrency, and cancellation policy explicit for deployment and automation steps.
- Protect destructive paths from empty values, broad globs, and unresolved variables.

## Testing

- Render representative valid, empty, unavailable, and malicious-input cases.
- Assert semantic output: escaped text, stable selectors, accessibility roles, key attributes, and expected branches.
- Use focused snapshots only for stable structured output and read every update.
- Parse configuration through the real schema or loader in tests.
- Test required, defaulted, malformed, out-of-range, unknown, and incompatible combinations.
- Run the native syntax or schema validator for YAML, JSON, workflow, build, and deployment files.
- Use dry-run or validation modes before workflows with external effects.
- Test generated commands as structured arguments where possible, not as fragile concatenated strings.

## Good and Bad

Bad: business logic, raw output, and hidden default are mixed into presentation.

```html
{% if user.balance - pending > 0 and config.mode|default('prod') == 'prod' %}
  <div onclick="run('{{ user.command|raw }}')">{{ user.html|raw }}</div>
{% endif %}
```

Good: source code supplies a validated view model, output stays escaped, and behavior hooks are stable.

```html
{% if account.can_submit_payment %}
  <button type="button" data-action="submit-payment">
    {{ account.submit_label }}
  </button>
{% endif %}
```

The view-model constructor owns the payment invariant. The framework escapes the label. JavaScript binds to an explicit behavior selector. Required deployment mode is validated in configuration rather than defaulted inside the template.

## Review Checklist

- Is non-trivial business or authorization logic outside the template and covered by tests?
- Is every untrusted value escaped for its actual output context?
- Are raw output and command interpolation absent or protected by a reviewed boundary?
- Are selectors, accessibility semantics, and external markup compatibility stable?
- Are configuration keys typed, validated, unit-aware, and documented through repository-native mechanisms?
- Are explicit defaults safe, and do required sensitive values fail closed?
- Are secrets redacted and operational effects bounded?
- Do render, schema, syntax, dry-run, and effect checks provide proportionate evidence?
