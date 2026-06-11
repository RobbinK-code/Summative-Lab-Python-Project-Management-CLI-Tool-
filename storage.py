
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





