# bootstrap-workspace 任务清单与自动建档 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让 `bootstrap-workspace` 在初始化时生成任务总清单和第一条初始化任务，并让后续 Agent 按工作目标自动续做或新建任务档案。

**Architecture:** 脚手架继续只创建缺失文件。首次初始化（目标目录还没有 `AGENTS.md`）写入 `docs/tasks/INDEX.md`、`TEMPLATE.md` 和 `{{DATE}}-initialize-workspace.md`；接管已有工作区时若缺清单则写入 stub INDEX，不伪造初始化任务。识别规则写进生成的 `AGENTS.md` 和 `package/SKILL.md`。

**Tech Stack:** Python 3 stdlib、unittest、Markdown 模板、现有 `scripts/install_skill.py`

**规格:** `docs/superpowers/specs/2026-09-22-bootstrap-workspace-task-tracking-design.md`

**提交约定:** 本仓库用户规则是未明确要求时不提交。下列 Commit 步骤仅在用户要求提交时执行；否则跳过并继续下一任务。

---

## File map

| 文件 | 职责 |
|---|---|
| `tests/test_scaffold_workspace.py` | 直接跑权威包里的脚手架：首次初始化、接管、占位符、AGENTS 规则 |
| `tests/test_install_skill.py` | 安装后 dry-run 也要看到 INDEX 和 initialize-workspace |
| `skills/bootstrap-workspace/package/assets/templates/INDEX.md.tmpl` | 首次初始化的任务总清单 |
| `skills/bootstrap-workspace/package/assets/templates/INDEX_STUB.md.tmpl` | 接管已有工作区时的空清单 |
| `skills/bootstrap-workspace/package/assets/templates/INIT_TASK.md.tmpl` | 已完成的初始化任务档案 |
| `skills/bootstrap-workspace/package/assets/templates/TASK_TEMPLATE.md.tmpl` | 新任务模板，增加 Related sessions / Related tasks |
| `skills/bootstrap-workspace/package/scripts/scaffold_workspace.py` | 按是否已有 `AGENTS.md` 选择模板，并更新目录地图 |
| `skills/bootstrap-workspace/package/assets/templates/AGENTS.md.tmpl` | 开工识别与完成时更新清单 |
| `skills/bootstrap-workspace/package/assets/templates/README.md.tmpl` | 地图和入门步骤指向 INDEX |
| `skills/bootstrap-workspace/package/assets/templates/STATE.md.tmpl` | 不再要求用户先建第一个任务 |
| `skills/bootstrap-workspace/package/assets/templates/HISTORY.md.tmpl` | 初始化条目链到任务档案 |
| `skills/bootstrap-workspace/package/assets/templates/DECISIONS.md.tmpl` | 任务以档案为准、不以会话为边界 |
| `skills/bootstrap-workspace/package/SKILL.md` | Skill 工作流：清单、识别规则、接管盘点 |
| `skills/bootstrap-workspace/package/references/workspace-profiles.md` | 接管时把已有任务收进 INDEX |
| `skills/bootstrap-workspace/VERIFY.md` | 更新检查步骤和最近结果 |
| `skills/bootstrap-workspace/HISTORY.md` | 记录此次迭代 |

不改直播安装目录，不给本仓库自己加 `docs/tasks/INDEX.md`。

---

### Task 1: 写下会失败的脚手架测试

**Files:**
- Create: `tests/test_scaffold_workspace.py`
- Modify: `tests/test_install_skill.py`

- [ ] **Step 1: 新增 `tests/test_scaffold_workspace.py`**

```python
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
            today = date.today().isoformat()
            self.assertIn("docs/tasks/INDEX.md", result.stdout)
            self.assertIn("docs/tasks/TEMPLATE.md", result.stdout)
            self.assertIn(
                f"docs/tasks/{today}-initialize-workspace.md", result.stdout
            )
            self.assertFalse((workspace / "docs" / "tasks" / "INDEX.md").exists())

    def test_fresh_write_creates_task_tracking_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            run_scaffold(workspace)
            today = date.today().isoformat()
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
            today = date.today().isoformat()
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


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 扩展 `tests/test_install_skill.py` 的 dry-run 断言**

在 `test_installed_scaffold_dry_run` 末尾、`self.assertFalse((workspace / "AGENTS.md").exists())` 之前加入：

```python
            today = date.today().isoformat()
            self.assertIn("docs/tasks/INDEX.md", result.stdout)
            self.assertIn(
                f"docs/tasks/{today}-initialize-workspace.md", result.stdout
            )
