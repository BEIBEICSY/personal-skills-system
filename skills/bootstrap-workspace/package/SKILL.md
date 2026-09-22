---
name: bootstrap-workspace
description: Initialize or adopt a local or GitHub workspace with one canonical AGENTS.md, durable project context and outcome history, safe file boundaries, and agent-host compatibility guidance. Use when a user starts a project, creates an empty workspace or repository, asks to initialize or organize the workspace context/environment, wants seamless switching among coding or office agents, or needs to repair missing or conflicting agent documentation in an existing workspace.
---

# Bootstrap Workspace

Create an agent-neutral workspace whose durable context lives in files and Git history rather than one agent's chat memory. Treat `AGENTS.md` as the only canonical agent-instruction source.

## Workflow

### 1. Identify the target and current host

- Resolve the exact workspace directory before writing.
- Identify the current agent host from reliable runtime or system metadata. Do not infer it only from files found in the repository.
- Inspect the workspace read-only: list files, detect Git state, manifests, existing instructions, documentation, sensitive-looking paths, large-file patterns, and current build/test commands.
- Preserve uncommitted and user-authored content.

### 2. Build minimum viable context

For an empty workspace, first extract facts from the user's request and directory name. Ask only for missing information that changes the structure or safety policy.

Ask this first when the purpose is unclear:

> What should this workspace ultimately accomplish? Include what you expect to put into it and the final deliverable you want.

Ask about local versus Git/GitHub storage and sensitive or large inputs only when relevant. For a code workspace, ask about stack and verification commands only if the user expects code scaffolding or those facts are required now. Ask at most one topic per round and normally no more than two rounds.

Proceed when these facts are known:

- goal;
- primary inputs or working material;
- expected output or definition of done.

If the user is unsure, use conservative defaults: no Git initialization, no remote, no uploads, no stack-specific scaffolding, and no tracking of raw inputs.

### 3. Choose a profile

Read [references/workspace-profiles.md](references/workspace-profiles.md) when choosing among `minimal`, `code`, `data`, `research`, `content`, and `mixed` profiles.

Always create only the missing core context:

- `README.md` for the human entry point;
- `AGENTS.md` for agent startup and operating rules;
- `docs/PROJECT.md` for stable goals and scope;
- `docs/STATE.md` for current state and next actions;
- `docs/HISTORY.md` for a concise history of meaningful work outcomes;
- `docs/DECISIONS.md` for durable decisions;
- `docs/tasks/INDEX.md` for the living task inventory;
- `docs/tasks/TEMPLATE.md` for new task files;
- `docs/tasks/YYYY-MM-DD-initialize-workspace.md` on first initialization only, when `AGENTS.md` is being created.

Add `inputs/`, `work/`, `outputs/`, or `scripts/` only when the selected profile benefits from them. Do not impose generic `src/` or `tests/` directories on an established repository or an undecided code stack.

### 4. Plan before mutation

- If the workspace is empty and the user's intent is sufficiently clear, proceed without an extra confirmation.
- If existing files overlap, present the intended additions and conflicts before editing.
- Never overwrite, delete, move, initialize Git, install dependencies, create a remote, commit, or push unless the user explicitly requests that action.

Run the deterministic scaffold in preview mode first:

先解析本 Skill 的安装目录，再运行其中的脚本；不要假设当前工作目录就是 Skill 目录：

```bash
python3 <skill-directory>/scripts/scaffold_workspace.py \
  --target /absolute/workspace/path \
  --profile data \
  --project-name "Example project" \
  --goal "Turn source records into a verified import workbook" \
  --inputs "Source record exports" \
  --outputs "Verified import workbook" \
  --dry-run
```

Review the preview, then rerun without `--dry-run`. Add `--git-mode git` or `--git-mode github` only when version control is already present or the user has chosen it. Add `--sensitive-inputs` when raw inputs must not be tracked. The script creates missing files exclusively and skips all existing files.

### 5. Adapt to the real workspace

Review every generated document. Replace generic wording with facts already present in manifests, commands, schemas, tests, and user-provided context. Do not invent commands, architecture, users, deadlines, or acceptance criteria.

For an existing workspace:

- use its current directory layout rather than adding profile directories blindly;
- point `AGENTS.md` to canonical existing documentation instead of copying it;
- when adding `docs/HISTORY.md` to an older scaffold, review and minimally update existing `AGENTS.md` and `README.md` so they expose it without replacing user-authored content;
- merge `.gitignore` rules only after inspecting the current file;
- explain conflicts among instruction files and propose a single-source repair without deleting anything automatically;
- if `docs/tasks/INDEX.md` was just created as a stub, inventory existing `docs/tasks/*.md` files except `TEMPLATE.md`; mark unknown status as `Unverified` and do not invent an initialize-workspace task;

