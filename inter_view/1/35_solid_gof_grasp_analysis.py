class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def calculate_discount(self, discount_percentage):
        # Метод расчета скидки остается в продукте, так как он касается цены продукта.
        return self.price * (1 - discount_percentage / 100)

class ShoppingCart:
    # Это НЕ нарушает принципы SOLID, так как:
    # 1. Корзина отвечает за управление продуктами (SRP), а клиент — за взаимодействие с корзиной.
    # 2. Метод корзины можно расширять, не нарушая других классов (OCP).
    # 3. Принцип инверсии зависимостей (DIP) соблюден, так как корзина не зависит от клиента напрямую.

    def __init__(self):
        # Корзина управляет списком продуктов и общим ценником.
        self.products = []
        self.total_price = 0

    def add_product(self, product):
        # Добавление продуктов в корзину — это ответственность корзины, а не клиента.
        # Это не нарушает SRP, так как корзина управляет продуктами.
        self.products.append(product)
        self.total_price += product.price

    def remove_product(self, product):
        # Удаление продуктов из корзины — также задача корзины, а не клиента.
        if product in self.products:
            self.products.remove(product)
            self.total_price -= product.price

    def apply_discount(self, discount_percentage):
        # Применение скидки к продуктам — это задача корзины, так как она управляет всеми продуктами.
        for product in self.products:
            product.price = product.calculate_discount(discount_percentage)
            self.total_price -= product.price

    def checkout(self, customer):
        # Создание заказа с продуктами — это логика корзины.
        order = Order(customer, self.products)
        order.place_order()

class Order:
    def __init__(self, customer, products):
        # Продукты не должны быть в заказе, потому что это результат действий клиента, а не сам процесс управления.
        self.customer = customer
        self.products = products

    def place_order(self):
        print("Order placed successfully!")


class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        # Продукты должны управляться клиентом, потому что он принимает решение, что добавить или удалить из корзины.

        # КЛИЕНТ ВЛАДЕЕТ ЗАКАЗАМИ ИЛИ ЗАКАЗІ ВЛАДЕЮТ КЛИЕНТОМ?

    def add_product_to_cart(self, product, shopping_cart):
        shopping_cart.add_product(product)

    def remove_product_from_cart(self, product, shopping_cart):
        shopping_cart.remove_product(product)

    def checkout(self, shopping_cart):
        shopping_cart.checkout(self)

    # Методы `add_product_to_cart` и `remove_product_from_cart` НЕ должны быть у клиента, так как это нарушает SRP.
    # Клиент не должен управлять продуктами в корзине напрямую — это задача корзины (ShoppingCart).
    # Клиент лишь вызывает эти действия через методы корзины, но сами операции добавления и удаления должны
    # быть инкапсулированы в корзине.


###№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

class Order:
    # SRP: Order class is responsible only for order-related logic (product management and order placement).
    # GRASP: Order is created and managed by Customer, following the Creator principle.
    def __init__(self, products):
        self.products = products

    # Information Expert (GRASP): Order is responsible for placing itself, since it knows the products.
    def place_order(self):
        print("Order placed successfully!")

class Customer:
    # SRP: Customer class manages customer information and orders.
    # GRASP: The Customer class follows the Creator principle, as it is responsible for creating and managing Orders.
    def __init__(self, name, email):
        self.name = name
        self.email = email
        # Customer now holds a list of orders, separating responsibilities.
        self.orders = []


# Example usage:
# customer = Customer(name="John Doe", email="john@example.com")
# customer.add_product_to_cart(product, shopping_cart)
# customer.checkout(shopping_cart)