```

并在文件顶部 import 区增加：

```python
from datetime import date
```

- [ ] **Step 3: 跑测试，确认失败**

Run:

```bash
python3 tests/test_scaffold_workspace.py -v
python3 tests/test_install_skill.py -v
```

Expected: `test_fresh_dry_run_lists_index_and_init_task` 因 stdout 不含 `docs/tasks/INDEX.md` 而 FAIL。`test_installed_scaffold_dry_run` 同样 FAIL。不要在这一步改脚手架去让测试通过。

- [ ] **Step 4: Commit（仅当用户要求提交）**

```bash
git add tests/test_scaffold_workspace.py tests/test_install_skill.py
git commit -m "$(cat <<'EOF'
test: require bootstrap scaffolding to create a task index

EOF
)"
```

---

### Task 2: 增加清单与初始化任务模板

**Files:**
- Create: `skills/bootstrap-workspace/package/assets/templates/INDEX.md.tmpl`
- Create: `skills/bootstrap-workspace/package/assets/templates/INDEX_STUB.md.tmpl`
- Create: `skills/bootstrap-workspace/package/assets/templates/INIT_TASK.md.tmpl`
- Modify: `skills/bootstrap-workspace/package/assets/templates/TASK_TEMPLATE.md.tmpl`

- [ ] **Step 1: 写入 `INDEX.md.tmpl`**

```markdown
# Task index

Living inventory of work tasks. Newest items first within each section. Do not copy task details here. `TEMPLATE.md` is not a task.

## In progress

- None.

## Paused

- None.

## Completed

- [Initialize workspace]({{DATE}}-initialize-workspace.md) — Establish durable, agent-neutral workspace context. Started {{DATE}}. Updated {{DATE}}.

## Cancelled

