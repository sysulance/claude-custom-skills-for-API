# File History Browser

替代 Claude Code 的 `/file` 命令，用于查看对话中的文件操作历史。

## 功能

- 列出对话中打开/编辑的所有文件
- 显示文件操作时间线
- 快速跳转到最近使用的文件
- 统计文件类型分布

## 使用方式

```bash
# 列出当前会话的文件历史
file-history

# 显示文件操作时间线
file-history timeline

# 显示最近使用的文件
file-history recent

# 统计文件类型
file-history stats

# 搜索文件名
file-history search <keyword>
```

## 别名

```bash
fh           # file-history 的快捷方式
fh-timeline  # file-history timeline
fh-recent    # file-history recent
fh-stats     # file-history stats
```

## 安装

```bash
chmod +x ~/.claude/custom-skills/file-history-browser/scripts/file_history.py
```
