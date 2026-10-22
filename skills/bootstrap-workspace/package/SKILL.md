---
name: bootstrap-workspace
description: Initialize or adopt a local or GitHub workspace with one canonical AGENTS.md, durable project context and outcome history, safe file boundaries, and agent-host compatibility guidance. Use when a user starts a project, creates an empty workspace or repository, asks to initialize or organize the workspace context/environment, wants seamless switching among coding or office agents, or needs to repair missing or conflicting agent documentation in an existing workspace.
---

# Bootstrap Workspace

Create an agent-neutral workspace whose durable context lives in files and Git history rather than one agent's chat memory. Treat `AGENTS.md` as the only canonical agent-instruction source.

## Workflow

### 0. Check for a newer version

Every time this Skill is used, first resolve its installed directory and run:

```bash
python3 <skill-directory>/scripts/check_update.py
```

It compares the local `VERSION` with the latest `VERSION` on the GitHub branch in `update.json`, using Git and the user's existing credentials. Act on `status`:

- `up-to-date`: continue silently.
- `update-available`: before other work, tell the user in their language the current version, the latest version, a short summary of each newer `changes` entry, and the `update_steps`. Ask whether to update now or continue with the current version. Do not update automatically. If the user chooses to update, run the steps, then re-read the updated `SKILL.md` before continuing.
- `ahead`: mention in one sentence that the local copy is newer than GitHub, probably not pushed yet, and continue.
- `unknown`: mention in one sentence that the check could not run and why, then continue.

Never let the check block the user's work, and never print or store credentials.

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
- `tasks/INDEX.md` for the living task inventory;
- `tasks/TEMPLATE.md` for new `TASK.md` files;
- `tasks/YYMMDD-initialize-workspace/TASK.md` on first initialization only, when `AGENTS.md` is being created.

Organize work by task, then by artifact type. Each task is one folder:

```text
tasks/YYMMDD-<task-description>/
├── TASK.md     objective, inputs used, progress, outputs, verification
├── inputs/     originals received for this task; read-only
├── work/       intermediate drafts; reproducible
└── outputs/    deliverables named <deliverable>-<草稿|定稿>.<ext>
```

Create a task subfolder only when there is a file to put in it. Artifact profiles (`data`, `research`, `content`, `mixed`) also get `shared/` for read-only material used by several tasks, such as standards, baselines, or templates. Do not create top-level `inputs/`, `work/`, or `outputs/`. Add `scripts/` only when the profile benefits from it. Do not impose generic `src/` or `tests/` directories on an established repository or an undecided code stack.

The generated `README.md` explains each directory in plain language for the user, including the rule of thumb: originals from others go to `inputs/`, things to use or send go to `outputs/`, everything else goes to `work/`.

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
- if `tasks/INDEX.md` was just created as a stub, inventory existing `tasks/*/TASK.md` files; mark unknown status as `Unverified` and do not invent an initialize-workspace task;
- if the scaffold reports `Legacy layout detected` (`docs/tasks/` or top-level `inputs/`, `work/`, `outputs/`), do not create a second task system and do not move anything yet. Present a migration table of old path, new path, and owning task, marking uncertain ownership for the user to decide. Move files only after the user confirms, record file hashes before moving, and verify afterwards that every file arrived unchanged. Then repair relative links in every Markdown file, including links that point outside the workspace, and report links that were already broken. Until confirmed, keep working in the legacy layout;

Maintain `docs/HISTORY.md` as a compact, reverse-chronological index rather than a session transcript:

- add an entry only after a meaningful outcome, reusable finding, or consequential failed attempt;
- include the date, task, result, artifacts, verification, and follow-up;
- link to detailed task records, decisions, outputs, or commits instead of copying them;
- do not record routine conversation, private reasoning, raw prompts, or exploration with no durable result;
- keep exact file-level history in Git when Git is in use.

### Task tracking after initialization

Before substantial work in a bootstrapped workspace, read `tasks/INDEX.md` and `docs/STATE.md`, then decide whether the request continues an unfinished task or starts a new one:

- Continue: the requested outcome matches an unfinished task (In progress or Paused). Open its `TASK.md` and continue in that folder. Do not create a new folder because the session changed.
- Follow-up of a Completed task: ask whether to start a new task folder or continue recording in the existing one. If continuing, set it back to In progress and log the date and reason in Progress. If new, link the old task under Related tasks.
- Start: the requested outcome matches no task. Create the folder `tasks/YYMMDD-<task-description>/` with `TASK.md` from `TEMPLATE.md`, Progress `In progress`; add it to `INDEX.md` and point `STATE.md` at it. Do not ask whether to create a task. `YYMMDD` is the start date (`%y%m%d`). `<task-description>` is a short summary of the current task in the user's language; replace spaces with hyphens and strip `/\:*?"<>|`. Do not use `YYYY-MM-DD-slug`. Do not rename the folder when continuing a task.
- Unsure: ask one question naming the closest existing task; do not ask whether to create a task system.

Match on the intended outcome, not the session, date, or wording. Multiple tasks may be in progress at once. Skip a task for pure questions, chat, explaining existing files, or when the user says not to record one. Once files will change or a deliverable will be produced, the work must belong to a task.

Keep every file the task produces inside its folder:

- Archive originals into the task's `inputs/` and record source and received date in `TASK.md`. Reference `shared/` or another task's files by relative path instead of copying; ask before promoting a task's file to `shared/`.
- Name deliverables `outputs/<deliverable>-<草稿|定稿>.<ext>`. Add `-v<N>` before the status only when an older version must be kept. Rename on status change and update links in `TASK.md`.
- List every input and output path in `TASK.md` so the task folder is self-explanatory.

If the user says this continues prior work but no matching task exists, create one and note in Progress that it was created from a continuation request. If one request contains two independent outcomes, split them; create the primary task first and list the other in `INDEX.md` and `STATE.md` next actions.

When completing a task, update `TASK.md`, move it to Completed in `INDEX.md`, and sync `STATE.md`. Keep it In progress when verification failed. Add `HISTORY.md` only for a meaningful outcome, and link the `TASK.md`. If `INDEX.md` and `TASK.md` disagree, trust `TASK.md` and repair `INDEX.md` and `STATE.md`. Never write secrets, bills, therapy transcripts, or conversation transcripts into task files.

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
- `tasks/INDEX.md` exists and `TEMPLATE.md` is not listed as a task;
- a first-initialization workspace lists `tasks/YYMMDD-initialize-workspace/TASK.md` as Completed;
- new tasks are folders named `YYMMDD-<task-description>/` containing `TASK.md`;
- no top-level `inputs/`, `work/`, or `outputs/` was created, and `README.md` explains each directory in plain language;
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
- Treat each task's `inputs/` and `shared/` as immutable by default. Write transformations to the task's `work/` and deliverables to its `outputs/`.
- Preserve unrelated user changes and disclose any validation that could not run.
- Keep tool-specific behavior outside the canonical project rules unless it is essential and explicitly approved.
