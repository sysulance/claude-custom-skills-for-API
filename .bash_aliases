# Claude Code Custom Skills Aliases
# Add to ~/.bashrc or ~/.zshrc: source ~/.claude/custom-skills/.bash_aliases

# Core Skills
alias resumer='python3 ~/.claude/custom-skills/conversation-resumer/scripts/scan_history.py'
alias session='python3 ~/.claude/custom-skills/session-manager/scripts/session_manager.py'
alias todo='python3 ~/.claude/custom-skills/todo-manager/scripts/todo_manager.py'
alias help-cc='python3 ~/.claude/custom-skills/help-system/scripts/help_system.py'

# Short aliases
alias sm='session'
alias td='todo'
alias hlp='help-cc'

echo "✅ Claude Code custom skills aliases loaded!"
echo "Available commands: resumer, session, todo, help-cc"
