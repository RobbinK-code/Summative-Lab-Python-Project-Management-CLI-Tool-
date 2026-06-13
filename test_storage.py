import json
import tempfile
import unittest
from pathlib import Path

import storage
from models import User, Project, Task


class DummyEngine:
    def __init__(self):
        self.users = {}
        self.projects = {}


class StorageTests(unittest.TestCase):
    def test_save_data_writes_json(self):
        user = User("alice", "password123", role="Member")
        project = Project("Website", "Build a launch website.", "alice")
        task = Task("Create homepage", "Design the landing page", "alice", assignee="alice")
        project.add_task(task)

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "project_data.json"
            storage.save_data(type("E", (), {"users": {"alice": user}, "projects": {"Website": project}})(), file_path=file_path)

            with file_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)

            self.assertIn("users", data)
            self.assertIn("projects", data)
            self.assertEqual(data["users"]["alice"]["role"], "Member")
            self.assertEqual(data["projects"]["Website"]["tasks"][0]["title"], "Create homepage")

    def test_load_data_reconstructs_objects(self):
        payload = {
            "users": {
                "bob": {
                    "name": "bob",
                    "role": "Manager",
                    "password_hash": User("bob", "secret").password_hash,
                    "joined_at": "2026-01-01T00:00:00"
                }
            },
            "projects": {
                "App": {
                    "name": "App",
                    "description": "Build mobile app.",
                    "owner": "bob",
                    "created_at": "2026-01-01T00:00:00",
                    "tasks": [
                        {
                            "title": "Setup repo",
                            "description": "Initialize git and structure",
                            "created_by": "bob",
                            "assignee": "bob",
                            "status": "Pending",
                            "due_date": "2026-06-30",
                            "created_at": "2026-01-01T00:00:00"
                        }
                    ]
                }
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "project_data.json"
            with file_path.open("w", encoding="utf-8") as handle:
                json.dump(payload, handle)

            engine = DummyEngine()
            storage.load_data(engine, file_path=file_path)

            self.assertIn("bob", engine.users)
            self.assertIn("App", engine.projects)
            self.assertEqual(engine.users["bob"].role, "Manager")
            self.assertEqual(engine.projects["App"].tasks[0].title, "Setup repo")

    def test_load_data_handles_missing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "missing.json"
            engine = DummyEngine()
            storage.load_data(engine, file_path=file_path)
            self.assertEqual(engine.users, {})
            self.assertEqual(engine.projects, {})

    def test_load_data_handles_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "bad.json"
            file_path.write_text("not valid json", encoding="utf-8")
            engine = DummyEngine()
            storage.load_data(engine, file_path=file_path)
            self.assertEqual(engine.users, {})
            self.assertEqual(engine.projects, {})

    def test_load_data_handles_empty_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "empty.json"
            file_path.write_text("", encoding="utf-8")
            engine = DummyEngine()
            storage.load_data(engine, file_path=file_path)
            self.assertEqual(engine.users, {})
            self.assertEqual(engine.projects, {})


if __name__ == "__main__":
    unittest.main()
