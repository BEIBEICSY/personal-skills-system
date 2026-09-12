# Personal Skills Repository Initialization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将当前工作区初始化为“陈贝贝个人 Skills 管理仓库”，为三个现有 Skill 建立彼此独立、可核验、可恢复的维护档案。

**Architecture:** 根目录 `SKILLS.md` 继续承担全局索引；`skills/<skill-id>/` 是每个 Skill 的独立维护单元；`templates/skill-record/` 定义新增 Skill 的统一档案结构。Skill 源码继续由各自权威来源维护，本仓库只保存管理元信息，不复制私人原始数据或现有源码。

**Tech Stack:** Markdown、YAML、Git、POSIX shell 检查命令

---

### Task 1: 建立安全边界与 Skill 档案模板

**Files:**
- Create: `.gitignore`
- Create: `templates/skill-record/README.md`
- Create: `templates/skill-record/manifest.yaml`
- Create: `templates/skill-record/VERIFY.md`
- Create: `templates/skill-record/RESTORE.md`
- Create: `templates/skill-record/HISTORY.md`

- [ ] **Step 1: 验证模板和忽略规则尚不存在**

Run:

```bash
test ! -e .gitignore &&
test ! -d templates/skill-record
```

Expected: PASS，退出码为 `0`。

- [ ] **Step 2: 创建 Git 安全边界**

`.gitignore` 必须忽略：

```gitignore
# Machine-local inventory and overrides
local/

# Secrets and environment overrides
.env
.env.*
!.env.example
*.key
*.pem
credentials.*
secrets.*

# Operating system and editor state
.DS_Store
Thumbs.db
*.swp
*.swo
```

- [ ] **Step 3: 创建统一档案模板**

模板职责固定如下：

- `README.md`：用途、场景、边界、当前状态和导航。
- `manifest.yaml`：使用 `schema_version`、`id`、`name`、`category`、`ownership`、`status`、`source`、`installations`、`compatibility`、`dependencies`、`sensitive_boundaries`、`verification`、`restore` 字段。
- `VERIFY.md`：检查范围、检查步骤、最近结果、未运行检查。
- `RESTORE.md`：前置条件、恢复步骤、恢复后验证、人工介入点。
- `HISTORY.md`：按日期倒序记录任务、结果、验证与后续。

模板中的值使用解释性示例，例如 `example-skill`，不得使用空字段、秘密值或本机私人数据。

- [ ] **Step 4: 验证模板结构**

Run:

```bash
for file in README.md manifest.yaml VERIFY.md RESTORE.md HISTORY.md; do
  test -s "templates/skill-record/$file" || exit 1
done
rg -n 'schema_version|sensitive_boundaries|verification|restore' \
  templates/skill-record/manifest.yaml
```

Expected: 五个模板文件均非空；`rg` 输出四类关键字段。

- [ ] **Step 5: 提交安全边界与模板**

```bash
git add .gitignore templates/skill-record
git commit -m "chore: add skill record template and safety rules"
```

### Task 2: 建立 `bootstrap-workspace` 独立维护档案

**Files:**
- Create: `skills/bootstrap-workspace/README.md`
- Create: `skills/bootstrap-workspace/manifest.yaml`
- Create: `skills/bootstrap-workspace/VERIFY.md`
- Create: `skills/bootstrap-workspace/RESTORE.md`
- Create: `skills/bootstrap-workspace/HISTORY.md`

- [ ] **Step 1: 重新核验 Skill 入口**

Run:

```bash
test -r /Users/beibei/.codex/skills/bootstrap-workspace/SKILL.md
rg -n '^name: bootstrap-workspace$|^description:' \
  /Users/beibei/.codex/skills/bootstrap-workspace/SKILL.md
```

Expected: 文件可读，并输出名称与描述；独立源码仓库仍没有证据时保持 `待核验`。

- [ ] **Step 2: 写入维护档案**

档案必须明确记录：

- 标识：`bootstrap-workspace`
- 分类：工作基础设施 / 工作区启动
- 所有权：个人深度定制
- 当前安装入口：`/Users/beibei/.codex/skills/bootstrap-workspace/SKILL.md`
- 权威来源：当前以安装目录为准，独立源项目待核验
- 用途：初始化或接管本地/GitHub 工作区，建立唯一 `AGENTS.md` 和持久项目上下文
- 敏感边界：不保存凭证、私人原始输入或 Agent 聊天记忆
- 当前验证：入口与元数据可读，不宣称全部真实任务已回归
- 恢复步骤：取得权威来源、安装到目标 Agent 的 Skills 目录、读取入口、执行一次安全的工作区预览

- [ ] **Step 3: 验证档案内容**

Run:

```bash
for file in README.md manifest.yaml VERIFY.md RESTORE.md HISTORY.md; do
  test -s "skills/bootstrap-workspace/$file" || exit 1
done
rg -n 'bootstrap-workspace|待核验|\.codex/skills/bootstrap-workspace' \
  skills/bootstrap-workspace
```

