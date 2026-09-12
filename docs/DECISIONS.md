# Decisions

## 2026-09-12 — 本仓库同时负责 Skill 包的迭代与安装更新

**Decision:** 管理仓库不只保存清单。可分享的 Skill 以 `skills/<id>/package/` 为权威包；用 `scripts/install_skill.py` 安装或更新到各 Agent 的 Skills 目录。个人路径、Key 和私人原文仍不进仓库。

**Reason:** 后续要在同一套机制里迭代 Skill，并让自己或朋友拉取后能安装使用。

## 2026-09-12 — 先把 bootstrap-workspace 做成第一份可安装包

**Decision:** 第一个迁入 package 的 Skill 是 `bootstrap-workspace`。记账、咨询和沟通复盘仍先保留档案，等拆出可分享部分后再收包。

**Reason:** 工作区启动 Skill 通用、隐私少，适合验证安装和更新流程。

## 2026-09-12 — 采用一 Skill 一档案目录的混合型管理仓库

**Decision:** 每个 Skill 在 `skills/<skill-id>/` 拥有独立维护档案；`SKILLS.md` 只做全局摘要。已有独立权威项目的 Skill 继续在原项目维护源码，本仓库不复制、不接管。

**Reason:** 仓库目标是 Skills 的管理和更新机制，不是源码单体仓。独立档案能体现分别维护，又避免与现有项目形成双份真相。

## 2026-09-12 — 已收包的 Skill 以本仓库 package 为权威来源

**Decision:** 已收入 `package/` 的 Skill，以本仓库为权威来源；未收包的 Skill 仍以原项目或当前安装目录为准，不自动复制。

**Reason:** 避免所有 Skill 立刻形成双份源码，同时让已收包 Skill 可以在此迭代和分发。

## 2026-09-12 — GitHub 作为主版本源，默认私有

**Decision:** 本地 Git 使用 `main`。主版本源为私有仓库 `https://github.com/BEIBEICSY/personal-skills-system`，账号 `BEIBEICSY`。

**Reason:** 需要跨设备拉取和按需分享，但个人 Skills 管理信息和本机路径不适合默认公开。

## 2026-09-12 — 将个人 Skills 系统设为 Personal 项目

**Decision:** 项目位于 `/Users/beibei/AI_Item_Agent/20_Personal_Projects/20260912-personal-skills-system/`。

**Reason:** 系统首先服务贝贝自己的工作与生活能力维护，即使部分 Skill 会用于工作，也属于个人长期基础设施。

## 2026-09-12 — 从三个真实 Skill 建立第一版基线

**Decision:** 第一版纳入工作区启动、心理咨询和记账三个 Skill。

**Reason:** 三者已经来自真实需求，分别覆盖工作基础设施、个人支持和生活管理，足以让系统从抽象清单进入实际维护。

## 2026-09-12 — 未收包 Skill 不自动复制源码

**Decision:** 没有进入 `package/` 的 Skill，仍只保存清单和维护档案，不自动复制或移动源码。

**Reason:** 现有 Skill 可能仍有独立项目或私人材料；只有明确要分发和迭代时才收包。

## 2026-09-12 — 证据不足时明确标为待核验

**Decision:** 路径、版本或可用性没有被检查时，统一写为 `待核验`，不根据名称推断。

**Reason:** 资产表的价值在于可恢复和可检查，错误的确定性会比暂缺信息更危险。

## 2026-09-12 — 保护私人数据与凭证

**Decision:** 只记录依赖和敏感边界，不保存明文凭证、账单原始数据或心理咨询原始内容。

**Reason:** 项目用于能力管理，不应成为私人数据或密钥的副本。

## 2026-09-12 — 使用一个 canonical AGENTS.md

**Decision:** 以项目根目录 `AGENTS.md` 作为唯一 Agent 操作规则源。

**Reason:** 避免不同 Agent 的规则副本发生漂移；无法自动读取时只使用外部薄适配。
