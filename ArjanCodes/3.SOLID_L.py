# [S]INGLE RESPONSIBILITY - лучше много маленьких, чем ОДИН ГИГАНТСКИЙ КЛАСС
# [O]PEN/CLOSED - про наследование, а не модификацию
# [L]ISKOV SUBSTITUTION
# - инстанс родительского класса можно заменить на инстанс дочернего класса
# - через конкретизацию атрибутов(__init__ ) и методов в родительском классе так и в дочерних (чтобы избежать проблем,
# связанных с отсутствием унифицированного подхода обработке данных, т.е. для возможности перебора в цикле инстансов род и дочернего класса)
# [I]NTERFACE SEGREGATION
# - Класс потомка не должен зависеть от ненужных методов родительского класса.
# - Решение: создаём миксины — небольшие классы с отдельными методами, которые наследуем только тогда, когда они нужны.т.е. подключать только нужные интрфейсы
# [D]EPENDENCY INVERSION
# - dependancy injection - лучше в метод передавать другой класс, чем в классе использовать напрямую другой класс
# крепкий/добротный - принципы и правила - это все хорошо, но не стоит забывать о здравом смысле,
# т.е. нен стоит быть слишком педантичным и следовать всем правилам и довыдам

# --- Problem ---
# If u have objects in a programme,
# you should be able to replace those objects with instances OF THEIR SUBTYPES


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

class PayPalPaymentProcessor(PaymentProcessor):
    def pay(self, order, security_code):
        print("Processing PayPal payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"

processor = PayPalPaymentProcessor()
processor.pay(order, "2308")


# предположим что  PayPalPaymentProcessor не работает с security_code, а работает с emails
# и хоть если даже в оттрибут мы будем передавть email, то оно будет работать,
# НО в pay(self, order, security_code) будет фигурировать security_code, а не email аттрибут
# --- Solution ---
# 1. Убрать security_code аттрибут с АБС метода + назначить его при иницилизации, в зависимости от каждого типа платежки

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
    def pay(self, order):  # 1.убираем security_code с РОД метода
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):  # 2.добавляем инициализацию ОТЛИЧИМОГО аттрибута к каждому типу SUBCLASS
        self.security_code = security_code

    def pay(self, order):  # 1.убираем security_code с дочернего метода
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):  # 2.добавляем инициализацию ОТЛИЧИМОГО аттрибута к каждому типу SUBCLASS
        self.security_code = security_code

    def pay(self, order):   # 1.убираем security_code с дочернего метода
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class PayPalPaymentProcessor(PaymentProcessor):
    def __init__(self, email):  # 2.добавляем инициализацию ОТЛИЧИМОГО аттрибута к каждому типу SUBCLASS,
        # что в данном кейсу БУДЕТ УЖЕ email attr
        self.email = email

    def pay(self, order):  # 1.убираем security_code с дочернего метода
        print("Processing PayPal payment type")
        print(f"Verifying security code: {self.email}")
        order.status = "paid"

# processor = PayPalPaymentProcessor()
# processor.pay(order, "2308") # ТЕПЕРЬ вместо ПЕРЕДАЧИ ПАРМЕТРА в метод класса, мы его инциализируем КАК ПАРАМЕТР класса
processor = PayPalPaymentProcessor("hello_world@gmail.com")
processor.pay(order)

# как результат, все параметры ЧЕТКО ОПРЕДЕЛЕНЫ



