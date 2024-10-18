import numpy as np

# Создание двумерного массива
np_array = np.array([
    [1, 2, 3],
    [2, 3, 4],
    [3, 4, 5]
])

# количество Лосей
np_array.ndim  # - в данном масиве всего 2 осей

# число елементов в массиве
np_array.size  # 9 елемнетов в массисве 3х3

# Изменение формы массива на (9, 1)
np_array.shape = (9, 1)
print(np_array.shape)
print(np_array)

# Установка типа данных int8
np_array = np_array.astype(np.int8)

# Проверка после изменения типа данных
print(np_array.dtype)
print(np_array)

#### MAT
# print(np.mat([1, 2, 3, 4, 5]))
# print(np.asmatrix([1, 2, 3, 4, 5]))
# print(np.diag([1, 2, 3, 4, 5]))

# print(np.diagflat([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

# print(np.eye(4))  # Создает единичную матрицу размером 4x4
# print(np.eye(4, 6))  # Создает единичную матрицу размером 4x6

# print(np.tri(4, 6))

matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# print(np.tril(matrix))
# [[1 0 0]
#  [4 5 0]
#  [7 8 9]]

print(np.triu(matrix))
# [[1 2 3]
#  [0 5 6]
#  [0 0 9]]