- None.
```

- [ ] **Step 2: 写入 `INDEX_STUB.md.tmpl`**

该文件不得包含 `{{` 占位符，也不得提到 `initialize-workspace.md`。

```markdown
# Task index

Living inventory of work tasks. Newest items first within each section. Do not copy task details here. `TEMPLATE.md` is not a task.

This file was added while adopting an existing workspace. Inventory existing `docs/tasks/*.md` files (except `TEMPLATE.md`) into the sections below. Use `Unverified` until the status is known; then move the item into one of the four status sections.

## In progress

- None.

## Paused

- None.

## Unverified

- None.

## Completed

- None.

## Cancelled

- None.
```

- [ ] **Step 3: 写入 `INIT_TASK.md.tmpl`**

```markdown
# Task: Initialize workspace

## Objective

Establish durable, agent-neutral workspace context.

## Inputs

- User request for workspace initialization
- Selected workspace profile and known project facts

## Outputs

- Core context files: `README.md`, `AGENTS.md`, `docs/PROJECT.md`, `docs/STATE.md`, `docs/HISTORY.md`, `docs/DECISIONS.md`, `docs/tasks/INDEX.md`, `docs/tasks/TEMPLATE.md`

## Constraints

- Create missing files only; do not overwrite existing user-authored files.
- Do not write secrets, credentials, or private raw data into context documents.

## Acceptance criteria

- Every path referenced by `AGENTS.md` exists.
- `docs/tasks/INDEX.md` lists this task as Completed.

## Progress

- Completed.
- {{DATE}}: Scaffolded the initial workspace context.

## Related sessions

- {{DATE}}: Workspace initialization.

## Related tasks

- None.

## Outcome

- Created the initial project context, current-state, history, decision, and task-document structure.

## Verification

- Confirmed that the initial context documents reference existing paths.
```

- [ ] **Step 4: 更新 `TASK_TEMPLATE.md.tmpl` 为完整文件**

```markdown
# Task: <short name>

## Objective

Describe the concrete outcome.

## Inputs

- List source files, links, issues, or data.

## Outputs

- List expected files, behavior, or decisions.

## Constraints

- Record boundaries, compatibility requirements, and prohibited changes.

## Acceptance criteria

- State observable checks that prove completion.

## Progress

- Not started.

## Related sessions

- Record the date and one sentence about what this session did. Do not paste chat transcripts.

## Related tasks

- None.

## Outcome

- When complete, record the final result and link to produced artifacts.

## Verification

- Record commands run, manual review performed, and checks that could not run.
```

- [ ] **Step 5: Commit（仅当用户要求提交）**

```bash
git add skills/bootstrap-workspace/package/assets/templates/INDEX.md.tmpl \
  skills/bootstrap-workspace/package/assets/templates/INDEX_STUB.md.tmpl \
  skills/bootstrap-workspace/package/assets/templates/INIT_TASK.md.tmpl \
  skills/bootstrap-workspace/package/assets/templates/TASK_TEMPLATE.md.tmpl
git commit -m "$(cat <<'EOF'
feat: add bootstrap task index and init-task templates

EOF
)"
```

---

### Task 3: 按是否已有 AGENTS.md 选择脚手架产物

**Files:**
- Modify: `skills/bootstrap-workspace/package/scripts/scaffold_workspace.py`

- [ ] **Step 1: 更新 `directory_map()` 中的任务相关行**

把现有的

```python
        "- `docs/tasks/TEMPLATE.md`：较大任务的记录模板。",
```

替换为：

```python
        "- `docs/tasks/INDEX.md`：任务总清单。",
        "- `docs/tasks/TEMPLATE.md`：任务档案模板。",
```

- [ ] **Step 2: 让 `build_plan` 接收 `target`，并按是否已有 `AGENTS.md` 选择模板**

将 `build_plan` 签名改为：

```python
def build_plan(
    args: argparse.Namespace, skill_root: Path, target: Path
) -> tuple[set[Path], list[PlannedFile]]:
```

在 `template_mapping` 里保留原有 README / AGENTS / PROJECT / STATE / HISTORY / DECISIONS / gitignore 映射。把原来的 `Path("docs/tasks/TEMPLATE.md"): "TASK_TEMPLATE.md.tmpl"` 换成下面逻辑，放在 `template_mapping` 建好之后、`files = [...]` 之前：

```python
    template_mapping[Path("docs/tasks/TEMPLATE.md")] = "TASK_TEMPLATE.md.tmpl"
    if (target / "AGENTS.md").exists():
        template_mapping[Path("docs/tasks/INDEX.md")] = "INDEX_STUB.md.tmpl"
    else:
        template_mapping[Path("docs/tasks/INDEX.md")] = "INDEX.md.tmpl"
        template_mapping[
            Path(f"docs/tasks/{values['DATE']}-initialize-workspace.md")
        ] = "INIT_TASK.md.tmpl"
```

`main()` 中的调用改为：

```python
        directories, files = build_plan(args, skill_root, target)
```

- [ ] **Step 3: 跑测试，确认文件创建相关断言已过，内容断言仍可能失败**

Run:

```bash
python3 tests/test_scaffold_workspace.py -v
```

Expected: `test_fresh_dry_run_lists_index_and_init_task`、`test_adopt_existing_agents_does_not_invent_init_task`、`test_adopt_does_not_overwrite_existing_index` PASS。`test_fresh_write_creates_task_tracking_files` 可能仍因 `AGENTS.md` 缺少 `IDENTIFY_RULE` 或 README/STATE/HISTORY 文案未改而 FAIL。不要在这一步为了过测试而弱化断言。

- [ ] **Step 4: Commit（仅当用户要求提交）**

```bash
git add skills/bootstrap-workspace/package/scripts/scaffold_workspace.py
git commit -m "$(cat <<'EOF'
feat: scaffold a task index and skip fake init tasks on adopt

EOF
)"
```

---

### Task 4: 更新生成的上下文模板

**Files:**
- Modify: `skills/bootstrap-workspace/package/assets/templates/AGENTS.md.tmpl`
- Modify: `skills/bootstrap-workspace/package/assets/templates/README.md.tmpl`
- Modify: `skills/bootstrap-workspace/package/assets/templates/STATE.md.tmpl`
- Modify: `skills/bootstrap-workspace/package/assets/templates/HISTORY.md.tmpl`
- Modify: `skills/bootstrap-workspace/package/assets/templates/DECISIONS.md.tmpl`

- [ ] **Step 1: 用下面全文替换 `AGENTS.md.tmpl`**

```markdown
# Workspace instructions

