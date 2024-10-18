import numpy as np

np.random.seed(42)

vector_1 = np.array([1, 2, 3, 4, 5])
vector_2 = np.array([2, 3, 4, 5, 6])

matrix_1 = np.random.randint(10, size=[3, 3])
matrix_2 = np.random.randint(10, size=[3, 3])

print(f"vector_1: {vector_1}")
print(f"vector_2: {vector_2}")
# vector_1: [1 2 3 4 5]  -> как правило используют вектор строку
# vector_2: [2 3 4 5 6]

print(f"matrix_1\n{matrix_1}")
print(f"matrix_2\n{matrix_2}")
# matrix_1
# [[6 3 7]
#  [4 6 9]
#  [2 6 7]]
# matrix_2
# [[4 3 7]
#  [7 2 5]
#  [4 1 7]

##############################################
###### скалярное произведение векторов ####### - сумма произведений соответвущих координат вектора
##############################################
# 1. func .dot()
print(np.dot(vector_1, vector_2))
# 70

# 2. перегруженный оператор @
print(vector_1 @ vector_2)
# 70

# 3. функция inner
print(np.inner(vector_1, vector_2))
# 70

# 4. Внешнее произведение - outer - (первый елемент vector_1, умножается на все елементы vector_2...
# потом 2й елемент умножается на все елементы vector_2... и т.д. и потом наоборот)
print(np.outer(vector_1, vector_2))
# [[ 2  3  4  5  6]
#  [ 4  6  8 10 12]
#  [ 6  9 12 15 18]
#  [ 8 12 16 20 24]
#  [10 15 20 25 30]]


###############################
###### Умножение матриц #######
###############################

# 1. func .dot()
print(np.dot(matrix_1, matrix_2))
# 2. перегруженный оператор @
print(matrix_1 @ matrix_2)
# 3. функция matmul
print(np.matmul(matrix_1, matrix_2))
# [[ 73  31 106]
#  [ 94  33 121]
#  [ 78  25  93]]
# 1. Рассчитаем первый элемент [0, 0] (первая строка matrix_1 на первый столбец matrix_2):
#  (6 * 4) + (3 * 7) + (7 * 4) = 24 + 21 + 28 = 73
# 2. Рассчитаем элемент [0, 1] (первая строка matrix_1 на второй столбец matrix_2):
# (6 * 3) + (3 * 2) + (7 * 1) = 18 + 6 + 7 = 31

##########################################
###### Умножение матриц на вектора ####### - принцип - строка на столбец
##########################################

np.random.seed(42)
vec_1 = np.array([1, 2, 3])
vec_2 = np.array([2, 3, 4, 5])
mat = np.random.randint(10, size=[4, 3])
print(mat)
# [[6 3 7]
#  [4 6 9]
#  [2 6 7]
#  [4 3 7]]

# 1. справа МАТРИЦА
print(np.dot(vec_2, mat))
print(vec_2 @ mat)
# [ 52  63 104]
# где, (2 * 6) + (3 * 4) + (4 * 2) + (5 * 4) = 12 + 12 + 8 + 20 = 52

# 2. справа Вектор
# print(np.dot(mat, vec_2))  # ValueError: shapes (4,3) and (4,) not aligned: 3 (dim 1) != 4 (dim 0)
# print(mat @ vec_2) # ValueError: shapes (4,3) and (4,) not aligned: 3 (dim 1) != 4 (dim 0)
# !!! нужно умножать НА ОДИННОКОВОЕ кол-во елементов
print(np.dot(mat, vec_1))
print(mat @ vec_1)
# [33 43 35 31]


# КАК ПЕРЕВЕТИ ВЕКТОР СТРОКУ В ВЕКТОР СТОЛБЕЦ?
print(f"vec_1 BEFORE {vec_1}")
# [1 2 3]
print(f"vec_1 AFTER \n{vec_1[:, np.newaxis]}")
# [[1]
#  [2]
#  [3]]
