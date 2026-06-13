import hashlib
from datetime import datetime, timezone

class Person:
    """Base class for all users in the project system."""

    def __init__(self, name, role="Member"):
        self.name = name
        self.role = role

class User(Person):
    """Represents a registered user with secure password storage."""

    def __init__(self, name, password, role="Member"):
        super().__init__(name, role)
        self.password_hash = self.hash_text(password)
        self.joined_at = datetime.now(timezone.utc).isoformat()

    def hash_text(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

    def check_password(self, password):
        return self.hash_text(password) == self.password_hash

    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "password_hash": self.password_hash,
            "joined_at": self.joined_at,
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["name"], "temporary", role=data.get("role", "Member"))
        user.password_hash = data["password_hash"]
        user.joined_at = data.get("joined_at", datetime.now(timezone.utc).isoformat())
        return user

class Task:
    """Represents a task inside a project."""

    def __init__(self, title, description, created_by, assignee=None, due_date=None, status="Pending"):
        self.title = title
        self.description = description
        self.created_by = created_by
        self.assignee = assignee
        self.status = status
        self.due_date = due_date
        self.created_at = datetime.now(timezone.utc).isoformat()

    def mark_complete(self):
        self.status = "Complete"

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "created_by": self.created_by,
            "assignee": self.assignee,
            "status": self.status,
            "due_date": self.due_date,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            data["title"],
            data["description"],
            data["created_by"],
            assignee=data.get("assignee"),
            due_date=data.get("due_date"),
            status=data.get("status", "Pending"),
        )
        task.created_at = data.get("created_at", task.created_at)
        return task

class Project:
    """Represents a project that can contain multiple tasks."""

    def __init__(self, name, description, owner):
        self.name = name
        self.description = description
        self.owner = owner
        self.tasks = []
        self.created_at = datetime.now(timezone.utc).isoformat()

    @property
    def progress(self):
        if not self.tasks:
            return 0
        completed = sum(1 for task in self.tasks if task.status == "Complete")
        return int((completed / len(self.tasks)) * 100)

    def add_task(self, task):
        self.tasks.append(task)

    def find_task(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "owner": self.owner,
            "created_at": self.created_at,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data):
        project = cls(data["name"], data["description"], data["owner"])
        project.created_at = data.get("created_at", project.created_at)
        for task_data in data.get("tasks", []):
            project.add_task(Task.from_dict(task_data))
        return project
