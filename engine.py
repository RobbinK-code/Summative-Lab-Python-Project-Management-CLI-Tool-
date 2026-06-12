from models import User, Product, Order

def require_manager(func):
    """Custom Decorator: Only allows users with the 'Manager' role to proceed."""
    def wrapper(self, active_user, *args, **kwargs):
        if active_user.role != "Manager":
            return False, "Access Denied: Only a Bakery Manager can do this!"
        return func(self, active_user, *args, **kwargs)
    return wrapper

class BakeryEngine:
    def __init__(self):
        self.users = {}      # {"username": UserObject}
        self.inventory = {}  # {"Croissant": ProductObject}

    def register(self, name, password, role="Staff"):
        if name in self.users:
            return False, "Username already exists."
        self.users[name] = User(name, password, role)
        return True, f"Employee '{name}' registered as {role}."

    def login(self, name, password):
        if name not in self.users or not self.users[name].check_password(password):
            return None, "Invalid credentials."
        return self.users[name], "Login successful."

    @require_manager
    def add_inventory_item(self, active_user, item_name, price, stock):
        """Manager Only: Adds a new pastry/bread type or updates stock."""
        if item_name in self.inventory:
            # Update stock safely using our setter property validation
            try:
                self.inventory[item_name].stock += stock
                return True, f"Updated '{item_name}' stock to {self.inventory[item_name].stock}."
            except ValueError as e:
                return False, str(e)
        
        self.inventory[item_name] = Product(item_name, price, stock)
        return True, f"Successfully added {item_name} to the bakery menu."

    def process_bakery_order(self, employee_username, item_name, quantity):
        """Processes a sale, calculates subtotals, and reduces stock."""
        if employee_username not in self.users:
            return False, "Employee user not found."
        if item_name not in self.inventory:
            return False, f"We don't bake '{item_name}' here!"
        
        user_obj = self.users[employee_username]
        product = self.inventory[item_name]

        # Business Rule: Check if we have enough stock items left
        if product.stock < quantity:
            return False, f"Incomplete Order: Only {product.stock} left in stock!"

        # Calculate Subtotal
        subtotal = product.price * quantity
        
        # Deduct stock using our encapsulation setter property
        product.stock -= quantity

        # Create order record and save to user history
        new_order = Order(item_name, quantity, subtotal)
        user_obj.completed_orders.append(new_order)

        return True, f"Order Complete! Total: ${subtotal:.2f}. (Remaining stock: {product.stock})"