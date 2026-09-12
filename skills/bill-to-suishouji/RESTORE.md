# bill-to-suishouji 恢复

## 前置条件

- 已取得权威项目 `20260706-随手记记账`。
- 目标 Agent 的 Skills 目录可写。
- 不把账单、导入文件、账户明细或凭证复制进本管理仓库。

## 恢复步骤

1. 先恢复权威项目，确认 `README.md`、`references/分类体系.md`、`references/classification-rules.md` 和两个处理脚本存在。
2. 再安装入口文件到目标 Agent 的 Skills 目录。
3. 读取入口 `SKILL.md`，确认它指向权威项目。
4. 最后在权威项目目录运行项目测试，不把测试输入提交到本仓库。

## 恢复后验证

- 入口文件可读。
- 权威项目路径可访问。
- 在权威项目目录运行：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/test_fill_suishouji.py tests/test_merge_bills.py
```

## 人工介入点

- 本机绝对路径需要按设备改写。
- 真实账单只放在权威项目的 `inputs/`，不进入本仓库。
- 账户和分类名称必须以权威项目的分类体系为准。
