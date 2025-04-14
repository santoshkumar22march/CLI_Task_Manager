"""
Simple command-line task manager.
Add, list, complete and delete tasks. Data stored in tasks.json.
"""

import json
import os
import argparse
from datetime import datetime

# File location for storing tasks
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from file and set up next ID"""
    global next_id
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                loaded_tasks = json.load(f)
                if not isinstance(loaded_tasks, list):
                    print(f"Warning: Tasks file '{TASKS_FILE}' contained invalid data. Starting fresh.")
                    loaded_tasks = []

                if loaded_tasks:
                    valid_ids = [task.get('id') for task in loaded_tasks if isinstance(task.get('id'), int)]
                    if valid_ids:
                         max_id = max(valid_ids)
                         next_id = max_id + 1
                    else:
                         next_id = 1
                else:
                    next_id = 1
                return loaded_tasks
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading tasks file '{TASKS_FILE}': {e}. Starting with empty list.")
            next_id = 1
            return []
    else:
        next_id = 1
        return []

def save_tasks(tasks_list):
    """Save tasks to file"""
    try:
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks_list, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving tasks to file '{TASKS_FILE}': {e}")

def add_task(description):
    """Add a new task"""
    global next_id
    if not description or description.isspace():
        print("Error: Task description cannot be empty.")
        return False

    new_task = {
        'id': next_id,
        'description': description.strip(),
        'done': False,
        'created_at': datetime.now().isoformat()
    }
    tasks.append(new_task)
    print(f"Added task: '{new_task['description']}' with ID {next_id}")
    next_id += 1
    return True

def list_tasks():
    """Show all tasks"""
    if not tasks:
        print("No tasks yet! Use the 'add' command to add some.")
        return

    print("\n--- Your Tasks ---")
    pending_tasks = False
    for task in sorted(tasks, key=lambda t: t.get('id', float('inf'))):
        status = "[X]" if task.get('done', False) else "[ ]"
        desc = task.get('description', 'No Description')
        task_id = task.get('id', 'N/A')
        print(f"{status} ID: {task_id} - {desc}")
        if not task.get('done', False):
            pending_tasks = True
    print("------------------")
    if not pending_tasks and tasks:
        print("All tasks complete! 🎉")
    print()

def complete_task(task_id):
    """Mark task as done"""
    found = False
    for task in tasks:
        if task.get('id') == task_id:
            if task.get('done', False):
                 print(f"Task ID {task_id}: '{task.get('description')}' is already marked as complete.")
            else:
                task['done'] = True
                task['completed_at'] = datetime.now().isoformat()
                print(f"Completed task ID {task_id}: '{task.get('description')}'")
            found = True
            save_tasks(tasks)
            return True

    if not found:
        print(f"Error: Task with ID {task_id} not found.")
        return False


def delete_task(task_id):
    """Remove a task"""
    global tasks
    original_length = len(tasks)
    tasks_before_delete = tasks[:]
    tasks[:] = [task for task in tasks if task.get('id') != task_id]

    if len(tasks) < original_length:
        print(f"Deleted task ID {task_id}")
        save_tasks(tasks)
        return True
    else:
        print(f"Error: Task with ID {task_id} not found for deletion.")
        return False


# Load tasks at startup
tasks = load_tasks()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simple CLI Task Manager.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python task_manager.py add Buy groceries for the week
  python task_manager.py list
  python task_manager.py complete 3
  python task_manager.py delete 5"""
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True, metavar='COMMAND')

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new task to the list.")
    parser_add.add_argument("description", type=str, nargs='+', help="The description of the task (can include spaces).")

    # List command
    parser_list = subparsers.add_parser("list", help="List all current tasks.")

    # Complete command
    parser_complete = subparsers.add_parser("complete", help="Mark a task as complete by its ID.")
    parser_complete.add_argument("id", type=int, help="The numeric ID of the task to mark as complete.")

    # Delete command
    parser_delete = subparsers.add_parser("delete", help="Delete a task by its ID.")
    parser_delete.add_argument("id", type=int, help="The numeric ID of the task to delete.")

    try:
        args = parser.parse_args()
    except SystemExit:
        pass

    if args.command == "add":
        full_description = " ".join(args.description)
        if add_task(full_description):
            save_tasks(tasks)
    elif args.command == "list":
        list_tasks()
    elif args.command == "complete":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)