Maintain `docs/HISTORY.md` as a compact, reverse-chronological index rather than a session transcript:

- add an entry only after a meaningful outcome, reusable finding, or consequential failed attempt;
- include the date, task, result, artifacts, verification, and follow-up;
- link to detailed task records, decisions, outputs, or commits instead of copying them;
- do not record routine conversation, private reasoning, raw prompts, or exploration with no durable result;
- keep exact file-level history in Git when Git is in use.

### Task tracking after initialization

Before substantial work in a bootstrapped workspace, read `docs/tasks/INDEX.md` and `docs/STATE.md`, then decide:

- Continue: the requested outcome matches an unfinished task (In progress or Paused). Open that file. Do not create a new file because the session changed.
- Start: the requested outcome matches no unfinished task. Create `docs/tasks/YYYY-MM-DD-slug.md` from `TEMPLATE.md` with Progress `In progress`, add it to `INDEX.md`, and point `STATE.md` at it. Do not ask whether to create a task.
- Unsure: ask one question naming the closest existing task; do not ask whether to create a task system.

Match on the intended outcome, not the session, date, or wording. Multiple tasks may be in progress at once. Skip a task file for pure questions, chat, explaining existing files, or when the user says not to record one. Once files will change or a deliverable will be produced, the work must belong to a task.

If the user says this continues prior work but no matching file exists, create one and note in Progress that it was created from a continuation request. If one request contains two independent outcomes, split them; create the primary task first and list the other in `INDEX.md` and `STATE.md` next actions.

When completing a task, update the task file, move it to Completed in `INDEX.md`, and sync `STATE.md`. Keep it In progress when verification failed. Add `HISTORY.md` only for a meaningful outcome, and link the task file. If `INDEX.md` and the task file disagree, trust the task file and repair `INDEX.md` and `STATE.md`. Never write secrets, bills, therapy transcripts, or conversation transcripts into task files.

### 6. Check agent compatibility

Read [references/agent-compatibility.md](references/agent-compatibility.md) only when the host is not obviously native, configuration needs auditing, or conflicting tool-specific files exist.

- If the host natively loads `AGENTS.md`, continue silently.
- If support is configurable and already configured, continue silently.
- If configuration or an adapter is required, finish the generic workspace setup, then identify the limitation and give the smallest safe options.
- Do not create, copy, overwrite, or remove `CLAUDE.md`, `GEMINI.md`, `CODEBUDDY.md`, tool rules, symlinks, or user-level settings without explicit approval.
- Prefer a one-time user/global discovery setting over per-project duplicate rule files.
- For project-instruction products such as WorkBuddy or Lingxi, tell the user where to place the bootstrap pointer when that setting cannot be changed from the current environment.
- If host identity or current support is uncertain, report `unknown` and verify current official documentation rather than guessing.
- Report compatibility in chat; do not add a compatibility report to the workspace unless requested.

### 7. Validate and hand off

Confirm that:

- every path referenced by `AGENTS.md` exists;
- `docs/tasks/INDEX.md` exists and `TEMPLATE.md` is not listed as a task;
- a first-initialization workspace lists `docs/tasks/YYYY-MM-DD-initialize-workspace.md` as Completed;
- `AGENTS.md` tells agents to identify whether a request continues an unfinished task or starts a new one;
- `AGENTS.md` and the human-facing navigation expose `HISTORY.md` when no equivalent work-history index already exists;
- `AGENTS.md` is concise and contains no duplicated project encyclopedia;
- `PROJECT.md`, `STATE.md`, `HISTORY.md`, and `DECISIONS.md` have distinct responsibilities;
- history entries describe completed outcomes or reusable findings, not chat turns;
- raw inputs, intermediate work, and deliverables have clear boundaries when those directories exist;
- sensitive files and generated artifacts are not accidentally selected for version control;
- discovered setup, test, build, and verification commands are exact and executable, or are explicitly documented as not yet defined.

Report created, skipped, and modified files; compatibility status; validation performed; conservative defaults used; and remaining decisions. Do not create a separate initialization report file.

## Safety constraints

- Keep chat history and proprietary agent memory as non-authoritative caches.
- Never write secrets, credentials, personal tokens, or private raw-data samples into context documents.
- Treat `inputs/` as immutable by default. Write transformations to `work/` and deliverables to `outputs/`.
- Preserve unrelated user changes and disclose any validation that could not run.
- Keep tool-specific behavior outside the canonical project rules unless it is essential and explicitly approved.
