# bill-to-suishouji 恢复

## 前置条件

- 已克隆 `https://github.com/BEIBEICSY/personal-skills-system`。
- 本机有 Python 3、openpyxl，以及 `soffice` 或 `SUISHOUJI_SOFFICE`。
- 另有本地工作台目录存放账单，不把账单写入本仓库。

## 安装或更新

```bash
python3 scripts/install_skill.py bill-to-suishouji --host codex
```

工作台示例：

```bash
export SUISHOUJI_WORKBENCH="$HOME/Documents/suishouji-workbench"
```

旧项目 `20260706-随手记记账` 可以继续当工作台，但规则以本仓库 package 为准。

## 恢复后验证

- 安装目录有 `SKILL.md`、`scripts/` 和 `references/分类体系.md`。
- 安装目录没有原始账单。
- 如需完整脚本回归，在安装目录运行 unittest。

## 人工介入点

- 分类体系和账户映射是个人规则，分享前要确认对方可以使用这套体系。
- 覆盖已有安装前，先确认没有未同步的本地改动。
