# bootstrap-workspace 任务文件夹结构设计

日期：2026-10-22
状态：用户已确认方向

## 背景

用 `bootstrap-workspace` 初始化后的内容工作区（例：`20260920-评级`）在日常工作中出现三个问题：

1. 任务档案命名混用 `YYYYMMDD-描述`、`描述-YYYYMMDD` 和无日期三种写法（该工作区由旧版 Skill 初始化，没有 `YYMMDD` 规则和 `INDEX.md`）。
2. `work/` 子目录名与任务名对不上。
3. `outputs/` 平铺，文件名看不出出自哪个任务；只能靠任务档案里的手写链接对应。

根因：Skill 只规定了任务档案的命名，没有规定任务与输入、过程、成品之间的组织关系；`inputs/`、`work/`、`outputs/` 按类型横向切分，同一件事散在三处。用户也不清楚各一级目录分别放什么。

## 决策

改为「一件事一个文件夹」：先按任务分，再在任务内部分 `inputs/`、`work/`、`outputs/` 和任务档案。

```text
<workspace>/
├── AGENTS.md / README.md
├── docs/                 项目说明书：PROJECT、STATE、HISTORY、DECISIONS
├── shared/               多个任务共用的资料（仅产物型 profile）
└── tasks/
    ├── INDEX.md          任务总清单
    ├── TEMPLATE.md       任务档案模板
    └── YYMMDD-任务描述/
        ├── TASK.md       目标、输入、进展、产物、验证
        ├── inputs/       本任务原件，只读
        ├── work/         过程稿，可再生成
        └── outputs/      成品
```

### 规则

- **任务编号**：`YYMMDD-<task-description>`，即任务文件夹名。`YYMMDD` 为开始日期；描述用用户语言，空格换连字符，去掉 `/\:*?"<>|`。续做时不改名。
- **子目录按需创建**：新建任务时只建 `TASK.md`；有原件、过程稿或成品要放时再建对应子目录，不建空目录。所有 profile 一致。
- **成品命名**：`outputs/<交付物名>-<草稿|定稿>.<ext>`；需要保留旧版时加 `-v<N>`，如 `V3修改建议-v2-草稿.md`。状态变化时重命名并同步 `TASK.md` 链接。
- **共用资料**：跨任务的标准、基线、模板放 `shared/`，只读；任务在 `TASK.md` 里引用路径，不复制。某任务的原件后来被别的任务用到时，用相对路径引用，不复制；是否提升到 `shared/` 先问用户。
- **任务匹配**：
  - 匹配到未完成任务（In progress / Paused）：直接续做，不询问。
  - 匹配到已完成任务（追加修改、二次复评等跟进）：问用户「新建任务文件夹」还是「在原文件夹继续记录」。选后者时把该任务改回 In progress，在 Progress 记日期和原因；选前者时新任务在 Related tasks 链接旧任务。
  - 不确定：问一个问题，点出最接近的任务。
- **代码工作区**：任务同样用 `tasks/<编号>/TASK.md`，但不预建 `shared/`，源码仍按项目原布局。

### 已有工作区（旧布局）

检测到 `docs/tasks/` 或顶层 `inputs/`、`work/`、`outputs/` 时视为旧布局：

- 脚手架不创建 `tasks/`、`shared/`，并输出提示。
- Agent 给出「旧路径 → 新路径」迁移对照表，用户确认后才移动，并同步修正文档内链接。
- 未确认前沿用旧布局继续工作，不形成两套任务体系。

### 版本控制

- `.gitignore`：`tasks/*/work/`；`--sensitive-inputs` 时加 `tasks/*/inputs/` 与 `shared/**`（保留 `shared/.gitkeep`）。

### 面向用户的目录说明

`README.md` 的目录地图用平实中文说明每个目录放什么，并给出判断口诀：别人给的、不该改的放 `inputs/`；要拿去用或发出去的放 `outputs/`；其余过程文件放 `work/`。

## 影响范围

- `skills/bootstrap-workspace/package/`：`SKILL.md`、`scripts/scaffold_workspace.py`、模板（AGENTS、README、STATE、HISTORY、DECISIONS、INDEX、INDEX_STUB、INIT_TASK、TASK_TEMPLATE、gitignore）、`references/workspace-profiles.md`。
- `tests/test_scaffold_workspace.py`、`tests/test_install_skill.py`。
- 维护档案：`skills/bootstrap-workspace/HISTORY.md`、`VERIFY.md`。

不在本次范围：自动迁移脚本；本仓库自身的 `docs/tasks/` 布局；评级工作区的实际迁移（Skill 改完后另出对照表，用户确认后执行）。

## 验收

- 新建工作区：`tasks/INDEX.md`、`tasks/TEMPLATE.md`、`tasks/YYMMDD-initialize-workspace/TASK.md` 存在；不存在 `docs/tasks/`；产物型 profile 有 `shared/`，没有顶层 `inputs/`、`work/`、`outputs/`。
- 生成的 `AGENTS.md` 含任务编号规则、`TASK.md`、子目录规则、成品命名规则、已完成任务询问规则。
- 旧布局工作区：不创建 `tasks/`，输出迁移提示，不覆盖任何文件。
- `python3 tests/test_scaffold_workspace.py -v` 与 `python3 tests/test_install_skill.py -v` 通过。
