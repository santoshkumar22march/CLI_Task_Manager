# CLI Task Manager

A command-line application written in Python to manage a simple to-do list. Tasks are stored locally in a `tasks.json` file.

## Features

*   **Add:** Add new tasks to your list.
*   **List:** View all current tasks with their status (pending/complete) and ID.
*   **Complete:** Mark tasks as complete using their ID.
*   **Delete:** Remove tasks from the list using their ID.
*   **Persistence:** Tasks are saved to `tasks.json` so they persist between runs.
*   **Timestamps:** Optionally tracks creation and completion times (ISO format).

## Requirements

*   Python 3.6+ (uses f-strings and standard libraries like `json`, `os`, `argparse`, `datetime`)

## Setup

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/santoshkumar22march/CLI_Task_Manager.git
    cd CLI_Task_Manager
    ```

2.  **Run the script:** No external libraries are needed! You can run it directly.
    ```bash
    python task_manager.py --help
    ```

## Usage

Commands are provided as the first argument after the script name.

*   **Add a task:**
    ```bash
    python task_manager.py add Buy groceries for the week
    ```

*   **List all tasks:**
    ```bash
    python task_manager.py list
    ```
    *Output Example:*
    ```
    --- Your Tasks ---
    [ ] ID: 1 - Buy groceries for the week
    [ ] ID: 2 - Call mom
    [X] ID: 3 - doing assignments
    ------------------
    ```

*   **Mark a task as complete:**
    ```bash
    python task_manager.py complete 1
    ```

*   **Delete a task:**
    ```bash
    python task_manager.py delete 2
    ```

*   **Get help:**
    ```bash
    python task_manager.py --help
    # or
    python task_manager.py add --help
    ```

## Task Data File (`tasks.json`)

*   The script automatically creates and manages `tasks.json` in the same directory.
*   You generally **don't need to edit this file manually**, but it contains a JSON list of task objects.
*   By default, this file is **not ignored** by Git in the provided `.gitignore`. If you prefer *not* to track your personal tasks list in Git history, uncomment the `tasks.json` line in the `.gitignore` file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
