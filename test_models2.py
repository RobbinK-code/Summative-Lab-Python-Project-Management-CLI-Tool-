import pytest
from models import Person, User, Project, Task


def test_user_inheritance_from_person():
    user = User("Alex", "password123", role="Member")
    assert isinstance(user, Person)
    assert user.name == "Alex"
    assert user.role == "Member"


def test_user_secure_password_hashing():
    user = User("ChefBob", "secureBake123", role="Manager")
    assert user.password_hash != "secureBake123"
    assert user.check_password("secureBake123") is True
    assert user.check_password("wrongPass") is False


def test_project_creation_and_progress():
    project = Project("Launch App", "Build MVP for client.", "alex")
    assert project.name == "Launch App"
    assert project.owner == "alex"
    assert project.progress == 0

    task = Task("Design UI", "Create mockups", "alex", assignee="dev")
    project.add_task(task)
    assert project.find_task("Design UI") is task
    assert project.progress == 0

    task.mark_complete()
    assert task.status == "Complete"
    assert project.progress == 100


def test_task_to_dict_and_from_dict():
    task = Task("Write Tests", "Add coverage for engine", "alex", assignee="dev", due_date="2026-06-30")
    data = task.to_dict()
    assert data["title"] == "Write Tests"
    assert data["assignee"] == "dev"
    assert data["due_date"] == "2026-06-30"

    reconstructed = Task.from_dict(data)
    assert reconstructed.title == "Write Tests"
    assert reconstructed.assignee == "dev"
    assert reconstructed.status == "Pending"


def test_user_to_dict_is_serializable():
    user = User("Emma", "secret", role="Member")
    data = user.to_dict()
    assert data["name"] == "Emma"
    assert data["role"] == "Member"
    assert data["password_hash"] == user.password_hash
