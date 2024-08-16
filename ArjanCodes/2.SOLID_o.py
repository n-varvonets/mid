# [S]INGLE RESPONSIBILITY
# [O]PEN/CLOSED
# [L]ISKOV SUBSTITUTION
# [I]NTERFACE SEGREGATION
# [D]EPENDENCY INVERSION

# --- Problem ---
# if we want to add extra payment_method as Apple_pay whatever.. we have to modify class PaymentProcessor,
# so that violets the open/closed principle
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

# --- Solution ---
# Open for extension and closed for modification.
# So we have to create subclass for each new payment type

from abc import ABC, abstractmethod

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


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order, security_code):
        pass


class DebitPaymentProcessor(PaymentProcessor):
    def pay(self, order, security_code):
        print("Processing debit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"

class DebitPaymentProcessor(PaymentProcessor):
    def pay(self, order, security_code):
        print("Processing credit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"

order = Order()
order.add_item("keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 7)

print(order.total_price())
processor = DebitPaymentProcessor()
processor.pay(order, "2308")

# and now we can add ONE EXTRA another payment type like PayPal - WE DON'T HAVE TO CHANGE class PaymentProcessor(ABC) anymore
class PayPalPaymentProcessor(PaymentProcessor):
    def pay(self, order, security_code):
        print("Processing PayPal payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"

processor = PayPalPaymentProcessor()
processor.pay(order, "2308")