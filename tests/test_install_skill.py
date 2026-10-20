#!/usr/bin/env python3
"""Verify Skill package installation without touching live Agent directories."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALLER = REPO_ROOT / "scripts" / "install_skill.py"
PACKAGED_SKILLS = (
    "bootstrap-workspace",
    "reviewing-therapy-transcripts",
    "reviewing-important-conversations",
    "bill-to-suishouji",
)


class InstallSkillTest(unittest.TestCase):
    def test_all_packages_have_portable_skill_entry(self) -> None:
        for skill_id in PACKAGED_SKILLS:
            package = REPO_ROOT / "skills" / skill_id / "package"
            skill_md = package / "SKILL.md"
            self.assertTrue(skill_md.is_file(), skill_id)
            text = skill_md.read_text(encoding="utf-8")
            self.assertIn(f"name: {skill_id}", text)
            for path in package.rglob("*"):
                if path.is_file():
                    self.assertNotIn("/Users/beibei", path.read_text(encoding="utf-8", errors="replace"), path)

    def test_install_copies_package_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "bootstrap-workspace"
            result = subprocess.run(
                [
                    sys.executable,
                    str(INSTALLER),
                    "bootstrap-workspace",
                    "--target",
                    str(dest),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("installed: bootstrap-workspace", result.stdout)
            self.assertTrue((dest / "SKILL.md").is_file())
            self.assertTrue((dest / "scripts" / "scaffold_workspace.py").is_file())
            self.assertFalse((dest / "manifest.yaml").exists())
            self.assertFalse((dest / "README.md").exists())

    def test_remaining_skills_install_without_private_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for skill_id in PACKAGED_SKILLS[1:]:
                dest = Path(tmp) / skill_id
                subprocess.run(
                    [
                        sys.executable,
                        str(INSTALLER),
                        skill_id,
                        "--target",
                        str(dest),
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                self.assertTrue((dest / "SKILL.md").is_file(), skill_id)
                self.assertFalse((dest / "manifest.yaml").exists(), skill_id)
                self.assertFalse(any(dest.rglob("*.csv")), skill_id)
        conversations = REPO_ROOT / "skills" / "reviewing-important-conversations" / "package"
        self.assertTrue((conversations / "templates.md").is_file())
        bill = REPO_ROOT / "skills" / "bill-to-suishouji" / "package"
        self.assertTrue((bill / "scripts" / "merge_bills.py").is_file())
        self.assertTrue((bill / "references" / "分类体系.md").is_file())
        self.assertFalse((bill / "inputs").exists())
        self.assertFalse((bill / "checks").exists())

    def test_installed_scaffold_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "bootstrap-workspace"
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            subprocess.run(
                [
                    sys.executable,
                    str(INSTALLER),
                    "bootstrap-workspace",
                    "--target",
                    str(dest),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(dest / "scripts" / "scaffold_workspace.py"),
                    "--target",
                    str(workspace),
                    "--profile",
                    "minimal",
                    "--project-name",
                    "Example project",
                    "--goal",
                    "Create durable workspace context",
                    "--inputs",
                    "User request",
                    "--outputs",
                    "Initialized workspace files",
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            today = date.today().strftime("%y%m%d")
            self.assertIn("AGENTS.md", result.stdout)
            self.assertIn("docs/tasks/INDEX.md", result.stdout)
            self.assertIn(
                f"docs/tasks/{today}-initialize-workspace.md", result.stdout
            )
            self.assertFalse((workspace / "AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()
