#!/usr/bin/env python3
"""
Cross-Project Search - 替代 /search 命令
跨所有历史对话项目搜索内容
"""

import json
import sys
import argparse
from pathlib import Path
from collections import defaultdict


def get_projects_dir():
    """获取项目目录"""
    return Path.home() / ".claude" / "projects"


def get_all_projects():
    """获取所有项目目录"""
    projects_dir = get_projects_dir()
    if not projects_dir.exists():
        return []
    return [d for d in projects_dir.iterdir() if d.is_dir()]


def search_in_conversation(project_dir, keyword):
    """在对话中搜索关键词"""
    conv_file = project_dir / "conversation.json"
    matches = []

    if not conv_file.exists():
        return matches

    try:
        with open(conv_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return matches

    messages = data.get('messages', [])
    for i, msg in enumerate(messages):
        text = ""
        if isinstance(msg.get('content'), list):
            for item in msg['content']:
                if isinstance(item, dict) and 'text' in item:
                    text += item['text'] + " "
        if 'text' in msg:
            text += msg['text']

        if keyword.lower() in text.lower():
            # 提取上下文
            start = max(0, text.lower().find(keyword.lower()) - 50)
            end = min(len(text), text.lower().find(keyword.lower()) + len(keyword) + 50)
            context = text[start:end]

            matches.append({
                'msg_index': i,
                'context': context,
                'role': msg.get('role', 'unknown')
            })

    return matches


def search_in_files(project_dir, keyword):
    """在项目文件中搜索关键词"""
    matches = []

    # 常见的代码文件扩展名
    text_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.h',
                       '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala',
                       '.md', '.txt', '.json', '.yaml', '.yml', '.xml', '.html', '.css',
                       '.sh', '.bash', '.zsh', '.sql', '.csv'}

    for file_path in project_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in text_extensions:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                if keyword.lower() in content.lower():
                    lines = content.split('\n')
                    for line_num, line in enumerate(lines, 1):
                        if keyword.lower() in line.lower():
                            matches.append({
                                'file': str(file_path.relative_to(project_dir)),
                                'line': line_num,
                                'content': line.strip()[:100]
                            })
            except:
                continue

    return matches


def format_project_name(name):
    """格式化项目名称"""
    name = name.replace('-Users-villageson-Desktop-CC-', '')
    name = name.replace('-Users-villageson-', '')
    name = name.replace('---', '/')
    return name


def search_all(keyword, search_files=True, search_messages=True, project_filter=None, limit=50):
    """搜索所有项目"""
    projects = get_all_projects()

    if project_filter:
        projects = [p for p in projects if project_filter.lower() in p.name.lower()]

    results = defaultdict(lambda: {'messages': [], 'files': []})

    total_matches = 0

    for project in projects:
        project_name = format_project_name(project.name)

        if search_messages:
            msg_matches = search_in_conversation(project, keyword)
            results[project_name]['messages'] = msg_matches
            total_matches += len(msg_matches)

        if search_files:
            file_matches = search_in_files(project, keyword)
            results[project_name]['files'] = file_matches
            total_matches += len(file_matches)

    return results, total_matches


def display_results(results, total, keyword, limit=50):
    """显示搜索结果"""
    print(f"\n🔍 搜索关键词: \"{keyword}\"")
    print(f"📊 找到 {total} 个匹配\n")

    displayed = 0

    for project_name, matches in sorted(results.items()):
        msg_count = len(matches['messages'])
        file_count = len(matches['files'])

        if msg_count == 0 and file_count == 0:
            continue

        print(f"📁 {project_name}")
        print(f"   💬 消息: {msg_count} | 📄 文件: {file_count}")

        # 显示消息匹配
        for match in matches['messages'][:3]:  # 最多显示3个
            if displayed >= limit:
                break

            context = match['context']
            # 高亮关键词
            start = context.lower().find(keyword.lower())
            if start >= 0:
                end = start + len(keyword)
                highlighted = context[:start] + f"\033[93m{context[start:end]}\033[0m" + context[end:]
            else:
                highlighted = context

            role_icon = "👤" if match['role'] == 'user' else "🤖"
            print(f"   {role_icon} ...{highlighted}...")
            displayed += 1

        # 显示文件匹配
        for match in matches['files'][:3]:  # 最多显示3个
            if displayed >= limit:
                break

            print(f"   📄 {match['file']}:{match['line']}")
            displayed += 1

        print()

    if total > limit:
        print(f"... 还有 {total - limit} 个结果未显示 (使用 --limit 增加)\n")


def show_stats(results, total, keyword):
    """显示搜索统计"""
    print(f"\n📊 搜索统计: \"{keyword}\"\n")

    project_stats = []
    for project_name, matches in results.items():
        msg_count = len(matches['messages'])
        file_count = len(matches['files'])
        if msg_count > 0 or file_count > 0:
            project_stats.append((project_name, msg_count, file_count))

    if not project_stats:
        print("❌ 没有找到匹配")
        return

    # 按匹配数排序
    project_stats.sort(key=lambda x: x[1] + x[2], reverse=True)

    print(f"{'项目':<30} {'消息':>8} {'文件':>8} {'总计':>8}")
    print("-" * 60)

    for name, msg, files in project_stats:
        print(f"{name:<30} {msg:>8} {files:>8} {msg + files:>8}")

    print("-" * 60)
    total_msg = sum(x[1] for x in project_stats)
    total_files = sum(x[2] for x in project_stats)
    print(f"{'总计':<30} {total_msg:>8} {total_files:>8} {total_msg + total_files:>8}\n")


def main():
    parser = argparse.ArgumentParser(
        description='跨项目搜索工具',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('keyword', help='搜索关键词')
    parser.add_argument('--files', '-f', action='store_true',
                        help='只搜索文件')
    parser.add_argument('--messages', '-m', action='store_true',
                        help='只搜索消息')
    parser.add_argument('--project', '-p', help='指定项目名称')
    parser.add_argument('--stats', '-s', action='store_true',
                        help='显示统计')
    parser.add_argument('--limit', '-l', type=int, default=50,
                        help='限制结果数量 (默认: 50)')

    args = parser.parse_args()

    # 确定搜索范围
    search_files = not args.messages or args.files
    search_messages = not args.files or args.messages

    # 执行搜索
    results, total = search_all(
        args.keyword,
        search_files=search_files,
        search_messages=search_messages,
        project_filter=args.project,
        limit=args.limit
    )

    # 显示结果
    if args.stats:
        show_stats(results, total, args.keyword)
    else:
        display_results(results, total, args.keyword, limit=args.limit)


if __name__ == '__main__':
    main()