## Startup

Before making changes:

1. Read `README.md`.
2. Read `docs/PROJECT.md` for stable goals and scope.
3. Read `docs/STATE.md` for current progress, next actions, and blockers.
4. Read `docs/tasks/INDEX.md` and identify whether this request continues an unfinished task or starts a new one.
5. If it continues an unfinished task, read that task file. If it is a new work task, create `docs/tasks/YYYY-MM-DD-slug.md` from `docs/tasks/TEMPLATE.md`, add it to `INDEX.md`, and point `docs/STATE.md` at it before doing substantial work. If unsure, ask one question naming the closest existing task; do not ask whether to create a task system.
6. When resuming prior work or when current context is insufficient, read the newest relevant entries in `docs/HISTORY.md`.
7. If this is a Git workspace, inspect current status and preserve existing user changes.

Match on the intended outcome, not the session, date, or wording. The same task may span multiple sessions. Multiple tasks may be in progress at once. Do not create a task for pure questions, chat, explaining existing files, or when the user says not to record one. Once files will change or a deliverable will be produced, the work must belong to a task.

## Source-of-truth order

When project information conflicts, use this order:

1. The user's current explicit instruction.
2. The active task specification.
3. Executable contracts such as tests, schemas, and API definitions.
4. `docs/DECISIONS.md`.
5. `docs/PROJECT.md` and other maintained project documentation.
6. `README.md`.
7. Chat history and proprietary agent memory, which are non-authoritative caches.

## Workspace boundaries

{{DIRECTORY_RULES}}

## Change rules

- Preserve user-authored and unrelated changes.
- Do not invent commands, requirements, architecture, or acceptance criteria.
- Do not write secrets, credentials, or private data into documentation.
- Keep this file concise; link to canonical project documents instead of copying them.
- Update documentation when a change makes an existing statement false.

## Completion

Before reporting completion:

1. Run the smallest relevant validation that actually exists.
2. Review the changed-file scope.
3. Update the active task file, `docs/tasks/INDEX.md`, and `docs/STATE.md` when progress changed. If verification failed, keep the task In progress, record the gap, and do not mark it Completed.
4. When the work produced a meaningful outcome or reusable finding, add one concise entry to `docs/HISTORY.md` and link the task file; do not log routine conversation or private reasoning.
5. Record durable decisions in `docs/DECISIONS.md`.
6. Report changed files, verification results, unrun checks, and remaining issues.
```

- [ ] **Step 2: 更新 `README.md.tmpl` 的 Getting started 第 4 步，并确认 Directory map 由脚本注入 INDEX 行**

将

```markdown
4. Create a task specification under `docs/tasks/` before substantial work.
```

替换为：

```markdown
4. Read `docs/tasks/INDEX.md`. Continue an unfinished task in place, or create a new task file when the work goal changes.
```

其余章节保持不变。

- [ ] **Step 3: 用下面全文替换 `STATE.md.tmpl`**

```markdown
# Current state

Last updated: {{DATE}}

## Current objective

{{GOAL}}

## Completed

- Initialized the workspace context structure. See [`docs/tasks/{{DATE}}-initialize-workspace.md`](tasks/{{DATE}}-initialize-workspace.md).

## In progress

- None.

## Next actions

1. Add or identify the primary inputs.
2. Start the next concrete work task; record it in `docs/tasks/` when work begins.
3. Define exact validation commands or review criteria when the implementation approach is known.

