# bootstrap-workspace 验证

## 检查范围

- 确认本仓库 `package/SKILL.md` 存在且不含本机绝对路径。
- 确认安装脚本只复制 package，不复制管理档案。
- 确认安装后的脚手架脚本可以 `--dry-run`。
- 确认首次初始化写入任务清单和初始化任务；接管已有 `AGENTS.md` 时不伪造初始化任务。
- 确认 `VERSION`、`manifest.yaml`、`CHANGELOG.md` 首条版本一致；更新检查在已最新、有新版、本机领先、无法访问四种情况下都不报错退出。
- 确认按任务文件夹组织：不建顶层 `inputs/`、`work/`、`outputs/`；产物型 profile 建 `shared/`；旧布局工作区只提示迁移、不混建 `tasks/`。

## 检查步骤

1. 读取 `skills/bootstrap-workspace/package/SKILL.md`。
2. 运行：

```bash
python3 tests/test_install_skill.py -v
python3 tests/test_scaffold_workspace.py -v
python3 tests/test_check_update.py -v
```

3. 空目录脚手架 dry-run / 实际写入必须包含 `tasks/INDEX.md`、`tasks/TEMPLATE.md`、`tasks/YYMMDD-initialize-workspace/TASK.md`，且不出现 `docs/tasks/`。
4. 已有 `AGENTS.md` 的目录不得被覆盖，也不得新增 initialize-workspace 任务；缺 INDEX 时只补 stub。
5. 需要更新本机安装时，再运行 `scripts/install_skill.py`，不要把测试目录写到直播 Skills 目录。

## 最近结果

- 日期：2026-10-22
- 结果：改为任务文件夹结构 `tasks/YYMMDD-<task-description>/`（`TASK.md` + `inputs/` / `work/` / `outputs/`），共用资料放 `shared/`；旧布局检测生效。
- 结果补充：版本 0.3.0，新增使用前更新检查。
- 证据：`python3 tests/test_check_update.py -v` 7 passed；对真实 GitHub 运行检查可访问私有仓库（约 1.8 秒），因远端尚无 `VERSION` 返回 `unknown` 并说明原因。`python3 tests/test_scaffold_workspace.py -v` 8 passed；`python3 tests/test_install_skill.py -v` 4 passed；对评级工作区 dry-run 输出 `Legacy layout detected`，未写入文件。随后安装到本机 Cursor 与 Codex，并与 package 逐文件比对一致。

## 未运行检查

- 未对真实私人项目做非 dry-run 脚手架试跑。
- 未在真实工作中试跑「跟进已完成任务时询问新建还是续记」规则。
- 未用对话模拟测试自动识别规则；规则写在 `SKILL.md` 与生成的 `AGENTS.md` 中。
