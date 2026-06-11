
from datetime import datetime
class Product:
    def __init__(self, product_id, name, price, stock_quantity, reorder_level, category="General"):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity
        self.reorder_level = reorder_level
        self.category = category

    def update_price(self, new_price):
        if new_price < 0:
            raise ValueError("Price cannot be negative.")
        self.price = new_price

    def update_stock(self, quantity_change):
        new_qty = self.stock_quantity + quantity_change
        if new_qty < 0:
            raise ValueError(f"Not enough stock for '{self.name}'.")
        self.stock_quantity = new_qty

    def is_low_stock(self):
        return self.stock_quantity <= self.reorder_level
    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock_quantity": self.stock_quantity,
            "reorder_level": self.reorder_level,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            product_id=data["product_id"],
            name=data["name"],
            price=data["price"],
            stock_quantity=data["stock_quantity"],
            reorder_level=data["reorder_level"],
            category=data["category"],
        )

    def __repr__(self):
        return f"Product(id={self.product_id}, name={self.name}, price=${self.price:.2f}, stock={self.stock_quantity})"


class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.unit_price = product.price 

    def subtotal(self):
        return self.unit_price * self.quantity

    def to_dict(self):
        return {
            "product_id": self.product.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
        }

class Order:
    STATUS_OPTIONS = ("pending", "confirmed", "cancelled")

    def __init__(self, order_id, customer_name):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = []               
        self.status = "pending"      
        self.created_at = datetime.now().isoformat()

    def add_item(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        for item in self.items:
            if item.product.product_id == product.product_id:
                item.quantity += quantity
                return
        self.items.append(OrderItem(product, quantity))

    def total(self):
        return sum(item.subtotal() for item in self.items)

    def set_status(self, status):
        if status not in self.STATUS_OPTIONS:
            raise ValueError(f"'{status}' is not a valid status.")
        self.status = status

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "status": self.status,
            "created_at": self.created_at,
            "items": [item.to_dict() for item in self.items],
        }

    def __repr__(self):
        return f"Order(id={self.order_id}, customer={self.customer_name}, status={self.status}, total=${self.total():.2f})"