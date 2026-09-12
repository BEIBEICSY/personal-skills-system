# reviewing-important-conversations 验证

## 检查范围

- 确认 `package/SKILL.md` 与 `package/templates.md` 存在。
- 确认 package 不含本机绝对路径或私人沟通原文。
- 确认安装脚本只复制 package。

## 检查步骤

1. 读取 `skills/reviewing-important-conversations/package/SKILL.md`。
2. 确认 `package/templates.md` 可读。
3. 运行 `python3 tests/test_install_skill.py -v`。

## 最近结果

- 日期：2026-09-12
- 结果：已收包；安装测试覆盖该 Skill
- 证据：核心原则、权力关系和完成前核对存在；`templates.md` 一并收录。

## 未运行检查

- 未进行真实沟通材料试跑。
- 未覆盖直播 Cursor 安装目录。
