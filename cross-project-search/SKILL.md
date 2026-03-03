# Cross-Project Search

替代 Claude Code 的 `/search` 命令，用于跨所有历史对话项目搜索内容。

## 功能

- 在所有对话项目中搜索文本
- 搜索文件内容
- 搜索对话消息
- 按项目名称过滤
- 搜索结果汇总

## 使用方式

```bash
# 在所有项目中搜索关键词
project-search <keyword>

# 搜索文件内容
project-search --files <keyword>

# 搜索对话消息
project-search --messages <keyword>

# 指定项目搜索
project-search --project <name> <keyword>

# 显示搜索结果统计
project-search --stats <keyword>

# 限制结果数量
project-search --limit 20 <keyword>
```

## 别名

```bash
ps          # project-search 的快捷方式
psf         # project-search --files
psm         # project-search --messages
```

## 安装

```bash
chmod +x ~/.claude/custom-skills/cross-project-search/scripts/cross_project_search.py
```
