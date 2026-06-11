import json
import os
from models import User, Product, Order

DATA_FILE = "bakery_data.json"

def save_data(users_dict, inventory_dict):
    try:
        saved_dict = {
            "users": {name: u.to_dict() for name, u in users_dict.items()},
            "inventory": {name: p.to_dict() for name, p in inventory_dict.items()}
        }
        with open(DATA_FILE, "w") as f:
            json.dump(saved_dict, f, indent=4)
    except IOError:
        print("[Storage Error] Failed to write data to file.")

def load_data(engine_instance):
    if not os.path.exists(DATA_FILE):
        return

    try:
        with open(DATA_FILE, "r") as f:
            raw_data = json.load(f)
            
            # 1. Rebuild Menu Inventory Items
            for item_name, p_data in raw_data.get("inventory", {}).items():
                engine_instance.inventory[item_name] = Product(item_name, p_data["price"], p_data["stock"])
            
            # 2. Rebuild Employee Profiles and Order History
            for username, u_data in raw_data.get("users", {}).items():
                new_user = User(username, "placeholder", u_data["role"])
                new_user.password_hash = u_data["password_hash"]
                
                for o_data in u_data.get("completed_orders", []):
                    new_order = Order(o_data["product_name"], o_data["quantity"], o_data["total_cost"])
                    new_user.completed_orders.append(new_order)
                    
                engine_instance.users[username] = new_user
    except (json.JSONDecodeError, IOError):
        print("[Storage Error] Database corrupted. Booting blank slate.")