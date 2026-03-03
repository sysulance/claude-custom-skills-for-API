# Claude Code Custom Skills

用于替代 Kimi API 下不可用的 Claude Code 原生斜杠命令。

## 已开发 Skill

| Skill | 替代命令 | 功能 |
|-------|---------|------|
| conversation-resumer | `/continue`, `/resume`, `/history` | 查看/恢复历史对话 |
| session-manager | `/rename`, `/exit`, `/info` | 会话管理 |
| todo-manager | `/todo` | 任务管理 |
| help-system | `/help` | 帮助系统 |
| file-history-browser | `/file` | 查看文件操作历史 |
| cross-project-search | `/search` | 跨项目搜索内容 |

## 安装方法

### 1. 克隆仓库
```bash
git clone https://github.com/yourusername/claude-custom-skills.git
```

### 2. 安装 Skill
```bash
cd claude-custom-skills
./install.sh
```

### 3. 启用 Skill（⚠️ 重要）

**必须**在 `~/.claude/settings.json` 中启用这些 skill，否则 Claude Code 无法识别：

```bash
# 编辑配置文件
nano ~/.claude/settings.json
```

在 `enabledPlugins` 中添加所有 skill：

```json
{
  "enabledPlugins": {
    "conversation-resumer@local": true,
    "cross-project-search@local": true,
    "file-history-browser@local": true,
    "help-system@local": true,
    "session-manager@local": true,
    "todo-manager@local": true
  }
}
```

**注意**：修改配置后需要**重启 Claude Code** 才能生效。

### 4. 配置别名（可选）
```bash
source ~/.claude/custom-skills/.bash_aliases
```

## 使用方式

```bash
resumer              # 查看历史对话
session list         # 列出会话
session rename XXX   # 重命名会话
todo add "任务"       # 添加任务
help-cc              # 显示帮助
file-history         # 查看文件操作历史
project-search XXX   # 跨项目搜索
```

## 文件结构

```
~/.claude/custom-skills/
├── conversation-resumer/     # 历史对话恢复
├── session-manager/          # 会话管理
├── todo-manager/             # 任务管理
├── help-system/              # 帮助系统
├── file-history-browser/     # 文件操作历史
├── cross-project-search/     # 跨项目搜索
├── .bash_aliases             # 快捷命令别名
├── install.sh                # 一键安装脚本
└── README.md                 # 使用说明
```

## 更新日志

### 2025-03-03 - 重要修复

**问题**：新终端窗口中 Claude Code 无法识别已安装的自定义 skill

**原因**：Claude Code 只在 `~/.claude/settings.json` 的 `enabledPlugins` 中加载明确启用的 skill。仅将 skill 文件放在 `custom-skills` 目录中是不够的。

**解决方案**：
1. 在 `~/.claude/settings.json` 中添加所有 skill 到 `enabledPlugins`
2. 格式为 `"skill-name@local": true`
3. 修改后需要**重启 Claude Code**

**参考配置**：
```json
{
  "enabledPlugins": {
    "conversation-resumer@local": true,
    "cross-project-search@local": true,
    "file-history-browser@local": true,
    "help-system@local": true,
    "session-manager@local": true,
    "todo-manager@local": true
  }
}
```

## License

MIT
