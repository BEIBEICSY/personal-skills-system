# Changelog

Newest version first. Each heading is `## <version> — <date>`.

## 0.4.0 — 2026-10-22

- New `Archive inputs first` rule: files the user provides, even outside the workspace (Desktop, Downloads, chat attachments), are copied into the task's `inputs/` before use, hash-checked, and recorded with source path, received date, and SHA-256 in `TASK.md`. Move only on explicit request; record a gap when a file cannot be archived.
- Task template and README explain the archive fields.

## 0.3.0 — 2026-10-22

- Work is organized as one folder per task: `tasks/YYMMDD-<task-description>/` with `TASK.md` and, when needed, `inputs/`, `work/`, `outputs/`. Shared material goes to `shared/`; no top-level `inputs/`, `work/`, `outputs/`, or `docs/tasks/`.
- Deliverables are named `<deliverable>-<草稿|定稿>`.
- Following up a completed task asks whether to start a new task folder or continue in the existing one.
- `README.md` explains each directory in plain language.
- Legacy layouts are detected; files move only after the user confirms a migration table, with hash and link checks.
- Each use first checks GitHub for a newer version and tells the user what changed and how to update.

## 0.2.0 — 2026-10-20

- Task index and initialize-workspace task on first initialization; tasks named `YYMMDD-<task-description>`.
