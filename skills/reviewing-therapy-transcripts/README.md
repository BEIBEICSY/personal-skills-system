# reviewing-therapy-transcripts

根据心理咨询逐字稿生成证据分层、非诊断性的咨询复盘。

## 用途与场景

- 适用场景：用户提供心理咨询或治疗逐字稿，并要求总结、复盘、咨询笔记或下次咨询准备。
- 不适用场景：不用于诊断、人格定性，也不把工作假设写成事实。老板、同事、朋友或家庭等非咨询沟通改用 [`reviewing-important-conversations`](../reviewing-important-conversations/)。
- 维护边界：可安装内容在 [`package/`](package/)。不保存逐字稿、咨询笔记原文或其他私人咨询内容。不得与沟通复盘脉络同时更新；用户明确允许且来源确实相关时可以相互引用，但不自动复制、合并或把一套结论归入另一套。

## 当前状态

- 状态：已收包，可安装
- 分类：个人支持 / 心理咨询复盘
- 所有权：个人自制
- 权威来源：本仓库 `skills/reviewing-therapy-transcripts/package/`
- 维护档案：
  - [清单](manifest.yaml)
  - [验证](VERIFY.md)
  - [恢复](RESTORE.md)
  - [维护历史](HISTORY.md)

## 安装或更新

```bash
python3 scripts/install_skill.py reviewing-therapy-transcripts --host cursor
```

## 导航

- 全局索引：[`SKILLS.md`](../../SKILLS.md)
- 可安装入口：[`package/SKILL.md`](package/SKILL.md)
