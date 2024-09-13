

### Что такое comprehensions (list, generator, set, dictionary) в Python?

**Comprehensions** — это сокращенная запись для создания списков, множеств, словарей и генераторов на основе существующих последовательностей (например, списков, range и т.д.). Они позволяют сделать код более лаконичным и читаемым.

#### 1. **List comprehension** (генератор списка):
Синтаксис для создания списка на основе существующей последовательности.

Пример:
```python
numbers = [1, 2, 3, 4, 5]
squares = [n ** 2 for n in numbers]  # [1, 4, 9, 16, 25]
```

#### 2. **Set comprehension** (генератор множества):
Создает множество, автоматически убирая дубликаты.

Пример:
```python
numbers = [1, 2, 2, 3, 4, 4]
unique_squares = {n ** 2 for n in numbers}  # {1, 4, 9, 16}
```

#### 3. **Dictionary comprehension** (генератор словаря):
Создает словарь, позволяя задать ключ и значение.

Пример:
```python
numbers = [1, 2, 3, 4]
squares_dict = {n: n ** 2 for n in numbers}  # {1: 1, 2: 4, 3: 9, 4: 16}
```

#### 4. **Generator comprehension** (генератор):
Создает генератор, который лениво вычисляет значения по мере необходимости, экономя память.

Пример:
```python
numbers = [1, 2, 2, 3, 4, 4]
unique_squares = {n ** 2 for n in numbers}
squares_gen = (n ** 2 for n in numbers)
print(unique_squares)  # {16, 1, 4, 9}
print(squares_gen)  # <generator object <genexpr> at 0x000001B4EB1036B0>
print(next(squares_gen))  # 1
print(next(squares_gen))  # 4
print(next(squares_gen))  # 4
```

### Итератор это генератор? А генератор итератор?

- **Итератор** — это объект, который реализует метод `__iter__()` и `__next__()`.  <u>**Любой объект, который реализует эти два метода, считается итератором.**</u>
  
- **Генератор** — это частный случай итератора. Генераторы автоматически реализуют методы итератора и создаются при помощи выражений `yield` или через **generator comprehension**.

Поэтому: **любой генератор — это итератор, но не любой итератор является генератором**.

```python
# Примером итератора
numbers = [1, 2, 3]
it = iter(numbers)

print(it) # <list_iterator object at 0x0000021587163460>
print(next(it))  # 1
print(next(it))  # 2
print(next(it))  # 3

# Пример генератора:
def my_generator():
    yield 1
    yield 2
    yield 3

gen = my_generator()
print(gen)  # <generator object my_generator at 0x0000021586DA4880>
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
```