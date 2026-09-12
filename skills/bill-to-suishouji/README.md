# bill-to-suishouji

将支付宝、微信账单清洗并写入随手记导入模板。

## 用途与场景

- 适用场景：把支付宝 / 微信账单或已合并账单转成随手记导入 xls，并按个人分类和账户体系处理。
- 不适用场景：不要用本仓库保存账单、导入文件或账户明细。
- 维护边界：可安装内容在 [`package/`](package/)，包括规则和脚本。原始账单只放本地工作台。

## 当前状态

- 状态：已收包，可安装
- 分类：生活管理 / 个人记账
- 所有权：个人自制
- 权威来源：本仓库 `skills/bill-to-suishouji/package/`
- 维护档案：
  - [清单](manifest.yaml)
  - [验证](VERIFY.md)
  - [恢复](RESTORE.md)
  - [维护历史](HISTORY.md)

## 安装或更新

```bash
python3 scripts/install_skill.py bill-to-suishouji --host codex
```

工作台目录用 `SUISHOUJI_WORKBENCH` 指向本地 `inputs/`、`outputs/`、`checks/`，不要放进本仓库。

## 导航

- 全局索引：[`SKILLS.md`](../../SKILLS.md)
- 可安装入口：[`package/SKILL.md`](package/SKILL.md)
