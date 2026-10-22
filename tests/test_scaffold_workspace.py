#!/usr/bin/env python3
"""Verify bootstrap-workspace scaffolding for task folders and task index."""

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
COMPLETED_TASK_RULE = (
    "ask whether to start a new task folder or continue recording in the existing one"
)
OUTPUT_NAME_RULE = "<deliverable>-<草稿|定稿>"
LEGACY_NOTICE = "Legacy layout detected"


def compact_today() -> str:
    return date.today().strftime("%y%m%d")


def run_scaffold(
    workspace: Path,
    *,
    dry_run: bool = False,
    profile: str = "minimal",
    extra: tuple[str, ...] = (),
) -> subprocess.CompletedProcess:
    command = [
        sys.executable,
        str(SCAFFOLD),
        "--target",
        str(workspace),
        "--profile",
        profile,
        "--project-name",
        "Example project",
        "--goal",
        "Create durable workspace context",
        "--inputs",
        "User request",
        "--outputs",
        "Initialized workspace files",
        *extra,
    ]
    if dry_run:
        command.append("--dry-run")
    return subprocess.run(command, check=True, capture_output=True, text=True)


class ScaffoldWorkspaceTest(unittest.TestCase):
    def test_fresh_dry_run_lists_index_and_init_task_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            result = run_scaffold(workspace, dry_run=True)
            today = compact_today()
            self.assertIn("tasks/INDEX.md", result.stdout)
            self.assertIn("tasks/TEMPLATE.md", result.stdout)
            self.assertIn(f"tasks/{today}-initialize-workspace/TASK.md", result.stdout)
            self.assertNotIn("docs/tasks", result.stdout)
            self.assertFalse((workspace / "tasks" / "INDEX.md").exists())

    def test_fresh_write_creates_task_folder_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            run_scaffold(workspace)
            today = compact_today()
            index = workspace / "tasks" / "INDEX.md"
            template = workspace / "tasks" / "TEMPLATE.md"
            init_task = workspace / "tasks" / f"{today}-initialize-workspace" / "TASK.md"
            agents = (workspace / "AGENTS.md").read_text(encoding="utf-8")
            readme = (workspace / "README.md").read_text(encoding="utf-8")
            state = (workspace / "docs" / "STATE.md").read_text(encoding="utf-8")
            history = (workspace / "docs" / "HISTORY.md").read_text(encoding="utf-8")
            self.assertTrue(index.is_file())
            self.assertTrue(template.is_file())
            self.assertTrue(init_task.is_file())
            self.assertFalse((workspace / "docs" / "tasks").exists())
            self.assertIn(
                f"{today}-initialize-workspace/TASK.md", index.read_text(encoding="utf-8")
            )
            self.assertIn("Completed", init_task.read_text(encoding="utf-8"))
            self.assertIn(IDENTIFY_RULE, agents)
            self.assertIn(DO_NOT_ASK_FOR_SYSTEM, agents)
            self.assertIn(COMPLETED_TASK_RULE, agents)
            self.assertIn(OUTPUT_NAME_RULE, agents)
            self.assertIn("tasks/INDEX.md", agents)
            self.assertIn("TASK.md", agents)
            self.assertIn(TASK_NAME_RULE, agents)
            self.assertNotIn("YYYY-MM-DD-slug.md", agents)
            self.assertNotIn("docs/tasks", agents)
            self.assertNotIn(OLD_MANUAL_TASK_STEP, readme)
            self.assertIn("tasks/INDEX.md", readme)
            self.assertNotIn("docs/tasks", readme)
            self.assertIn(f"tasks/{today}-initialize-workspace/TASK.md", state)
            self.assertIn(f"tasks/{today}-initialize-workspace/TASK.md", history)
            for path in workspace.rglob("*.md"):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("{{", text, path)
                self.assertNotIn("}}", text, path)

    def test_content_profile_uses_shared_not_top_level_artifact_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            run_scaffold(
                workspace,
                profile="content",
                extra=("--git-mode", "git", "--sensitive-inputs"),
            )
            self.assertTrue((workspace / "shared").is_dir())
            self.assertTrue((workspace / "shared" / ".gitkeep").is_file())
            for name in ("inputs", "work", "outputs"):
                self.assertFalse((workspace / name).exists(), name)
            readme = (workspace / "README.md").read_text(encoding="utf-8")
            self.assertIn("shared/", readme)
            self.assertIn("<YYMMDD-任务描述>/inputs/", readme)
            gitignore = (workspace / ".gitignore").read_text(encoding="utf-8")
            self.assertIn("tasks/*/work/", gitignore)
            self.assertIn("tasks/*/inputs/", gitignore)
            self.assertIn("shared/**", gitignore)
            self.assertIn("!shared/.gitkeep", gitignore)

    def test_code_profile_has_no_shared_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            run_scaffold(workspace, profile="code")
            self.assertTrue((workspace / "scripts").is_dir())
            self.assertFalse((workspace / "shared").exists())
            self.assertTrue((workspace / "tasks" / "INDEX.md").is_file())

    def test_adopt_existing_agents_does_not_invent_init_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            (workspace / "AGENTS.md").write_text("# existing\n", encoding="utf-8")
            run_scaffold(workspace)
            today = compact_today()
            index = workspace / "tasks" / "INDEX.md"
            self.assertEqual(
                (workspace / "AGENTS.md").read_text(encoding="utf-8"), "# existing\n"
            )
            self.assertFalse((workspace / "tasks" / f"{today}-initialize-workspace").exists())
            self.assertTrue(index.is_file())
            index_text = index.read_text(encoding="utf-8")
            self.assertIn("Unverified", index_text)
            self.assertIn("adopting an existing workspace", index_text)
            self.assertNotIn("initialize-workspace", index_text)

    def test_adopt_does_not_overwrite_existing_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            tasks = workspace / "tasks"
            tasks.mkdir(parents=True)
            (workspace / "AGENTS.md").write_text("# existing\n", encoding="utf-8")
            (tasks / "INDEX.md").write_text("# keep me\n", encoding="utf-8")
            run_scaffold(workspace)
            self.assertEqual((tasks / "INDEX.md").read_text(encoding="utf-8"), "# keep me\n")

    def test_legacy_layout_is_not_mixed_with_task_folders(self) -> None:
        for legacy in ("docs/tasks", "outputs"):
            with self.subTest(legacy=legacy), tempfile.TemporaryDirectory() as tmp:
                workspace = Path(tmp) / "workspace"
                (workspace / legacy).mkdir(parents=True)
                (workspace / "AGENTS.md").write_text("# existing\n", encoding="utf-8")
                result = run_scaffold(workspace, profile="content")
                self.assertIn(LEGACY_NOTICE, result.stdout)
                self.assertFalse((workspace / "tasks").exists())
                self.assertFalse((workspace / "shared").exists())
                self.assertEqual(
                    (workspace / "AGENTS.md").read_text(encoding="utf-8"), "# existing\n"
                )

    def test_skill_documents_task_folder_rules(self) -> None:
        skill_md = (
            REPO_ROOT
            / "skills"
            / "bootstrap-workspace"
            / "package"
            / "SKILL.md"
        )
        text = skill_md.read_text(encoding="utf-8")
        self.assertIn("tasks/INDEX.md", text)
        self.assertIn("tasks/YYMMDD-initialize-workspace/TASK.md", text)
        self.assertIn("continues an unfinished task or starts a new one", text)
        self.assertIn("do not ask whether to create a task system", text)
        self.assertIn(COMPLETED_TASK_RULE, text)
        self.assertIn(OUTPUT_NAME_RULE, text)
        self.assertIn("migration table", text)
        self.assertIn(TASK_NAME_RULE, text)
        self.assertNotIn("YYYY-MM-DD-slug.md", text)


if __name__ == "__main__":
    unittest.main()
