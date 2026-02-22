from app import Customer, Product, Order, OrderLine

def test_order_price():
    c = Customer("Test", 0.10)
    order = Order(c)
    order.addOrderLine(OrderLine(Product("Laptop", 1000.0), 1))
    order.addOrderLine(OrderLine(Product("Mouse", 50.0), 2))
    assert order.calculateBasePrice() == 1100.0
    assert order.calculateDiscounts() == 110.0
    assert order.calculatePrice() == 990.0