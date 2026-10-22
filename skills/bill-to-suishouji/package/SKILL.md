---
name: bill-to-suishouji
description: Use when the user wants to turn Alipay/WeChat bills or a merged bill into a Suishouji import xls, apply this personal Suishouji category/account system, handle refunds, remind manual supplements, adjust manual-reviewed categories/remarks, or continue the personal bookkeeping workflow.
---

# 随手记记账

把支付宝、微信账单清洗合并后写入随手记导入模板。

规则和脚本以**本 Skill 安装目录**为准：`scripts/merge_bills.py`、`scripts/fill_suishouji.py`、`references/分类体系.md`、`references/classification-rules.md`。分类和账户只维护 `references/分类体系.md` 这一份正式文件。

原始账单、导入结果和校对报告放在用户指定的**本地工作台**，不要写入 Skills 管理仓库。工作台可用环境变量 `SUISHOUJI_WORKBENCH`；未设置时先询问用户。LibreOffice 可执行文件可用 `SUISHOUJI_SOFFICE` 覆盖，默认查找 `soffice`。

## 使用前：检查新版

每次使用本 Skill，先解析其安装目录并运行：

```bash
python3 <skill-directory>/scripts/check_update.py
```

脚本用 Git 和用户已有凭据，对比本机 `VERSION` 与 `update.json` 指定的 GitHub 分支上的版本。按 `status` 处理：

- `up-to-date`：不提示，直接继续。
- `update-available`：在开始其他工作前，告诉用户当前版本、最新版本、`changes` 中每个新版本的简要改动，以及 `update_steps`；询问现在更新还是先用当前版本继续。不自动更新。用户选择更新时，执行更新步骤后重新读取新的 `SKILL.md` 再继续。
- `ahead`：用一句话说明本机版本比 GitHub 新（多半尚未推送），然后继续。
- `unknown`：用一句话说明无法检查及原因，然后继续。

检查不得阻塞用户的工作，也不得输出或记录任何凭据。

## 资料入口

优先把资料整理到工作台目录：

| 文件类型 | 默认位置 |
|---|---|
| 支付宝 CSV、微信 XLSX 原始账单 | `inputs/raw/` |
| 已清洗合并账单 | `inputs/merged/` |
| 随手记模板 | `inputs/templates/template_suishouji.xls` |
| 分类与账户体系 | Skill 安装目录 `references/分类体系.md` |
| 生成的随手记导入文件 | `outputs/` |
| 人工校对文件、对比报告 | `checks/` |

如果用户给的是桌面或其他目录文件，先请求文件权限，再复制或读取处理。

## 标准流程

1. 读取本 skill 后，打开安装目录的 `references/分类体系.md`。处理表格时也使用 spreadsheet 工具/依赖。命令在工作台目录执行，`--` 后的脚本路径指向本 Skill 安装目录。
2. 如果用户提供支付宝和微信原始账单，先运行合并清洗：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 <skill-directory>/scripts/merge_bills.py \
  --alipay <支付宝csv> \
  --wechat <微信xlsx> \
  --output inputs/merged/合并账单_<日期范围>.xlsx \
  --report checks/账单清洗_<日期范围>.md
```

3. 如果用户已经提供合并账单，直接进入随手记写入。
4. 按用户给定的起始时间录入，起始时间必须包含该条记录。没有起始时间且无法从上下文判断时再询问。

```bash
PYTHONDONTWRITEBYTECODE=1 python3 <skill-directory>/scripts/fill_suishouji.py \
  --bills <合并账单xlsx> \
  --template <随手记模板xls> \
  --output outputs/随手记导入_<起止时间>.xls \
  --report checks/随手记录入_<日期>.md \
  --start "YYYY-MM-DD HH:MM:SS"
```

5. 生成 xls 后，必须先提醒用户检查账户是否准确，再让用户做手工分类校对。
6. 根据本次账单覆盖日期提醒手动补记：05 号前后工资收入、13 号左右公积金收入、05 号和 25 号左右房租支出。只提醒，不自动写入模板。
7. 在会话里告诉用户本次录入了哪些记录。记录很多时，可以给简洁列表，并指向 `checks/随手记录入_*.md` 的完整逐笔明细。
8. 如果用户提供人工校对后的 xls，要按用户要求同步分类、子分类、账户、备注等字段。只有用户明确要求“沉淀规则”时，才把这次人工调整写回规则；若用户说“不需要记录为调整准则”，不要更新分类准则。

## 必守规则

详细规则见 `references/classification-rules.md`；分类与账户名称必须以 `references/分类体系.md` 为准。

- 退款不进入新合并账单；能匹配到原支出的退款，要把退款和原支出一起抵消。
- 模板每个 sheet 的第 2 行是第一条示例数据，不是真实数据。输出真实数据前必须清空示例行；真实数据从第 2 行开始写入。没有真实数据的 sheet 也不能保留示例行。
- 只写支出、收入、转账这几个模板 sheet 需要的列；不要改模板列结构。
- 分类、子分类、账户名必须完全匹配 `references/分类体系.md`，不要创造新名称。
- 招商银行储蓄卡只映射为 `招行`，不要套用还款账户。
- 招商银行信用卡(6020)：交易日期在 6 月 15 日之前映射为 `招行7.2还款`；6 月 15 日当天及之后映射为 `招行8.2还款`。
- 微信零钱、空付款方式、`/` 默认映射为 `微信钱`；支付宝账户余额、支付宝小荷包、猫猫饭卡等映射为 `支付宝`。
- 手动补记提醒只根据日期范围提示，不代表这些项目已经写入导入文件。

## 校验

在 Skill 安装目录运行项目测试：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/test_fill_suishouji.py tests/test_merge_bills.py
```

交付前至少确认：

- 清洗报告中退款及被抵消原支出没有进入合并账单。
- 输出 xls 的支出/收入/转账 sheet 没有残留模板示例行。
- 账户名、分类名、子分类名均在当前分类体系内。
- 最终回复里包含输出文件、检查报告、账户检查提醒、手动补记提醒、本次录入记录摘要。
- 原始账单和导入结果没有写入 Skills 管理仓库。