Expected: 五个文件均非空，且名称、待核验来源和当前安装入口均可检索。

- [ ] **Step 4: 提交该 Skill 档案**

```bash
git add skills/bootstrap-workspace
git commit -m "docs: add bootstrap workspace skill record"
```

### Task 3: 核验并建立心理咨询 Skill 独立维护档案

**Files:**
- Create: `skills/reviewing-therapy-transcripts/README.md`
- Create: `skills/reviewing-therapy-transcripts/manifest.yaml`
- Create: `skills/reviewing-therapy-transcripts/VERIFY.md`
- Create: `skills/reviewing-therapy-transcripts/RESTORE.md`
- Create: `skills/reviewing-therapy-transcripts/HISTORY.md`

- [ ] **Step 1: 核验候选入口与完整内容**

Run:

```bash
test -r /Users/beibei/.cursor/skills/reviewing-therapy-transcripts/SKILL.md
rg -n '^name: reviewing-therapy-transcripts$|^description:|^## 基本边界|^## 输出前自检' \
  /Users/beibei/.cursor/skills/reviewing-therapy-transcripts/SKILL.md
```

Expected: 文件可读，并确认名称、触发描述、基本边界和输出前自检存在。

- [ ] **Step 2: 写入维护档案**

档案必须明确记录：

- 标识：`reviewing-therapy-transcripts`
- 分类：个人支持 / 心理咨询复盘
- 当前安装入口：`/Users/beibei/.cursor/skills/reviewing-therapy-transcripts/SKILL.md`
- 权威来源：当前以安装目录为准，独立源项目待核验
- 用途：根据心理咨询逐字稿生成证据分层、非诊断性的咨询复盘
- 关键边界：明确内容、互动观察与工作假设分离；不保存逐字稿；不把假设写成诊断或事实
- 当前验证：完整入口可读，关键安全章节存在；尚未进行新的私人逐字稿真实试跑
- 恢复步骤：从确认后的权威来源安装；恢复时只验证规则结构，不把私人逐字稿提交到本仓库

- [ ] **Step 3: 验证隐私表述与档案结构**

Run:

```bash
for file in README.md manifest.yaml VERIFY.md RESTORE.md HISTORY.md; do
  test -s "skills/reviewing-therapy-transcripts/$file" || exit 1
done
rg -n '不保存|非诊断|工作假设|待核验' \
  skills/reviewing-therapy-transcripts
```

Expected: 五个文件均非空，且隐私边界、非诊断边界和来源状态均有明确记录。

- [ ] **Step 4: 提交该 Skill 档案**

```bash
git add skills/reviewing-therapy-transcripts
git commit -m "docs: add therapy transcript review skill record"
```

### Task 4: 建立 `bill-to-suishouji` 独立维护档案

**Files:**
- Create: `skills/bill-to-suishouji/README.md`
- Create: `skills/bill-to-suishouji/manifest.yaml`
- Create: `skills/bill-to-suishouji/VERIFY.md`
- Create: `skills/bill-to-suishouji/RESTORE.md`
- Create: `skills/bill-to-suishouji/HISTORY.md`

- [ ] **Step 1: 核验安装入口、权威项目与测试**

Run:

```bash
test -r /Users/beibei/.codex/skills/bill-to-suishouji/SKILL.md
test -r /Users/beibei/AI_Item_Agent/20_Personal_Projects/20260706-随手记记账/README.md
test -r /Users/beibei/AI_Item_Agent/20_Personal_Projects/20260706-随手记记账/tests/test_fill_suishouji.py
test -r /Users/beibei/AI_Item_Agent/20_Personal_Projects/20260706-随手记记账/tests/test_merge_bills.py
```

Expected: 四个入口均可读。

- [ ] **Step 2: 写入维护档案**

档案必须明确记录：

- 标识：`bill-to-suishouji`
- 分类：生活管理 / 个人记账
- 权威项目：`/Users/beibei/AI_Item_Agent/20_Personal_Projects/20260706-随手记记账/`
- 当前安装入口：`/Users/beibei/.codex/skills/bill-to-suishouji/SKILL.md`
- 用途：将支付宝、微信账单清洗并写入随手记导入模板
- 规则源：项目 `README.md`、`references/分类体系.md`、`references/classification-rules.md` 和两个处理脚本
- 敏感边界：本仓库不保存账单、导入文件、账户明细或凭证
- 验证命令：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/test_fill_suishouji.py tests/test_merge_bills.py`
- 当前验证：入口、项目与测试文件可读；本轮不运行外部项目完整测试，必须如实记录
- 恢复步骤：先恢复权威项目，再安装入口文件，最后运行项目测试

- [ ] **Step 3: 验证档案结构和敏感边界**

Run:

```bash
for file in README.md manifest.yaml VERIFY.md RESTORE.md HISTORY.md; do
  test -s "skills/bill-to-suishouji/$file" || exit 1
