# Agent compatibility

Treat this matrix as a starting point, not an eternal product guarantee. Inspect effective configuration and verify current official documentation when behavior may have changed.

Last reviewed: 2026-08-29.

## Compatibility states

| State | Meaning | Skill behavior |
| --- | --- | --- |
| `native` | Current host discovers `AGENTS.md` without extra setup | Continue without asking compatibility questions |
| `configured` | Host can use `AGENTS.md` and effective configuration already enables it | Continue silently |
| `adapter-required` | Host needs a global instruction, project setting, config change, import, or symlink | Finish generic setup, then explain options and ask before mutation |
| `unknown` | Host or behavior cannot be identified reliably | Do not guess; report uncertainty and verify documentation |

## Known host patterns

| Host | Starting classification | Check or recommendation |
| --- | --- | --- |
| OpenAI Codex | `native` | Codex discovers root and scoped nested `AGENTS.md`; no compatibility question is needed. See [official discovery rules](https://learn.chatgpt.com/docs/agent-configuration/agents-md). |
| Cursor | `native` | Cursor supports a root `AGENTS.md` as a simple project rule. Keep Cursor-only scoped behavior in `.cursor/rules`. See [Cursor Rules](https://docs.cursor.com/context/rules-for-ai). |
| CodeBuddy IDE | `native` when fallback applies | When root `CODEBUDDY.md` is absent, CodeBuddy loads root `AGENTS.md`. If both exist, inspect for drift instead of assuming the canonical file wins. See [CodeBuddy Rules](https://www.workbuddy.cn/docs/ide/User-guide/Rules). |
| Gemini CLI | `configured` or `adapter-required` | Inspect effective settings. Prefer a one-time `context.fileName` configuration containing `AGENTS.md`; do not add `GEMINI.md` just for compatibility. See [Gemini context files](https://geminicli.com/docs/cli/gemini-md/). |
| Claude Code | `adapter-required` | Claude Code officially discovers `CLAUDE.md`, not `AGENTS.md`. Prefer one user-level pointer in `~/.claude/CLAUDE.md` telling Claude to read the current workspace root `AGENTS.md`; ask before editing it. See [Claude Code memory](https://docs.anthropic.com/en/docs/claude-code/memory). |
| Tencent WorkBuddy | `adapter-required` | Automatic `AGENTS.md` discovery is not established. For a WorkBuddy **Project**, put only the discovery pointer in the project's **Instructions** field; all project tasks inherit it. For an ordinary local task, use the pointer in the opening prompt or a small WorkBuddy Skill. See [WorkBuddy project configuration](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project). |
| Lingxi | `adapter-required` | Put a short discovery pointer in **Project → Instructions** so new project tasks inherit it; do not copy the project rules themselves into that field. See [Lingxi project configuration](https://www.lingxi.cn/docs). |

## Detection rules

- Trust explicit runtime/system identity over repository filenames.
- A `CLAUDE.md`, `GEMINI.md`, or `CODEBUDDY.md` file indicates configuration presence, not necessarily the current host.
- Inspect whether an adapter imports or points to `AGENTS.md`; do not assume any file with that name is compatible.
- Detect conflicting duplicated rules and report drift risk. Never delete or rewrite them automatically.
- Do not edit user-home configuration from a workspace task without explicit authorization and appropriate filesystem permission.
- If the host uses a GUI-only project instruction and it cannot be inspected, say that compatibility cannot be verified automatically and provide this thin bootstrap pointer to copy:

  > Before every new task, read the workspace-root `AGENTS.md` and follow its referenced project context in order.

- For an ordinary WorkBuddy task that is not inside a configured WorkBuddy Project, provide the pointer as a new-task prompt or recommend packaging it as a small WorkBuddy Skill. Do not pretend that merely selecting a filesystem workspace guarantees discovery.
