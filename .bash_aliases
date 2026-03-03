# Claude Code Custom Skills Aliases
# Add to ~/.bashrc or ~/.zshrc: source ~/.claude/custom-skills/.bash_aliases

# Core Skills
alias resumer='python3 ~/.claude/skills/conversation-resumer/scripts/scan_history.py'
alias session='python3 ~/.claude/skills/session-manager/scripts/session_manager.py'
alias todo='python3 ~/.claude/skills/todo-manager/scripts/todo_manager.py'
alias help-cc='python3 ~/.claude/skills/help-system/scripts/help_system.py'

# File History Browser
alias file-history='python3 ~/.claude/skills/file-history-browser/scripts/file_history.py'
alias fh='file-history'
alias fh-timeline='file-history timeline'
alias fh-recent='file-history recent'
alias fh-stats='file-history stats'

# Cross-Project Search
alias project-search='python3 ~/.claude/skills/cross-project-search/scripts/cross_project_search.py'
alias ps='project-search'
alias psf='project-search --files'
alias psm='project-search --messages'

# Short aliases
alias sm='session'
alias td='todo'
alias hlp='help-cc'

echo "✅ Claude Code custom skills aliases loaded!"
echo "Available commands: resumer, session, todo, help-cc, file-history"