done
rg -n 'bill-to-suishouji|不保存账单|unittest|随手记记账' \
  skills/bill-to-suishouji
```

Expected: 五个文件均非空，且权威项目、隐私边界和测试命令均有记录。

- [ ] **Step 4: 提交该 Skill 档案**

```bash
git add skills/bill-to-suishouji
git commit -m "docs: add Suishouji bookkeeping skill record"
```

### Task 5: 更新全局索引、项目状态与决策记录

**Files:**
- Modify: `README.md`
- Modify: `SKILLS.md`
- Modify: `docs/PROJECT.md`
- Modify: `docs/STATE.md`
- Modify: `docs/HISTORY.md`
- Modify: `docs/DECISIONS.md`
- Create: `docs/tasks/2026-09-12-initialize-personal-skills-management-repository.md`

- [ ] **Step 1: 更新全局定位与导航**

更新必须包含：

- 正式名称“陈贝贝个人 Skills 管理仓库”。
- 明确本仓库管理档案和更新机制，不集中接管 Skill 源码。
- `README.md` 和 `SKILLS.md` 链接三个 `skills/<id>/` 目录。
- 心理咨询 Skill 从“位置待核验”更新为已找到 `reviewing-therapy-transcripts` 安装入口；独立源码来源继续标记待核验。
- 下一步改为补充版本信息、真实试跑记录、跨设备恢复以及 GitHub 私有远程仓库。

- [ ] **Step 2: 记录任务、决策与历史**

新增任务卡需要记录目标、输入、输出、约束、验收标准、进度和验证。决策记录必须写明：

- 采用“一 Skill 一档案目录”的混合型管理仓库。
- 本仓库管理机制，源码仍以独立权威来源为准。
- GitHub 后续作为主版本源，默认私有，创建远程前确认账号和仓库名。

历史记录必须说明本轮新建了三个档案目录、核验了哪些入口、哪些检查未运行。

- [ ] **Step 3: 运行仓库级验证**

Run:

```bash
for skill in bootstrap-workspace reviewing-therapy-transcripts bill-to-suishouji; do
  for file in README.md manifest.yaml VERIFY.md RESTORE.md HISTORY.md; do
    test -s "skills/$skill/$file" || exit 1
  done
  rg -q "skills/$skill" SKILLS.md || exit 1
done

for path in README.md SKILLS.md docs/PROJECT.md docs/STATE.md docs/HISTORY.md docs/DECISIONS.md; do
  test -s "$path" || exit 1
done

rg -n '(BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|api[_-]?key[[:space:]]*[:=][[:space:]]*[^<]|token[[:space:]]*[:=][[:space:]]*[^<])' \
  --glob '!docs/superpowers/**' .
```

Expected: 结构和导航检查全部通过；敏感模式扫描无匹配并以 `1` 退出。

- [ ] **Step 4: 检查变更范围**

Run:

```bash
git status --short
git diff --check
git diff --stat
```

Expected: 只包含本计划指定文件；`git diff --check` 无输出并以 `0` 退出。

- [ ] **Step 5: 提交全局索引与项目状态**

```bash
git add README.md SKILLS.md docs/PROJECT.md docs/STATE.md \
  docs/HISTORY.md docs/DECISIONS.md \
  docs/tasks/2026-09-12-initialize-personal-skills-management-repository.md
git commit -m "docs: establish personal skills management repository"
```

### Task 6: 最终验证与交付

**Files:**
- Modify: `docs/tasks/2026-09-12-initialize-personal-skills-management-repository.md`
- Modify: `docs/STATE.md`
- Modify: `docs/HISTORY.md`

- [ ] **Step 1: 执行最终验证**

Run:

```bash
git status --short
git log --oneline --decorate -6
test "$(git branch --show-current)" = "main"
test -z "$(git remote)"
```

Expected: 工作区干净；最近提交按任务顺序出现；当前分支为 `main`；本轮尚未配置远程仓库。

- [ ] **Step 2: 写入最终验证结果**

将实际提交哈希、已通过检查、未运行的外部项目测试和剩余的 GitHub 远程创建任务写入任务卡；同步更新 `docs/STATE.md` 与 `docs/HISTORY.md`。不得把未执行的检查写成已通过。

- [ ] **Step 3: 提交验证记录**

```bash
git add docs/tasks/2026-09-12-initialize-personal-skills-management-repository.md \
  docs/STATE.md docs/HISTORY.md
git commit -m "docs: record repository initialization verification"
```

- [ ] **Step 4: 确认最终状态**

Run:

```bash
git status --short --branch
git log -1 --format='%h %s'
```

Expected: 输出 `## main` 且无未提交文件；最新提交为验证记录提交。
