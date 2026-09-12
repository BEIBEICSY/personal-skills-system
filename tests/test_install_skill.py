#!/usr/bin/env python3
"""Verify Skill package installation without touching live Agent directories."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALLER = REPO_ROOT / "scripts" / "install_skill.py"
PACKAGE = REPO_ROOT / "skills" / "bootstrap-workspace" / "package"


class InstallSkillTest(unittest.TestCase):
    def test_bootstrap_package_has_skill_entry(self) -> None:
        skill_md = PACKAGE / "SKILL.md"
        self.assertTrue(skill_md.is_file())
        text = skill_md.read_text(encoding="utf-8")
        self.assertIn("name: bootstrap-workspace", text)
        self.assertNotIn("/Users/beibei", text)

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
            self.assertIn("AGENTS.md", result.stdout)
            self.assertFalse((workspace / "AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()
