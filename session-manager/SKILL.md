---
name: session-manager
description: "Manage Claude Code sessions for Kimi API users. Provides functionality to rename sessions, view session info, and gracefully exit - replacing the native /rename, /exit, and /info slash commands that are unavailable when using third-party APIs like Kimi. Use when user wants to: (1) Rename the current conversation session, (2) View detailed information about the current session, (3) List recent sessions, (4) Gracefully exit with optional state saving."
---

# Session Manager

Manage Claude Code sessions for users on third-party APIs (Kimi) where native slash commands like `/rename`, `/exit`, and `/info` are unavailable.

## Overview

When using Claude Code with third-party APIs (e.g., Kimi), the native slash commands for session management are not available. This skill provides equivalent functionality through executable scripts that operate directly on the local conversation storage.

## Commands

### Rename Current Session

Rename the current conversation session (replaces native `/rename`):

```bash
python3 ~/.claude/custom-skills/session-manager/scripts/session_manager.py rename "New Session Name"
```

### View Session Information

Display detailed information about the current session (replaces native `/info`):

```bash
python3 ~/.claude/custom-skills/session-manager/scripts/session_manager.py info
```

**Shows:**
- Session ID
- Start time and duration
- Number of messages
- Current working directory
- File size

### List Recent Sessions

List recent conversation sessions:

```bash
python3 ~/.claude/custom-skills/session-manager/scripts/session_manager.py list
python3 ~/.claude/custom-skills/session-manager/scripts/session_manager.py list --limit 20
```

### Graceful Exit

Exit with optional state saving (replaces native `/exit`):

```bash
python3 ~/.claude/custom-skills/session-manager/scripts/session_manager.py exit
python3 ~/.claude/custom-skills/session-manager/scripts/session_manager.py exit --save-note "Checkpoint before major changes"
```

## File Locations

| Type | Path |
|------|------|
| Conversation files | `~/.claude/projects/<project_name>/<session_id>.jsonl` |
| Script | `~/.claude/custom-skills/session-manager/scripts/session_manager.py` |

## Workflow: Rename Session

When user wants to rename the current session:

1. Identify current session from environment/context
2. Locate the `.jsonl` file in `~/.claude/projects/`
3. Rename the file (keeping session ID, updating project folder if needed)
4. Confirm the rename was successful

## Notes

- Renaming changes the project folder name for better organization
- Session ID (UUID) remains unchanged for continuity
- All conversation data is preserved during rename
- Exit command can add a note to the session for future reference
