# reviewing-therapy-transcripts 恢复

## 前置条件

- 已克隆 `https://github.com/BEIBEICSY/personal-skills-system`。
- 目标 Agent 的 Skills 目录可写。
- 不复制逐字稿或复盘产物到本仓库。

## 安装或更新

```bash
python3 scripts/install_skill.py reviewing-therapy-transcripts --host cursor
```

## 恢复后验证

- 目标目录存在 `SKILL.md`。
- 基本边界和输出前自检仍在。
- 本仓库没有新增私人咨询原文。

## 人工介入点

- 真实复盘只在用户主动提供逐字稿时进行。
- 复盘产物保存在用户指定的外部工作区。
- 仓库是私有的；朋友使用前需要 GitHub 协作权限。
