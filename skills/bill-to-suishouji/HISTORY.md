# bill-to-suishouji 维护历史

按日期倒序记录该 Skill 的重要试跑、更新、失败和修复。不保存聊天转录或私人原始数据。

## 2026-10-22 — 0.2.0：使用前检查 GitHub 新版

- **任务：** 与 `bootstrap-workspace` 一致，每次使用先运行 `scripts/check_update.py` 对比 GitHub `main` 上的版本，有新版时告知版本、改动与更新方法，不自动更新。
- **结果：** 新增 `VERSION`（0.2.0）、`CHANGELOG.md`、`update.json`、`scripts/check_update.py`；`SKILL.md` 增加「使用前：检查新版」。
- **验证：** `python3 tests/test_check_update.py -v` 校验版本三处一致、配置指向本包、检查脚本与其他 Skill 完全一致。
- **验证补充：** 首次在 package 内完整运行 `python3 -m unittest discover -s tests`，20 tests 通过。
- **安装：** 未更新。本机 Codex 安装仍是收包前的旧版（指向 `20260706-随手记记账` 项目，缺少支付宝理财转账等规则）；切换为新版需用户确认，并配合 `SUISHOUJI_WORKBENCH` 真实试跑。

## 2026-09-12 — 收成可安装包

- **任务：** 把规则和脚本收入 `package/`，账单仍留在本地工作台。
- **结果：** 收录脚本、分类体系和测试；去掉本机路径和 soffice 绝对路径；未收录原始账单。
- **验证：** 安装脚本测试覆盖该 Skill；未运行原项目完整 unittest。
- **后续：** 需要时安装到 Codex / Cursor，并用 `SUISHOUJI_WORKBENCH` 指向本地账单目录。

## 2026-09-12 — 纳入个人 Skills 管理仓库

- **任务：** 为随手记记账 Skill 建立独立维护档案。
- **结果：** 确认安装入口、权威项目和测试文件可读，并记录不保存账单的边界。
- **验证：** 入口、项目 README 与两个 unittest 文件可读；本轮未运行外部项目完整测试。
- **后续：** 补充版本、最近一次成功试跑，以及跨设备恢复时的路径覆盖方式。
