# Bakery Project Management CLI Tool

This repository implements a bakery-themed command-line project management tool. It is designed to manage users, bakery projects, and tasks using an interactive and modular CLI.

Features include:
- Object-oriented design using classes, inheritance, encapsulation, and dynamic behavior
- JSON persistence for users and projects
- Role-based authentication with password hashing
- Interactive menu plus argparse subcommands for structured CLI usage
- External package usage via `rich` for polished terminal output

## Running the application

Install dependencies:

    pip install -r requirements.txt

Run the interactive CLI:

    python main.py

Use subcommands directly, for example:

    python main.py register --name alice --password secret --role Member
    python main.py create-project --user admin --password admin123 --name "Bakery Launch" --description "Plan bakery opening"
    python main.py add-task --user admin --password admin123 --project "Bakery Launch" --title "Design menu" --description "Choose pastry offerings" --assignee alice --due 2026-07-01
    python main.py list-projects --user admin --password admin123
    python main.py list-users --user admin --password admin123
    python main.py list-tasks --user admin --password admin123 --assignee alice
    python main.py edit-task --user admin --password admin123 --project "Bakery Launch" --task "Design menu" --description "Finalize pastry list"

## Supported commands

- `register` — add a new user
- `login` — validate credentials
- `create-project` — create bakery project plans (`Manager` only)
- `add-task` — add a task inside a project
- `assign-task` — assign an existing task to a user (`Manager` only)
- `complete-task` — mark a task complete
- `list-projects` — show current projects (optionally filter by owner)
- `list-users` — display registered users
- `list-tasks` — display tasks assigned to a specific user
- `edit-task` — update a task description, due date, or assignee
- `project-details` — inspect a project's tasks

## Persistence

Project and user data are saved to `project_data.json`.

## Testing

Run tests with:

    pytest -q

## Notes

- A default admin account is seeded when the data file is empty:
  - username: `admin`
  - password: `admin123`

- The repository includes a sample `project_data.json` file to show file-based persistence structure.
