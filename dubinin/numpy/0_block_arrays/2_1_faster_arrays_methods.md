# Работа с массивами в NumPy: np.empty, np.ones, np.ones_like, np.zeros, np.zeros_like, np.full, np.full_like, np.diag, np.diagflat, np.eye, np.identity, np.tri, np.tril

## Использование функций для создания массивов

### np.empty

```python
np.empty(7)
```

- **Функция**: `np.empty`
- **Описание**: Инициализация массива из 7 элементов с неопределёнными значениями.
- **Типичный вывод**: `array([2.8750571e-322, 0.0000000e+000, ...])`
    - Значения зависят от состояния памяти.

### np.ones

```python
np.ones([3, 3, 2])
```

- **Функция**: `np.ones`
- **Описание**: Создаёт массив, заполненный единицами, с формой (3, 3, 2).
- **Вывод**:

```
array([[[1., 1.],
        [1., 1.],
        [1., 1.]],

       [[1., 1.],
        [1., 1.],
        [1., 1.]],

       [[1., 1.],
        [1., 1.],
        [1., 1.]]])
```

### np.ones_like

```python
np.ones_like(np_array, dtype=np.int8)
```

- **Функция**: `np.ones_like`
- **Описание**: Создаёт массив той же формы, что и `np_array`, но заполненный единицами и с типом данных `int8`.
- **Вывод**:

```
array([[[1, 1],
        [1, 1]],

       [[1, 1],
        [1, 1]],

       [[1, 1],
        [1, 1]]], dtype=int8)
```

### np.zeros

```python
np.zeros([3, 2, 3])
```

- **Функция**: `np.zeros`
- **Описание**: Создаёт массив, заполненный нулями, с формой (3, 2, 3).
- **Вывод**:

```
array([[[0., 0., 0.],
        [0., 0., 0.]],

       [[0., 0., 0.],
        [0., 0., 0.]],

       [[0., 0., 0.],
        [0., 0., 0.]]])
```

### np.zeros_like

```python
print(np.zeros_like(np_array))
```

- **Функция**: `np.zeros_like`
- **Описание**: Создаёт массив той же формы, что и `np_array`, но все элементы инициализируются нулями.
- **Вывод**:

```
array([[[0., 0.],
        [0., 0.]],

       [[0., 0.],
        [0., 0.]],

       [[0., 0.],
        [0., 0.]]])
```

### np.full

```python
np.full([3, 2, 3], 7)
```

- **Функция**: `np.full`
- **Описание**: Создаёт массив с формой (3, 2, 3), заполненный значением 7.
- **Вывод**:

```
array([[[7, 7, 7],
        [7, 7, 7]],

       [[7, 7, 7],
        [7, 7, 7]],

       [[7, 7, 7],
        [7, 7, 7]]])
```

### np.full_like

```python
print(np.full_like(np_array, 7, dtype=np.int32))
```

- **Функция**: `np.full_like`
- **Описание**: Создаёт массив той же формы, что и `np_array`, но все элементы инициализируются значением 7 и типом
  данных `int32`.
- **Вывод**:

```
array([[[7, 7],
        [7, 7]],

       [[7, 7],
        [7, 7]],

       [[7, 7],
        [7, 7]]], dtype=int32)
```

---

## Используемые методы: np.arange, np.mat, np.diag

## Массивы из числовых диапазонов

### np.arange

```python
np.arange(7)  # Создает массив из 7 элементов, начиная с 0 до 6
```

**Описание**: Создает одномерный массив с числами от 0 до указанного числа, не включая его.

```python
np.arange(7, 17)  # Создает массив чисел от 7 до 16
```

**Описание**: Создает одномерный массив с числами от начального до конечного значения, не включая последнее.

```python
np.arange(7, 17, 3)  # Создает массив чисел от 7 до 16 с шагом 3
```

**Описание**: Создает одномерный массив с указанным шагом между значениями.

```python
np.arange(7, 10, 0.5)  # Создает массив чисел от 7 до 9.5 с шагом 0.5
```

**Описание**: Позволяет создать массив с дробным шагом.

## Матрицы - прямоугольная таблица чисел с 2мя осями

### np.mat

```python
np.mat([1, 2, 3, 4, 5])  # Преобразует список в матрицу ИЗ ОДНОЙ СТРОКИ - expired, new one below
print(np.asmatrix([1, 2, 3, 4, 5]))  # [[1 2 3 4 5]] - БУДЕТ ДВУМЕРНІЙ МАССИВ (ДВЕ СКОБКИ), т.к. это матрица
np.mat([[1, 2, 3], [4, 5, 6]])  # Создает матрицу из списка списков
```

**Описание**: Создает двумерную матрицу из вложенных списков.
---

### np.diag - преобразует значения в диогональную матрицу,

```python
# 1. передать список - на главной диоганале которой, лежат главные елементы этого списка
np.diag([1, 2, 3, 4, 5])  # Создает диагональную матрицу
# [[1 0 0 0 0]
#  [0 2 0 0 0]
#  [0 0 3 0 0]
#  [0 0 0 4 0]
#  [0 0 0 0 5]]

# 1. передать список - вернет значенияя диогонали матрицы
np.diag([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])  # вернет значения
# [1, 5, 9]
```

---

### np.diagflat - лююой массив превратит в диогональную матрицу

```python
np.diagflat([[1, 2, 3], [4, 5, 6], [7, 8, 9]])  # Создает диагональную матрицу из элементов входного массива

# [[1 0 0 0 0 0 0 0 0]
# [0 2 0 0 0 0 0 0 0]
# [0 0 3 0 0 0 0 0 0]
# [0 0 0 4 0 0 0 0 0]
# [0 0 0 0 5 0 0 0 0]
# [0 0 0 0 0 6 0 0 0]
# [0 0 0 0 0 0 7 0 0]
# [0 0 0 0 0 0 0 8 0]
# [0 0 0 0 0 0 0 0 9]]
```

**Описание**: Создает матрицу, где элементы входного массива располагаются на диагонали.
---

### np.eye - Создает квадратную единичную матрицу (матрицу идентичности) размером n x n.

```python
np.eye(4)  # Создает единичную матрицу размером 4x4
# [[1. 0. 0. 0.]
# [0. 1. 0. 0.]
# [0. 0. 1. 0.]
# [0. 0. 0. 1.]]

np.eye(4, 6)  # Создает единичную матрицу размером 4x6
# [[1. 0. 0. 0. 0. 0.]
# [0. 1. 0. 0. 0. 0.]
# [0. 0. 1. 0. 0. 0.]
# [0. 0. 0. 1. 0. 0.]]
```

---

### np.identity

```python
np.identity(5)  # Создает единичную матрицу размером 5x5
```

**Описание**: Создает квадратную единичную матрицу размером n x n, аналогично `np.eye`.
---

### np.tri

```python
np.tri(4, 6)  # Создает треугольную матрицу с единицами ниже и включая диагональ
# [[1. 0. 0. 0. 0. 0.]
# [1. 1. 0. 0. 0. 0.]
# [1. 1. 1. 0. 0. 0.]
# [1. 1. 1. 1. 0. 0.]]
```

---

### np.tril - преобразует матрицу так, что все элементы выше главной диагонали обнуляются.

```python
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Применение np.tril
print(np.tril(matrix))
# [[1 0 0]
#  [4 5 0]
#  [7 8 9]]
```

---

### np.triu преобразует матрицу так, что все элементы ниже главной диагонали обнуляются.

```python
# Применение np.triu
print(np.triu(matrix))
# [[1 2 3]
#  [0 5 6]
#  [0 0 9]]
```



