# bootstrap-workspace 任务清单与自动建档

## 目标

初始化工作区时一并建立任务追踪骨架。之后在该工作区开始**一项新的工作任务**时，Agent 自动识别并建档，不必再由用户提醒「需要一个 task 记录清单」。同一工作任务可以跨越多个会话；换会话时更新原档案，不按会话新建。

## 背景与缺口

当前 `bootstrap-workspace` 只创建 `docs/tasks/TEMPLATE.md`。`STATE.md` 和 `README.md` 仍把「请再创建第一个任务」写成下一步，`AGENTS.md` 只在「已有任务时」才去读 `docs/tasks/`。结果是：初始化完成后，用户每次都要再交代一次任务记录方式。

## 选定方案

采用**任务清单 + 一任务一档案**：

- `docs/tasks/INDEX.md` 是总清单。
- 每个工作任务一份 `docs/tasks/YYMMDD-<task-description>.md`。
- `STATE.md` 只指向当前进行中的任务，不替代清单。
- `HISTORY.md` 只记录有结果的完成项，并链到任务档案。

不采用单页 `TASKS.md` 看板，也不限制同一时间只能有一条进行中任务。

## 初始化产物

空工作区脚手架在现有核心文件之外，必须补齐：

| 路径 | 作用 |
|---|---|
| `docs/tasks/INDEX.md` | 任务总清单 |
| `docs/tasks/TEMPLATE.md` | 新任务复制模板（已有） |
| `docs/tasks/{{DATE_COMPACT}}-initialize-workspace.md` | 把「初始化工作区」写成已完成的第一条任务 |

`README.md` 的工作区地图增加 `docs/tasks/INDEX.md`。入门步骤从「开始干活前先自己建任务」改为：对照 `INDEX.md`；新任务自动建档，旧任务接着更新。

`STATE.md` 的进行中/下一步不再要求「创建第一个任务规格」。进行中可为空或指向后续真实工作；已完成中包含初始化任务链接。

`HISTORY.md` 的初始化条目的 Task 字段链到上述初始化任务档案。Follow-up 不再写「定义第一个具体任务」。

`DECISIONS.md` 增加一条：工作任务以 `docs/tasks/` 档案为记录，以 `INDEX.md` 为清单；不以聊天会话为任务边界。

## 文件分工

- **INDEX.md**：只保留名称（链接）、一句话目标、开始日期、最后更新日期；按状态分组。不复制档案正文。
- **任务档案**：目标、输入、输出、约束、验收、进度、结果、验证、关联会话、相关任务。
- **STATE.md**：当前目标、进行中任务链接、下一步、阻塞、最近验证。
- **HISTORY.md**：有结果的完成项索引，链到任务档案。
- **AGENTS.md**：开工识别规则与完成时更新义务。这是自动建档能发生的原因。
- **TEMPLATE.md**：新建档案时的复制源，本身不出现在清单里。

生成文件的语言与现有模板保持一致：`AGENTS.md`、`STATE.md`、`HISTORY.md`、任务模板和任务档案用英文；`README.md` 中的目录说明保持中文。

## 自动识别规则

Agent 在做任何实质性工作之前，必须先读 `docs/tasks/INDEX.md` 和 `STATE.md` 的当前目标，再拿用户请求比对，只走三条路：

1. **续做**：与某条未完成任务（In progress 或 Paused）的目标一致 → 打开该档案继续写进度。不因换会话、换措辞而新建。
2. **新开**：与所有未完成项都对不上 → 按模板新建档案，立刻写入 `INDEX.md`，并把 `STATE.md` 当前目标指过去。不问「要不要建任务」。
3. **拿不准**：只问一句，带上最像的任务名：「这是接着《某任务》还是新开？」得到回答前不新建、不改状态。不问「要不要建立任务系统」。

判定依据是**要完成的结果**，不是会话、日期或字面措辞。

不建档：纯问答、闲聊、解释已有文件、用户明确说不要记。一旦开始改文件或产出交付物，必须落在某条任务上。

允许多条 In progress。新开时不必先结束旧任务。

完成一条时：更新档案的结果和验证 → `INDEX.md` 标 Completed → 同步 `STATE.md`。仅当产生可复用结果时，才在 `HISTORY.md` 追加一条并链回档案。

## INDEX 格式

按状态分组，组内最新在上：

```markdown
# Task index

Living inventory of work tasks. Newest items first within each section. Do not copy task details here. `TEMPLATE.md` is not a task.

## In progress

- None.

## Paused

- None.

## Completed

- [Initialize workspace]({{DATE_COMPACT}}-initialize-workspace.md) — Establish durable, agent-neutral workspace context. Started {{DATE}}. Updated {{DATE}}.

## Cancelled

- None.
```

一行的固定字段：任务名（相对链接）、破折号后的一句话目标、Started 日期、Updated 日期。

默认只有上述四组。`Unverified` 只出现在接管已有工作区、Agent 尚未盘点完旧档案时，盘点后必须并入四态之一。

## 任务档案格式

文件名：`docs/tasks/YYMMDD-<task-description>.md`。`YYMMDD` 是任务开始日期（`%y%m%d`）；`<task-description>` 是当前任务的简短描述，可用用户语言，空格改成短横线，去掉 `/\:*?"<>|`。同一任务换会话不改文件名、不复制新文件。

在现有 `TASK_TEMPLATE.md.tmpl` 上增加两节，其余保留：

```markdown
# Task: <short name>

## Objective
## Inputs
## Outputs
## Constraints
## Acceptance criteria
## Progress
## Related sessions
## Related tasks
## Outcome
## Verification
```

