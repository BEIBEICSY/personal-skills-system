# bootstrap-workspace 验证

## 检查范围

- 确认本仓库 `package/SKILL.md` 存在且不含本机绝对路径。
- 确认安装脚本只复制 package，不复制管理档案。
- 确认安装后的脚手架脚本可以 `--dry-run`。
- 确认首次初始化写入任务清单和初始化任务；接管已有 `AGENTS.md` 时不伪造初始化任务。

## 检查步骤

1. 读取 `skills/bootstrap-workspace/package/SKILL.md`。
2. 运行：

```bash
python3 tests/test_install_skill.py -v
python3 tests/test_scaffold_workspace.py -v
```

3. 空目录脚手架 dry-run / 实际写入必须包含 `docs/tasks/INDEX.md`、`docs/tasks/TEMPLATE.md`、`docs/tasks/当天日期-initialize-workspace.md`。
4. 已有 `AGENTS.md` 的目录不得被覆盖，也不得新增 initialize-workspace 任务；缺 INDEX 时只补 stub。
5. 需要更新本机安装时，再运行 `scripts/install_skill.py`，不要把测试目录写到直播 Skills 目录。

## 最近结果

- 日期：2026-09-22
- 结果：安装脚本测试与脚手架测试通过
- 证据：`python3 tests/test_scaffold_workspace.py -v` 5 passed；`python3 tests/test_install_skill.py -v` 4 passed。随后按用户要求安装到本机 Cursor 与 Codex。

## 未运行检查

- 未对真实私人项目做非 dry-run 脚手架试跑。
- 未用对话模拟测试自动识别规则；规则写在 `SKILL.md` 与生成的 `AGENTS.md` 中。
