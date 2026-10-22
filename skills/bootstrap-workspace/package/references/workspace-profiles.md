# Workspace profiles

Use the smallest profile that matches the user's actual work. The profile selects useful directory boundaries; it does not choose a technology stack or application architecture.

Every profile organizes work as `tasks/YYMMDD-<task-description>/` folders containing `TASK.md` and, when needed, `inputs/`, `work/`, and `outputs/`. The table lists only the additional top-level directories.

## Selection table

| Profile | Use when | Top-level directories | Default assumptions |
| --- | --- | --- | --- |
| `minimal` | Purpose is early, general, or still evolving | None | Create only context documents |
| `code` | Main deliverable is software, scripts, or infrastructure | `scripts/` | Preserve framework-native source and test layout |
| `data` | Raw files are transformed into datasets, workbooks, reports, or imports | `shared/`, `scripts/` | Raw inputs are immutable; intermediate work is reproducible |
| `research` | Main work is collecting evidence, notes, citations, and analysis | `shared/` | Preserve source provenance and retrieval dates when applicable |
| `content` | Inputs become articles, reports, decks, media scripts, or campaigns | `shared/` | Separate source material, drafts, and approved deliverables |
| `mixed` | Code and non-code artifacts are both first-class | `shared/`, `scripts/` | Use existing code conventions and general artifact boundaries together |

## Empty-workspace questions

Do not present a long questionnaire. Extract known facts first.

When purpose is missing, ask:

> What should this workspace ultimately accomplish? Include what you expect to put into it and the final deliverable you want.

Ask a storage and safety follow-up only when needed:

> Will this remain local or be synchronized with Git/GitHub? Do the inputs contain private, credential-bearing, customer, or unusually large files?

Ask one profile-specific follow-up only when it changes the initial structure:

- `code`: Ask for language, framework, package manager, and known verification commands. If undecided, do not create stack-specific scaffolding.
- `data`: Confirm whether raw inputs must remain unchanged. Default to yes.
- `research`: Ask whether formal sources, citations, and retrieval dates are required. Default to preserving them.
- `content`: Ask for primary audience and delivery format if they are not inferable.
- `mixed`: Clarify which artifacts are authoritative and how code-generated outputs should be separated.

## Adoption rules for non-empty workspaces

- Prefer existing directory names and manifests over a profile's suggested directories.
- Treat `docs/tasks/` or top-level `inputs/`, `work/`, `outputs/` as a legacy layout: do not add `tasks/` or `shared/` beside it. Propose a migration table and move files only after the user confirms.
- Do not create `src/`, `tests/`, dependency files, or build configuration solely because the profile is `code`.
- Record discovered commands and boundaries in `AGENTS.md`; link to detailed existing docs rather than duplicating them.
- If the workspace has no reliable definition of done, record that it is not yet defined and ask before claiming completion criteria.
- If `tasks/` already contains task folders, do not overwrite them. Create a missing `INDEX.md` only as a stub and inventory existing `TASK.md` files into it.

## Git policy

- `none`: Do not create or modify Git configuration.
- `git`: The workspace uses local Git. Create a new `.gitignore` only when none exists; otherwise propose additions.
- `github`: Apply the same local behavior as `git`. Never create a remote or push automatically.
- Sensitive inputs: exclude `tasks/*/inputs/` and `shared/**` while allowing `shared/.gitkeep`, unless the user explicitly chooses to version sanitized inputs.
- Intermediate work: exclude `tasks/*/work/` for data, research, content, and mixed profiles.
- Large files: recommend an appropriate external store or Git LFS after confirming the user's intended workflow; do not enable it automatically.
