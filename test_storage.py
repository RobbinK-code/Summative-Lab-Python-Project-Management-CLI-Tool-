<<<<<<< HEAD
import json
import tempfile
import unittest
from pathlib import Path

import storage
from models import User, Product, Order


class DummyEngine:
    def __init__(self):
        self.users = {}
        self.inventory = {}


class StorageTests(unittest.TestCase):
    def test_save_data_writes_json(self):
        user = User("alice", "password123", role="Staff")
        user.completed_orders.append(Order("Croissant", 2, 5.00))
        item = Product("Croissant", 2.50, 50)

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "bakery_data.json"
            storage.save_data({"alice": user}, {"Croissant": item}, file_path=file_path)

            with file_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)

            self.assertIn("users", data)
            self.assertIn("inventory", data)
            self.assertIn("alice", data["users"])
            self.assertEqual(data["users"]["alice"]["role"], "Staff")
            self.assertEqual(data["inventory"]["Croissant"]["stock"], 50)
            self.assertEqual(data["users"]["alice"]["completed_orders"][0]["product_name"], "Croissant")

    def test_load_data_reconstructs_objects(self):
        payload = {
            "users": {
                "bob": {
                    "name": "bob",
                    "role": "Manager",
                    "password_hash": User("bob", "secret").password_hash,
                    "completed_orders": [
                        {"product_name": "Baguette", "quantity": 3, "total_cost": 7.50}
                    ]
                }
            },
            "inventory": {
                "Baguette": {"name": "Baguette", "price": 2.50, "stock": 10}
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "bakery_data.json"
            with file_path.open("w", encoding="utf-8") as handle:
                json.dump(payload, handle)

            engine = DummyEngine()
            storage.load_data(engine, file_path=file_path)

            self.assertIn("bob", engine.users)
            self.assertIn("Baguette", engine.inventory)
            self.assertEqual(engine.users["bob"].role, "Manager")
            self.assertEqual(engine.inventory["Baguette"].stock, 10)
            self.assertEqual(engine.users["bob"].completed_orders[0].product_name, "Baguette")

    def test_load_data_handles_missing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "missing.json"
            engine = DummyEngine()
            storage.load_data(engine, file_path=file_path)
            self.assertEqual(engine.users, {})
            self.assertEqual(engine.inventory, {})

    def test_load_data_handles_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "bad.json"
            file_path.write_text("not valid json", encoding="utf-8")

            engine = DummyEngine()
            storage.load_data(engine, file_path=file_path)
            self.assertEqual(engine.users, {})
            self.assertEqual(engine.inventory, {})

    def test_load_data_handles_empty_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "empty.json"
            file_path.write_text("", encoding="utf-8")

            engine = DummyEngine()
            storage.load_data(engine, file_path=file_path)
            self.assertEqual(engine.users, {})
            self.assertEqual(engine.inventory, {})


if __name__ == "__main__":
    unittest.main()
=======
import json
import tempfile
import unittest
from pathlib import Path

import storage


class DummyTask:
    def __init__(self, title, is_completed=False):
        self.title = title
        self.is_completed = is_completed


class DummyProject:
    def __init__(self, title, tasks=None):
        self.title = title
        self.tasks = tasks or []


class DummyUser:
    def __init__(self, name, projects=None):
        self.name = name
        self.projects = projects or []


class DummyEngine:
    def __init__(self):
        self.users = {}


class StorageTests(unittest.TestCase):
    def test_save_data_writes_json(self):
        user = DummyUser("alice", [DummyProject("Website", [DummyTask("Draft", False)])])
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "data.json"
            storage.save_data({"alice": user}, file_path=file_path)

            with file_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)

            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["name"], "alice")
            self.assertEqual(data[0]["projects"][0]["title"], "Website")
            self.assertEqual(data[0]["projects"][0]["tasks"][0]["title"], "Draft")

    def test_load_data_reconstructs_objects(self):
        payload = [
            {
                "name": "bob",
                "projects": [
                    {
                        "title": "Launch",
                        "tasks": [
                            {"title": "Plan", "is_completed": True},
                            {"title": "Execute", "is_completed": False},
                        ],
                    }
                ],
            }
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "data.json"
            with file_path.open("w", encoding="utf-8") as handle:
                json.dump(payload, handle)

            engine = DummyEngine()
            storage.load_data(engine, file_path=file_path)

            self.assertIn("bob", engine.users)
            user = engine.users["bob"]
            self.assertEqual(user.name, "bob")
            self.assertEqual(len(user.projects), 1)
            self.assertEqual(user.projects[0].title, "Launch")
            self.assertEqual(len(user.projects[0].tasks), 2)
            self.assertEqual(user.projects[0].tasks[0].title, "Plan")
            self.assertTrue(user.projects[0].tasks[0].is_completed)

    def test_load_data_handles_missing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "missing.json"
            engine = DummyEngine()
            storage.load_data(engine, file_path=file_path)
            self.assertEqual(engine.users, {})

    def test_load_data_handles_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "bad.json"
            file_path.write_text("not valid json", encoding="utf-8")

            engine = DummyEngine()
            storage.load_data(engine, file_path=file_path)
            self.assertEqual(engine.users, {})

    def test_load_data_handles_empty_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "empty.json"
            file_path.write_text("", encoding="utf-8")

            engine = DummyEngine()
            storage.load_data(engine, file_path=file_path)
            self.assertEqual(engine.users, {})


if __name__ == "__main__":
    unittest.main()
>>>>>>> c912bea30394ebc62f7b51ba0361bded235f4dde
