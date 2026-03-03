---
name: todo-manager
description: "Enhanced todo/task management for Claude Code. Replaces native /todo slash command with advanced features: cross-project task views, priority levels, tags/categories, completion statistics, and overdue tracking. Use when user wants to: (1) View all pending todos across projects, (2) Add tasks with priorities and tags, (3) Track task completion statistics, (4) Filter todos by project, priority, or tag."
---

# Todo Manager

Enhanced task management for Claude Code users on Kimi API.

## Overview

Replaces the native `/todo` command with enhanced functionality including cross-project views, priorities, tags, and statistics.

## Commands

### View Todos
```bash
python3 ~/.claude/custom-skills/todo-manager/scripts/todo_manager.py
python3 ~/.claude/custom-skills/todo-manager/scripts/todo_manager.py --all
python3 ~/.claude/custom-skills/todo-manager/scripts/todo_manager.py --priority high
```

### Add Tasks
```bash
python3 ~/.claude/custom-skills/todo-manager/scripts/todo_manager.py add "Complete DCF model"
python3 ~/.claude/custom-skills/todo-manager/scripts/todo_manager.py add "Review report" --priority high --tag urgent
```

### Complete Tasks
```bash
python3 ~/.claude/custom-skills/todo-manager/scripts/todo_manager.py done 3
```

### Statistics
```bash
python3 ~/.claude/custom-skills/todo-manager/scripts/todo_manager.py --stats
```

## Features

- Cross-project views
- Priority levels: High, Medium, Low
- Tags/Categories
- Due dates
- Statistics
