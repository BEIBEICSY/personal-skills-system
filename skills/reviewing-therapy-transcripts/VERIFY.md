# reviewing-therapy-transcripts 验证

## 检查范围

- 确认 `package/SKILL.md` 存在，且含基本边界和输出前自检。
- 确认 package 不含本机绝对路径或私人逐字稿。
- 确认安装脚本只复制 package。

## 检查步骤

1. 读取 `skills/reviewing-therapy-transcripts/package/SKILL.md`。
2. 运行 `python3 tests/test_install_skill.py -v`。

## 最近结果

- 日期：2026-09-12
- 结果：已收包；安装测试覆盖该 Skill
- 证据：package 含名称、基本边界和输出前自检；未覆盖直播安装目录。

## 未运行检查

- 未进行新的私人逐字稿真实试跑。
- 未覆盖直播 Cursor 安装目录。
