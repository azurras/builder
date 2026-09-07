"""Read-only Git inspection with explicit errors."""
from pathlib import Path
import os
import subprocess

def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}, timeout=30, check=False,
    )
    if result.returncode:
        raise ValueError(f"git {' '.join(args)} failed ({result.returncode}): {result.stderr.strip()}")
    return result.stdout.strip()



def inspect_repository(repo: Path) -> tuple[str, bool]:
    repo = repo.expanduser().resolve()
    try:
        if Path(git(repo, "rev-parse", "--show-toplevel")).resolve() != repo:
            raise ValueError("Path must be the repository root")
        branch = git(repo, "branch", "--show-current") or "detached"
        head = git(repo, "rev-parse", "HEAD")
        remotes = git(repo, "remote").splitlines()
        remote = git(repo, "remote", "get-url", "origin") if "origin" in remotes else "not configured"
        status = git(repo, "status", "--short") or "clean"
        return (f"- Repository: `{repo}`\n- Origin: `{remote}`\n- Branch: `{branch}`\n"
                f"- HEAD: `{head}`\n- Working tree:\n```text\n{status}\n```\n", False)
    except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
        return f"- Repository: `{repo}`\n- Inspection error: {exc}\n", True
