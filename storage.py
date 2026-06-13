import json
from pathlib import Path

from models import User, Project

DATA_FILE = Path("project_data.json")


def save_data(engine, file_path=None):
    path = Path(file_path) if file_path else DATA_FILE
    try:
        payload = {
            "users": {name: user.to_dict() for name, user in engine.users.items()},
            "projects": {name: project.to_dict() for name, project in engine.projects.items()},
        }
        with path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)
    except IOError:
        print("[Storage Error] Failed to write data to file.")


def load_data(engine, file_path=None):
    path = Path(file_path) if file_path else DATA_FILE
    if not path.exists():
        return
    try:
        with path.open("r", encoding="utf-8") as f:
            raw_data = json.load(f)

            for username, user_data in raw_data.get("users", {}).items():
                engine.users[username] = User.from_dict(user_data)

            for project_name, project_data in raw_data.get("projects", {}).items():
                engine.projects[project_name] = Project.from_dict(project_data)
    except (json.JSONDecodeError, IOError):
        print("[Storage Error] Database corrupted. Booting blank slate.")
