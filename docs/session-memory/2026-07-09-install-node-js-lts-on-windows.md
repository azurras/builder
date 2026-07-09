# 2026-07-09 - Install Node.js LTS on Windows

## 20:14 - Install Node.js LTS on Windows

### Request
The user asked to install Node.js on this Windows machine so Builder can coordinate work against spoke repos such as `christopherbell.dev` without relying only on the Codex bundled Node runtime.

### Project Context
Builder is the hub at `C:\Users\Christopher\Developer\builder`. The current spoke is `C:\Users\Christopher\Developer\christopherbell.dev`, which contains JavaScript files that may need syntax checks during future work.

### Work Completed
Installed Node.js LTS through Windows Package Manager:

```text
winget install --id OpenJS.NodeJS.LTS --source winget --accept-package-agreements --accept-source-agreements --disable-interactivity
```

Winget installed Node.js LTS `24.18.0` from `https://nodejs.org/dist/v24.18.0/node-v24.18.0-x64.msi`.

Verified the installed files under `C:\Program Files\nodejs`, including `node.exe`, `npm.cmd`, and `npx.cmd`.

Updated `docs/spokes/repos.md` so the `christopherbell.dev` spoke notes now record the global Node.js install path and explain that new terminals should have `node`, `npm`, and `npx` on PATH.

### Validation
Verified direct executable versions:

```text
C:\Progra~1\nodejs\node.exe --version -> v24.18.0
C:\Progra~1\nodejs\npm.cmd --version -> 10.9.1
```

Verified the machine PATH includes `C:\Program Files\nodejs\`.

Verified Node can syntax-check the spoke JavaScript file when the install directory is on the command PATH:

```text
node --check website\src\main\resources\static\js\canes-box-tracker.js
```

The syntax check completed successfully.

### Follow-ups
The current Codex process environment still did not resolve `node` immediately after install because PATH updates are picked up by newly launched terminals/processes. Open a new terminal, or restart Codex, before expecting plain `node` to resolve without a manual PATH prefix.
