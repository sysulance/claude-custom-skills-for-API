#!/usr/bin/env python3
"""
File History Browser - 替代 /file 命令
查看对话中的文件操作历史
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter

def get_current_session_dir():
    """获取当前会话目录"""
    # 从环境变量或查找最近的会话
    projects_dir = Path.home() / ".claude" / "projects"
    if not projects_dir.exists():
        return None

    # 找到最近修改的会话目录
    sessions = [d for d in projects_dir.iterdir() if d.is_dir()]
    if not sessions:
        return None

    return max(sessions, key=lambda d: d.stat().st_mtime)

def parse_conversation_json(session_dir):
    """解析 conversation.json 文件提取文件操作"""
    conv_file = session_dir / "conversation.json"
    if not conv_file.exists():
        return []

    try:
        with open(conv_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return []

    files = []
    messages = data.get('messages', [])

    for msg in messages:
        content = msg.get('content', [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    # 检查 tool_use 中的文件路径
                    if item.get('type') == 'tool_use':
                        tool_input = item.get('input', {})
                        file_path = tool_input.get('file_path')
                        if file_path:
                            files.append({
                                'path': file_path,
                                'action': tool_input.get('command', 'read'),
                                'time': msg.get('created_at', ''),
                                'type': 'file'
                            })

        # 从文本中提取文件路径
        text = msg.get('text', '')
        if text:
            import re
            # 匹配常见的文件路径模式
            file_patterns = [
                r'/Users/[^\s\n\]\)\"\']+',
                r'/home/[^\s\n\]\)\"\']+',
                r'~[/\\][^\s\n\]\)\"\']+',
            ]
            for pattern in file_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    if '.' in match and not match.endswith('.'):
                        files.append({
                            'path': match,
                            'action': 'referenced',
                            'time': msg.get('created_at', ''),
                            'type': 'reference'
                        })

    return files

def list_files(session_dir):
    """列出会话中的所有文件"""
    files = parse_conversation_json(session_dir)

    if not files:
        print("📂 没有找到文件操作记录")
        return

    # 去重，保留最新的
    seen = set()
    unique_files = []
    for f in reversed(files):  # 从后往前，保留最新的
        path = f['path']
        if path not in seen:
            seen.add(path)
            unique_files.insert(0, f)

    print(f"\n📂 当前会话中的文件 (共 {len(unique_files)} 个):\n")

    for i, f in enumerate(unique_files, 1):
        path = f['path']
        action = f['action']

        # 获取文件图标
        icon = '📄'
        if any(path.endswith(ext) for ext in ['.py', '.js', '.ts', '.java']):
            icon = '🐍' if path.endswith('.py') else '📜'
        elif path.endswith(('.md', '.txt', '.rst')):
            icon = '📝'
        elif path.endswith(('.json', '.yaml', '.yml', '.xml')):
            icon = '📋'
        elif path.endswith(('.sh', '.bash')):
            icon = '⚡'
        elif path.endswith(('.xlsx', '.xls', '.csv')):
            icon = '📊'
        elif path.endswith(('.pptx', '.ppt')):
            icon = '📽️'
        elif path.endswith(('.pdf')):
            icon = '📕'

        action_icon = {'read': '👁️', 'write': '✏️', 'edit': '🔧'}.get(action, '📌')

        print(f"  {i:2}. {icon} {path}")
        print(f"      {action_icon} {action}")

    print()

def show_timeline(session_dir):
    """显示文件操作时间线"""
    files = parse_conversation_json(session_dir)

    if not files:
        print("📂 没有找到文件操作记录")
        return

    print("\n⏱️ 文件操作时间线:\n")

    for i, f in enumerate(files[-20:], 1):  # 显示最近20个
        path = Path(f['path']).name
        action = f['action']
        time_str = f['time'][:19] if f['time'] else 'Unknown'

        action_emoji = {'read': '👁️', 'write': '✏️', 'edit': '🔧'}.get(action, '📌')

        print(f"  [{time_str}] {action_emoji} {action:10} {path}")

    print()

def show_recent(session_dir, limit=10):
    """显示最近使用的文件"""
    files = parse_conversation_json(session_dir)

    if not files:
        print("📂 没有找到文件操作记录")
        return

    # 去重，获取最近使用的
    seen = set()
    recent = []
    for f in reversed(files):
        path = f['path']
        if path not in seen:
            seen.add(path)
            recent.append(f)
        if len(recent) >= limit:
            break

    print(f"\n🕐 最近使用的 {len(recent)} 个文件:\n")

    for i, f in enumerate(recent, 1):
        path = f['path']
        icon = '📄'
        if path.endswith('.py'):
            icon = '🐍'
        elif path.endswith(('.md', '.txt')):
            icon = '📝'
        elif path.endswith('.json'):
            icon = '📋'

        print(f"  {i}. {icon} {path}")

    print()

def show_stats(session_dir):
    """显示文件类型统计"""
    files = parse_conversation_json(session_dir)

    if not files:
        print("📂 没有找到文件操作记录")
        return

    # 统计扩展名
    extensions = []
    for f in files:
        path = f['path']
        ext = Path(path).suffix.lower()
        if ext:
            extensions.append(ext)

    counts = Counter(extensions)

    print("\n📊 文件类型统计:\n")

    for ext, count in counts.most_common():
        bar = '█' * min(count, 20)
        print(f"  {ext:8} {bar} {count}")

    print(f"\n  总计: {len(files)} 个文件操作\n")

def search_files(session_dir, keyword):
    """搜索文件名"""
    files = parse_conversation_json(session_dir)

    matches = [f for f in files if keyword.lower() in f['path'].lower()]

    if not matches:
        print(f"🔍 没有找到包含 '{keyword}' 的文件")
        return

    print(f"\n🔍 找到 {len(matches)} 个匹配的文件:\n")

    seen = set()
    for f in matches:
        path = f['path']
        if path not in seen:
            seen.add(path)
            print(f"  📄 {path}")

    print()

def main():
    if len(sys.argv) < 2:
        command = 'list'
    else:
        command = sys.argv[1]

    session_dir = get_current_session_dir()
    if not session_dir:
        print("❌ 未找到当前会话目录")
        sys.exit(1)

    if command == 'list' or command == 'ls':
        list_files(session_dir)
    elif command == 'timeline' or command == 't':
        show_timeline(session_dir)
    elif command == 'recent' or command == 'r':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        show_recent(session_dir, limit)
    elif command == 'stats' or command == 's':
        show_stats(session_dir)
    elif command == 'search':
        if len(sys.argv) < 3:
            print("用法: file-history search <keyword>")
            sys.exit(1)
        search_files(session_dir, sys.argv[2])
    else:
        print(f"未知命令: {command}")
        print("用法: file-history [list|timeline|recent|stats|search]")
        sys.exit(1)

if __name__ == '__main__':
    main()
