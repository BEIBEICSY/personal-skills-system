# Task: bootstrap-workspace 强调外部输入先归档进任务

## Objective

初始化生成的规则必须强调：用户提供的文件即使在当前目录之外（桌面、下载、聊天附件），也要先归档到所属任务的 `inputs/`，再使用，避免用户删除原件后无法追溯。

## Inputs

- 用户要求（2026-10-22）。
- 前例：评级工作区 5 份桌面原件未归档，原件删除后相关链接失效。

## Outputs

- `AGENTS.md.tmpl` 新增「Archive inputs first」规则；`SKILL.md`、`TASK_TEMPLATE.md.tmpl`、README 目录说明同步。
- 版本升为 0.4.0，CHANGELOG 与 manifest 同步。

## Constraints

- 默认复制、不移动；用户明确要求时才移动工作区外的文件。
- 不覆盖已有归档；归档后核对 SHA-256。

## Acceptance criteria

- 生成的 `AGENTS.md`、`README.md`、`tasks/TEMPLATE.md` 含归档规则与登记字段，并有测试覆盖。
- 全部测试通过，安装副本与 package 一致，更新检查显示 `up-to-date`。

## Progress

- Completed.
- 2026-10-22：默认复制而非移动，理由是移动会改动工作区外的用户文件。

## Outcome

- 0.4.0：`AGENTS.md.tmpl` 新增 `Archive inputs first`；`SKILL.md`、`TASK_TEMPLATE.md.tmpl`、README 目录说明（`scaffold_workspace.py`）同步；CHANGELOG、manifest、决策与历史已更新。

## Verification

- `python3 tests/test_scaffold_workspace.py -v`、`test_check_update.py -v`、`test_install_skill.py -v` 全部通过。
- 实际生成 content 工作区，人工检查 `AGENTS.md` 归档规则与任务模板登记字段。
- 安装到本机 Cursor / Codex 后与 package 一致；推送后更新检查见下一条提交记录。
