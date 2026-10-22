# Work history

这是个人 Skills 系统的重要成果索引，按时间倒序维护。只记录可复用的结果、验证和关键失败，不保存聊天转录或私人原始数据。

## 2026-10-22 — bootstrap-workspace 0.3.0 增加使用前更新检查

- **任务：** [任务档案](tasks/261022-bootstrap-workspace-更新检查.md)。
- **结果：** Skill 每次使用先对比本机与 GitHub `main` 的版本，有新版时提示版本、改动与更新命令；本仓库 `AGENTS.md` 增加发版纪律。
- **产物：** `package/VERSION`、`CHANGELOG.md`、`update.json`、`scripts/check_update.py`；`tests/test_check_update.py`。
- **验证：** 更新检查 7 passed、脚手架 8 passed、安装 4 passed；真实私有仓库可访问。
- **推广：** 同日应用户要求推广到其余三个 Skill（各升 0.2.0），四份检查脚本由测试保证一致；两个复盘 Skill 已更新本机安装，记账 Skill 本机为收包前旧版，未覆盖。
- **后续：** 推送后在真实仓库确认四个 Skill 均为 `up-to-date`。

## 2026-10-22 — bootstrap-workspace 改为任务文件夹结构

- **任务：** [任务档案](tasks/261022-bootstrap-workspace-任务文件夹结构.md)；[设计](superpowers/specs/2026-10-22-bootstrap-workspace-task-folders-design.md)。
- **结果：** 新工作区按「一件事一个文件夹」组织：`tasks/YYMMDD-任务描述/` 内含 `TASK.md`、`inputs/`、`work/`、`outputs/`，共用资料放 `shared/`；跟进已完成任务时询问新建还是续记；旧布局工作区只提示迁移。
- **产物：** `skills/bootstrap-workspace/package/` 的 `SKILL.md`、脚手架、模板与 profile 参考；两份测试。
- **验证：** 脚手架测试 8 passed，安装测试 4 passed；评级工作区 dry-run 正确识别旧布局，未写入。
- **后续：** 已安装到本机 Cursor / Codex；评级工作区已按用户确认的对照表迁移为 14 个任务文件夹，文件无缺失、哈希一致。待在真实工作中试跑「跟进已完成任务」询问规则。

## 2026-10-20 — 任务档案命名改为 YYMMDD-任务描述

- **任务：** 约束 `bootstrap-workspace` 新建任务文件名为 `YYMMDD-<当前任务描述>`。
- **结果：** 不再使用 `YYYY-MM-DD-slug`；初始化任务为 `YYMMDD-initialize-workspace.md`。
- **验证：** 脚手架与安装测试。
- **后续：** 覆盖本机 Cursor / Codex 安装。

## 2026-09-22 — bootstrap-workspace 增加任务清单与自动建档

- **任务：** [规格](superpowers/specs/2026-09-22-bootstrap-workspace-task-tracking-design.md)；[计划](superpowers/plans/2026-09-22-bootstrap-workspace-task-tracking.md)。
- **结果：** 首次初始化写入 `docs/tasks/INDEX.md` 和 `YYMMDD-initialize-workspace` 任务；接管已有工作区只补 stub。生成的 `AGENTS.md` 要求按工作目标续做或新建 `YYMMDD-<task-description>` 任务。
- **产物：** `skills/bootstrap-workspace/package/` 模板与脚手架、`tests/test_scaffold_workspace.py`。
- **验证：** `python3 tests/test_scaffold_workspace.py -v` 与 `python3 tests/test_install_skill.py -v` 通过。
- **后续：** 本机 Cursor / Codex 按用户要求用安装脚本覆盖；不把本仓库自身改造成新模板示例。

## 2026-09-12 — 文档状态校准为稳态运营

- **任务：** 用户确认体系已建好，核对项目文档是否仍停留在建设中口径。
- **结果：** 第一里程碑标为已完成；`STATE.md` 改为无进行中基建、按需运营；`SKILLS.md` 与档案模板补齐 `已收包，可安装` 状态口径；澄清未收包 vs 已收包权威来源决策。
- **产物：** 更新 `docs/STATE.md`、`docs/PROJECT.md`、`SKILLS.md`、`templates/skill-record/README.md`、`docs/DECISIONS.md`。
- **验证：** 对照四个 Skill 任务卡均为 Completed、四个 `package/` 已存在、安装测试此前已通过；本轮未重跑安装测试。
- **后续：** 无基建待办；按需新建 Skill、本机安装或做真实试跑。

## 2026-09-12 — 确认工作区为 Skills 工坊

