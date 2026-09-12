# 个人 Skills 系统

这是属于贝贝自己的 Skills 能力资产库，用来盘点、维护、验证和迁移个人制作的 Skills，让已经跑通的能力能够持续迭代，并在更换 Agent、客户端、账号或电脑时恢复。

## 当前基线

第一版从三个真实 Skill 出发：

- 工作区启动：`bootstrap-workspace`
- 心理咨询：名称与位置待核验
- 记账：`bill-to-suishouji`

详细状态见 [`SKILLS.md`](SKILLS.md)。原始想法与收敛过程见 [`2026-05-25-ai-skills-environment-inventory.md`](2026-05-25-ai-skills-environment-inventory.md)。

## 维护闭环

1. 登记：记录用途、来源、安装入口、依赖和敏感边界。
2. 核验：确认文件存在、触发描述准确，并运行适合该 Skill 的检查。
3. 使用：通过真实任务试跑，记录问题和人工介入点。
4. 迭代：只在权威规则源中修改，再同步安装版本。
5. 恢复：保留重装、迁移和兼容性说明，不记录明文凭证。

## Workspace map

- `SKILLS.md`：个人自制 Skills 总表与登记规则。
- `AGENTS.md`：所有 Agent 共用的项目操作规则。
- `docs/PROJECT.md`：稳定目标、范围和完成标准。
- `docs/STATE.md`：当前状态、下一步与待核验项。
- `docs/HISTORY.md`：重要成果与验证记录。
- `docs/DECISIONS.md`：长期有效的项目决策。
- `docs/tasks/`：较大维护任务的任务卡。
- `scripts/`：后续用于盘点、校验或同步的可复现脚本。

## 开始工作

先读 `docs/PROJECT.md`、`docs/STATE.md` 和 `SKILLS.md`。修改某个 Skill 前，再读取该 Skill 自己的 `SKILL.md`、权威项目文档和相关测试。
