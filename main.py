import argparse
from rich.console import Console
from rich.table import Table

import storage
from engine import ProjectManagementEngine

console = Console()


def authenticate(engine, username, password):
    return engine.login(username, password)


def show_project_table(projects):
    table = Table(title="Project Summary")
    table.add_column("Project", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Owner", style="green")
    table.add_column("Progress", style="yellow")
    for project in projects:
        table.add_row(project.name, project.description, project.owner, f"{project.progress}%")
    console.print(table)


def show_task_table(task_list):
    table = Table(title="Project Tasks")
    table.add_column("Title", style="cyan")
    table.add_column("Assignee", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Due Date", style="magenta")
    table.add_column("Created By", style="white")
    for task in task_list:
        table.add_row(
            task.title,
            task.assignee or "Unassigned",
            task.status,
            task.due_date or "N/A",
            task.created_by,
        )
    console.print(table)


def interactive_menu(engine):
    active_user = None
    while True:
        console.print("\n[bold blue]Project Management CLI[/bold blue]")
        console.print("1. Register")
        console.print("2. Login")
        console.print("3. Create Project (Manager only)")
        console.print("4. Add Task")
        console.print("5. Assign Task (Manager only)")
        console.print("6. Complete Task")
        console.print("7. List Projects")
        console.print("8. View Project Details")
        console.print("9. List Users")
        console.print("10. List Tasks by Assignee")
        console.print("11. Edit Task")
        console.print("12. Save Data")
        console.print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "0":
            storage.save_data(engine)
            console.print("[green]Saved and exiting.[/green]")
            break
        if choice == "1":
            name = input("Username: ").strip()
            password = input("Password: ").strip()
            role = input("Role [Manager/Member]: ").strip() or "Member"
            success, message = engine.register(name, password, role)
            console.print(f"[green]{message}[/green]" if success else f"[red]{message}[/red]")
            continue
        if choice == "2":
            name = input("Username: ").strip()
            password = input("Password: ").strip()
            user, message = authenticate(engine, name, password)
            if user:
                active_user = user
                console.print(f"[green]{message} Logged in as {user.name} ({user.role}).[/green]")
            else:
                console.print(f"[red]{message}[/red]")
            continue

        if choice in {"3", "4", "5", "6", "7", "8", "9", "10", "11"} and active_user is None:
            console.print("[red]You must login before using this option.[/red]")
            continue

        if choice == "3":
            project_name = input("Project name: ").strip()
            description = input("Project description: ").strip()
            success, message = engine.create_project(active_user, project_name, description)
            console.print(f"[green]{message}[/green]" if success else f"[red]{message}[/red]")
        elif choice == "4":
            project_name = input("Project name: ").strip()
            title = input("Task title: ").strip()
            description = input("Task description: ").strip()
            assignee = input("Assignee (optional): ").strip() or None
            due_date = input("Due date (optional): ").strip() or None
            success, message = engine.add_task(active_user, project_name, title, description, assignee=assignee, due_date=due_date)
            console.print(f"[green]{message}[/green]" if success else f"[red]{message}[/red]")
        elif choice == "5":
            project_name = input("Project name: ").strip()
            title = input("Task title: ").strip()
            assignee = input("Assignee username: ").strip()
            success, message = engine.assign_task(active_user, project_name, title, assignee)
            console.print(f"[green]{message}[/green]" if success else f"[red]{message}[/red]")
        elif choice == "6":
            project_name = input("Project name: ").strip()
            title = input("Task title: ").strip()
            success, message = engine.complete_task(active_user, project_name, title)
            console.print(f"[green]{message}[/green]" if success else f"[red]{message}[/red]")
        elif choice == "7":
            owner = input("Show only projects by owner (optional): ").strip() or None
            show_project_table(engine.list_projects(active_user, owner_name=owner))
        elif choice == "8":
            project_name = input("Project name: ").strip()
            project = engine.get_project(active_user, project_name)
            if project is None:
                console.print(f"[red]Project '{project_name}' not found.[/red]")
            else:
                console.print(f"[bold]{project.name}[/bold] — Owned by [green]{project.owner}[/green] — Progress: [yellow]{project.progress}%[/yellow]")
                show_task_table(project.tasks)
        elif choice == "9":
            users = engine.list_users(active_user)
            user_table = Table(title="Registered Users")
            user_table.add_column("Username", style="cyan")
            user_table.add_column("Role", style="green")
            user_table.add_column("Joined At", style="white")
            for user in users:
                user_table.add_row(user.name, user.role, user.joined_at)
            console.print(user_table)
        elif choice == "10":
            assignee = input("Assignee username: ").strip()
            tasks = engine.tasks_for_assignee(active_user, assignee)
            if not tasks:
                console.print(f"[yellow]No assigned tasks found for {assignee}.[/yellow]")
            else:
                task_table = Table(title=f"Tasks Assigned to {assignee}")
                task_table.add_column("Project", style="cyan")
                task_table.add_column("Title", style="white")
                task_table.add_column("Status", style="green")
                task_table.add_column("Due Date", style="yellow")
                for project_name, task in tasks:
                    task_table.add_row(project_name, task.title, task.status, task.due_date or "N/A")
                console.print(task_table)
        elif choice == "11":
            project_name = input("Project name: ").strip()
            title = input("Task title: ").strip()
            description = input("New description (leave blank to keep): ").strip() or None
            due_date = input("New due date (leave blank to keep): ").strip() or None
            assignee = input("New assignee (leave blank to keep): ").strip() or None
            success, message = engine.update_task(active_user, project_name, title, description=description, due_date=due_date, assignee=assignee)
            console.print(f"[green]{message}[/green]" if success else f"[red]{message}[/red]")
        elif choice == "12":
            storage.save_data(engine)
            console.print("[green]Data saved successfully.[/green]")
        else:
            console.print("[red]Unknown option. Please choose a valid number.[/red]")

        storage.save_data(engine)


def main():
    engine = ProjectManagementEngine()
    storage.load_data(engine)

    if not engine.users:
        engine.register("admin", "admin123", role="Manager")

    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    p_register = subparsers.add_parser("register", help="Register a new user")
    p_register.add_argument("--name", required=True)
    p_register.add_argument("--password", required=True)
    p_register.add_argument("--role", choices=["Manager", "Member"], default="Member")

    p_login = subparsers.add_parser("login", help="Login to validate credentials")
    p_login.add_argument("--name", required=True)
    p_login.add_argument("--password", required=True)

    p_project = subparsers.add_parser("create-project", help="Create a new project (Manager only)")
    p_project.add_argument("--user", required=True)
    p_project.add_argument("--password", required=True)
    p_project.add_argument("--name", required=True)
    p_project.add_argument("--description", required=True)

    p_task = subparsers.add_parser("add-task", help="Add a task to a project")
    p_task.add_argument("--user", required=True)
    p_task.add_argument("--password", required=True)
    p_task.add_argument("--project", required=True)
    p_task.add_argument("--title", required=True)
    p_task.add_argument("--description", required=True)
    p_task.add_argument("--assignee", required=False)
    p_task.add_argument("--due", required=False)

    p_assign = subparsers.add_parser("assign-task", help="Assign a task to a user (Manager only)")
    p_assign.add_argument("--user", required=True)
    p_assign.add_argument("--password", required=True)
    p_assign.add_argument("--project", required=True)
    p_assign.add_argument("--task", required=True)
    p_assign.add_argument("--assignee", required=True)

    p_complete = subparsers.add_parser("complete-task", help="Mark a task as complete")
    p_complete.add_argument("--user", required=True)
    p_complete.add_argument("--password", required=True)
    p_complete.add_argument("--project", required=True)
    p_complete.add_argument("--task", required=True)

    p_list = subparsers.add_parser("list-projects", help="List all projects")
    p_list.add_argument("--user", required=True)
    p_list.add_argument("--password", required=True)
    p_list.add_argument("--owner", required=False, help="Filter by project owner")

    p_users = subparsers.add_parser("list-users", help="List registered users")
    p_users.add_argument("--user", required=True)
    p_users.add_argument("--password", required=True)

    p_list_tasks = subparsers.add_parser("list-tasks", help="List tasks assigned to a user")
    p_list_tasks.add_argument("--user", required=True)
    p_list_tasks.add_argument("--password", required=True)
    p_list_tasks.add_argument("--assignee", required=True)

    p_edit = subparsers.add_parser("edit-task", help="Edit an existing task")
    p_edit.add_argument("--user", required=True)
    p_edit.add_argument("--password", required=True)
    p_edit.add_argument("--project", required=True)
    p_edit.add_argument("--task", required=True)
    p_edit.add_argument("--description", required=False)
    p_edit.add_argument("--due", required=False)
    p_edit.add_argument("--assignee", required=False)

    p_details = subparsers.add_parser("project-details", help="Show tasks for a single project")
    p_details.add_argument("--user", required=True)
    p_details.add_argument("--password", required=True)
    p_details.add_argument("--project", required=True)

    args = parser.parse_args()

    if args.command is None:
        interactive_menu(engine)
        return

    if args.command == "register":
        success, message = engine.register(args.name, args.password, args.role)
        console.print(f"[green]{message}[/green]" if success else f"[red]{message}[/red]")
        if success:
            storage.save_data(engine)

    elif args.command == "login":
        _, message = authenticate(engine, args.name, args.password)
        console.print(f"[green]{message}[/green]" if _ else f"[red]{message}[/red]")

    else:
        user, message = authenticate(engine, args.user, args.password)
        if user is None:
            console.print(f"[red]{message}[/red]")
            return

        if args.command == "create-project":
            success, message = engine.create_project(user, args.name, args.description)
        elif args.command == "add-task":
            success, message = engine.add_task(user, args.project, args.title, args.description, assignee=args.assignee, due_date=args.due)
        elif args.command == "assign-task":
            success, message = engine.assign_task(user, args.project, args.task, args.assignee)
        elif args.command == "complete-task":
            success, message = engine.complete_task(user, args.project, args.task)
        elif args.command == "list-projects":
            show_project_table(engine.list_projects(user, owner_name=args.owner))
            return
        elif args.command == "list-users":
            users = engine.list_users(user)
            user_table = Table(title="Registered Users")
            user_table.add_column("Username", style="cyan")
            user_table.add_column("Role", style="green")
            user_table.add_column("Joined At", style="white")
            for u in users:
                user_table.add_row(u.name, u.role, u.joined_at)
            console.print(user_table)
            return
        elif args.command == "list-tasks":
            tasks = engine.tasks_for_assignee(user, args.assignee)
            if not tasks:
                console.print(f"[yellow]No tasks found for {args.assignee}.[/yellow]")
                return
            task_table = Table(title=f"Tasks Assigned to {args.assignee}")
            task_table.add_column("Project", style="cyan")
            task_table.add_column("Title", style="white")
            task_table.add_column("Status", style="green")
            task_table.add_column("Due Date", style="yellow")
            for project_name, task in tasks:
                task_table.add_row(project_name, task.title, task.status, task.due_date or "N/A")
            console.print(task_table)
            return
        elif args.command == "edit-task":
            success, message = engine.update_task(user, args.project, args.task, description=args.description, due_date=args.due, assignee=args.assignee)
        elif args.command == "project-details":
            project = engine.get_project(user, args.project)
            if project is None:
                console.print(f"[red]Project '{args.project}' not found.[/red]")
                return
            console.print(f"[bold]{project.name}[/bold] — Owned by [green]{project.owner}[/green] — Progress: [yellow]{project.progress}%[/yellow]")
            show_task_table(project.tasks)
            return
        else:
            console.print("[red]Unknown command.[/red]")
            return

        console.print(f"[green]{message}[/green]" if success else f"[red]{message}[/red]")
        if success:
            storage.save_data(engine)


if __name__ == "__main__":
    main()
