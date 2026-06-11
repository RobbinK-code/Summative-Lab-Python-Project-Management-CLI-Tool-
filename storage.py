
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




