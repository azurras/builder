# Shell and PowerShell

Follow the repository's target shells and versions, `shellcheck` or PSScriptAnalyzer settings, and test frameworks such as Bats or Pester. This guide applies the shared rules and the [principles](jane-street-principles.md) to POSIX shell, Bash, and PowerShell. Shell scripts fail in quiet ways: unquoted variables split and glob, a failed command in a pipeline is ignored, and a native program's non-zero exit code does not stop PowerShell. The style makes failure loud, keeps every argument a single literal value, gives scripts typed and validated parameters, and cleans up on every exit.

Keep scripts small. When a script grows logic, data structures, or error handling that the shell expresses poorly, move that logic into the repository's main language and keep the script as a thin entry point.

## Bash Idioms at a Glance

| Prefer | Avoid | Why |
|---|---|---|
| `set -euo pipefail` at the top of Bash scripts, understood rather than relied on blindly | No error handling; assuming `set -e` catches everything | Failures stop the script; `pipefail` reports failures inside pipelines |
| `"$variable"` and `"${array[@]}"` everywhere | Unquoted expansions | Prevents word splitting and globbing |
| `--` before path arguments where the command supports it | Paths that may begin with `-` passed bare | A path is never read as an option |
| Arrays for argument lists | Building a command in a string and running `$command` | Each argument stays one argument |
| Globs (`for log_file in "$log_directory"/*.log`) | Parsing `ls` output | File names with spaces and newlines work |
| `mktemp` with `trap 'rm -rf -- "$work_directory"' EXIT` | Fixed temp paths; no cleanup | No collisions; cleanup on every exit |
| `local` variables with descriptive names in functions | Global variables shared between functions | State has an owner |
| `[[ ... ]]` in Bash; `printf '%s\n'` for output | `[ ... ]` with unquoted operands; `echo` with data | Fewer parsing surprises |
| `read -r` | `read` without `-r` | Backslashes in input are preserved |
| `command -v tool >/dev/null` checks with a clear message | Assuming a tool exists | Fails early with the reason |
| Meaningful exit codes and messages on stderr | `exit 1` with no explanation | Callers and operators know what failed |

## PowerShell Idioms at a Glance

