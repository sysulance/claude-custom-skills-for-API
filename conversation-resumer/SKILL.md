---
name: conversation-resumer
description: "Resume and restore previous Claude Code conversations from local history. Use when user wants to: (1) Continue a previous conversation or project, (2) View conversation history with visual formatting, (3) Restore context from past work, (4) List all past conversations grouped by time or project, (5) Export conversations to markdown. This skill scans ~/.claude/projects/ to find and display conversation history with timestamps, working directories, and message previews."
---

# Conversation Resumer

Scan and restore Claude Code conversation history from local storage with enhanced visualization.

## Overview

Claude Code stores conversation history in `~/.claude/projects/`. This skill helps users:
1. View all past conversations with **visual formatting** (time-grouped or project-grouped)
2. See **message counts** and **conversation duration**
3. Find specific projects or topics quickly
4. Restore context from previous work
5. Export conversations for review

## Commands

### Default: Time-Grouped View (Recommended)

Shows conversations grouped by time periods (Today, Yesterday, This Week, etc.):

```bash
python3 ~/.claude/plugins/conversation-resumer/scripts/scan_history.py
```

### Project-Grouped View

Shows conversations grouped by project category:

```bash
python3 ~/.claude/plugins/conversation-resumer/scripts/scan_history.py --project
```

### Statistics Only

Display summary statistics:

```bash
python3 ~/.claude/plugins/conversation-resumer/scripts/scan_history.py --stats
```

### Export a Conversation

Export specific conversation to markdown:

```bash
python3 ~/.claude/plugins/conversation-resumer/scripts/scan_history.py --export <jsonl_file_path> <output_markdown_file>
```

### Interactive Mode

Show list and allow interactive selection:

```bash
python3 ~/.claude/plugins/conversation-resumer/scripts/scan_history.py --interactive
```

## Display Format

The enhanced visualization shows:

```
╔══════════════════════════════════════════════════════════════════════════════════════════╗
║                             📚 CONVERSATION HISTORY 📚                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════════╣
║  Total: 22 conversations  (showing top 22)                                               ║
╚══════════════════════════════════════════════════════════════════════════════════════════╝

📅 Today
────────────────────────────────────────────────────────────────────────────────────────────
  [ 1] 03/02 14:38   393KB    206 msgs, 12h8m
      📂 ~
      💬 可以帮我把工作目录调整到桌面上的 CC 文件夹中吗？

📅 Yesterday
────────────────────────────────────────────────────────────────────────────────────────────
  [ 2] 03/01 13:59   6.3MB   1031 msgs, 21h53m
      📂 ~-Desktop-CC-20180901-OSA-dietary
      💬 这是一个尚未完成的研究项目...

🔬 OSA Dietary Research (5 conversations, 9.2MB)
────────────────────────────────────────────────────────────────────────────────────────────
  [ 1] 03/01 13:59   6.3MB   1031 msgs, 21h53m
      💬 这是一个尚未完成的研究项目...
```

## Workflow: Resume Previous Work

When user says "continue my previous work" or similar:

### Step 1: Scan History

Run the scan script with visual output:

```bash
python3 ~/.claude/plugins/conversation-resumer/scripts/scan_history.py
```

### Step 2: Present Options

Show user the formatted list with:
- **Time grouping**: Today, Yesterday, This Week, etc.
- **Or project grouping**: OSA Research, Financial Plugins, CATL Analysis, etc.
- **Key metrics**: File size, message count, duration
- **Message preview**: First user message

### Step 3: User Selection

Ask user: "Which conversation would you like to continue? (Enter number 1-20, or describe the topic)"

### Step 4: Read and Summarize

After user selects, read the corresponding JSONL file and extract:
- Original user request (first user message)
- Main deliverables or outputs created
- Files created or modified
- Decisions made
- Pending items or next steps

Provide a brief summary:

> "Based on your conversation from [date], you were working on [project]. Progress: [summary]. Next step: [action]. Would you like to continue?"

## File Locations

| Type | Path |
|------|------|
| Projects directory | `~/.claude/projects/` |
| Conversation files | `~/.claude/projects/<project_name>/<session_id>.jsonl` |
| Skill script | `~/.claude/plugins/conversation-resumer/scripts/scan_history.py` |

## Notes

- Conversations are sorted by timestamp (newest first)
- File sizes indicate conversation length (larger = more content)
- Message count and duration help identify substantial conversations
- Project names are auto-formatted (`-Users-villageson` → `~`)
- Icons indicate project type: 🔬 Research, 💰 Finance, 🔋 CATL, 🧪 Test
