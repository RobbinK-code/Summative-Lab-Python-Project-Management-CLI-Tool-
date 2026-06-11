
import abc
import json
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_STORAGE_FILE = Path("storage.json") # Default storage file path

class StorageInterface(abc.ABC):
    """Storage backend interface for loading and saving user data."""

    @abc.abstractmethod
    def save(self, users: Dict[str, Any]) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def load(self, engine: Any) -> None:
        raise NotImplementedError

class FileStorage(StorageInterface):
    """File-based storage implementation using JSON persistence."""

    def __init__(self, file_path: Path | str = DEFAULT_STORAGE_FILE) -> None:
        self.file_path = Path(file_path)

def save(self, users: Dict[str, Any]) -> None:
        payload = [_serialize_user(user) for user in users.values()]
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with self.file_path.open("w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2, ensure_ascii=False)
        except OSError:
            # If the file cannot be written, swallow the error to avoid crashing the app.
            pass

  def load(self, engine: Any) -> None:
        data = _load_json(self.file_path)
        engine.users = {}

        if not isinstance(data, list):
            return

        for user_data in data:
            if not isinstance(user_data, dict):
                continue

            user = PersistentUser.from_dict(user_data)
            engine.users[user.name] = user

def save_data(users: Dict[str, Any], file_path: Path | str = DEFAULT_STORAGE_FILE) -> None:
    """Serialize engine users and save them to a JSON file."""
    FileStorage(file_path).save(users)


def load_data(engine: Any, file_path: Path | str = DEFAULT_STORAGE_FILE) -> None:
    """Load JSON storage and populate the engine users dictionary."""
    FileStorage(file_path).load(engine)

class PersistentTask:
    def __init__(self, title: str, is_completed: bool = False) -> None:
        self.title = title
        self.is_completed = is_completed

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "is_completed": self.is_completed,
        }

@classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PersistentTask":
        return cls(
            title=str(data.get("title", "")),
            is_completed=bool(data.get("is_completed", False)),
        )

class PersistentProject:
    def __init__(self, title: str, tasks: List[PersistentTask] | None = None) -> None:
        self.title = title
        self.tasks = tasks or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "tasks": [task.to_dict() for task in self.tasks],
        }

@classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PersistentProject":
        raw_tasks = data.get("tasks", [])
        tasks = []
        if isinstance(raw_tasks, list):
            for task_data in raw_tasks:
                if isinstance(task_data, dict):
                    tasks.append(PersistentTask.from_dict(task_data))
        return cls(title=str(data.get("title", "")), tasks=tasks)

class PersistentUser:
    def __init__(self, name: str, projects: List[PersistentProject] | None = None) -> None:
        self.name = name
        self.projects = projects or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "projects": [project.to_dict() for project in self.projects],
        }

@classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PersistentUser":
        raw_projects = data.get("projects", [])
        projects = []
        if isinstance(raw_projects, list):
            for project_data in raw_projects:
                if isinstance(project_data, dict):
                    projects.append(PersistentProject.from_dict(project_data))
        return cls(name=str(data.get("name", "")), projects=projects)


def _serialize_task(task: Any) -> Dict[str, Any]:
    return {
        "title": getattr(task, "title", ""),
        "is_completed": bool(getattr(task, "is_completed", False)),
    }

def _serialize_project(project: Any) -> Dict[str, Any]:
    tasks = getattr(project, "tasks", []) or []
    return {
        "title": getattr(project, "title", ""),
        "tasks": [_serialize_task(task) for task in tasks if task is not None],
    }


def _serialize_user(user: Any) -> Dict[str, Any]:
    projects = getattr(user, "projects", []) or []
    return {
        "name": getattr(user, "name", ""),
        "projects": [_serialize_project(project) for project in projects if project is not None],
    }


def _load_json(file_path: Path) -> Any:
    try:
        with Path(file_path).open("r", encoding="utf-8") as handle:
            content = handle.read()
            if not content.strip():
                return []
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []






