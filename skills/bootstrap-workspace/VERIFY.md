# bootstrap-workspace 验证

## 检查范围

- 确认本仓库 `package/SKILL.md` 存在且不含本机绝对路径。
- 确认安装脚本只复制 package，不复制管理档案。
- 确认安装后的脚手架脚本可以 `--dry-run`。

## 检查步骤

1. 读取 `skills/bootstrap-workspace/package/SKILL.md`。
2. 运行：

```bash
python3 tests/test_install_skill.py -v
```

3. 需要更新本机安装时，再运行 `scripts/install_skill.py`，不要把测试目录写到直播 Skills 目录。

## 最近结果

- 日期：2026-09-12
- 结果：安装脚本测试通过
- 证据：`test_bootstrap_package_has_skill_entry`、`test_install_copies_package_only`、`test_installed_scaffold_dry_run` 均通过。未覆盖直播 Codex 安装目录。

## 未运行检查

- 未对直播 `~/.codex/skills/bootstrap-workspace` 执行覆盖安装。
- 未在 Cursor 宿主做真实安装回归。
- 未对真实空项目执行非 dry-run 脚手架。
