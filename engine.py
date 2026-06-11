from models import User, Project, Task

def require_admin(func):
    def wrapper(self, active_user, *args, **kwargs):
        if active_user.role != "Admin":
            return False, "Access Denied: Only Admins can do this action!"
        return func(self, active_user, *args, **kwargs)
    return wrapper

class ProjectManagerEngine:
    def __init__(self):
        self.users = {}  # Dictionary to hold: {"username": UserObject}

    def register(self, name, password, role="User"):
        if name in self.users:
            return False, "This username is already taken!"
        
        # Create user object and save it to our dictionary
        self.users[name] = User(name, password, role)
        return True, f"User '{name}' registered successfully as a {role}."

    def login(self, name, password):
        if name not in self.users:
            return None, "User not found!"
        
        user_obj = self.users[name]
        if not user_obj.check_password(password):
            return None, "Wrong password!"
        
        return user_obj, "Login successful!"

    @require_admin
    def create_project(self, active_user, target_username, project_title):
        """Uses the @require_admin decorator to restrict access."""
        if target_username not in self.users:
            return False, "The user you want to assign this project to doesn't exist!"
        
        target_user_obj = self.users[target_username]
        
        # Check if project title already exists for this user
        for p in target_user_obj.projects:
            if p.title == project_title:
                return False, "This project already exists for this user!"
        
        # Add the project
        new_project = Project(project_title)
        target_user_obj.projects.append(new_project)
        return True, f"Project '{project_title}' assigned to '{target_username}'."

    @require_admin
    def create_task(self, active_user, username, project_title, task_title):
        if username not in self.users:
            return False, "User not found."
        
        user_obj = self.users[username]
        
        # Find the project
        project_obj = None
        for p in user_obj.projects:
            if p.title == project_title:
                project_obj = p
                break
                
        if project_obj is None:
            return False, "Project not found for this user."
        
        # Add the task
        new_task = Task(task_title)
        project_obj.tasks.append(new_task)
        return True, f"Task '{task_title}' added to project '{project_title}'."