## Blockers

- None recorded.

## Last verification

- Confirmed that the initial context documents reference existing paths.
```

- [ ] **Step 4: 更新 `HISTORY.md.tmpl` 的初始化条目**

```markdown
# Work history

This is a concise, reverse-chronological index of meaningful outcomes and reusable findings. Keep the newest entry first. Link to detailed task records, decisions, outputs, or commits instead of copying them. Do not paste chat transcripts, raw prompts, or private reasoning.

## {{DATE}} — Workspace context initialized

- **Task:** [Initialize workspace](tasks/{{DATE}}-initialize-workspace.md)
- **Result:** Created the initial project context, current-state, history, decision, and task-document structure.
- **Artifacts:** `README.md`, `AGENTS.md`, and `docs/` context files including `docs/tasks/INDEX.md`.
- **Verification:** Confirmed that the initial context documents reference existing paths.
- **Follow-up:** Begin the next real work task when ready; record it in `docs/tasks/INDEX.md`.
```

- [ ] **Step 5: 在 `DECISIONS.md.tmpl` 末尾追加**

```markdown

## {{DATE}} — Record work as tasks in docs/tasks

**Decision:** Track each work task as a file under `docs/tasks/` and list it in `docs/tasks/INDEX.md`. Do not treat a chat session as the task boundary. The same task may span multiple sessions.

**Reason:** Work needs to be resumable across agents and sessions without relying on chat memory or a user reminder to start a task list.
```

保留文件原有三条决策，不要删除。

- [ ] **Step 6: 跑脚手架测试和安装测试**

Run:

```bash
python3 tests/test_scaffold_workspace.py -v
python3 tests/test_install_skill.py -v
```

Expected: 全部 PASS。若 `test_fresh_write_creates_task_tracking_files` 仍失败，对照断言字符串修正模板，不要改测试放宽规格。

- [ ] **Step 7: Commit（仅当用户要求提交）**

```bash
git add skills/bootstrap-workspace/package/assets/templates/AGENTS.md.tmpl \
  skills/bootstrap-workspace/package/assets/templates/README.md.tmpl \
  skills/bootstrap-workspace/package/assets/templates/STATE.md.tmpl \
  skills/bootstrap-workspace/package/assets/templates/HISTORY.md.tmpl \
  skills/bootstrap-workspace/package/assets/templates/DECISIONS.md.tmpl
git commit -m "$(cat <<'EOF'
feat: teach bootstrapped workspaces to auto-record work tasks

EOF
)"
```

---

### Task 5: 更新 Skill 工作流与接管规则

**Files:**
- Modify: `skills/bootstrap-workspace/package/SKILL.md`
- Modify: `skills/bootstrap-workspace/package/references/workspace-profiles.md`
- Modify: `tests/test_scaffold_workspace.py`

- [ ] **Step 1: 在 `tests/test_scaffold_workspace.py` 增加 Skill 正文断言**

```python
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
        self.assertIn("YYYY-MM-DD-initialize-workspace.md", text)
```

先跑这一条，确认 FAIL。

Run:

```bash
python3 tests/test_scaffold_workspace.py TestScaffoldWorkspace.test_skill_documents_task_identification_rules -v
```

Expected: FAIL，因为 `SKILL.md` 还没有这些句子。

- [ ] **Step 2: 更新 `SKILL.md` 第 3 节核心文件列表**

将

```markdown
- `docs/tasks/TEMPLATE.md` for task-level specifications.
```

替换为：

```markdown
- `docs/tasks/INDEX.md` for the living task inventory;
- `docs/tasks/TEMPLATE.md` for new task files;
- `docs/tasks/YYYY-MM-DD-initialize-workspace.md` on first initialization only, when `AGENTS.md` is being created.
```

- [ ] **Step 3: 在 `SKILL.md` 第 5 节「For an existing workspace」列表中追加**

```markdown
- if `docs/tasks/INDEX.md` was just created as a stub, inventory existing `docs/tasks/*.md` files except `TEMPLATE.md`; mark unknown status as `Unverified` and do not invent an initialize-workspace task;
```

并在第 5 节 `HISTORY.md` 规则之后新增一节：

```markdown
### Task tracking after initialization

