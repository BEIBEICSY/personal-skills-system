#!/usr/bin/env python3
"""Verify bootstrap-workspace scaffolding for task index and init task files."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAFFOLD = (
    REPO_ROOT
    / "skills"
    / "bootstrap-workspace"
    / "package"
    / "scripts"
    / "scaffold_workspace.py"
)
IDENTIFY_RULE = (
    "identify whether this request continues an unfinished task or starts a new one"
)
DO_NOT_ASK_FOR_SYSTEM = "do not ask whether to create a task system"
OLD_MANUAL_TASK_STEP = (
    "Create a task specification under `docs/tasks/` before substantial work"
)
TASK_NAME_RULE = "YYMMDD-<task-description>"


def compact_today() -> str:
    return date.today().strftime("%y%m%d")


def run_scaffold(workspace: Path, *, dry_run: bool = False) -> subprocess.CompletedProcess:
    command = [
        sys.executable,
        str(SCAFFOLD),
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
    ]
    if dry_run:
        command.append("--dry-run")
    return subprocess.run(command, check=True, capture_output=True, text=True)


class ScaffoldWorkspaceTest(unittest.TestCase):
    def test_fresh_dry_run_lists_index_and_init_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            result = run_scaffold(workspace, dry_run=True)
            today = compact_today()
            self.assertIn("docs/tasks/INDEX.md", result.stdout)
            self.assertIn("docs/tasks/TEMPLATE.md", result.stdout)
            self.assertIn(
                f"docs/tasks/{today}-initialize-workspace.md", result.stdout
            )
            self.assertNotIn("-initialize-workspace.md", result.stdout.replace(f"{today}-initialize-workspace.md", ""))
            self.assertFalse((workspace / "docs" / "tasks" / "INDEX.md").exists())

    def test_fresh_write_creates_task_tracking_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            run_scaffold(workspace)
            today = compact_today()
            index = workspace / "docs" / "tasks" / "INDEX.md"
            template = workspace / "docs" / "tasks" / "TEMPLATE.md"
            init_task = (
                workspace / "docs" / "tasks" / f"{today}-initialize-workspace.md"
            )
            agents = (workspace / "AGENTS.md").read_text(encoding="utf-8")
            readme = (workspace / "README.md").read_text(encoding="utf-8")
            state = (workspace / "docs" / "STATE.md").read_text(encoding="utf-8")
            history = (workspace / "docs" / "HISTORY.md").read_text(encoding="utf-8")
            self.assertTrue(index.is_file())
            self.assertTrue(template.is_file())
            self.assertTrue(init_task.is_file())
            self.assertIn(f"{today}-initialize-workspace.md", index.read_text(encoding="utf-8"))
            self.assertIn("Completed", init_task.read_text(encoding="utf-8"))
            self.assertIn(IDENTIFY_RULE, agents)
            self.assertIn(DO_NOT_ASK_FOR_SYSTEM, agents)
            self.assertIn("docs/tasks/INDEX.md", agents)
            self.assertIn(TASK_NAME_RULE, agents)
            self.assertNotIn("YYYY-MM-DD-slug.md", agents)
            self.assertNotIn(OLD_MANUAL_TASK_STEP, readme)
            self.assertIn("docs/tasks/INDEX.md", readme)
            self.assertNotIn("Create the first task specification", state)
            self.assertIn(f"tasks/{today}-initialize-workspace.md", history)
            for path in workspace.rglob("*.md"):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("{{", text, path)
                self.assertNotIn("}}", text, path)

    def test_adopt_existing_agents_does_not_invent_init_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            (workspace / "AGENTS.md").write_text("# existing\n", encoding="utf-8")
            run_scaffold(workspace)
            today = compact_today()
            index = workspace / "docs" / "tasks" / "INDEX.md"
            init_task = (
                workspace / "docs" / "tasks" / f"{today}-initialize-workspace.md"
            )
            self.assertEqual(
                (workspace / "AGENTS.md").read_text(encoding="utf-8"), "# existing\n"
            )
            self.assertFalse(init_task.exists())
            self.assertTrue(index.is_file())
            index_text = index.read_text(encoding="utf-8")
            self.assertIn("Unverified", index_text)
            self.assertIn("adopting an existing workspace", index_text)
            self.assertNotIn("initialize-workspace.md", index_text)

    def test_adopt_does_not_overwrite_existing_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            tasks = workspace / "docs" / "tasks"
            tasks.mkdir(parents=True)
            (workspace / "AGENTS.md").write_text("# existing\n", encoding="utf-8")
            (tasks / "INDEX.md").write_text("# keep me\n", encoding="utf-8")
            run_scaffold(workspace)
            self.assertEqual((tasks / "INDEX.md").read_text(encoding="utf-8"), "# keep me\n")

    def test_skill_documents_task_identification_rules(self) -> None:
        skill_md = (
            REPO_ROOT
            / "skills"
            / "bootstrap-workspace"
            / "package"
            / "SKILL.md"
        )
        text = skill_md.read_text(encoding="utf-8")
        self.assertIn("docs/tasks/INDEX.md", text)
        self.assertIn("continues an unfinished task or starts a new one", text)
        self.assertIn("do not ask whether to create a task system", text)
        self.assertIn("YYMMDD-initialize-workspace.md", text)
        self.assertIn(TASK_NAME_RULE, text)
        self.assertNotIn("YYYY-MM-DD-slug.md", text)


if __name__ == "__main__":
    unittest.main()
