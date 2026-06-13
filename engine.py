from functools import wraps

from models import User, Project, Task


def require_manager(func):
    @wraps(func)
    def wrapper(self, active_user, *args, **kwargs):
        if active_user.role != "Manager":
            return False, "Access Denied: Manager role required."
        return func(self, active_user, *args, **kwargs)
    return wrapper


def require_authenticated(func):
    @wraps(func)
    def wrapper(self, active_user, *args, **kwargs):
        if active_user is None:
            return False, "Authentication required."
        return func(self, active_user, *args, **kwargs)
    return wrapper


class ProjectManagementEngine:
    def __init__(self):
        self.users = {}
        self.projects = {}

    def register(self, name, password, role="Member"):
        if name in self.users:
            return False, "Username already exists."
        if role not in {"Manager", "Member"}:
            return False, "Role must be Manager or Member."
        self.users[name] = User(name, password, role)
        return True, f"User '{name}' registered as {role}."

    def login(self, name, password):
        if name not in self.users:
            return None, "Invalid credentials."
        user = self.users[name]
        if not user.check_password(password):
            return None, "Invalid credentials."
        return user, "Login successful."

    @require_manager
    def create_project(self, active_user, project_name, description):
        if project_name in self.projects:
            return False, "Project already exists."
        self.projects[project_name] = Project(project_name, description, active_user.name)
        return True, f"Project '{project_name}' created by {active_user.name}."

    @require_authenticated
    def list_users(self, active_user):
        return list(self.users.values())

    @require_authenticated
    def list_projects(self, active_user, owner_name=None):
        projects = list(self.projects.values())
        if owner_name:
            return [project for project in projects if project.owner == owner_name]
        return projects

    @require_authenticated
    def tasks_for_assignee(self, active_user, assignee_name):
        if assignee_name not in self.users:
            return []
        tasks = []
        for project in self.projects.values():
            for task in project.tasks:
                if task.assignee == assignee_name:
                    tasks.append((project.name, task))
        return tasks

    @require_authenticated
    def update_task(self, active_user, project_name, task_title, description=None, due_date=None, assignee=None):
        if project_name not in self.projects:
            return False, "Project not found."
        project = self.projects[project_name]
        task = project.find_task(task_title)
        if task is None:
            return False, "Task not found."
        if active_user.role != "Manager" and project.owner != active_user.name and task.assignee != active_user.name:
            return False, "Only the assignee, project owner, or a Manager can update the task."
        if assignee and assignee not in self.users:
            return False, "Assignee user does not exist."
        if description:
            task.description = description
        if due_date is not None:
            task.due_date = due_date
        if assignee:
            task.assignee = assignee
        return True, f"Task '{task_title}' updated in project '{project_name}'."

    @require_authenticated
    def add_task(self, active_user, project_name, title, description, assignee=None, due_date=None):
        if project_name not in self.projects:
            return False, "Project not found."
        project = self.projects[project_name]
        if active_user.role != "Manager" and project.owner != active_user.name:
            return False, "Only the project owner or a Manager can add tasks."
        if project.find_task(title):
            return False, "Task title already exists in the project."
        if assignee and assignee not in self.users:
            return False, "Assignee user does not exist."
        new_task = Task(title, description, active_user.name, assignee=assignee, due_date=due_date)
        project.add_task(new_task)
        return True, f"Task '{title}' added to project '{project_name}'."

    @require_manager
    def assign_task(self, active_user, project_name, task_title, assignee_name):
        if project_name not in self.projects:
            return False, "Project not found."
        if assignee_name not in self.users:
            return False, "Assignee does not exist."
        project = self.projects[project_name]
        task = project.find_task(task_title)
        if task is None:
            return False, "Task not found."
        task.assignee = assignee_name
        return True, f"Task '{task_title}' assigned to {assignee_name}."

    @require_authenticated
    def complete_task(self, active_user, project_name, task_title):
        if project_name not in self.projects:
            return False, "Project not found."
        project = self.projects[project_name]
        task = project.find_task(task_title)
        if task is None:
            return False, "Task not found."
        if task.assignee and task.assignee != active_user.name and active_user.role != "Manager":
            return False, "Only the assignee or a Manager can complete this task."
        task.mark_complete()
        return True, f"Task '{task_title}' in project '{project_name}' marked complete."

    @require_authenticated
    def get_project(self, active_user, project_name):
        return self.projects.get(project_name)
