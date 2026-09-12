# bootstrap-workspace

初始化或接管本地 / GitHub 工作区，建立唯一的 `AGENTS.md` 和持久项目上下文。

## 用途与场景

- 适用场景：新建空工作区、接管已有项目、补齐项目上下文，或在更换 Agent 后修复冲突的操作规则。
- 不适用场景：不要用它复制私人原始数据，也不要用它接管其他 Skill 的源码。
- 维护边界：本目录只保存管理档案。权威源码仍在独立项目或当前安装目录，本仓库不复制源码。

## 当前状态

- 状态：已安装，入口可读
- 分类：工作基础设施 / 工作区启动
- 所有权：个人深度定制
- 维护档案：
  - [清单](manifest.yaml)
  - [验证](VERIFY.md)
  - [恢复](RESTORE.md)
  - [维护历史](HISTORY.md)

## 导航

- 全局索引：[`SKILLS.md`](../../SKILLS.md)
- 权威来源：当前以安装目录为准，独立源项目待核验
- 当前安装入口：`/Users/beibei/.codex/skills/bootstrap-workspace/SKILL.md`
