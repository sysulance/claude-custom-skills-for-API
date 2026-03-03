#!/usr/bin/env python3
"""
Scan and display Claude Code conversation history from ~/.claude/projects/
Enhanced version with better visualization and grouping
"""

import os
import json
import glob
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

PROJECTS_DIR = os.path.expanduser("~/.claude/projects")

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def extract_first_user_message(jsonl_file):
    """Extract the first user message from a conversation"""
    try:
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    if data.get('type') == 'user' and 'message' in data:
                        msg = data['message']
                        if isinstance(msg, dict) and 'content' in msg:
                            content = msg['content']
                            if isinstance(content, list) and len(content) > 0:
                                if 'text' in content[0]:
                                    return clean_message(content[0]['text'])
                            elif isinstance(content, str):
                                return clean_message(content)
                except:
                    continue
    except Exception as e:
        return f"Error reading: {str(e)[:50]}"
    return "(No message found)"

def clean_message(text):
    """Clean message text for display"""
    # Remove XML-like tags
    import re
    text = re.sub(r'<[^>]+>', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text[:150]

def get_conversation_info(jsonl_file):
    """Get conversation metadata"""
    info = {
        'file': jsonl_file,
        'timestamp': None,
        'cwd': '',
        'preview': '',
        'size': os.path.getsize(jsonl_file),
        'message_count': 0,
        'duration_minutes': 0
    }

    try:
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            info['message_count'] = len([l for l in lines if json.loads(l).get('type') in ['user', 'assistant']])

            if lines:
                first_data = json.loads(lines[0].strip())
                info['timestamp'] = first_data.get('timestamp', '')
                info['sessionId'] = first_data.get('sessionId', '')

                # Calculate duration if multiple timestamps
                if len(lines) > 1:
                    try:
                        last_data = json.loads(lines[-1].strip())
                        first_ts = datetime.fromisoformat(first_data.get('timestamp', '').replace('Z', '+00:00'))
                        last_ts = datetime.fromisoformat(last_data.get('timestamp', '').replace('Z', '+00:00'))
                        info['duration_minutes'] = int((last_ts - first_ts).total_seconds() / 60)
                    except:
                        pass

            if len(lines) > 1:
                data2 = json.loads(lines[1].strip())
                info['cwd'] = data2.get('cwd', '')
    except:
        pass

    info['preview'] = extract_first_user_message(jsonl_file)
    return info

def scan_all_projects():
    """Scan all project directories and return conversation list"""
    conversations = []

    if not os.path.exists(PROJECTS_DIR):
        return conversations

    for project_name in os.listdir(PROJECTS_DIR):
        project_path = os.path.join(PROJECTS_DIR, project_name)
        if not os.path.isdir(project_path):
            continue

        jsonl_files = glob.glob(os.path.join(project_path, "*.jsonl"))

        for jsonl_file in jsonl_files:
            info = get_conversation_info(jsonl_file)
            info['project'] = project_name
            conversations.append(info)

    conversations.sort(key=lambda x: x['timestamp'] or '', reverse=True)
    return conversations

def format_size(size_bytes):
    """Format file size"""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f}KB"
    else:
        return f"{size_bytes/(1024*1024):.1f}MB"

def format_project_name(name):
    """Format project name for display"""
    if name.startswith('-Users-villageson'):
        name = name.replace('-Users-villageson', '~')
        name = name.replace('---', '/')
        name = name.replace('--', '/')
    return name

def get_time_group(timestamp_str):
    """Categorize conversation by time"""
    if not timestamp_str:
        return "Unknown"

    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now(dt.tzinfo)
        delta = now - dt

        if delta.days == 0:
            return "📅 Today"
        elif delta.days == 1:
            return "📅 Yesterday"
        elif delta.days < 7:
            return f"📅 This Week ({dt.strftime('%A')})"
        elif delta.days < 14:
            return "📅 Last Week"
        elif delta.days < 30:
            return "📅 This Month"
        else:
            return f"📅 {dt.strftime('%B %Y')}"
    except:
        return "Unknown"

def get_project_icon(project_name):
    """Get icon based on project name patterns"""
    name_lower = project_name.lower()

    icons = {
        'test': '🧪',
        'finan': '💰',
        'equity': '📈',
        'osa': '🔬',
        'dietary': '🍎',
        'catl': '🔋',
        'hood': '🏦',
        'rubbish': '🗑️',
        'research': '🔍'
    }

    for key, icon in icons.items():
        if key in name_lower:
            return icon

    return '💬'

