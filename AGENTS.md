# Workspace instructions

## Startup

Before making changes:

1. Read `README.md`.
2. Read `docs/PROJECT.md` and `docs/STATE.md`.
3. Read `SKILLS.md` to identify the relevant Skill, its source of truth, installation path, and verification status.
4. Read the newest relevant entry in `docs/HISTORY.md` and the active task under `docs/tasks/` when one exists.
5. Before modifying a Skill, read its complete `SKILL.md` and any referenced rules or tests.
6. Preserve existing user-authored content and inspect Git status when a managed source workspace uses Git.

## Source-of-truth order

1. The user's current explicit instruction.
2. The active task specification.
3. The managed Skill's tests, schemas, and executable contracts.
4. `docs/DECISIONS.md`.
5. `docs/PROJECT.md`, `docs/STATE.md`, and `SKILLS.md`.
6. `README.md`.
7. Chat history and agent-specific memory.

## Workspace boundaries

- This workspace is where personal Skills are created, registered, packaged, and maintained. It is also the source of truth for Skills that already have `skills/<id>/package/`.
- Create or change a Skill only when the user's instruction or an active task requires it. Do not copy, relocate, install, or uninstall a managed Skill casually.
- New Skills start from `templates/skill-record/`, live under `skills/<id>/`, put installable content in `package/` when ready, and register in `SKILLS.md`.
- For a packaged Skill, edit `skills/<id>/package/` here, then install or update with `scripts/install_skill.py`. Do not treat a host install directory as the canonical source after packaging.
- Keep personal finance records, psychological consultation content, important-conversation recordings or transcripts, credentials, tokens, and other private raw data out of this workspace.
- Inventory credentials only by dependency type and storage location; never record secret values.
- Record uncertainty explicitly. A user-confirmed Skill with an unverified path must remain marked `待核验`.
- Put repeatable inventory, validation, or synchronization steps in `scripts/` and document how to run them.

## Completion

Before reporting completion:

1. Run the smallest relevant validation that exists.
2. Confirm every path added to `SKILLS.md` exists, or mark it unverified.
3. Review changed-file scope and preserve unrelated changes.
4. Update the active task and `docs/STATE.md` when progress changes.
5. Record meaningful outcomes in `docs/HISTORY.md` and durable choices in `docs/DECISIONS.md`.
6. Report changed files, verification results, unrun checks, and remaining issues.