约定：

- **Progress**：状态为 `Not started` / `In progress` / `Paused` / `Completed` / `Cancelled` 之一，后接带日期的短笔记。自动识别后新建的任务从 `In progress` 起记，因为建档发生在工作已经开始时。`TEMPLATE.md` 仍可保留 `Not started`，供偶尔手工复制。
- **Related sessions**：只记日期和一句「本次做了什么」，不粘贴聊天记录或原文。
- **Related tasks**：可选。指向被暂停、拆出或依赖的其它任务档案。
- 初始化任务在脚手架写入时即为 `Completed`，验收为「核心上下文文件已创建且路径互相引用」。

## AGENTS.md 开工与收尾

Startup 在读完 `STATE.md` 之后增加：读取 `INDEX.md`；按识别规则决定续做、新开或提问；新开则先建档再动手。删除「有任务规格时才读 `docs/tasks/`」和任何「开始干活前请用户自己建任务」的表述。

Completion 在更新 `STATE.md` 之外，必须更新活跃任务档案和 `INDEX.md`。`HISTORY.md` 仍只在有意义结果时追加。

Source-of-truth 顺序不变：用户当前指令仍高于活跃任务规格。

## 脚手架脚本行为

`scaffold_workspace.py` 继续只创建缺失文件，不覆盖已有文件。

区分两种写入：

1. **首次初始化**（本次会新建 `AGENTS.md`）：创建 `INDEX.md`、`TEMPLATE.md`、以及 `{{DATE_COMPACT}}-initialize-workspace.md`。INDEX 的 Completed 中包含该初始化任务。
2. **接管已有工作区**（`AGENTS.md` 已存在，因而会被 skip）：不创建「刚刚初始化」这种任务。若 `INDEX.md` 缺失，写入空分组清单，并在文首用英文注明由 Agent 将已有 `docs/tasks/*.md`（排除 `TEMPLATE.md`）收进清单；认不出的状态标为 `Unverified`，不擅自写成 In progress 或 Completed。`Unverified` 项可暂时放在 Completed 组之前的独立小节，盘点完成后再移入四态之一。

`directory_map()` 增加 `docs/tasks/INDEX.md` 一行。

## 异常与冲突

- 认不出新开还是续做：只问一句；确认前不改文件。
- 用户说接着做，但清单没有对应项：新建档案，并在 Progress 写明由续做请求创建、此前无档案。
- 同一请求包含两件独立工作：拆成两条；能判断主次时先建主要那条，另一条写入 INDEX，并在 `STATE.md` 列为下一步。
- `INDEX.md` 与档案状态不一致：以任务档案为准，当场改齐 INDEX 和 `STATE.md`，并在 Progress 记一笔。
- 已有 `docs/tasks/` 或其它任务文件：不覆盖。只补缺失 INDEX，由 Agent 盘点已有档案。
- 完成时验证失败：保持 In progress，把缺口写入档案；不标 Completed，不写 `HISTORY.md`。
- 敏感内容：档案只写目标和产物路径，不写凭证、账单原文、咨询或沟通逐字稿。

## 范围外

- 不接入 GitHub Issues、TickTick、Linear 或其它外部任务系统。
- 不把本仓库正在使用的 Cursor / Codex 直播安装目录一并覆盖；本机生效仍走现有 `scripts/install_skill.py`，且需用户明确要求。
- 不在本轮把个人 Skills 管理仓库自身改造成新模板的示例工作区。
- 不保存会话全文，不按聊天轮次建任务。
- 不增加模拟对话的自动识别测试；识别规则写在 `SKILL.md` 与 `AGENTS.md` 中，靠对照检查。

## 实现落点

只改 `bootstrap-workspace` 的权威包与相关测试/档案：

- `skills/bootstrap-workspace/package/SKILL.md`
- `skills/bootstrap-workspace/package/scripts/scaffold_workspace.py`
- `skills/bootstrap-workspace/package/assets/templates/`（含新增 `INDEX.md.tmpl`、初始化任务模板，以及 `AGENTS.md.tmpl`、`README.md.tmpl`、`STATE.md.tmpl`、`HISTORY.md.tmpl`、`DECISIONS.md.tmpl`、`TASK_TEMPLATE.md.tmpl`）
- `skills/bootstrap-workspace/package/references/workspace-profiles.md`（若其中仍写「请再创建第一个任务」）
- `tests/test_install_skill.py`
- `skills/bootstrap-workspace/VERIFY.md`、`HISTORY.md`

## 验证

1. `python3 tests/test_install_skill.py -v` 继续通过。
2. 安装后的脚手架对空目录 `--dry-run` 与实际写入，输出/产物包含 `docs/tasks/INDEX.md`、`docs/tasks/TEMPLATE.md`、`docs/tasks/YYMMDD-initialize-workspace.md`。
3. 写入结果中，`AGENTS.md` 含对照清单识别新开/续做的规则，且不含「开始干活前先自己建任务」。
4. 对已有 `AGENTS.md` 的目录运行脚手架：已有文件不被覆盖；不新增 initialize-workspace 任务；若缺 INDEX 则补空清单。
5. 模板渲染后无未替换占位符；package 内仍无本机绝对路径。
6. 识别歧义、一句话两件事、状态不一致等规则存在于 `SKILL.md` / `AGENTS.md`，不做对话模拟测试。

本轮不覆盖直播安装目录，也不对真实私人项目做非 dry-run 试跑，除非用户另行要求。
