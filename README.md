# Claude Code Custom Skills

用于替代 Kimi API 下不可用的 Claude Code 原生斜杠命令。

## 已开发 Skill

| Skill | 替代命令 | 功能 |
|-------|---------|------|
| conversation-resumer | `/continue`, `/resume`, `/history` | 查看/恢复历史对话 |
| session-manager | `/rename`, `/exit`, `/info` | 会话管理 |
| todo-manager | `/todo` | 任务管理 |
| help-system | `/help` | 帮助系统 |

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

### 3. 配置别名（可选）
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
```

## 文件结构

```
~/.claude/custom-skills/
├── conversation-resumer/
├── session-manager/
├── todo-manager/
├── help-system/
└── .bash_aliases
```

## License

MIT
