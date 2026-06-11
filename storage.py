
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