Before substantial work in a bootstrapped workspace, read `docs/tasks/INDEX.md` and `docs/STATE.md`, then decide:

- Continue: the requested outcome matches an unfinished task (In progress or Paused). Open that file. Do not create a new file because the session changed.
- Start: the requested outcome matches no unfinished task. Create `docs/tasks/YYYY-MM-DD-slug.md` from `TEMPLATE.md` with Progress `In progress`, add it to `INDEX.md`, and point `STATE.md` at it. Do not ask whether to create a task.
- Unsure: ask one question naming the closest existing task; do not ask whether to create a task system.

Match on the intended outcome, not the session, date, or wording. Multiple tasks may be in progress at once. Skip a task file for pure questions, chat, explaining existing files, or when the user says not to record one. Once files will change or a deliverable will be produced, the work must belong to a task.

If the user says this continues prior work but no matching file exists, create one and note in Progress that it was created from a continuation request. If one request contains two independent outcomes, split them; create the primary task first and list the other in `INDEX.md` and `STATE.md` next actions.

When completing a task, update the task file, move it to Completed in `INDEX.md`, and sync `STATE.md`. Keep it In progress when verification failed. Add `HISTORY.md` only for a meaningful outcome, and link the task file. If `INDEX.md` and the task file disagree, trust the task file and repair `INDEX.md` and `STATE.md`. Never write secrets, bills, therapy transcripts, or conversation transcripts into task files.
```

- [ ] **Step 4: 更新 `SKILL.md` 第 7 节确认项**

在 “every path referenced by `AGENTS.md` exists” 之后增加：

```markdown
- `docs/tasks/INDEX.md` exists and `TEMPLATE.md` is not listed as a task;
- a first-initialization workspace lists `docs/tasks/YYYY-MM-DD-initialize-workspace.md` as Completed;
- `AGENTS.md` tells agents to identify whether a request continues an unfinished task or starts a new one;
```

- [ ] **Step 5: 在 `workspace-profiles.md` 的 Adoption rules 列表末尾追加**

```markdown
- If `docs/tasks/` already contains task files, do not overwrite them. Create a missing `INDEX.md` only as a stub and inventory existing task files into it.
```

- [ ] **Step 6: 跑全部相关测试**

Run:

```bash
python3 tests/test_scaffold_workspace.py -v
python3 tests/test_install_skill.py -v
```

Expected: 全部 PASS。`test_all_packages_have_portable_skill_entry` 仍确认 package 内无 `/Users/beibei`。

- [ ] **Step 7: Commit（仅当用户要求提交）**

```bash
git add skills/bootstrap-workspace/package/SKILL.md \
  skills/bootstrap-workspace/package/references/workspace-profiles.md \
  tests/test_scaffold_workspace.py
git commit -m "$(cat <<'EOF'
docs: require bootstrap-workspace to auto-identify work tasks

EOF
)"
```

---

### Task 6: 更新 Skill 档案与仓库状态

**Files:**
- Modify: `skills/bootstrap-workspace/VERIFY.md`
- Modify: `skills/bootstrap-workspace/HISTORY.md`
- Modify: `docs/STATE.md`
- Modify: `docs/HISTORY.md`
- Modify: `docs/DECISIONS.md`

- [ ] **Step 1: 更新 `VERIFY.md` 的检查步骤**

在现有安装测试步骤中增加：

```markdown
2. 运行：

```bash
python3 tests/test_install_skill.py -v
python3 tests/test_scaffold_workspace.py -v
```

3. 空目录脚手架 dry-run / 实际写入必须包含 `docs/tasks/INDEX.md`、`docs/tasks/TEMPLATE.md`、`docs/tasks/当天日期-initialize-workspace.md`。
4. 已有 `AGENTS.md` 的目录不得被覆盖，也不得新增 initialize-workspace 任务；缺 INDEX 时只补 stub。
```

将「最近结果」日期改为实施当天，结果写实际测试输出。未运行检查仍包括：未覆盖直播安装目录、未对真实私人项目做非 dry-run 试跑。

- [ ] **Step 2: 在 `skills/bootstrap-workspace/HISTORY.md` 顶部增加一条**

```markdown
## {{TODAY}} — 初始化即带任务清单，并自动识别新任务

