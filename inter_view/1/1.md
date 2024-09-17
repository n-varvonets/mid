### Методы `__new__` и `__init__`

- **`__new__`** всегда вызывается первым при создании объекта. Этот метод отвечает за выделение памяти и создание экземпляра класса.

- **`__init__`** вызывается после `__new__` и предназначен для инициализации созданного объекта.

- Если метод `__new__` не переопределяется, его поведение скрыто, и можно ошибочно подумать, что сначала вызывается `__init__`.

- Таким образом, `__new__` всегда выполняется первым, но это может быть неочевидно, если он явно не переопределен.


```python
class Base:
    def __new__(cls):
        print("Base __new__")
        return super().__new__(cls)
    
    def __init__(self):
        print("Base __init__")

class Derived(Base):
    def __init__(self):
        print("Derived __init__")

obj = Derived()

# Base __new__
# Derived __init__

```

```python
class Base:
    def __new__(cls):
        print("Base __new__")
        return super().__new__(cls)

    def __init__(self):
        print("Base __init__")


class Derived(Base):

    def __new__(cls):
        print("Derived __new__")
        return super().__new__(cls)
    
    def __init__(self):
        print("Derived __init__")


obj = Derived()

# Derived __new__
# Base __new__
# Derived __init__
```