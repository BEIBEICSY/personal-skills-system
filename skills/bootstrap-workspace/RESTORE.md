# bootstrap-workspace 恢复

## 前置条件

- 已克隆 `https://github.com/BEIBEICSY/personal-skills-system`。
- 目标 Agent 的 Skills 目录可写。
- 不把凭证或私人原始输入复制进本仓库。

## 自己或朋友安装

```bash
git clone https://github.com/BEIBEICSY/personal-skills-system.git
cd personal-skills-system
python3 scripts/install_skill.py bootstrap-workspace --host cursor
# 或
python3 scripts/install_skill.py bootstrap-workspace --host codex
```

自定义目录：

```bash
python3 scripts/install_skill.py bootstrap-workspace --target ~/custom/skills/bootstrap-workspace
```

## 更新

1. 在本仓库修改 `skills/bootstrap-workspace/package/`。
2. `git push`。
3. 各设备 `git pull` 后重新运行安装脚本。

## 恢复后验证

- 目标目录存在 `SKILL.md`。
- `python3 <install-dir>/scripts/scaffold_workspace.py --help` 可运行。
- 管理档案 `manifest.yaml` 没有被复制到安装目录。

## 人工介入点

- 覆盖已有安装前先确认对方没有未同步的本地改动。
- 本机自定义路径写到 `local/bootstrap-workspace.yaml`，不要提交。
- 仓库是私有的；朋友使用前需要先获得 GitHub 协作权限。
