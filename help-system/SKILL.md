---
name: help-system
description: "Help system for Claude Code custom skills. Replaces native /help command by providing information about all installed custom skills. Use when user wants to: (1) List all available custom skills, (2) Get help on a specific skill, (3) View all available commands, (4) Understand how to use the skill system."
---

# Help System

Help system for Claude Code custom skills on Kimi API.

## Overview

Replaces the native `/help` command by providing comprehensive information about all installed custom skills and their usage.

## Commands

```bash
# List all installed skills
python3 ~/.claude/custom-skills/help-system/scripts/help_system.py

# Get help for specific skill
python3 ~/.claude/custom-skills/help-system/scripts/help_system.py todo-manager
python3 ~/.claude/custom-skills/help-system/scripts/help_system.py session-manager

# Show all available commands
python3 ~/.claude/custom-skills/help-system/scripts/help_system.py --commands

# Show help about skills in general
python3 ~/.claude/custom-skills/help-system/scripts/help_system.py --about
```

## Available Skills

### Core Skills
- **conversation-resumer**: View and resume previous conversations
- **session-manager**: Rename sessions, view info, graceful exit
- **todo-manager**: Enhanced task management with priorities
- **help-system**: This help system

## Quick Reference

| Command | Skill | Purpose |
|---------|-------|---------|
| `resumer` | conversation-resumer | List/restore conversations |
| `session` | session-manager | Session management |
| `todo` | todo-manager | Task management |
| `help` | help-system | Show this help |
