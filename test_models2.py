import pytest
from models import Product, OrderItem, Order


def test_product_creation():
    p = Product("P001", "Apple", 1.50, 100, 10)
    assert p.product_id == "P001"
    assert p.name == "Apple"
    assert p.price == 1.50
    assert p.stock_quantity == 100
    assert p.reorder_level == 10

def test_update_price():
    p = Product("P001", "Apple", 1.50, 100, 10)
    p.update_price(2.00)
    assert p.price == 2.00

def test_update_price_negative_raises_error():
    p = Product("P001", "Apple", 1.50, 100, 10)
    with pytest.raises(ValueError):
        p.update_price(-5)

def test_update_stock_increase():
    p = Product("P001", "Apple", 1.50, 50, 10)
    p.update_stock(20)
    assert p.stock_quantity == 70

def test_update_stock_decrease():
    p = Product("P001", "Apple", 1.50, 50, 10)
    p.update_stock(-10)
    assert p.stock_quantity == 40

def test_update_stock_below_zero_raises_error():
    p = Product("P001", "Apple", 1.50, 5, 10)
    with pytest.raises(ValueError):
        p.update_stock(-10)

def test_is_low_stock_true():
    p = Product("P001", "Apple", 1.50, 5, 10)
    assert p.is_low_stock() == True

def test_is_low_stock_false():
    p = Product("P001", "Apple", 1.50, 50, 10)
    assert p.is_low_stock() == False

def test_product_to_dict():
    p = Product("P001", "Apple", 1.50, 100, 10, "Fruit")
    d = p.to_dict()
    assert d["product_id"] == "P001"
    assert d["name"] == "Apple"
    assert d["price"] == 1.50

def test_product_from_dict():
    data = {
        "product_id": "P001",
        "name": "Apple",
        "price": 1.50,
        "stock_quantity": 100,
        "reorder_level": 10,
        "category": "Fruit",
    }
    p = Product.from_dict(data)
    assert p.name == "Apple"
    assert p.stock_quantity == 100

def test_orderitem_subtotal():
    p = Product("P001", "Apple", 2.00, 100, 10)
    item = OrderItem(p, 5)
    assert item.subtotal() == 10.00

def test_orderitem_locks_price():
    p = Product("P001", "Apple", 2.00, 100, 10)
    item = OrderItem(p, 3)
    p.update_price(5.00)
    assert item.unit_price == 2.00

def test_order_creation():
    o = Order("ORD-001", "Victor")
    assert o.order_id == "ORD-001"
    assert o.customer_name == "Victor"
    assert o.status == "pending"
    assert o.items == []

def test_add_item_to_order():
    p = Product("P001", "Apple", 2.00, 100, 10)
    o = Order("ORD-001", "Victor")
    o.add_item(p, 3)
    assert len(o.items) == 1
    assert o.items[0].quantity == 3

def test_add_same_item_merges():
    p = Product("P001", "Apple", 2.00, 100, 10)
    o = Order("ORD-001", "Victor")
    o.add_item(p, 3)
    o.add_item(p, 2)
    assert len(o.items) == 1
    assert o.items[0].quantity == 5

def test_add_item_zero_quantity_raises_error():
    p = Product("P001", "Apple", 2.00, 100, 10)
    o = Order("ORD-001", "Victor")
    with pytest.raises(ValueError):
        o.add_item(p, 0)

def test_order_total():
    p1 = Product("P001", "Apple", 2.00, 100, 10)
    p2 = Product("P002", "Banana", 1.00, 100, 10)
    o = Order("ORD-001", "Victor")
    o.add_item(p1, 3)
    o.add_item(p2, 4)
    assert o.total() == 10.00

def test_set_status_valid():
    o = Order("ORD-001", "Victor")
    o.set_status("confirmed")
    assert o.status == "confirmed"

def test_set_status_invalid_raises_error():
    o = Order("ORD-001", "Victor")
    with pytest.raises(ValueError):
        o.set_status("shipped")

def test_order_to_dict():
    p = Product("P001", "Apple", 2.00, 100, 10)
    o = Order("ORD-001", "Victor")
    o.add_item(p, 2)
    d = o.to_dict()
    assert d["order_id"] == "ORD-001"
    assert d["status"] == "pending"
    assert len(d["items"]) == 1