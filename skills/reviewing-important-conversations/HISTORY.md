# reviewing-important-conversations 维护历史

按日期倒序记录该 Skill 的重要试跑、更新、失败和修复。不保存聊天转录或私人原始数据。

## 2026-10-22 — 0.2.0：使用前检查 GitHub 新版

- **任务：** 与 `bootstrap-workspace` 一致，每次使用先运行 `scripts/check_update.py` 对比 GitHub `main` 上的版本，有新版时告知版本、改动与更新方法，不自动更新。
- **结果：** 新增 `VERSION`（0.2.0）、`CHANGELOG.md`、`update.json`、`scripts/check_update.py`；`SKILL.md` 增加「使用前：检查新版」。
- **验证：** `python3 tests/test_check_update.py -v` 校验版本三处一致、配置指向本包、检查脚本与其他 Skill 完全一致。
- **安装：** 已更新本机 Cursor 与 Codex，安装后与 package 一致。

## 2026-09-12 — 收成可安装包

- **任务：** 把规则和模板收入 `package/`。
- **结果：** 收录 `SKILL.md` 与 `templates.md`，不收录沟通原文。
- **验证：** 安装脚本测试覆盖该 Skill；未覆盖直播安装目录。
- **后续：** 需要时运行安装脚本同步到 Cursor。

## 2026-09-12 — 纳入个人 Skills 管理仓库

- **任务：** 将重要沟通复盘 Skill 登记为独立维护档案。
- **结果：** 确认 Cursor 入口与 `templates.md` 可读；记录与心理咨询 Skill 的分流、可相互引用条件，以及不保存沟通原文的边界。
- **验证：** 完整 `SKILL.md` 可读，核心原则、权力关系和完成前核对存在；独立源项目待核验；未进行真实沟通材料试跑。
- **后续：** 确认独立来源、版本、沟通复盘工作区位置，以及一次不把原文写入本仓库的真实试跑记录。
