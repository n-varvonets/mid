# Базовый класс наблюдателя с абстрактным методом update
class Observer:
    # Метод, который будет вызван для обновления состояния наблюдателя
    def update(self, message):
        pass

# Конкретный наблюдатель, который реализует метод update
class ConcreteObserver(Observer):
    # Переопределение метода update для получения сообщений
    def update(self, message):
        print(f"Received message: {message}")

# Субъект, за которым наблюдают
class Subject:
    def __init__(self):
        # Список всех зарегистрированных наблюдателей
        self._observers = []

    # Метод для регистрации наблюдателей
    def register(self, observer):
        self._observers.append(observer)

    # Метод для уведомления всех наблюдателей
    def notify_observers(self, message):
        for observer in self._observers:
            observer.update(message)

# Создание субъекта
subject = Subject()

# Создание наблюдателя
observer1 = ConcreteObserver()

# Регистрация наблюдателя в субъекте
subject.register(observer1)

# Уведомление наблюдателей сообщением
subject.notify_observers("Hello Observers!")


### ----------- Fabric ---------- ###

# Абстрактный класс Продукта
# Абстрактный продукт представляет интерфейс для всех конкретных продуктов.
# Это позволяет в будущем добавлять новые типы продуктов без изменения клиентского кода.
class Product:
    def operation(self):
        pass

# Конкретный Продукт 1
# Это одна из реализаций абстрактного продукта.
class ConcreteProduct1(Product):
    def operation(self):
        return "Operation of ConcreteProduct1"

# Конкретный Продукт 2
class ConcreteProduct2(Product):
    def operation(self):
        return "Operation of ConcreteProduct2"

# Класс Фабрики, который создает Продукты
# Паттерн Фабрика используется для создания объектов без указания точного класса, который будет создан.
# Это позволяет скрыть логику создания объектов и делать код более гибким.
class ProductFactory:
    @staticmethod
    def create_product(type):
        if type == "product1":
            return ConcreteProduct1()
        elif type == "product2":
            return ConcreteProduct2()
        else:
            raise ValueError("Unknown product type")

# Пример использования паттерна Фабрика
factory = ProductFactory()

# Создаем продукт 1
product1 = factory.create_product("product1")
print(product1.operation())  # Output: Operation of ConcreteProduct1

# Создаем продукт 2
product2 = factory.create_product("product2")
print(product2.operation())  # Output: Operation of ConcreteProduct2

