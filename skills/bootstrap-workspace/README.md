# bootstrap-workspace

初始化或接管本地 / GitHub 工作区，建立唯一的 `AGENTS.md` 和持久项目上下文。

## 用途与场景

- 适用场景：新建空工作区、接管已有项目、补齐项目上下文，或在更换 Agent 后修复冲突的操作规则。
- 不适用场景：不要用它复制私人原始数据，也不要用它接管其他 Skill 的源码。
- 维护边界：可安装内容在 [`package/`](package/)。本目录的其他文件是管理档案，不会被安装脚本复制。

## 当前状态

- 状态：已收包，可安装
- 分类：工作基础设施 / 工作区启动
- 所有权：个人深度定制
- 权威来源：本仓库 `skills/bootstrap-workspace/package/`
- 维护档案：
  - [清单](manifest.yaml)
  - [验证](VERIFY.md)
  - [恢复](RESTORE.md)
  - [维护历史](HISTORY.md)

## 安装或更新

```bash
python3 scripts/install_skill.py bootstrap-workspace --host cursor
python3 scripts/install_skill.py bootstrap-workspace --host codex
```

先预览：

```bash
python3 scripts/install_skill.py bootstrap-workspace --host cursor --dry-run
```

## 导航

- 全局索引：[`SKILLS.md`](../../SKILLS.md)
- 可安装入口：[`package/SKILL.md`](package/SKILL.md)
- 当前本机 Codex 安装：`~/.codex/skills/bootstrap-workspace/SKILL.md`
