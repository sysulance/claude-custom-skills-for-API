#!/usr/bin/env python3
"""
Help System for Claude Code Custom Skills
Replaces native slash command: /help
"""

import os
import json
import argparse
from pathlib import Path
import zipfile

CLAUDE_DIR = Path.home() / ".claude"
PLUGINS_DIR = CLAUDE_DIR / "plugins"
CUSTOM_SKILLS_DIR = CLAUDE_DIR / "custom-skills"

SKILL_COMMANDS = {
    'conversation-resumer': {
        'command': 'resumer',
        'usage': 'python3 ~/.claude/custom-skills/conversation-resumer/scripts/scan_history.py',
        'description': 'View and resume previous conversations',
        'examples': [
            'resumer                    # List conversations by time',
            'resumer --project          # Group by project',
            'resumer --interactive      # Interactive selection'
        ]
    },
    'session-manager': {
        'command': 'session',
        'usage': 'python3 ~/.claude/custom-skills/session-manager/scripts/session_manager.py',
        'description': 'Manage sessions: rename, info, exit',
        'examples': [
            'session rename "New Name"  # Rename current session',
            'session info               # Show session info',
            'session list               # List recent sessions',
            'session exit               # Graceful exit'
        ]
    },
    'todo-manager': {
        'command': 'todo',
        'usage': 'python3 ~/.claude/custom-skills/todo-manager/scripts/todo_manager.py',
        'description': 'Task management with priorities',
        'examples': [
            'todo                       # Show pending todos',
            'todo --all                 # Show all projects',
            'todo add "Task" --priority high',
            'todo done 3                # Complete task #3',
            'todo --stats               # Show statistics'
        ]
    },
    'help-system': {
        'command': 'help',
        'usage': 'python3 ~/.claude/custom-skills/help-system/scripts/help_system.py',
        'description': 'Show help for custom skills',
        'examples': [
            'help                       # Show this help',
            'help todo-manager          # Help for specific skill'
        ]
    }
}

def list_skills():
    """List all installed custom skills."""
    print("\n" + "="*70)
    print("📚 CUSTOM SKILLS HELP")
    print("="*70)
    print("\nInstalled Skills:\n")
    
    for skill_name, info in SKILL_COMMANDS.items():
        cmd = info['command']
        desc = info['description']
        print(f"  {cmd:<15} - {desc}")
    
    print("\n" + "-"*70)
    print("\nUsage: <command> [options]")
    print("  Examples: todo --all, session info, resumer --project")
    print("\nFor detailed help: help <skill-name>")
    print("="*70 + "\n")

def show_skill_help(skill_name):
    """Show detailed help for a specific skill."""
    # Normalize skill name
    skill_key = skill_name.lower().replace('.skill', '')
    
    # Try to find matching skill
    found_skill = None
    for key in SKILL_COMMANDS:
        if key == skill_key or key.replace('-', '') == skill_key.replace('-', ''):
            found_skill = key
            break
    
    if not found_skill:
        print(f"❌ Skill '{skill_name}' not found")
        print("\nAvailable skills:")
        for key in SKILL_COMMANDS:
            print(f"  - {key}")
        return
    
    info = SKILL_COMMANDS[found_skill]
    
    print("\n" + "="*70)
    print(f"📖 {found_skill.upper().replace('-', ' ')}")
    print("="*70)
    print(f"\nDescription: {info['description']}")
    print(f"\nCommand: {info['command']}")
    print(f"Usage: {info['usage']}")
    print("\nExamples:")
    for example in info['examples']:
        print(f"  $ {example}")
    print("="*70 + "\n")

def show_all_commands():
    """Show all available commands."""
    print("\n" + "="*70)
    print("⌨️  ALL AVAILABLE COMMANDS")
    print("="*70)
    
    for skill_name, info in SKILL_COMMANDS.items():
        print(f"\n{info['command']}")
        print(f"  {info['description']}")
        for example in info['examples'][:2]:
            print(f"    {example}")
    
    print("\n" + "="*70 + "\n")

def show_about():
    """Show information about the custom skill system."""
    print("\n" + "="*70)
    print("🎯 ABOUT CUSTOM SKILLS")
    print("="*70)
    print("""
These custom skills replace native Claude Code slash commands
that are unavailable when using third-party APIs like Kimi.

SKILL LOCATIONS:
  Source:   ~/.claude/custom-skills/<skill-name>/
  Installed: ~/.claude/plugins/<skill-name>.skill

CLI PARAMETERS (Always Available):
  claude -c              Continue recent session
  claude -r              Resume specific session
  claude --version       Show version

COMMANDS (Replaced by Skills):
  /continue  → resumer
  /resume    → resumer
  /history   → resumer
  /rename    → session rename
  /exit      → session exit
  /todo      → todo
  /help      → help

For more info: https://github.com/anthropics/claude-code
""")
    print("="*70 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description='Help System for Claude Code Custom Skills'
    )
    parser.add_argument('skill', nargs='?', help='Show help for specific skill')
    parser.add_argument('--commands', action='store_true', help='Show all commands')
    parser.add_argument('--about', action='store_true', help='About custom skills')
    
    args = parser.parse_args()
    
    if args.about:
        show_about()
    elif args.commands:
        show_all_commands()
    elif args.skill:
        show_skill_help(args.skill)
    else:
        list_skills()

if __name__ == '__main__':
    main()
