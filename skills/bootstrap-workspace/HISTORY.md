# bootstrap-workspace 维护历史

按日期倒序记录该 Skill 的重要试跑、更新、失败和修复。不保存聊天转录或私人原始数据。

## 2026-10-22 — 0.3.0：使用前检查 GitHub 新版

- **任务：** 用户要求每次使用时查询 GitHub 是否有新版，有则提示更新并告知新版内容。
- **结果：** 新增 `VERSION`、`CHANGELOG.md`、`update.json` 与 `scripts/check_update.py`；`SKILL.md` 第 0 步先运行检查，有新版时说明版本、改动和更新命令，不自动更新；检查失败不阻塞。与任务文件夹改造合并为 0.3.0。
- **验证：** `python3 tests/test_check_update.py -v` 7 passed；真实私有仓库可访问。
- **后续：** 推送到 `main` 后检查才能比较到 0.3.0；跑通后再推广到其他 Skill。

## 2026-10-22 — 改为一件事一个任务文件夹

- **任务：** 评级工作区产出命名混乱、任务与产物难以对应；用户看不懂一级目录用途。
- **结果：** 任务改为 `tasks/YYMMDD-<task-description>/`，内含 `TASK.md`、`inputs/`、`work/`、`outputs/`；成品命名 `<deliverable>-<草稿|定稿>`；跨任务资料放 `shared/`；跟进已完成任务时先问新建还是续记；README 用平实中文解释目录；旧布局只提示迁移，不混建。
- **验证：** `python3 tests/test_scaffold_workspace.py -v` 8 passed；`python3 tests/test_install_skill.py -v` 4 passed。
- **后续：** 已安装到本机 Cursor / Codex；评级工作区已迁移。迁移中补充规则：移动前记哈希、移动后核对，并重算指向工作区外的链接。

## 2026-10-20 — 任务文件名改为 YYMMDD-任务描述

- **任务：** 约束任务档案命名为 `YYMMDD-<task-description>`，描述取当前任务摘要。
- **结果：** 脚手架初始化任务与 `AGENTS.md` / `SKILL.md` 均改为该格式，不再使用 `YYYY-MM-DD-slug`。
- **验证：** `python3 tests/test_scaffold_workspace.py -v` 与 `python3 tests/test_install_skill.py -v`。
- **后续：** 用安装脚本覆盖本机 Cursor / Codex。

## 2026-09-22 — 初始化即带任务清单，并自动识别新任务

- **任务：** 初始化时创建 `docs/tasks/INDEX.md` 和初始化任务档案；后续按工作目标续做或新建。
- **结果：** 脚手架首次初始化写入清单与 init 任务；接管已有工作区只补 stub INDEX。`AGENTS.md` 与 `SKILL.md` 写入识别规则。
- **验证：** `python3 tests/test_scaffold_workspace.py -v` 与 `python3 tests/test_install_skill.py -v` 通过。
- **后续：** 按用户要求用 `scripts/install_skill.py` 更新本机 Cursor / Codex。

## 2026-09-12 — 收成可安装包

- **任务：** 把本仓库设为权威来源，并提供安装/更新脚本。
- **结果：** 新增 `package/` 与 `scripts/install_skill.py`。
- **验证：** `python3 tests/test_install_skill.py -v` 通过；未覆盖直播安装目录。
- **后续：** 需要时用安装脚本同步到 Cursor / Codex。

## 2026-09-12 — 纳入个人 Skills 管理仓库

- **任务：** 为工作区启动 Skill 建立独立维护档案。
- **结果：** 确认 Codex 安装入口可读，并记录用途、敏感边界和恢复步骤。
- **验证：** `SKILL.md` 可读，`name` 与 `description` 存在；独立源项目待核验；未运行脚手架预览。
- **后续：** 确认独立来源、版本和跨 Agent 兼容记录。
