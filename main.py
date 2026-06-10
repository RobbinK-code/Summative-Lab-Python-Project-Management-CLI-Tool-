# main.py
import argparse
from engine import ProjectManagerEngine
from models import Product # Keeps namespace clean
import storage

# External framework imports for visual terminal design
from rich.console import Console
from rich.table import Table

console = Console()

def main():
    engine = ProjectManagerEngine()
    storage.load_data(engine)

    # Building command interface structure
    parser = argparse.ArgumentParser(description="Multi-User Project Management Core Console App")
    subparsers = parser.add_subparsers(dest="command", help="Available Operations CLI Subcommands")

    # Command interface: add-user
    user_parser = subparsers.add_parser("add-user", help="Register a new developer profile")
    user_parser.add_argument("--name", required=True, help="Developer name tag")

    # Command interface: add-project
    project_parser = subparsers.add_parser("add-project", help="Bind a project target to a user profile")
    project_parser.add_argument("--user", required=True, help="Target username")
    project_parser.add_argument("--title", required=True, help="Project name string")

    # Command interface: add-task
    task_parser = subparsers.add_parser("add-task", help="Appends execution items to user project lists")
    task_parser.add_argument("--user", required=True, help="Target username profile")
    task_parser.add_argument("--project", required=True, help="Target project branch")
    task_parser.add_argument("--title", required=True, help="Description task title")

    # Command interface: list
    subparsers.add_parser("list", help="Render complete dashboard matrix view")

    args = parser.parse_args()

    # Route execution based on argparse subcommand choices
    if args.command == "add-user":
        success, msg = engine.create_user(args.name)
        if success: console.print(f"[green]{msg}[/green]")
        else: console.print(f"[bold red]{msg}[/bold red]")
        storage.save_data(engine.users)

    elif args.command == "add-project":
        success, msg = engine.create_project(args.user, args.title)
        if success: console.print(f"[green]{msg}[/green]")
        else: console.print(f"[bold red]{msg}[/bold red]")
        storage.save_data(engine.users)

    elif args.command == "add-task":
        success, msg = engine.create_task(args.user, args.project, args.title)
        if success: console.print(f"[green]{msg}[/green]")
        else: console.print(f"[bold red]{msg}[/bold red]")
        storage.save_data(engine.users)

    elif args.command == "list":
        # Initialize Rich table structure for presentation output
        table = Table(title="System Operational Context Framework")
        table.add_column("Developer Profile", style="bold cyan", no_wrap=True)
        table.add_column("Active Projects", style="bold magenta")
        table.add_column("Subtask Specifications Matrix", style="yellow")

        for user in engine.users.values():
            if not user.projects:
                table.add_row(user.name, "[italic red]No projects assigned[/italic red]", "N/A")
            for proj in user.projects:
                task_status_strings = [f"{t.title} ({'✓' if t.is_completed else '✗'})" for t in proj.tasks]
                task_list_output = ", ".join(task_status_strings) or "[italic red]No tasks listed[/italic red]"
                table.add_row(user.name, proj.title, task_list_output)
        
        console.print(table)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()