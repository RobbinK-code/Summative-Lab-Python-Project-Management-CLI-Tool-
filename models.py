import hashlib

class Person:
    """Base class to demonstrate Inheritance."""
    def __init__(self, name, role="Staff"):
        self.name = name
        self.role = role  # "Manager" (Admin) or "Staff" (User)

class Product:
    """Represents a bakery item like Cake, Bread, or Croissant."""
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self._stock = stock  # Underscore means protected (Encapsulation)

    # Getter: Safely view stock
    @property
    def stock(self):
        return self._stock

    # Setter: Prevents the bakery from having negative inventory
    @stock.setter
    def stock(self, value):
        if value < 0:
            raise ValueError("Stock levels cannot be negative!")
        self._stock = value

    def to_dict(self):
        return {"name": self.name, "price": self.price, "stock": self.stock}

class Order:
    """Handles individual client or counter orders."""
    def __init__(self, product_name, quantity, total_cost):
        self.product_name = product_name
        self.quantity = quantity
        self.total_cost = total_cost

    def to_dict(self):
        return {
            "product_name": self.product_name,
            "quantity": self.quantity,
            "total_cost": self.total_cost
        }

class User(Person):
    """Child class inheriting from Person to represent Bakery employees."""
    def __init__(self, name, password, role="Staff"):
        super().__init__(name, role)
        self.password_hash = self.hash_text(password)
        self.completed_orders = []  # Tracks orders processed by this employee

    def hash_text(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

    def check_password(self, password):
        return self.hash_text(password) == self.password_hash

    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "password_hash": self.password_hash,
            "completed_orders": [o.to_dict() for o in self.completed_orders]
        }