# Executable Templates and Configuration

- Validate source data before rendering; escape for the actual HTML, JavaScript, URL, shell or serialization context. Avoid string-built executable commands.
- Render valid syntax across supported branches, including empty, missing and malformed inputs. Test generated behavior, not just template text.
- Keep defaults and precedence explicit. Missing required security or production configuration must fail clearly rather than silently enabling an unsafe fallback.
- Verify effective environment/profile values, credentials boundaries and output paths. A test profile or alternate port alone does not prove data/effect isolation.
- For migrations or deployment configuration, verify compatibility, backup prerequisites, bounded success/failure criteria and the supported recovery path.
- Use repository-native schema validators, parsers or dry runs and relevant runtime checks. Read output diffs; generated snapshots do not approve themselves.

## Required Procedure

1. Identify the interpreter/parser, effective profile/environment, precedence, and which values come from an untrusted source.
2. Define valid values and required settings. Show the actual unit and role in parameter, column, key, and variable names.
3. Validate values before rendering/executing. Keep source input, parsed configuration, and effective settings in separately named values when their meanings differ.
4. Use the native parameterization/argument API for the destination context. Escape HTML, URL, script, shell, and SQL contexts according to their distinct rules.
5. Validate rendered/effective output, not only the source template. Cover empty, malformed, optional, and required branches relevant to the change.
6. For deployment/migration effects, establish ownership, exact targets, compatibility, bounded success criteria, and recovery through the repository's supported procedure.

Dedicated guides go deeper: [Shell and PowerShell](shell.md) for scripts and [SQL and data stores](sql.md) for queries, schema, and migrations.

## Good and Bad Path Arguments

Bad shell fragment:

```sh
cat $config_path
```

Good shell fragment:

```sh
cat -- "$config_path"
```

Quoting preserves the path as one argument; the option terminator prevents a leading hyphen from selecting an option. Choose the native command's supported syntax rather than assuming every utility accepts the same options.

Bad PowerShell fragment:

```powershell
Get-Content $configPath
```

Good PowerShell fragment:

```powershell
Get-Content -LiteralPath $configPath
```

LiteralPath preserves a path containing wildcard characters as a literal target. A descriptive `configPath` variable and the parameter role express the read operation.

## SQL and Migrations

Use parameter binding for data values. Select allowed dynamic identifiers from an explicit trusted mapping when identifiers cannot be bound; do not interpolate arbitrary input. Use meaningful columns and aliases so the relationship between input and selected/updated data is clear.

Apply database constraints where the database owns the invariant. Inspect old/new consumers and deployment order before removing or changing a stored field. Verify transaction behavior, bounded batches, failure diagnosis, and recovery where the change needs them. A parsed migration or dry-run alone cannot prove an actual database transition.

## Generated Output and Defaults

Use context-appropriate encoding at the final insertion boundary. A JSON string encoded correctly for JSON may still need different handling when embedded in an HTML script context. Make configuration precedence and absence explicit; defaults that change production/security behavior need the actual requirement and effective-value evidence.

For a behavior-preserving template refactor, compare meaningful output before and after. For a runtime/configuration change, record the actual runtime input and result through the repository's verification workflow.
