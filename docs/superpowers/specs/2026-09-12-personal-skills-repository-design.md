# 陈贝贝个人 Skills 管理仓库设计

## 目标

将当前工作区建设为陈贝贝个人 Skills 的统一管理入口，用于登记、核验、更新、安装、迁移和恢复。仓库管理 Skills 的元信息与维护机制，不集中接管已有 Skill 源码。

## 仓库边界

- 每个 Skill 都有独立维护档案。
- 已有独立权威项目的 Skill 继续在原项目维护源码。
- 本仓库只记录权威来源、安装入口、兼容环境、验证方法、恢复步骤和维护历史。
- 没有独立项目的 Skill 将来可以单独决定是否内置，但不属于本轮初始化范围。
- 不提交凭证、Token、账单原文、心理咨询原文、本机扫描结果或其他私人原始数据。

## 目录结构

```text
personal-skills-system/
├── README.md
├── AGENTS.md
├── SKILLS.md
├── skills/
│   ├── bootstrap-workspace/
│   │   ├── README.md
│   │   ├── manifest.yaml
│   │   ├── VERIFY.md
│   │   ├── RESTORE.md
│   │   └── HISTORY.md
│   ├── reviewing-therapy-transcripts/
│   │   └── 同上
│   └── bill-to-suishouji/
│       └── 同上
├── docs/
│   ├── PROJECT.md
│   ├── STATE.md
│   ├── HISTORY.md
│   ├── DECISIONS.md
│   ├── tasks/
│   └── superpowers/specs/
├── scripts/
├── templates/
└── local/
```

`local/` 只保存本机路径覆盖或扫描结果，并由 Git 忽略。空的 `scripts/` 不在本轮强行创建；真实的重复操作出现后再加入脚本。

## 每个 Skill 的维护单元

- `README.md`：用途、适用场景、维护边界和当前状态。
- `manifest.yaml`：稳定标识、权威来源、安装入口、支持的 Agent、依赖、版本和敏感边界。
- `VERIFY.md`：可重复的检查方法、最近验证结果和未运行检查。
- `RESTORE.md`：新设备或新账号上的安装与恢复步骤。
- `HISTORY.md`：该 Skill 的重要试跑、更新、失败和修复记录。

根目录 `SKILLS.md` 只作为全局摘要与导航，详细信息以各 Skill 目录为准。

## 初始 Skills

1. `bootstrap-workspace`：已确认安装入口可读，源码权威项目仍待确认。
2. `reviewing-therapy-transcripts`：作为心理咨询 Skill 的候选标识；写入前必须核验实际文件及隐私边界。
3. `bill-to-suishouji`：已确认安装入口和现有权威项目。

证据不足的字段保持 `待核验`，不根据名称或历史记忆推断。

## Git 与 GitHub

- 本地仓库使用 `main` 分支。
- 首次提交保存当前项目基线、设计和初始化后的维护结构。
- GitHub 将作为后续主版本源，默认创建私有仓库。
- 创建远程仓库前单独确认 GitHub 账号归属和仓库名称。
- 不将本机绝对路径视为跨设备安装契约；后续通过变量、本地覆盖或恢复脚本处理设备差异。

## 验证

- 三个初始 Skill 都能从 `SKILLS.md` 导航到独立档案目录。
- 所有已登记路径存在，或明确标记为 `待核验`。
- `.gitignore` 排除 `local/`、环境变量、密钥、凭证和系统文件。
- 提交前检查待提交文件中不存在疑似密钥和私人原始内容。
- 检查 Git 状态，确保没有遗漏或误纳入的文件。

## 本轮不做

- 不迁移或复制现有 Skill 源码。
- 不编写尚无真实需求的自动扫描、安装或同步脚本。
- 不创建公开仓库。
- 不上传到 GitHub，远程仓库创建作为下一步独立操作。
