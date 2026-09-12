#!/usr/bin/env python3
"""Install a packaged Skill from this repository into an Agent skills directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOST_DEFAULTS = {
    "cursor": Path.home() / ".cursor" / "skills",
    "codex": Path.home() / ".codex" / "skills",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy skills/<id>/package into a host Skills directory."
    )
    parser.add_argument("skill_id", help="Skill directory name under skills/")
    parser.add_argument(
        "--host",
        choices=("cursor", "codex"),
        help="Install into the default directory for this host",
    )
    parser.add_argument(
        "--target",
        help="Override the destination Skill directory. Use for tests or custom hosts.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned copy without writing files",
    )
    return parser.parse_args()


def package_dir(skill_id: str) -> Path:
    path = REPO_ROOT / "skills" / skill_id / "package"
    if not path.is_dir():
        raise SystemExit(f"No installable package at {path}")
    skill_md = path / "SKILL.md"
    if not skill_md.is_file():
        raise SystemExit(f"Package is missing SKILL.md: {skill_md}")
    return path


def destination(skill_id: str, host: str | None, target: str | None) -> Path:
    if target:
        return Path(target).expanduser().resolve()
    if not host:
        raise SystemExit("Specify --host or --target")
    return (HOST_DEFAULTS[host] / skill_id).resolve()


def planned_files(package: Path) -> list[Path]:
    return sorted(path for path in package.rglob("*") if path.is_file())


def install(package: Path, dest: Path, dry_run: bool) -> list[str]:
    written: list[str] = []
    if not dry_run:
        dest.mkdir(parents=True, exist_ok=True)
    for src in planned_files(package):
        relative = src.relative_to(package)
        target = dest / relative
        written.append(str(relative))
        if dry_run:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
    return written


def main() -> None:
    args = parse_args()
    package = package_dir(args.skill_id)
    dest = destination(args.skill_id, args.host, args.target)
    files = install(package, dest, args.dry_run)
    mode = "dry-run" if args.dry_run else "installed"
    print(f"{mode}: {args.skill_id}")
    print(f"source: {package}")
    print(f"target: {dest}")
    for name in files:
        print(f"  {name}")


if __name__ == "__main__":
    main()
