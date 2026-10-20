#!/usr/bin/env python3
"""Safely scaffold durable, tool-neutral workspace context files."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


PROFILE_DIRECTORIES = {
    "minimal": (),
    "code": ("scripts",),
    "data": ("inputs", "work", "outputs", "scripts"),
    "research": ("inputs", "work", "outputs"),
    "content": ("inputs", "work", "outputs"),
    "mixed": ("inputs", "work", "outputs", "scripts"),
}

ARTIFACT_PROFILES = {"data", "research", "content", "mixed"}

PROFILE_LABELS = {
    "minimal": "minimal（仅上下文）",
    "code": "code（代码项目）",
    "data": "data（数据处理）",
    "research": "research（调研项目）",
    "content": "content（内容生产）",
    "mixed": "mixed（混合工作区）",
}


@dataclass(frozen=True)
class PlannedFile:
    relative_path: Path
    content: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create missing workspace context files without overwriting existing files."
        )
    )
    parser.add_argument("--target", required=True, help="Existing workspace directory")
    parser.add_argument(
        "--profile",
        choices=tuple(PROFILE_DIRECTORIES),
        default="minimal",
        help="Workspace profile (default: minimal)",
    )
    parser.add_argument("--project-name", required=True, help="Human-readable project name")
    parser.add_argument("--goal", required=True, help="Primary project goal")
    parser.add_argument("--inputs", required=True, help="Expected source materials or inputs")
    parser.add_argument("--outputs", required=True, help="Expected final deliverables")
    parser.add_argument("--audience", help="Primary audience or user, if known")
    parser.add_argument(
        "--git-mode",
        choices=("none", "git", "github"),
        default="none",
        help="Describe intended version-control mode; does not initialize Git",
    )
    parser.add_argument(
        "--sensitive-inputs",
        action="store_true",
        help="Keep inputs out of Git via generated .gitignore rules",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the proposed changes without writing anything",
    )
    return parser.parse_args()


def require_text(label: str, value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{label} must not be empty")
    if "\x00" in cleaned:
        raise ValueError(f"{label} contains a null byte")
    return cleaned


def resolve_target(raw_target: str) -> Path:
    target = Path(raw_target).expanduser()
    if target.is_symlink():
        raise ValueError("target workspace must not be a symbolic link")
    if not target.exists():
        raise ValueError("target workspace must already exist")
    if not target.is_dir():
        raise ValueError("target workspace must be a directory")

    resolved = target.resolve()
    if resolved == Path(resolved.anchor):
        raise ValueError("refusing to scaffold a filesystem root")
    return resolved


def read_template(skill_root: Path, name: str) -> str:
    template_path = skill_root / "assets" / "templates" / name
    if not template_path.is_file():
        raise ValueError(f"missing bundled template: {template_path}")
    return template_path.read_text(encoding="utf-8")


def render(template: str, values: dict[str, str]) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    if "{{" in rendered or "}}" in rendered:
        raise ValueError("template contains an unresolved placeholder")
    return rendered


def directory_map(profile: str) -> str:
    rows = [
        "- `AGENTS.md`：所有 Agent 共用的入口、边界和工作规则。",
        "- `README.md`：给人看的项目入口。",
        "- `docs/PROJECT.md`：项目目标、范围、输入和交付物。",
        "- `docs/STATE.md`：当前进度、下一步与阻塞项。",
        "- `docs/HISTORY.md`：过去完成事项、结果和产物的简明索引。",
        "- `docs/DECISIONS.md`：重要决策及其理由。",
        "- `docs/tasks/INDEX.md`：任务总清单。",
        "- `docs/tasks/TEMPLATE.md`：任务档案模板。",
    ]
    additions = {
        "scripts": "- `scripts/`：可复现的自动化脚本。",
        "inputs": "- `inputs/`：原始输入；默认视为只读。",
        "work": "- `work/`：可再生成的中间产物。",
        "outputs": "- `outputs/`：最终或可交付成果。",
    }
    rows.extend(additions[name] for name in PROFILE_DIRECTORIES[profile])
    return "\n".join(rows)


def directory_rules(profile: str) -> str:
    rules = []
    if "inputs" in PROFILE_DIRECTORIES[profile]:
        rules.append("- 不修改 `inputs/` 中的原始材料；需要清洗或转换时写入 `work/`。")
    if "work" in PROFILE_DIRECTORIES[profile]:
        rules.append("- `work/` 中只放可重建的中间产物，不把它当作唯一事实来源。")
    if "outputs" in PROFILE_DIRECTORIES[profile]:
        rules.append("- 最终交付物写入 `outputs/`，并在 `docs/STATE.md` 标注状态。")
    if "scripts" in PROFILE_DIRECTORIES[profile]:
        rules.append("- 重复执行的步骤优先沉淀到 `scripts/`，并写明运行方式。")
    if not rules:
        rules.append("- 新增目录前先确认其长期用途，避免为了模板完整而制造空结构。")
    return "\n".join(rules)


def profile_decision(profile: str) -> str:
    if profile in ARTIFACT_PROFILES:
        return (
            "采用原始输入、中间过程和最终交付物分离的结构：`inputs/` 保留原始材料，"
            "`work/` 存放可再生成的过程文件，`outputs/` 存放交付物。"
        )
    if profile == "code":
        return (
            "当前只预建 `scripts/`，不在不了解技术栈时猜测 `src/`、`tests/` 或依赖结构。"
        )
    return "先采用最小上下文结构；仅在实际工作需要时增加业务目录。"


def gitignore_rules(profile: str, sensitive_inputs: bool) -> str:
    rules = []
    if profile in ARTIFACT_PROFILES:
        rules.extend(("work/**", "!work/.gitkeep"))
    if sensitive_inputs and "inputs" in PROFILE_DIRECTORIES[profile]:
        rules.extend(("inputs/**", "!inputs/.gitkeep"))
    return "\n".join(rules)


def build_plan(
    args: argparse.Namespace, skill_root: Path, target: Path
) -> tuple[set[Path], list[PlannedFile]]:
    project_name = require_text("project name", args.project_name)
    goal = require_text("goal", args.goal)
    inputs = require_text("inputs", args.inputs)
    outputs = require_text("outputs", args.outputs)
    audience = args.audience.strip() if args.audience and args.audience.strip() else "尚未明确；确认后更新。"

    values = {
        "PROJECT_NAME": project_name,
        "GOAL": goal,
        "PROFILE": PROFILE_LABELS[args.profile],
        "INPUTS": inputs,
        "OUTPUTS": outputs,
        "AUDIENCE_SECTION": audience,
        "DIRECTORY_MAP": directory_map(args.profile),
        "DIRECTORY_RULES": directory_rules(args.profile),
        "PROFILE_DECISION": profile_decision(args.profile),
        "PROFILE_IGNORE_RULES": gitignore_rules(args.profile, args.sensitive_inputs),
        "DATE": date.today().isoformat(),
        "DATE_COMPACT": date.today().strftime("%y%m%d"),
        "GIT_MODE": args.git_mode,
    }

    template_mapping = {
        Path("README.md"): "README.md.tmpl",
        Path("AGENTS.md"): "AGENTS.md.tmpl",
        Path("docs/PROJECT.md"): "PROJECT.md.tmpl",
        Path("docs/STATE.md"): "STATE.md.tmpl",
        Path("docs/HISTORY.md"): "HISTORY.md.tmpl",
        Path("docs/DECISIONS.md"): "DECISIONS.md.tmpl",
    }
    if args.git_mode != "none":
        template_mapping[Path(".gitignore")] = "gitignore.tmpl"

    template_mapping[Path("docs/tasks/TEMPLATE.md")] = "TASK_TEMPLATE.md.tmpl"
    if (target / "AGENTS.md").exists():
        template_mapping[Path("docs/tasks/INDEX.md")] = "INDEX_STUB.md.tmpl"
    else:
        template_mapping[Path("docs/tasks/INDEX.md")] = "INDEX.md.tmpl"
        template_mapping[
            Path(f"docs/tasks/{values['DATE_COMPACT']}-initialize-workspace.md")
        ] = "INIT_TASK.md.tmpl"

    files = [
        PlannedFile(relative_path, render(read_template(skill_root, template_name), values))
        for relative_path, template_name in template_mapping.items()
    ]

    directories = {Path("docs"), Path("docs/tasks")}
    profile_directories = {Path(name) for name in PROFILE_DIRECTORIES[args.profile]}
    directories.update(profile_directories)

    if args.git_mode != "none":
        for relative_dir in profile_directories:
            files.append(PlannedFile(relative_dir / ".gitkeep", ""))

    return directories, files


def assert_safe_destination(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise ValueError(f"unsafe relative path: {relative_path}")

    current = root
    for part in relative_path.parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"refusing to traverse symbolic link: {current}")

    destination = root / relative_path
    try:
        destination.parent.resolve(strict=False).relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes target workspace: {relative_path}") from exc
    if destination.is_symlink():
        raise ValueError(f"refusing to write through symbolic link: {destination}")
    return destination


def show_plan(root: Path, directories: set[Path], files: list[PlannedFile]) -> None:
    print(f"Target: {root}")
    print("Would create directories:")
    for relative_path in sorted(directories, key=lambda item: (len(item.parts), str(item))):
        destination = assert_safe_destination(root, relative_path / ".path-check")
        status = "exists" if destination.parent.exists() else "create"
        print(f"  [{status}] {relative_path}/")
    print("Would create files:")
    for planned in files:
        destination = assert_safe_destination(root, planned.relative_path)
        status = "skip-existing" if destination.exists() else "create"
        print(f"  [{status}] {planned.relative_path}")
    print("Dry run only; no files were written.")


def apply_plan(root: Path, directories: set[Path], files: list[PlannedFile]) -> None:
    created: list[Path] = []
    skipped: list[Path] = []

    for relative_path in sorted(directories, key=lambda item: (len(item.parts), str(item))):
        destination = assert_safe_destination(root, relative_path / ".path-check").parent
        if destination.exists():
            if not destination.is_dir():
                raise ValueError(f"expected a directory but found a file: {destination}")
            skipped.append(relative_path)
            continue
        destination.mkdir()
        created.append(relative_path)

    for planned in files:
        destination = assert_safe_destination(root, planned.relative_path)
        if destination.exists():
            skipped.append(planned.relative_path)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(planned.content)
        created.append(planned.relative_path)

    print(f"Target: {root}")
    print("Created:")
    if created:
        for relative_path in created:
            suffix = "/" if (root / relative_path).is_dir() else ""
            print(f"  {relative_path}{suffix}")
    else:
        print("  nothing")
    print("Skipped because already present:")
    if skipped:
        for relative_path in skipped:
            print(f"  {relative_path}")
    else:
        print("  nothing")
    print("No existing file was overwritten.")


def main() -> int:
    try:
        args = parse_args()
        target = resolve_target(args.target)
        skill_root = Path(__file__).resolve().parent.parent
        directories, files = build_plan(args, skill_root, target)
        if args.dry_run:
            show_plan(target, directories, files)
        else:
            apply_plan(target, directories, files)
        return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
