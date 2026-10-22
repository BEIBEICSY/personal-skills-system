#!/usr/bin/env python3
"""Compare this installed Skill with the latest version on its Git remote."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
HEADING_RE = re.compile(r"^## (\d+\.\d+\.\d+)\b.*$", re.MULTILINE)


class CheckError(Exception):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", help="Override the remote in update.json")
    parser.add_argument("--branch", help="Override the branch in update.json")
    parser.add_argument("--timeout", type=float, default=20, help="Seconds per Git call")
    return parser.parse_args()


def version_tuple(value: str) -> tuple[int, ...]:
    value = value.strip()
    if not VERSION_RE.match(value):
        raise CheckError(f"invalid version: {value!r}")
    return tuple(int(part) for part in value.split("."))


def run_git(args: list[str], cwd: Path, timeout: float) -> str:
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        raise CheckError("git is not installed") from exc
    except subprocess.TimeoutExpired as exc:
        raise CheckError(f"git timed out after {timeout:g}s") from exc
    if result.returncode != 0:
        detail = (result.stderr.strip().splitlines() or ["unknown error"])[-1]
        raise CheckError(f"git {args[0]} failed: {detail}")
    return result.stdout


def fetch_remote(repository: str, branch: str, path: str, timeout: float) -> tuple[str, str]:
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "remote"
        run_git(
            [
                "clone",
                "--quiet",
                "--depth",
                "1",
                "--filter=blob:none",
                "--no-checkout",
                "--branch",
                branch,
                repository,
                str(clone),
            ],
            Path(tmp),
            timeout,
        )
        version = run_git(["show", f"HEAD:{path}/VERSION"], clone, timeout)
        try:
            changelog = run_git(["show", f"HEAD:{path}/CHANGELOG.md"], clone, timeout)
        except CheckError:
            changelog = ""
    return version.strip(), changelog


def newer_entries(changelog: str, local: tuple[int, ...]) -> list[str]:
    headings = list(HEADING_RE.finditer(changelog))
    entries = []
    for index, heading in enumerate(headings):
        if version_tuple(heading.group(1)) <= local:
            continue
        end = headings[index + 1].start() if index + 1 < len(headings) else len(changelog)
        entries.append(changelog[heading.start():end].strip())
    return entries


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parent.parent
    try:
        config = json.loads((skill_root / "update.json").read_text(encoding="utf-8"))
        local_raw = (skill_root / "VERSION").read_text(encoding="utf-8").strip()
        local = version_tuple(local_raw)
    except (OSError, ValueError, CheckError) as exc:
        print("status: unknown")
        print(f"reason: cannot read local version metadata: {exc}")
        return 0

    repository = args.repository or config["repository"]
    branch = args.branch or config["branch"]
    print(f"skill: {config['skill_id']}")
    print(f"local_version: {local_raw}")
    print(f"repository: {repository} ({branch})")
    try:
        latest_raw, changelog = fetch_remote(repository, branch, config["path"], args.timeout)
        latest = version_tuple(latest_raw)
    except CheckError as exc:
        print("status: unknown")
        print(f"reason: {exc}")
        return 0

    print(f"latest_version: {latest_raw}")
    if latest == local:
        print("status: up-to-date")
    elif latest < local:
        print("status: ahead")
        print("note: the local copy is newer than the remote branch, likely not pushed yet.")
    else:
        print("status: update-available")
        print("changes:")
        for entry in newer_entries(changelog, local) or ["(no changelog entries found)"]:
            print(entry)
            print()
        print("update_steps:")
        print("  cd <your clone of the Skills repository>   # first time: git clone " + repository)
        print("  git pull")
        print(f"  python3 scripts/install_skill.py {config['skill_id']} --host cursor   # or --host codex")
    return 0


if __name__ == "__main__":
    sys.exit(main())
