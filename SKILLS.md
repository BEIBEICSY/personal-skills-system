# 个人 Skills 总表

最后核验：2026-10-22

本表是陈贝贝个人 Skills 管理仓库的全局索引。优先登记自己制作、深度定制或承担长期个人工作流的 Skills。详细维护信息以 `skills/<skill-id>/` 为准。第三方通用 Skills、插件和 MCP 可以作为依赖登记，但不自动算作“自己的 Skill”。

## 当前自制 Skills

| Skill | 场景分类 | 当前状态 | 权威来源 / 项目 | 当前安装入口 | 本轮核验 | 下一步 |
|---|---|---|---|---|---|---|
| [`bootstrap-workspace`](skills/bootstrap-workspace/) | 工作基础设施 / 工作区启动 | 已收包，可安装 | 本仓库 `skills/bootstrap-workspace/package/` | Cursor `~/.cursor/skills/bootstrap-workspace/SKILL.md`；Codex `~/.codex/skills/bootstrap-workspace/SKILL.md` | 0.4.0；2026-10-22 脚手架、安装与更新检查测试通过；已覆盖本机 Cursor / Codex | 待真实工作试跑「跟进已完成任务」询问规则 |
| [`reviewing-therapy-transcripts`](skills/reviewing-therapy-transcripts/) | 个人支持 / 心理咨询复盘 | 已收包，可安装 | 本仓库 `skills/reviewing-therapy-transcripts/package/` | `~/.cursor/skills/reviewing-therapy-transcripts/SKILL.md` | 0.2.0；安装与更新检查测试通过；已更新本机 Cursor；未收录逐字稿 | 按需继续迭代 |
| [`reviewing-important-conversations`](skills/reviewing-important-conversations/) | 个人支持 / 重要沟通复盘 | 已收包，可安装 | 本仓库 `skills/reviewing-important-conversations/package/` | `~/.cursor/skills/reviewing-important-conversations/SKILL.md` | 0.2.0；安装与更新检查测试通过；已更新本机 Cursor / Codex；含 `templates.md`，未收录沟通原文 | 按需继续迭代 |
| [`bill-to-suishouji`](skills/bill-to-suishouji/) | 生活管理 / 个人记账 | 已收包，可安装 | 本仓库 `skills/bill-to-suishouji/package/` | `~/.codex/skills/bill-to-suishouji/SKILL.md` | 0.2.0；安装、更新检查与包内 20 个 unittest 通过；本机 Codex 仍是收包前旧版 | 决定是否切换到新版，并用 `SUISHOUJI_WORKBENCH` 真实试跑 |

## 每个 Skill 的登记字段

后续新增或维护 Skill 时，先复制 `templates/skill-record/`，至少记录：

- 名称与一句话用途
- 工作 / 生活 / 通用分类
- 自制、深度定制或外部依赖的归属
- 权威来源与安装入口
- 支持的 Agent / 客户端
- 依赖的插件、MCP、账号或运行环境
- 敏感数据边界
- 版本或最后更新时间
- 最近一次真实任务试跑
- 校验命令或人工检查标准
- 安装、迁移和恢复步骤
- 当前负责人和下一步

## 后续资产池

以下项目来自早期清单，尚未按“自制 Skill / 外部能力 / 环境依赖”完成重新分类：

- 金山文档 Skills
- Superpowers Skills
- TickTick / 滴答清单 MCP
- Codex、Cursor、Chrome、WPS 等客户端插件
- `AGENTS.md`、Cursor rules 与个人偏好配置
- 账号授权和环境变量位置（只记用途与位置，不记明文）

## 状态口径

- `已收包，可安装`：本仓库已有 `package/`，可通过 `scripts/install_skill.py` 安装或更新；不等于已覆盖直播安装目录，也不等于真实任务已回归。
- `已安装，入口可读`：本轮已确认目标 Agent 安装入口存在且可读取；不等于所有真实任务都已回归通过。
- `已验证`：除入口可读外，还完成了该 Skill 规定的测试或真实任务检查。
- `待核验`：来自用户确认或历史记录，但本轮没有找到足够证据确认位置或可用性。
- `失效`：已经确认当前入口、依赖或关键流程不可用，并记录了证据。
