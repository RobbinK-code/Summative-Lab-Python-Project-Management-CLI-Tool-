import pytest

from engine import ProjectManagementEngine
from models import User, Project, Task


def test_list_users_returns_registered_users():
    engine = ProjectManagementEngine()
    engine.register("alice", "password", role="Member")
    engine.register("bob", "password", role="Manager")

    user, _ = engine.login("bob", "password")
    users = engine.list_users(user)

    assert len(users) == 2
    assert {u.name for u in users} == {"alice", "bob"}


def test_list_projects_can_filter_by_owner():
    engine = ProjectManagementEngine()
    engine.register("manager", "password", role="Manager")
    user, _ = engine.login("manager", "password")
    engine.create_project(user, "Bakery Launch", "Open a new bakery.")
    engine.create_project(user, "Holiday Menu", "Plan seasonal pastries.")

    projects = engine.list_projects(user, owner_name="manager")
    assert len(projects) == 2
    assert projects[0].owner == "manager"


def test_tasks_for_assignee_returns_assigned_tasks():
    engine = ProjectManagementEngine()
    engine.register("manager", "password", role="Manager")
    engine.register("chef", "password", role="Member")
    manager, _ = engine.login("manager", "password")
    engine.create_project(manager, "Bakery Sprint", "Prepare holiday launch.")
    engine.add_task(manager, "Bakery Sprint", "Bake bread", "Prepare sourdough loaves", assignee="chef")

    tasks = engine.tasks_for_assignee(manager, "chef")
    assert len(tasks) == 1
    project_name, task = tasks[0]
    assert project_name == "Bakery Sprint"
    assert task.title == "Bake bread"
    assert task.assignee == "chef"


def test_update_task_allows_task_owner_or_manager():
    engine = ProjectManagementEngine()
    engine.register("manager", "password", role="Manager")
    engine.register("owner", "password", role="Member")
    engine.register("chef", "password", role="Member")
    manager, _ = engine.login("manager", "password")
    owner, _ = engine.login("owner", "password")
    engine.create_project(manager, "Bakery Plan", "Develop bakery launch plan.")
    engine.add_task(manager, "Bakery Plan", "Design menu", "Create the pastry list", assignee="chef")

    success, message = engine.update_task(owner, "Bakery Plan", "Design menu", description="Revise pastry list", due_date="2026-07-15")
    assert success is False
    assert "Only the assignee" in message or "project owner" in message

    chef, _ = engine.login("chef", "password")
    success, message = engine.update_task(chef, "Bakery Plan", "Design menu", description="Finalize pastry list")
    assert success is True
    project = engine.get_project(chef, "Bakery Plan")
    assert project.find_task("Design menu").description == "Finalize pastry list"
