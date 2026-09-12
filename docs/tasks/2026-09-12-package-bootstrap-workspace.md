# Task: 将 bootstrap-workspace 收成可安装包

## Objective

把仓库决策改为「可安装、可迭代」，并以 `bootstrap-workspace` 作为第一份可分享、可更新的 Skill 包。

## Inputs

- `/Users/beibei/.codex/skills/bootstrap-workspace/`
- 现有 `skills/bootstrap-workspace/` 管理档案

## Outputs

- `skills/bootstrap-workspace/package/`
- `scripts/install_skill.py`
- `tests/test_install_skill.py`
- 更新后的决策、总表和恢复说明

## Constraints

- 不把本机绝对路径、凭证或私人数据写入 package。
- 不自动覆盖当前已安装的 Codex / Cursor Skill，除非用户明确要求安装。
- 管理档案与可安装包分离。

## Acceptance criteria

- package 含 `SKILL.md` 且不含 `/Users/beibei`。
- 安装脚本能把 package 拷到临时目录，且不拷贝 `manifest.yaml`。
- 安装后的 `scaffold_workspace.py --dry-run` 可运行。

## Progress

- Completed on 2026-09-12.

## Outcome

- `bootstrap-workspace` 现在以本仓库 `package/` 为权威来源，可通过 `scripts/install_skill.py` 安装或更新。

## Verification

- `python3 tests/test_install_skill.py -v`：3 passed。
- 未对直播 `~/.codex/skills/bootstrap-workspace` 执行覆盖安装。
