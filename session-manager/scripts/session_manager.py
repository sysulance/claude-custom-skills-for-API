#!/usr/bin/env python3
"""
Session Manager for Claude Code (Kimi API users)
Replaces native slash commands: /rename, /exit, /info
"""

import os
import sys
import json
import argparse
import shutil
from datetime import datetime
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"

def get_current_session_id():
    """Get current session ID from environment."""
    session_id = os.environ.get('CLAUDE_SESSION_ID')
    if session_id:
        return session_id
    session_file = CLAUDE_DIR / "session"
    if session_file.exists():
        return session_file.read_text().strip()
    return None

def find_session_file(session_id):
    """Find the JSONL file for a given session ID."""
    if not PROJECTS_DIR.exists():
        return None
    for project_dir in PROJECTS_DIR.iterdir():
        if project_dir.is_dir():
            for jsonl_file in project_dir.glob("*.jsonl"):
                if jsonl_file.stem == session_id:
                    return jsonl_file
    return None

def get_session_info(jsonl_file):
    """Extract session information from JSONL file."""
    info = {
        'session_id': jsonl_file.stem,
        'file_path': jsonl_file,
        'project': jsonl_file.parent.name,
        'size': jsonl_file.stat().st_size,
        'modified': datetime.fromtimestamp(jsonl_file.stat().st_mtime),
        'message_count': 0,
        'duration': 'Unknown'
    }
    try:
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            info['message_count'] = len(lines)
            if lines:
                first_line = json.loads(lines[0])
                last_line = json.loads(lines[-1])
                first_time = first_line.get('timestamp', '')
                last_time = last_line.get('timestamp', '')
                if first_time and last_time:
                    try:
                        start = datetime.fromisoformat(first_time.replace('Z', '+00:00'))
                        end = datetime.fromisoformat(last_time.replace('Z', '+00:00'))
                        duration = end - start
                        hours, remainder = divmod(duration.seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        info['duration'] = f"{hours}h {minutes}m {seconds}s"
                    except:
                        pass
    except:
        pass
    return info

def format_size(size_bytes):
    """Format bytes to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def rename_session(new_name):
    """Rename the current session."""
    session_id = get_current_session_id()
    if not session_id:
        print("Error: Cannot determine current session ID")
        return False
    jsonl_file = find_session_file(session_id)
    if not jsonl_file:
        print(f"Error: Cannot find session file for ID: {session_id}")
        return False
    safe_name = "".join(c for c in new_name if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_name = safe_name.replace(' ', '-')
    if not safe_name:
        print("Error: Invalid session name")
        return False
    new_project_dir = PROJECTS_DIR / safe_name
    counter = 1
    original_name = safe_name
    while new_project_dir.exists():
        safe_name = f"{original_name}-{counter}"
        new_project_dir = PROJECTS_DIR / safe_name
        counter += 1
    try:
        new_project_dir.mkdir(parents=True, exist_ok=True)
        new_jsonl_path = new_project_dir / f"{session_id}.jsonl"
        shutil.move(str(jsonl_file), str(new_jsonl_path))
        old_dir = jsonl_file.parent
        try:
            old_dir.rmdir()
        except:
            pass
        print(f"Session renamed successfully!")
        print(f"  New name: {safe_name}")
        print(f"  Session ID: {session_id}")
        return True
    except Exception as e:
        print(f"Error renaming session: {e}")
        return False

def show_info():
    """Display information about the current session."""
    session_id = get_current_session_id()
    if not session_id:
        print("Error: Cannot determine current session ID")
        return
    jsonl_file = find_session_file(session_id)
    if not jsonl_file:
        print(f"Error: Cannot find session file for ID: {session_id}")
        return
    info = get_session_info(jsonl_file)
    print("\n" + "="*60)
    print("SESSION INFORMATION")
    print("="*60)
    print(f"  Session ID:      {info['session_id']}")
    print(f"  Project:         {info['project']}")
    print(f"  Messages:        {info['message_count']}")
    print(f"  Duration:        {info['duration']}")
    print(f"  File Size:       {format_size(info['size'])}")
    print(f"  Last Modified:   {info['modified'].strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")

def list_sessions(limit=10):
    """List recent conversation sessions."""
    if not PROJECTS_DIR.exists():
        print("No projects directory found")
        return
    sessions = []
    for project_dir in PROJECTS_DIR.iterdir():
        if project_dir.is_dir():
            for jsonl_file in project_dir.glob("*.jsonl"):
                try:
                    stat = jsonl_file.stat()
                    sessions.append({
                        'project': project_dir.name,
                        'session_id': jsonl_file.stem,
                        'modified': datetime.fromtimestamp(stat.st_mtime),
                        'size': stat.st_size
                    })
                except:
                    pass
    sessions.sort(key=lambda x: x['modified'], reverse=True)
    sessions = sessions[:limit]
    if not sessions:
        print("No sessions found")
        return
    print("\n" + "="*80)
    print("RECENT SESSIONS")
    print("="*80)
    print(f"{'#':<3} {'Project':<30} {'Modified':<20} {'Size':<10}")
    print("-"*80)
    for i, session in enumerate(sessions, 1):
        project = session['project'][:28]
        modified = session['modified'].strftime('%Y-%m-%d %H:%M')
        size = format_size(session['size'])
        print(f"{i:<3} {project:<30} {modified:<20} {size:<10}")
    print("="*80)
    print(f"\nShowing {len(sessions)} most recent sessions")
    print(f"All sessions stored in: {PROJECTS_DIR}\n")

def graceful_exit(save_note=None):
    """Gracefully exit with optional note."""
    session_id = get_current_session_id()
    if save_note and session_id:
        jsonl_file = find_session_file(session_id)
        if jsonl_file:
            note_entry = {
                'type': 'system',
                'content': f'[Session Exit Note]: {save_note}',
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
            with open(jsonl_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(note_entry) + '\n')
            print(f"Exit note saved: {save_note}")
    print("\nExiting Claude Code...")
    print("Tip: Use 'claude -c' to continue this session later\n")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description='Session Manager for Claude Code (Kimi API users)'
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    rename_parser = subparsers.add_parser('rename', help='Rename current session')
    rename_parser.add_argument('name', help='New session name')
    
    subparsers.add_parser('info', help='Show current session information')
    
    list_parser = subparsers.add_parser('list', help='List recent sessions')
    list_parser.add_argument('--limit', type=int, default=10)
    
    exit_parser = subparsers.add_parser('exit', help='Gracefully exit')
    exit_parser.add_argument('--save-note', help='Save a note before exiting')
    
    args = parser.parse_args()
    
    if args.command == 'rename':
        rename_session(args.name)
    elif args.command == 'info':
        show_info()
    elif args.command == 'list':
        list_sessions(args.limit)
    elif args.command == 'exit':
        graceful_exit(args.save_note)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
