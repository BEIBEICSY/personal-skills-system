# Task: bootstrap-workspace 改为任务文件夹结构

## Objective

让初始化后的工作区按「一件事一个文件夹」组织：`tasks/YYMMDD-任务描述/` 内含 `TASK.md`、`inputs/`、`work/`、`outputs/`，任务、原件、过程稿、成品能一眼对应。

## Inputs

- 用户反馈：评级工作区产出无命名规范、难以映射；看不懂一级目录用途。
- 设计：[2026-10-22 任务文件夹结构设计](../superpowers/specs/2026-10-22-bootstrap-workspace-task-folders-design.md)

## Outputs

- 更新 `skills/bootstrap-workspace/package/` 的 `SKILL.md`、脚手架和模板。
- 更新 `tests/test_scaffold_workspace.py`、`tests/test_install_skill.py`。

## Constraints

- 已有工作区不自动迁移；先出对照表，用户确认后再移动。
- 不改本仓库自身的 `docs/tasks/` 布局。
- 未经用户同意不覆盖本机 Cursor / Codex 安装。

## Acceptance criteria

- 见设计文档「验收」一节。

## Progress

- Completed.
- 2026-10-22：用户确认按任务分文件夹，任务内再分 inputs/work/outputs；补充「跟进已完成任务时询问新建还是续记」规则；评级工作区迁移需先出对照表。
- 2026-10-22：Skill 包、模板、profile 参考与测试已更新，测试通过。剩余：更新本机 Cursor / Codex 安装（待用户同意）；评级工作区迁移对照表。
- 2026-10-22：用户同意后安装到本机 Cursor / Codex。用户确认对照表（切入判断单独成任务、初稿合为一个任务、ZIP 留作独立任务）后完成评级工作区迁移。迁移中发现指向工作区外的链接需重算层级，已补入 `SKILL.md` 并重装。

## Outcome

- Skill 包已完成改造：`skills/bootstrap-workspace/package/`。
- 维护档案：`skills/bootstrap-workspace/HISTORY.md`、`VERIFY.md`。
- 本机安装：`~/.cursor/skills/bootstrap-workspace/`、`~/.codex/skills/bootstrap-workspace/`。
- 评级工作区（`20_Personal_Projects/20260920-评级/`）已迁移为 14 个任务文件夹加 `shared/`，并有 `tasks/INDEX.md`。

## Verification

- `python3 tests/test_scaffold_workspace.py -v`：8 passed。
- `python3 tests/test_install_skill.py -v`：4 passed。
- 对评级工作区 `--dry-run`：输出 `Legacy layout detected`，未写入任何文件。
- 安装后与源 `package/` 逐文件比对一致（diff -rq）。
- 评级迁移：483 个文件全部对应到新位置，非 Markdown 文件 SHA-256 一致；201 个相对链接中 194 个可打开，7 个指向桌面上已不存在的 5 份原件（迁移前即缺失，已记入该工作区 STATE）。
- 未运行：真实工作中的「已完成任务跟进」询问规则试跑。