- **任务：** `/bootstrap-workspace`，明确以后在此创建各类 Skills。
- **结果：** 核心上下文已齐全，未重建脚手架；未新增 `inputs/` / `work/` / `outputs/`。更新 README、PROJECT、AGENTS、STATE、DECISIONS，把「新建 Skill」写进正式目标。
- **产物：** 决策「本仓库作为长期 Skills 工坊」。
- **验证：** `AGENTS.md` 引用路径均存在；Cursor 对 `AGENTS.md` 为 native；`python3 tests/test_install_skill.py -v` 本轮未重跑（结构未改安装逻辑）。
- **后续：** 按模板新建 Skill；本机按需安装。

## 2026-09-12 — 其余三个 Skill 收成可安装包

- **任务：** 让咨询、沟通复盘和记账也能从本仓库安装和迭代。
- **结果：** 三个 Skill 均新增 `package/`。咨询和沟通只收规则；记账收脚本和分类规则，未收账单原文。
- **产物：** 任务卡 `docs/tasks/2026-09-12-package-remaining-skills.md`。
- **验证：** 安装测试覆盖全部四个 Skill；package 内无本机绝对路径。未覆盖直播安装，未跑记账完整 unittest。
- **后续：** 本机按需安装；记账使用本地工作台。

## 2026-09-12 — bootstrap-workspace 收成可安装包

- **任务：** 把仓库改成可迭代入口，并先收一份可安装 Skill。
- **结果：** 新增 `skills/bootstrap-workspace/package/` 与 `scripts/install_skill.py`；朋友或新设备可在获得仓库权限后安装。
- **产物：** 安装脚本、测试、任务卡 `docs/tasks/2026-09-12-package-bootstrap-workspace.md`。
- **验证：** `python3 tests/test_install_skill.py -v` 通过；未覆盖直播安装目录。
- **后续：** 本机按需安装；其余 Skill 等拆出可分享部分后再收包。

## 2026-09-12 — 建立 GitHub 私有主版本源

- **任务：** 提交四个 Skill 档案，并创建可跨设备拉取的 GitHub 环境。
- **结果：** 私有仓库已建立并推送 `main`。
- **产物：** https://github.com/BEIBEICSY/personal-skills-system
- **验证：** 推送前敏感模式扫描无匹配；远程为 private；`main` 已跟踪 `origin/main`。未运行外部项目测试，也未试跑私人材料。
- **后续：** 换设备时用该仓库克隆；继续补充版本和真实试跑记录。

## 2026-09-12 — 增补重要沟通复盘 Skill

- **任务：** 将 `reviewing-important-conversations` 纳入个人 Skills 管理仓库。
- **结果：** 建立独立维护档案，并与 `reviewing-therapy-transcripts` 写明分流：咨询走咨询 Skill，非咨询沟通走沟通复盘 Skill；不得同时更新两套脉络，但用户明确允许且来源相关时可以相互引用。
- **产物：** `skills/reviewing-important-conversations/`、任务卡 `docs/tasks/2026-09-12-register-reviewing-important-conversations.md`。
- **验证：** Cursor 入口与 `templates.md` 可读；核心原则、权力关系和完成前核对存在；独立源项目待核验；未进行真实沟通材料试跑。
- **后续：** 确认独立来源、沟通复盘工作区位置，以及一次不把原文写入本仓库的真实试跑。

## 2026-09-12 — 初始化陈贝贝个人 Skills 管理仓库

- **任务：** 在本地 Git 中建立“一 Skill 一档案目录”的管理仓库，不集中接管源码。
- **结果：** 新增模板、三个独立档案目录，以及全局索引和决策记录；心理咨询 Skill 定位为 `reviewing-therapy-transcripts`。
- **产物：** `.gitignore`、`templates/skill-record/`、`skills/bootstrap-workspace/`、`skills/reviewing-therapy-transcripts/`、`skills/bill-to-suishouji/`。
- **验证：** 三个安装入口均可读取；记账权威项目 README 与两个测试文件可读；仓库结构与敏感扫描通过；本轮未运行外部项目 unittest，也未做私人逐字稿或真实账单试跑。本地 `main` 尚无远程。
- **后续：** 补充版本与真实试跑，并在确认账号和仓库名后创建 GitHub 私有远程仓库。

## 2026-09-12 — 个人 Skills 系统正式成立

- **任务：** 将 Inbox 中的个人 AI 环境资产想法转为正式 Personal 项目，并建立第一版资产基线。
- **结果：** 建立项目上下文与 `SKILLS.md`；纳入工作区启动、心理咨询、记账三个真实 Skill。
- **产物：** `README.md`、`AGENTS.md`、`SKILLS.md`、`docs/` 以及迁入的原始想法记录。
- **验证：** `bootstrap-workspace` 与 `bill-to-suishouji` 的安装入口可读取；心理咨询 Skill 当时尚未定位并明确标为 `待核验`。
- **后续：** 补齐心理咨询 Skill 路径，并为三个 Skill 建立版本、真实试跑和恢复记录。
