#!/usr/bin/env python3
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
TODOS_DIR = CLAUDE_DIR / "todos"

def get_current_project():
    session_id = os.environ.get('CLAUDE_SESSION_ID', '')
    if TODOS_DIR.exists():
        for json_file in TODOS_DIR.glob("*.json"):
            return json_file.stem
    return "default"

def load_todos(project=None):
    if project is None:
        project = get_current_project()
    todos_file = TODOS_DIR / f"{project}.json"
    todos = []
    if todos_file.exists():
        try:
            with open(todos_file, 'r') as f:
                data = json.load(f)
                todos = data.get('todos', [])
        except:
            pass
    return todos, project

def save_todos(todos, project=None):
    if project is None:
        project = get_current_project()
    todos_file = TODOS_DIR / f"{project}.json"
    TODOS_DIR.mkdir(parents=True, exist_ok=True)
    with open(todos_file, 'w') as f:
        json.dump({'todos': todos}, f, indent=2)

def list_todos(all_projects=False, priority=None):
    all_todos = []
    if all_projects:
        if TODOS_DIR.exists():
            for json_file in TODOS_DIR.glob("*.json"):
                proj_name = json_file.stem
                todos, _ = load_todos(proj_name)
                for todo in todos:
                    todo['project'] = proj_name
                all_todos.extend(todos)
    else:
        todos, project = load_todos()
        for todo in todos:
            todo['project'] = project
        all_todos.extend(todos)
    
    if priority:
        all_todos = [t for t in all_todos if t.get('priority', 'medium').lower() == priority.lower()]
    
    pending = [t for t in all_todos if not t.get('completed', False)]
    
    if not pending:
        print("No pending todos found!")
        return
    
    print("TODO LIST")
    print("-" * 80)
    for i, todo in enumerate(pending, 1):
        p = todo.get('priority', 'medium').upper()
        project = todo.get('project', 'default')
        content = todo.get('content', 'No content')
        print(f"{i}. [{p}] ({project}) {content}")
    print("-" * 80)
    print(f"Total: {len(pending)} pending tasks")

def add_todo(content, priority='medium'):
    todos, project = load_todos()
    todo_id = len(todos) + 1
    todo = {
        'id': todo_id,
        'content': content,
        'priority': priority.lower(),
        'completed': False,
        'created': datetime.now().isoformat()
    }
    todos.append(todo)
    save_todos(todos, project)
    print(f"Added: {content} (Priority: {priority})")

def complete_todo(todo_id):
    todos, project = load_todos()
    for todo in todos:
        if todo.get('id') == todo_id:
            todo['completed'] = True
            save_todos(todos, project)
            print(f"Completed: {todo.get('content')}")
            return
    print(f"Todo #{todo_id} not found")

def show_stats():
    all_todos = []
    if TODOS_DIR.exists():
        for json_file in TODOS_DIR.glob("*.json"):
            proj_name = json_file.stem
            todos, _ = load_todos(proj_name)
            all_todos.extend(todos)
    total = len(all_todos)
    completed = len([t for t in all_todos if t.get('completed')])
    pending = total - completed
    print("TODO STATISTICS")
    print("-" * 40)
    print(f"Total: {total}")
    print(f"Completed: {completed}")
    print(f"Pending: {pending}")

def main():
    parser = argparse.ArgumentParser(description='Todo Manager')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--priority')
    parser.add_argument('--stats', action='store_true')
    subparsers = parser.add_subparsers(dest='command')
    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('content')
    add_parser.add_argument('--priority', default='medium')
    done_parser = subparsers.add_parser('done')
    done_parser.add_argument('id', type=int)
    args = parser.parse_args()
    
    if args.command == 'add':
        add_todo(args.content, args.priority)
    elif args.command == 'done':
        complete_todo(args.id)
    elif args.stats:
        show_stats()
    else:
        list_todos(args.all, args.priority)

if __name__ == '__main__':
    main()
