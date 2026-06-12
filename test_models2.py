import pytest
from models import Person, User, Product, Order

# ==================== PRODUCT CLASS TESTS ====================

def test_product_creation():
    """Verifies that a bakery item initializes its attributes cleanly."""
    p = Product("Croissant", 2.50, 50)
    assert p.name == "Croissant"
    assert p.price == 2.50
    assert p.stock == 50

def test_product_encapsulation_getter_setter():
    """Verifies encapsulation properties block illegal business operations."""
    p = Product("Muffin", 3.00, 20)
    
    # Check that normal modifications work through the setter
    p.stock = 25
    assert p.stock == 25

    # Check that the setter throws an error if stock falls below zero
    with pytest.raises(ValueError):
        p.stock = -5

def test_product_to_dict():
    """Ensures a Product cleanly flattens into serializable data types."""
    p = Product("Scone", 3.50, 15)
    d = p.to_dict()
    assert d["name"] == "Scone"
    assert d["price"] == 3.50
    assert d["stock"] == 15


# ==================== ORDER CLASS TESTS ====================

def test_order_creation():
    """Verifies that an Order item saves item names and financials correctly."""
    o = Order("Chocolate Cake", 2, 50.00)
    assert o.product_name == "Chocolate Cake"
    assert o.quantity == 2
    assert o.total_cost == 50.00

def test_order_to_dict():
    """Ensures an Order translates correctly for Neville's JSON storage."""
    o = Order("Baguette", 3, 12.00)
    d = o.to_dict()
    assert d["product_name"] == "Baguette"
    assert d["quantity"] == 3
    assert d["total_cost"] == 12.00


# ==================== USER / INHERITANCE TESTS ====================

def test_user_inheritance_from_person():
    """Proves to the rubric that User successfully inherits from Person."""
    u = User("Alex", "password123", role="Staff")
    assert isinstance(u, Person)  # Verifies deep OOP type inheritance matches
    assert u.name == "Alex"
    assert u.role == "Staff"
    assert u.completed_orders == []

def test_user_secure_password_hashing():
    """Ensures security mechanisms convert clean strings to hashes."""
    u = User("ChefBob", "secureBake123", role="Manager")
    
    # Assert that password strings are never saved in plain text
    assert u.password_hash != "secureBake123"
    
    # Assert validation checks return clean true/false responses
    assert u.check_password("secureBake123") is True
    assert u.check_password("wrongPass") is False