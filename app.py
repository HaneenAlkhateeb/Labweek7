from flask import Flask, render_template, request

# --- UML classes ---
class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def getprice(self) -> float:
        return self.price


class Customer:
    def __init__(self, name: str, discount_rate: float):
        self.name = name
        self.discount_rate = discount_rate

    def getDiscountInfo(self) -> float:
        return self.discount_rate


class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def getQuantity(self) -> int:
        return self.quantity

    def getproduct(self) -> Product:
        return self.product


class Order:
    def __init__(self, customer: Customer):
        self.customer = customer
        self.orderlines: list[OrderLine] = []

    def addOrderLine(self, orderline: OrderLine) -> None:
        self.orderlines.append(orderline)

    def calculateBasePrice(self) -> float:
        return sum(
            line.getproduct().getprice() * line.getQuantity()
            for line in self.orderlines
        )

    def calculateDiscounts(self) -> float:
        return self.calculateBasePrice() * self.customer.getDiscountInfo()

    def calculatePrice(self) -> float:
        return self.calculateBasePrice() - self.calculateDiscounts()


# --- Web UI ---
app = Flask(__name__)

# A tiny “catalog”
PRODUCTS = {
    "Laptop": 1000.0,
    "Mouse": 50.0,
    "Keyboard": 80.0,
}

@app.get("/")
def home():
    return render_template("index.html", products=PRODUCTS, result=None)

@app.post("/calculate")
def calculate():
    customer_name = request.form.get("customer_name", "Student")
    discount_rate = float(request.form.get("discount_rate", "0.10"))

    product_name = request.form.get("product_name", "Laptop")
    quantity = int(request.form.get("quantity", "1"))

    customer = Customer(customer_name, discount_rate)
    order = Order(customer)

    product = Product(product_name, PRODUCTS[product_name])
    order.addOrderLine(OrderLine(product, quantity))

    result = {
        "base": order.calculateBasePrice(),
        "discount": order.calculateDiscounts(),
        "final": order.calculatePrice(),
        "product": product_name,
        "qty": quantity,
        "customer": customer_name,
        "rate": discount_rate,
    }
    return render_template("index.html", products=PRODUCTS, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