| Prefer | Avoid | Why |
|---|---|---|
| `[CmdletBinding()]` and a typed `param()` block with validation attributes | Untyped `$args` or parameters checked by hand | Invalid input is rejected before the body runs |
| `Set-StrictMode -Version Latest` and `$ErrorActionPreference = 'Stop'` in scripts | Default non-terminating errors | Mistyped variables and failed cmdlets stop the script |
| Checking `$LASTEXITCODE` after native commands (or `$PSNativeCommandUseErrorActionPreference` on 7.3+) | Assuming `git` or `dotnet` failures throw | Native exit codes are not errors by default |
| `-LiteralPath` | `-Path` with paths that may contain `[` or `*` | Paths are not treated as wildcards |
| `SupportsShouldProcess` with `$PSCmdlet.ShouldProcess` for destructive actions | Destructive functions with no `-WhatIf` | Callers can preview changes |
| Returning objects (`[pscustomobject]`) | Returning formatted text or using `Write-Host` for data | Output can be filtered, sorted, and tested |
| Full cmdlet and parameter names in scripts | Aliases (`gci`, `?`, `%`, `rm`) and positional parameters | Scripts read the same on every machine |
| Approved `Verb-Noun` names (`Get-`, `Remove-`, `Test-`) | Ad hoc names | Discoverable and uniform |
| Splatting (`@parameters`) for long parameter lists | Very long single lines | Each argument's role is visible |
| `try`/`finally` for cleanup | Cleanup only on the success path | Resources are released on failure |
| `Join-Path` | String concatenation with `\` or `/` | Correct separators on every platform |

## Smells Reviewers Flag

- Unquoted `$variable` in Bash, especially in `rm`, `cp`, `mv`, `cd`, and `for` loops.
- `for file in $(ls ...)`, `cat file | while read line` without `-r`, or `eval` with any input.
- Pipelines in Bash scripts without `pipefail` whose first command can fail (`curl ... | tar ...`).
- `cd` without checking it succeeded before destructive commands.
- `rm -rf "$directory/"` where `$directory` could be empty (use `${directory:?}`).
- PowerShell calls to `git`, `npm`, `java`, or other native programs with no exit-code check.
- `Write-Host` used to return data; `"$name:"` inside strings (PowerShell reads `$name:` as a scoped variable, write `"${name}:"`).
- `Remove-Item -Recurse -Force` without `-LiteralPath` or a `ShouldProcess` gate.
- Secrets passed as command-line arguments, where other processes and logs can read them.

## Good and Bad Pairs

### Quote Paths and Do Not Parse `ls`

Bad (Bash fragment):

```bash
for log_file in $(ls $log_directory/*.log); do
  gzip $log_file
done
```

A directory or file name with a space splits into several words, glob characters in names are expanded a second time, and `ls` output is not a reliable list of names.

Good (complete Bash example):

```bash
compress_logs_in() {
  local log_directory="$1"
  local log_file
  for log_file in "$log_directory"/*.log; do
    [[ -e "$log_file" ]] || continue
    gzip -- "$log_file"
  done
}
```

The glob produces each file name as one word, quoting keeps it one word, `--` ends option parsing, and the existence check handles a directory with no matching files.

Check: a directory containing `my report.log` and `-x.log` compresses both; an empty directory does nothing.

### Clean Up on Every Exit

Bad (Bash fragment):

```bash
mkdir /tmp/build
cp -r src /tmp/build
make -C /tmp/build
rm -rf /tmp/build
```

The fixed path collides with other runs, and if `make` fails the directory is left behind (or, without `set -e`, `rm` runs while something still uses it).

Good (complete Bash example):

```bash
#!/usr/bin/env bash
set -euo pipefail

work_directory="$(mktemp -d)"
trap 'rm -rf -- "$work_directory"' EXIT

cp -R -- src "$work_directory/"
make -C "$work_directory/src"
```

Each run gets its own directory, and the `EXIT` trap removes it on success, failure, or interruption.

### Pipelines Fail Loudly

Bad (Bash fragment):

```bash
curl --silent "$release_url" | tar -xz -C "$install_directory"
echo "Installed"
```

If the download returns a 404 page or fails, `tar` reports its own error or extracts nothing, and the script still prints "Installed" because the pipeline's status is `tar`'s.

Good (Bash fragment):

```bash
set -euo pipefail

curl --fail --silent --show-error --location -- "$release_url" | tar -xz -C "$install_directory"
printf 'Installed %s into %s\n' "$release_url" "$install_directory"
```

`--fail` turns HTTP errors into a non-zero exit, `pipefail` makes the pipeline report it, and `set -e` stops before the success message. For release artifacts, also verify a checksum before extracting.

### Arguments Belong in Arrays

Bad (Bash fragment):

```bash
rsync_command="rsync -a --delete $source_directory $destination_directory"
$rsync_command
```

Paths with spaces split, and quoting inside the string does not help because the string is split after expansion.

Good (Bash fragment):

```bash
rsync_arguments=(--archive --delete -- "$source_directory/" "$destination_directory/")
rsync "${rsync_arguments[@]}"
```

Each array element is passed as exactly one argument. Long option names make the effect readable, and the trailing slashes state that contents are copied.

### PowerShell: Check Native Exit Codes

Bad (PowerShell fragment):

```powershell
git push origin main
Write-Host "Published"
```

A rejected push writes to stderr, sets `$LASTEXITCODE`, and the script still says "Published".

Good (PowerShell fragment):

```powershell
git push origin main
if ($LASTEXITCODE -ne 0) {
    throw "git push origin main failed with exit code $LASTEXITCODE"
}
Write-Information "Published main to origin" -InformationAction Continue
```

The exit code is checked immediately, and failure becomes a terminating error that names the command. On PowerShell 7.3+, setting `$PSNativeCommandUseErrorActionPreference = $true` with `$ErrorActionPreference = 'Stop'` does this automatically.

### PowerShell: Typed, Validated, Previewable Functions

Bad (PowerShell fragment):

```powershell
function cleanup($dir, $days) {
    gci $dir *.log | ? { $_.LastWriteTime -lt (Get-Date).AddDays(-$days) } | % { rm $_.FullName }
}
```

Parameters are untyped and unchecked, aliases hide the commands, `$dir` is treated as a wildcard, and there is no way to preview the deletion.

Good (complete PowerShell example):

```powershell
function Remove-StaleLogFile {
    [CmdletBinding(SupportsShouldProcess)]
    param(
        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [string] $LogDirectory,

        [Parameter(Mandatory)]
        [ValidateRange(1, 3650)]
        [int] $OlderThanDays
    )

    $cutoffTime = (Get-Date).AddDays(-$OlderThanDays)
    $staleLogFiles = Get-ChildItem -LiteralPath $LogDirectory -Filter '*.log' -File |
        Where-Object { $_.LastWriteTime -lt $cutoffTime }

    foreach ($staleLogFile in $staleLogFiles) {
        if ($PSCmdlet.ShouldProcess($staleLogFile.FullName, 'Remove stale log file')) {
            Remove-Item -LiteralPath $staleLogFile.FullName
        }
    }
}
```

The call `Remove-StaleLogFile -LogDirectory $logDirectory -OlderThanDays 30 -WhatIf` reads as a sentence, rejects a missing directory name or an absurd age before doing anything, and previews deletions. `-LiteralPath` treats brackets in paths literally.

Check: `-WhatIf` deletes nothing; without it, only `.log` files older than the cutoff are removed; `-OlderThanDays 0` is rejected.

### PowerShell: Return Objects, Not Text

Bad (PowerShell fragment):

```powershell
foreach ($file in $files) {
    Write-Host "$file.Name: $($file.Length)"
}
```

`Write-Host` output cannot be captured, sorted, or tested, and `"$file.Name"` expands `$file` then appends the literal text `.Name`.

Good (PowerShell fragment):

```powershell
foreach ($reportFile in $reportFiles) {
    [pscustomobject]@{
        Name      = $reportFile.Name
        SizeBytes = $reportFile.Length
    }
}
```

The function emits objects with named, unit-bearing properties. Callers can pipe them to `Sort-Object`, `Format-Table`, `ConvertTo-Json`, or a Pester assertion.

## Implementation Recipe

1. Identify the target shells and versions (POSIX `sh`, Bash 3.2 on macOS, Bash 5, Windows PowerShell 5.1, PowerShell 7) and use only their features.
2. Declare parameters with types and validation (PowerShell) or check arguments and print usage (Bash) before doing work.
3. Quote every expansion, keep arguments in arrays, and use `--` and `-LiteralPath` for paths.
4. Make failures stop the script: `set -euo pipefail`, `$ErrorActionPreference = 'Stop'`, and explicit native exit-code checks.
5. Own temporary files, processes, and locks with `trap` or `try`/`finally`.
6. Gate destructive actions behind `-WhatIf`/`ShouldProcess` or a `--dry-run` flag.
7. Run `shellcheck` or PSScriptAnalyzer when available, parse scripts with `bash -n` or the PowerShell parser, and test behavior with Bats or Pester in temporary directories.

## Evidence and Review

A script that parses and runs once on the author's machine has not been tested on paths with spaces, empty directories, failed downloads, or non-zero exit codes. Test those cases in a temporary directory, and use dry-run output as evidence for destructive scripts. See [configuration and templates](templates-and-configuration.md) for rendering and deployment rules.