- **任务：** 初始化时创建 `docs/tasks/INDEX.md` 和初始化任务档案；后续按工作目标续做或新建。
- **结果：** 脚手架首次初始化写入清单与 init 任务；接管已有工作区只补 stub INDEX。`AGENTS.md` 与 `SKILL.md` 写入识别规则。
- **验证：** `python3 tests/test_scaffold_workspace.py -v` 与 `python3 tests/test_install_skill.py -v` 通过；未覆盖直播安装目录。
- **后续：** 用户明确要求后再用 `scripts/install_skill.py` 更新本机 Cursor / Codex。
```

把 `{{TODAY}}` 换成实施当天的 ISO 日期，不要把占位符写进仓库。

- [ ] **Step 3: 更新仓库 `docs/STATE.md`**

- Current objective：无进行中的 `bootstrap-workspace` 规格工作。
- Completed：增加「bootstrap-workspace 初始化即带任务清单与自动建档」。
- In progress：无。
- Next actions：本机安装需用户明确要求；其它按需项保持新建 Skill、记账试跑、早期清单分流。
- Last verification：写入本轮两个测试命令的通过结果。

- [ ] **Step 4: 在 `docs/HISTORY.md` 顶部增加对应成果条目**，Task 链到规格 `docs/superpowers/specs/2026-09-22-bootstrap-workspace-task-tracking-design.md` 和本计划。

- [ ] **Step 5: 在 `docs/DECISIONS.md` 顶部增加**

```markdown
## {{TODAY}} — 工作区任务按工作目标建档，不以会话为边界

**Decision:** `bootstrap-workspace` 初始化必须生成 `docs/tasks/INDEX.md`。之后 Agent 按工作目标自动续做或新建 `docs/tasks/YYYY-MM-DD-slug.md`，同一任务可跨会话。不按聊天会话建任务，也不再要求用户提醒「需要一个 task 记录清单」。

**Reason:** 用户确认初始化后每次新工作任务都要自动记录；换会话继续同一件事时应更新原档案。
```

把 `{{TODAY}}` 换成实施当天日期。

- [ ] **Step 6: 最终回归**

Run:

```bash
python3 tests/test_scaffold_workspace.py -v
python3 tests/test_install_skill.py -v
```

Expected: 全部 PASS。Git 状态中无直播 Skills 目录、无 `local/`、无密钥文件。

- [ ] **Step 7: Commit（仅当用户要求提交）**

```bash
git add skills/bootstrap-workspace/VERIFY.md \
  skills/bootstrap-workspace/HISTORY.md \
  docs/STATE.md docs/HISTORY.md docs/DECISIONS.md
git commit -m "$(cat <<'EOF'
docs: record bootstrap-workspace task-tracking iteration

EOF
)"
```

---

## Spec coverage

| 规格要求 | 任务 |
|---|---|
| 初始化创建 INDEX、TEMPLATE、initialize-workspace 任务 | Task 2–3 |
| 接管不覆盖、不伪造 init 任务、补 stub INDEX / Unverified | Task 2–3 |
| AGENTS 识别续做 / 新开 / 问一句 | Task 4–5 |
| README / STATE / HISTORY / DECISIONS 口径 | Task 4 |
| 任务档案增加 Related sessions / Related tasks | Task 2 |
| 新任务从 In progress 起记；验证失败保持进行中 | Task 4–5 |
| 敏感内容不入库 | Task 5（SKILL 约束；测试禁止 `/Users/beibei`） |
| 安装测试 + 脚手架写入/接管测试 | Task 1、3、4、6 |
| 不覆盖直播安装、不改造本仓库为示例工作区 | File map 与 Task 6 |

## 实施后请用户确认

是否把更新后的 `bootstrap-workspace` 安装到本机 Cursor / Codex。默认不安装。
