
# Общая реализация паттернов "Наблюдатель" и "Фабрика"

## Паттерн "Наблюдатель" (Observer)

**Общая реализация:**
1. **Издатель (Subject):** Управляет подпиской и оповещением наблюдателей.
2. **Наблюдатель (Observer):** Интерфейс с методом `update`, который вызывается при изменениях.
3. **Конкретные наблюдатели (Concrete Observers):** Классы, реализующие интерфейс наблюдателя.

**Пример кода:**

```python
class Observer:
    def update(self, message):
        pass

class ConcreteObserver(Observer):
    def update(self, message):
        print(f"Received message: {message}")

class Subject:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        self._observers.append(observer)

    def notify_observers(self, message):
        for observer in self._observers:
            observer.update(message)

subject = Subject()
observer1 = ConcreteObserver()
subject.register(observer1)
subject.notify_observers("Hello Observers!")
```

## Паттерн "Фабрика" (Factory)

**Общая реализация:**
1. **Класс Фабрика (Factory):** Определяет метод `factory_method` для создания объектов.
2. **Конкретные фабрики (Concrete Factories):** Реализуют фабричный метод, создавая конкретные продукты.
3. **Продукты (Products):** Объекты, созданные фабрикой, с общим интерфейсом.

**Пример кода:**

```python
class Product:
    def use(self):
        pass

class ConcreteProductA(Product):
    def use(self):
        print("Using Product A")

class Factory:
    def create_product(self, type):
        if type == "A":
            return ConcreteProductA()
        raise ValueError("Unknown product type")

factory = Factory()
product = factory.create_product("A")
product.use()
```

Эти паттерны способствуют улучшению структуры программ и повышению гибкости, делая системы более модульными и легко расширяемыми.
