#!/usr/bin/env python3
"""Verify the bootstrap-workspace update check against a local Git remote."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "bootstrap-workspace"
PACKAGE = SKILL_DIR / "package"
PACKAGE_PATH = "skills/bootstrap-workspace/package"


def git(cwd: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
    )


def make_remote(tmp: Path, version: str, changelog: str) -> str:
    source = tmp / "source"
    package = source / PACKAGE_PATH
    package.mkdir(parents=True)
    (package / "VERSION").write_text(version + "\n", encoding="utf-8")
    (package / "CHANGELOG.md").write_text(changelog, encoding="utf-8")
    git(source, "init", "-q", "-b", "main")
    git(source, "add", ".")
    git(source, "commit", "-q", "-m", "release")
    bare = tmp / "remote.git"
    git(tmp, "clone", "-q", "--bare", str(source), str(bare))
    return bare.as_uri()


def install_copy(tmp: Path, version: str) -> Path:
    skill = tmp / "installed" / "bootstrap-workspace"
    shutil.copytree(PACKAGE, skill)
    (skill / "VERSION").write_text(version + "\n", encoding="utf-8")
    return skill


def run_check(skill: Path, repository: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            str(skill / "scripts" / "check_update.py"),
            "--repository",
            repository,
            "--timeout",
            "30",
        ],
        capture_output=True,
        text=True,
    )


CHANGELOG = """# Changelog

## 0.5.0 — 2026-12-01

- Newest change.

## 0.4.0 — 2026-11-01

- Middle change.

## 0.3.0 — 2026-10-22

- Current change.
"""


class CheckUpdateTest(unittest.TestCase):
    def test_reports_update_with_newer_changes_only(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            remote = make_remote(tmp, "0.5.0", CHANGELOG)
            result = run_check(install_copy(tmp, "0.3.0"), remote)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("status: update-available", result.stdout)
            self.assertIn("local_version: 0.3.0", result.stdout)
            self.assertIn("latest_version: 0.5.0", result.stdout)
            self.assertIn("Newest change.", result.stdout)
            self.assertIn("Middle change.", result.stdout)
            self.assertNotIn("Current change.", result.stdout)
            self.assertIn("git pull", result.stdout)
            self.assertIn("install_skill.py bootstrap-workspace", result.stdout)

    def test_up_to_date(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            remote = make_remote(tmp, "0.5.0", CHANGELOG)
            result = run_check(install_copy(tmp, "0.5.0"), remote)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("status: up-to-date", result.stdout)
            self.assertNotIn("update_steps", result.stdout)

    def test_local_ahead(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            remote = make_remote(tmp, "0.4.0", CHANGELOG)
            result = run_check(install_copy(tmp, "0.5.0"), remote)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("status: ahead", result.stdout)
            self.assertIn("latest_version: 0.4.0", result.stdout)

    def test_unreachable_remote_does_not_fail(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            missing = (tmp / "missing.git").as_uri()
            result = run_check(install_copy(tmp, "0.3.0"), missing)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("status: unknown", result.stdout)
            self.assertIn("reason:", result.stdout)


PACKAGED_SKILLS = sorted(
    path.parent.name for path in (REPO_ROOT / "skills").glob("*/package")
)


class VersionConsistencyTest(unittest.TestCase):
    def test_every_package_is_versioned(self) -> None:
        self.assertEqual(len(PACKAGED_SKILLS), 4)
        for skill_id in PACKAGED_SKILLS:
            with self.subTest(skill=skill_id):
                package = REPO_ROOT / "skills" / skill_id / "package"
                version = (package / "VERSION").read_text(encoding="utf-8").strip()
                self.assertRegex(version, r"^\d+\.\d+\.\d+$")
                manifest = (package.parent / "manifest.yaml").read_text(encoding="utf-8")
                self.assertIn(f"version: {version}\n", manifest)
                changelog = (package / "CHANGELOG.md").read_text(encoding="utf-8")
                first = re.search(r"^## (\d+\.\d+\.\d+)", changelog, re.MULTILINE)
                self.assertIsNotNone(first)
                self.assertEqual(first.group(1), version)

    def test_update_config_points_at_own_package(self) -> None:
        for skill_id in PACKAGED_SKILLS:
            with self.subTest(skill=skill_id):
                package = REPO_ROOT / "skills" / skill_id / "package"
                config = json.loads((package / "update.json").read_text(encoding="utf-8"))
                self.assertEqual(config["skill_id"], skill_id)
                self.assertEqual(config["path"], f"skills/{skill_id}/package")
                self.assertEqual(config["branch"], "main")
                self.assertTrue(config["repository"].startswith("https://github.com/"))

    def test_check_scripts_are_identical(self) -> None:
        reference = (PACKAGE / "scripts" / "check_update.py").read_bytes()
        for skill_id in PACKAGED_SKILLS:
            with self.subTest(skill=skill_id):
                script = REPO_ROOT / "skills" / skill_id / "package" / "scripts" / "check_update.py"
                self.assertEqual(script.read_bytes(), reference)

    def test_skill_runs_check_first(self) -> None:
        for skill_id in PACKAGED_SKILLS:
            with self.subTest(skill=skill_id):
                text = (REPO_ROOT / "skills" / skill_id / "package" / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                self.assertIn("scripts/check_update.py", text)
                self.assertTrue(
                    "Do not update automatically" in text or "不自动更新" in text
                )


if __name__ == "__main__":
    unittest.main()
