# 陈贝贝个人 Skills 管理仓库

这是陈贝贝个人 Skills 的统一入口：以后新 Skill 也在这里创建、登记、收包和迭代；同时用于核验、安装、迁移和恢复已跑通的 Skills。已收包 Skill 都以 `skills/<id>/package/` 为权威来源。

主版本源（私有）：https://github.com/BEIBEICSY/personal-skills-system

安装：

```bash
python3 scripts/install_skill.py bootstrap-workspace --host cursor
python3 scripts/install_skill.py reviewing-therapy-transcripts --host cursor
python3 scripts/install_skill.py reviewing-important-conversations --host cursor
python3 scripts/install_skill.py bill-to-suishouji --host codex
```

## 当前基线

当前已登记的自制 Skill 都有独立维护档案：

- 工作区启动：[`bootstrap-workspace`](skills/bootstrap-workspace/)
- 心理咨询复盘：[`reviewing-therapy-transcripts`](skills/reviewing-therapy-transcripts/)
- 重要沟通复盘：[`reviewing-important-conversations`](skills/reviewing-important-conversations/)
- 记账：[`bill-to-suishouji`](skills/bill-to-suishouji/)

详细状态见 [`SKILLS.md`](SKILLS.md)。原始想法与收敛过程见 [`2026-05-25-ai-skills-environment-inventory.md`](2026-05-25-ai-skills-environment-inventory.md)。

## 维护闭环

1. 登记：在 `skills/<skill-id>/` 记录用途、来源、安装入口、依赖和敏感边界。
2. 核验：确认文件存在、触发描述准确，并运行适合该 Skill 的检查。
3. 使用：通过真实任务试跑，记录问题和人工介入点。
4. 迭代：只在权威规则源中修改，再同步安装版本。
5. 恢复：保留重装、迁移和兼容性说明，不记录明文凭证。

## Workspace map

- `SKILLS.md`：个人自制 Skills 总表与登记规则。
- `skills/<skill-id>/`：单个 Skill 的独立维护档案。
- `skills/<skill-id>/package/`：已收包 Skill 的可安装内容。
- `scripts/install_skill.py`：把 package 安装或更新到 Agent Skills 目录。
- `templates/skill-record/`：新增 Skill 时复制的档案模板。
- `AGENTS.md`：所有 Agent 共用的项目操作规则。
- `docs/PROJECT.md`：稳定目标、范围和完成标准。
- `docs/STATE.md`：当前状态、下一步与待核验项。
- `docs/HISTORY.md`：重要成果与验证记录。
- `docs/DECISIONS.md`：长期有效的项目决策。
- `docs/tasks/`：较大维护任务的任务卡。
- `scripts/`：后续用于盘点、校验或同步的可复现脚本。
- `local/`：本机路径覆盖或扫描结果，不提交 Git。

## 开始工作

先读 `docs/PROJECT.md`、`docs/STATE.md` 和 `SKILLS.md`。新建 Skill 时复制 `templates/skill-record/`；修改已有 Skill 前，再读取该 Skill 的维护档案、权威 `SKILL.md` 和相关测试。
