# Current state

Last updated: 2026-09-12

## Current objective

维护可迭代的个人 Skills 管理仓库：四个自制 Skill 都从本仓库安装和更新。

## Completed

- 将 2026-05-25 的“个人 AI 环境资产清单”想法转为 Personal 项目。
- 建立项目级 README、AGENTS、项目说明、状态、历史、决策和任务模板。
- 初始化本地 Git `main` 分支，并写入仓库设计与实施计划。
- 建立 `.gitignore` 与 `templates/skill-record/`。
- 为 `bootstrap-workspace`、`reviewing-therapy-transcripts`、`bill-to-suishouji` 建立独立维护档案。
- 将心理咨询 Skill 从“位置待核验”更新为已找到 Cursor 安装入口。
- 增补 `reviewing-important-conversations` 独立维护档案，并记录与心理咨询 Skill 的分流。
- 创建 GitHub 私有远程仓库并推送 `main`：`https://github.com/BEIBEICSY/personal-skills-system`。
- 将仓库决策改为可安装、可迭代，并以 `bootstrap-workspace` 作为第一份 package。
- 将其余三个自制 Skill 也收入 `package/`。

## In progress

- 按需把安装脚本同步到本机 Cursor / Codex。

## Next actions

1. 需要本机生效时，对四个 Skill 运行 `scripts/install_skill.py`。
2. 记账 Skill 指定 `SUISHOUJI_WORKBENCH` 后做一次真实试跑。
3. 把早期清单中的金山文档、Superpowers、TickTick MCP 等区分为“自制 Skill”与“外部依赖”。

## Blockers

- 无。直播安装目录尚未用新包覆盖，不影响仓库作为权威来源。

## Last verification

- 2026-09-12：确认 `/Users/beibei/.codex/skills/bootstrap-workspace/SKILL.md` 可读取。
- 2026-09-12：确认 `/Users/beibei/.cursor/skills/reviewing-therapy-transcripts/SKILL.md` 可读取，且基本边界、输出前自检存在。
- 2026-09-12：确认 `/Users/beibei/.cursor/skills/reviewing-important-conversations/SKILL.md` 与 `templates.md` 可读取，且核心原则、权力关系、完成前核对存在。
- 2026-09-12：确认 `/Users/beibei/.codex/skills/bill-to-suishouji/SKILL.md`、权威项目 README 和两个测试文件可读取。
- 2026-09-12：四个 Skill 的 `package/` 均已建立，且 package 内无 `/Users/beibei`。
- 2026-09-12：`python3 tests/test_install_skill.py -v` 通过。
- 2026-09-12：未覆盖直播 Codex / Cursor 安装目录。
- 2026-09-12：未运行记账完整 unittest，也未做私人逐字稿、真实账单或沟通材料试跑。
