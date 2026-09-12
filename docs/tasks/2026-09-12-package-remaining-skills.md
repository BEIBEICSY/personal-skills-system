# Task: 将其余三个 Skill 收成可安装包

## Objective

把 `reviewing-therapy-transcripts`、`reviewing-important-conversations`、`bill-to-suishouji` 收成与 `bootstrap-workspace` 相同的可安装包。

## Inputs

- 各 Skill 当前安装目录
- 随手记项目中的脚本、分类体系和测试

## Outputs

- 三个 `skills/<id>/package/`
- 更新后的档案、总表和安装测试

## Constraints

- 不收录账单、咨询逐字稿、沟通原文。
- package 中不写本机绝对路径。
- 不自动覆盖直播安装目录。

## Acceptance criteria

- 四个 Skill 都有 `package/SKILL.md`。
- `python3 tests/test_install_skill.py -v` 通过。
- 记账 package 不含 `inputs/raw` 或 `checks/` 原文。

## Progress

- Completed on 2026-09-12.

## Outcome

- 四个 Skill 都可以从本仓库安装和迭代。

## Verification

- 见 `python3 tests/test_install_skill.py -v`。
- 未覆盖直播安装，未跑记账完整 unittest，未试跑私人材料。
