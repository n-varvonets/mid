# [S]INGLE RESPONSIBILITY
# [O]PEN/CLOSED
# [L]ISKOV SUBSTITUTION
# [I]NTERFACE SEGREGATION
# [D]EPENDENCY INVERSION


# --- Problem ---

class Order:
    items = []
    quantities = []
    prices = []
    status = "Open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total

    def pay(self, payment_type, security_code):
        if payment_type == "debit":
            print("Processing debit payment type")
            print(f"Verifying security code: {security_code}")
            self.status = "paid"
        elif payment_type == "credit":
            print("Processing credit payment type")
            print(f"Verifying security code: {security_code}")
            self.status = "paid"
        else:
            raise Exception(f"Unknown payment type: {payment_type}")


order = Order()
order.add_item("keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 7)

print(order.total_price())
order.pay("debit", "2308")

# Single responsibility
# 1. add_items and total price - it's part of order, but
# method pay shouldn't be a part of order.
# 2. to resolve it we have to putting this method into separate class. Why?
# If later we want to add another payments types Like Bitcoin, Apple pay - we don't neet to chang Order class

# --- Solution ---
class Order:
    items = []
    quantities = []
    prices = []
    status = "Open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total


class PaymentProcessor:
    def pay_debit(self, order, security_code):   # exclude payment_type attr, but we have to change order.status
        print("Processing debit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"

    def pay_credit(self, order, security_code):   # exclude payment_type attr, but we have to change order.status
        print("Processing credit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"

order = Order()
order.add_item("keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 7)

print(order.total_price())
# order.pay("debit", "2308")  # useless
processor = PaymentProcessor()
processor.pay_debit(order, "2308")

# As result, Order class has one responibility as PaymentProcessor