def group_conversations_by_project(conversations):
    """Group conversations by project name"""
    groups = defaultdict(list)
    for conv in conversations:
        project = conv['project']
        # Group similar projects
        if 'OSA' in project or 'dietary' in project.lower():
            groups['OSA Dietary Research'].append(conv)
        elif 'Finan' in project or 'plugin' in project.lower():
            groups['Financial Plugins'].append(conv)
        elif 'CC---2' in project or 'catl' in project.lower():
            groups['CATL Analysis'].append(conv)
        elif 'test' in project.lower():
            groups['Test Projects'].append(conv)
        elif project == '-Users-villageson' or project == '~':
            groups['Home Directory'].append(conv)
        else:
            groups[format_project_name(project)].append(conv)
    return groups

def display_conversations_visual(conversations, limit=30, group_by='time'):
    """Display conversations with enhanced visualization"""
    if not conversations:
        print("No conversation history found.")
        return

    use_color = os.environ.get('TERM') in ['xterm-256color', 'screen-256color', 'tmux-256color']
    c = Colors if use_color else type('Colors', (), {k: '' for k in ['HEADER', 'BLUE', 'CYAN', 'GREEN', 'YELLOW', 'RED', 'ENDC', 'BOLD', 'DIM']})()

    print(f"\n{c.BOLD}{c.CYAN}╔{'═'*98}╗{c.ENDC}")
    print(f"{c.BOLD}{c.CYAN}║{' '*35}📚 CONVERSATION HISTORY 📚{' '*38}║{c.ENDC}")
    print(f"{c.BOLD}{c.CYAN}╠{'═'*98}╣{c.ENDC}")
    print(f"{c.CYAN}║{c.ENDC}  Total: {c.BOLD}{len(conversations)}{c.ENDC} conversations  {c.DIM}(showing top {min(limit, len(conversations))}){' '*55}{c.ENDC}{c.CYAN}║{c.ENDC}")
    print(f"{c.BOLD}{c.CYAN}╚{'═'*98}╝{c.ENDC}\n")

    if group_by == 'time':
        # Group by time periods
        current_group = None
        for i, conv in enumerate(conversations[:limit], 1):
            group = get_time_group(conv.get('timestamp', ''))

            if group != current_group:
                current_group = group
                print(f"\n{c.BOLD}{c.YELLOW}{group}{c.ENDC}")
                print(f"{c.DIM}{'─'*100}{c.ENDC}")

            display_single_conversation(conv, i, c)

    elif group_by == 'project':
        # Group by project
        groups = group_conversations_by_project(conversations[:limit])

        for project_name, convs in sorted(groups.items(), key=lambda x: x[1][0].get('timestamp', ''), reverse=True):
            icon = get_project_icon(project_name)
            total_size = sum(c['size'] for c in convs)

            print(f"\n{c.BOLD}{c.YELLOW}{icon} {project_name}{c.ENDC} {c.DIM}({len(convs)} conversations, {format_size(total_size)}){c.ENDC}")
            print(f"{c.DIM}{'─'*100}{c.ENDC}")

            for i, conv in enumerate(convs, 1):
                display_single_conversation(conv, i, c, show_project=False)

def display_single_conversation(conv, index, colors, show_project=True):
    """Display a single conversation entry"""
    c = colors

    # Parse timestamp
    ts = conv.get('timestamp', '')
    if ts:
        try:
            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            time_str = dt.strftime('%m/%d %H:%M')
            date_str = dt.strftime('%Y-%m-%d')
        except:
            time_str = ts[5:16] if len(ts) > 16 else ts[:16]
            date_str = ""
    else:
        time_str = "Unknown"
        date_str = ""

    # Format project name
    project = format_project_name(conv.get('project', 'Unknown'))

    # Format preview
    preview = conv.get('preview', '')
    if len(preview) > 70:
        preview = preview[:67] + "..."

    # Format cwd
    cwd = conv.get('cwd', '')
    if cwd:
        cwd_display = f" 📁 {cwd.replace('/Users/villageson', '~')}"
    else:
        cwd_display = ""

    # Format message count and duration
    msg_count = conv.get('message_count', 0)
    duration = conv.get('duration_minutes', 0)
    meta_info = f"{msg_count} msgs"
    if duration > 0:
        if duration < 60:
            meta_info += f", {duration}min"
        else:
            meta_info += f", {duration//60}h{duration%60}m"

    # Print formatted entry
    print(f"  {c.BOLD}[{index:2}]{c.ENDC} {c.BLUE}{time_str}{c.ENDC}  {c.GREEN}{format_size(conv['size']):>6}{c.ENDC}  {c.DIM}{meta_info:>12}{c.ENDC}")

    if show_project:
        print(f"      {c.CYAN}📂 {project}{c.ENDC}")

    if cwd_display:
        print(f"      {c.DIM}{cwd_display}{c.ENDC}")

    if preview:
        # Truncate preview for display
        display_preview = preview[:75] + "..." if len(preview) > 75 else preview
        print(f"      💬 {display_preview}")

    print()

