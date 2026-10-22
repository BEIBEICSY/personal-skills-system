# Decisions

## 2026-10-22 — 已收包 Skill 以 VERSION 发版，使用前对比 GitHub main

**Decision:** 带 `package/VERSION` 的 Skill 每次改包都升版本、写 CHANGELOG、同步 manifest；推送到 `main` 即发布。Skill 每次使用先运行 `check_update.py`，通过 Git 和用户已有凭据读取 `main` 上的版本，有新版时提示版本、改动和更新命令，不自动更新，检查失败不阻塞。用户要求四个已收包 Skill 同时落地；四份检查脚本必须完全一致，由测试保证。

**Reason:** 用户希望每次使用都能知道是否有新版及新版内容；仓库私有，`gh` 未必登录，Git 凭据是本机与有权限朋友都具备的最小依赖。

## 2026-10-22 — 工作区先按任务分，再在任务内分 inputs/work/outputs

**Decision:** `bootstrap-workspace` 生成的工作区以 `tasks/YYMMDD-<task-description>/` 为单位组织工作，内含 `TASK.md` 与按需创建的 `inputs/`、`work/`、`outputs/`；不再建顶层 `inputs/`、`work/`、`outputs/` 和 `docs/tasks/`。跨任务资料放 `shared/`。成品命名 `<deliverable>-<草稿|定稿>`。跟进已完成任务时询问用户新建还是续记。已有旧布局的工作区先出迁移对照表，用户确认后才移动。本仓库自身的 `docs/tasks/` 不随之迁移。

**Reason:** 按类型横向切分导致同一件事散在三处、命名各异，用户难以把任务、原件和成品对上；用户明确要求按任务组织。

## 2026-09-22 — 工作区任务按工作目标建档，不以会话为边界

**Decision:** `bootstrap-workspace` 初始化必须生成 `docs/tasks/INDEX.md`。之后 Agent 按工作目标自动续做或新建 `docs/tasks/YYMMDD-<task-description>.md`，同一任务可跨会话。文件名里的 `YYMMDD` 是开始日期，后面是当前任务的简短描述。不按聊天会话建任务，也不再要求用户提醒「需要一个 task 记录清单」。

**Reason:** 用户确认初始化后每次新工作任务都要自动记录；换会话继续同一件事时应更新原档案。

## 2026-09-12 — 本仓库作为长期 Skills 工坊

**Decision:** 以后各类个人 Skills 都在本工作区创建、登记、收包和迭代；不只管理已有四个 Skill。目录沿用现有 `skills/`、`templates/`、`scripts/`、`local/`，不额外引入通用 `inputs/` / `work/` / `outputs/`。

**Reason:** 用户明确要把此工作区当作建 Skills 的长期入口；现有布局已覆盖创建与分发闭环。

## 2026-09-12 — 本仓库同时负责 Skill 包的迭代与安装更新

**Decision:** 管理仓库不只保存清单。可分享的 Skill 以 `skills/<id>/package/` 为权威包；用 `scripts/install_skill.py` 安装或更新到各 Agent 的 Skills 目录。个人路径、Key 和私人原文仍不进仓库。

**Reason:** 后续要在同一套机制里迭代 Skill，并让自己或朋友拉取后能安装使用。

## 2026-09-12 — 四个自制 Skill 都收入可安装包

**Decision:** `bootstrap-workspace`、`reviewing-therapy-transcripts`、`reviewing-important-conversations`、`bill-to-suishouji` 都以本仓库 `package/` 为权威来源。咨询和沟通只收规则；记账收脚本和分类规则，账单仍留本地工作台。

**Reason:** 用户要在这个仓库迭代和安装全部自制 Skill，同时继续把私人原文挡在仓库外。

## 2026-09-12 — 采用一 Skill 一档案目录的混合型管理仓库

**Decision:** 每个 Skill 在 `skills/<skill-id>/` 拥有独立维护档案；`SKILLS.md` 只做全局摘要。未收包 Skill 若仍有独立权威项目，继续在原项目维护源码，本仓库不自动复制、不接管。

**Reason:** 仓库目标是 Skills 的管理和更新机制，不是源码单体仓。独立档案能体现分别维护，又避免与现有项目形成双份真相。

**Clarification:** 已收包 Skill 的权威来源以本仓库 `package/` 为准，见下一条决策；本条只约束「未收包」情形。

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
