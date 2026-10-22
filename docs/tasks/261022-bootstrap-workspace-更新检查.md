# Task: bootstrap-workspace 使用前检查 GitHub 新版

## Objective

每次使用 `bootstrap-workspace` 时先对比本机版本与 GitHub `main` 上的版本；有新版时告诉用户最新版本号、改了什么、如何更新，不自动更新。

## Inputs

- 用户要求：每次使用时查询 GitHub 是否有最新版，有则提示更新并告知最新版是什么。
- 仓库：`https://github.com/BEIBEICSY/personal-skills-system`（私有，本机 Git 通过钥匙串凭据可读）。

## Outputs

- `package/VERSION`、`package/CHANGELOG.md`、`package/update.json`、`package/scripts/check_update.py`。
- `SKILL.md` 增加使用前检查步骤；本仓库 `AGENTS.md` 增加发版纪律。
- 测试：`tests/test_check_update.py`。

## Constraints

- 只用 Git 访问，不依赖 `gh` 登录；不读取或记录凭据。
- 检查失败（无网、无权限、超时）不得阻塞工作。
- 起初只覆盖 `bootstrap-workspace`；用户随后要求推广到全部四个已收包 Skill。

## Acceptance criteria

- 已最新、有新版、本机领先、无法访问四种情况都有测试覆盖。
- `VERSION`、`manifest.yaml`、`CHANGELOG.md` 首条版本一致，并有测试保证。
- 安装后的副本可运行检查脚本。

## Progress

- Completed.
- 2026-10-22：用户确认设计，范围先限 `bootstrap-workspace`；与任务文件夹改造合并发布为 0.3.0。
- 2026-10-22：实现并测试完成，安装到本机 Cursor / Codex。推送与否待用户决定；推送前远端无 `VERSION`，检查返回 `unknown`。
- 2026-10-22：用户要求提交推送，并把检查推广到其余三个 Skill（各升 0.2.0）。两个复盘 Skill 已更新本机安装；记账 Skill 的 Codex 安装是收包前旧版，未覆盖，待用户决定。

## Outcome

- `skills/bootstrap-workspace/package/` 新增 `VERSION`（0.3.0）、`CHANGELOG.md`、`update.json`、`scripts/check_update.py`；`SKILL.md` 第 0 步。
- 本仓库 `AGENTS.md` 发版纪律；决策见 `docs/DECISIONS.md`。

## Verification

- `python3 tests/test_check_update.py -v`：7 passed（已最新、有新版只列更新条目、本机领先、远端不可达、三处版本一致、配置、SKILL 步骤）。
- `python3 tests/test_scaffold_workspace.py -v`：8 passed；`python3 tests/test_install_skill.py -v`：4 passed。
- 真实仓库：私有仓库经钥匙串凭据可读，约 1.8 秒；远端尚无 `VERSION`，返回 `unknown` 并说明原因。
- 推送后（`062c1b1`）真实链路：本机五份安装副本均为 `up-to-date`（每次约 2–4 秒）；把 bootstrap-workspace 副本改为 0.2.0 后返回 `update-available`，列出 0.3.0 改动与更新命令。
