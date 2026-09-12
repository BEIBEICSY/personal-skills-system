# bill-to-suishouji 验证

## 检查范围

- 确认 `package/SKILL.md`、脚本、分类体系和测试文件存在。
- 确认 package 不含本机绝对路径、原始账单或 checks 原文。
- 确认安装脚本只复制 package。

## 检查步骤

1. 读取 `skills/bill-to-suishouji/package/SKILL.md`。
2. 确认 `scripts/`、`references/分类体系.md` 和两个测试文件存在。
3. 运行 `python3 tests/test_install_skill.py -v`。

## 最近结果

- 日期：2026-09-12
- 结果：已收包；本机路径和 soffice 绝对路径已去掉
- 证据：安装测试覆盖该 Skill；未复制 `inputs/raw` 或 `checks/` 账单文件。

## 未运行检查

- 未在 package 目录运行 `python3 -m unittest tests/test_fill_suishouji.py tests/test_merge_bills.py`。
- 未做真实账单导入试跑。
- 未覆盖直播 Codex 安装目录。