def display_statistics(conversations):
    """Display overall statistics"""
    if not conversations:
        return

    total_size = sum(c['size'] for c in conversations)
    total_msgs = sum(c.get('message_count', 0) for c in conversations)

    # Count by project
    project_counts = defaultdict(int)
    for c in conversations:
        project_counts[c['project']] += 1

    print(f"\n📊 STATISTICS:")
    print(f"   Total Conversations: {len(conversations)}")
    print(f"   Total Size: {format_size(total_size)}")
    print(f"   Total Messages: {total_msgs}")
    print(f"   Projects: {len(project_counts)}")

    # Top projects by conversation count
    top_projects = sorted(project_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"\n   Top Projects:")
    for proj, count in top_projects:
        print(f"     • {format_project_name(proj)}: {count} conversations")

def export_conversation(jsonl_file, output_file):
    """Export a conversation to a readable markdown format"""
    try:
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open(output_file, 'w', encoding='utf-8') as out:
            out.write("# Conversation Export\n\n")
            out.write(f"**Source:** `{jsonl_file}`\n\n")
            out.write(f"**Total Lines:** {len(lines)}\n\n")
            out.write("---\n\n")

            for line in lines:
                try:
                    data = json.loads(line.strip())
                    msg_type = data.get('type', 'unknown')
                    timestamp = data.get('timestamp', '')

                    if msg_type == 'user':
                        msg = data.get('message', {})
                        if isinstance(msg, dict) and 'content' in msg:
                            content = msg['content']
                            if isinstance(content, list) and len(content) > 0:
                                text = content[0].get('text', '')
                            else:
                                text = str(content)
                            if text.strip():
                                out.write(f"## 👤 User\n\n{text}\n\n")
                                if timestamp:
                                    out.write(f"*{timestamp}*\n\n")

                    elif msg_type == 'assistant':
                        msg = data.get('message', {})
                        if isinstance(msg, dict) and 'content' in msg:
                            content = msg['content']
                            if isinstance(content, list) and len(content) > 0:
                                text = content[0].get('text', '')
                            else:
                                text = str(content)
                            if text.strip():
                                out.write(f"## 🤖 Assistant\n\n{text}\n\n")
                                if timestamp:
                                    out.write(f"*{timestamp}*\n\n")
                except:
                    continue

        return True
    except Exception as e:
        print(f"Error exporting: {e}")
        return False

def interactive_select(conversations):
    """Interactive conversation selection"""
    if not conversations:
        print("No conversations to select from.")
        return None

    print("\n🎯 Select a conversation by number, or:")
    print("   'q' = quit, 'e <num>' = export, 's' = show stats\n")

    try:
        choice = input("Your choice: ").strip()

        if choice.lower() == 'q':
            return None

        if choice.lower() == 's':
            display_statistics(conversations)
            return interactive_select(conversations)

        if choice.startswith('e '):
            try:
                idx = int(choice.split()[1]) - 1
                if 0 <= idx < len(conversations):
                    conv = conversations[idx]
                    output_file = f"conversation_{idx+1}_export.md"
                    if export_conversation(conv['file'], output_file):
                        print(f"✅ Exported to: {output_file}")
                    return conv
            except:
                print("Invalid export command")
            return interactive_select(conversations)

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(conversations):
                return conversations[idx]
            else:
                print("Invalid number. Please try again.")
                return interactive_select(conversations)
        except ValueError:
            print("Invalid input. Please enter a number.")
            return interactive_select(conversations)

    except KeyboardInterrupt:
        print("\nCancelled.")
        return None

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--export":
        if len(sys.argv) >= 4:
            export_conversation(sys.argv[2], sys.argv[3])
        else:
            print("Usage: python3 scan_history.py --export <jsonl_file> <output_file>")
    elif len(sys.argv) > 1 and sys.argv[1] == "--stats":
        conversations = scan_all_projects()
        display_statistics(conversations)
    elif len(sys.argv) > 1 and sys.argv[1] == "--project":
        conversations = scan_all_projects()
        display_conversations_visual(conversations, group_by='project')
    elif len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        conversations = scan_all_projects()
        display_conversations_visual(conversations)
        selected = interactive_select(conversations)
        if selected:
            print(f"\n✅ Selected: {selected['file']}")
            print(f"   Project: {format_project_name(selected['project'])}")
            print(f"   First message: {selected['preview'][:80]}...")
    else:
        # Default: show time-based view
        conversations = scan_all_projects()
        display_conversations_visual(conversations, group_by='time')
