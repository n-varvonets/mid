import numpy as np

# 1.a. Добавление новых осей
np_array = np.array([[1, 2, 3], [4, 5, 6]])
expanded_array = np.expand_dims(np_array, axis=0)  # Добавление новой оси в начале массива
print("Добавленная новая ось в начале массива:\n")
print(expanded_array)
print("Форма массива после добавления оси:\n", expanded_array.shape)
# Вывод:
# [[[1 2 3]
#   [4 5 6]]]
# Форма массива после добавления оси: (1, 2, 3)

# 1.b. Изменения в одном представлении массива отражаются в другом
expanded_array[0, 0, 0] = 100
print("Исходный массив после изменения в expanded_array:\n")
print(np_array)  # Исходный массив также изменится, т.к. expanded_array является представлением исходного массива
# Вывод:
# [[100   2   3]
#  [  4   5   6]]
print("expanded_array такой же \n", expanded_array)
# Вывод:
# [[100   2   3]
#  [  4   5   6]]

# 1.1. Добавление новой оси в конец
new_array = np_array[np.newaxis, :]
print(f"Размер массива new_array после добавления оси в конец:\n {new_array.shape}")
# Вывод:
# Размер массива new_array после добавления оси в конец: (1, 3, 4)

# 1.2. Добавление новой оси в начало
new_array_2 = np_array[:, np.newaxis]
print(f"Размер массива new_array_2 после добавления оси в начало:\n {new_array_2.shape}")
# Вывод:
# Размер массива new_array_2 после добавления оси в начало: (3, 1, 4)

# 1.3. Добавление новой оси между существующими осями
new_array_3 = np_array[:, :, np.newaxis]
print(f"Размер массива new_array_3 после добавления оси между существующими осями:\n {new_array_3.shape}")
# Вывод:
# Размер массива new_array_3 после добавления оси между существующими осями: (3, 4, 1)

# 1.4. Альтернативный синтаксис для добавления новой оси в начало с использованием ...
new_array_4 = np_array[..., np.newaxis]
print(f"Размер массива new_array_4 после добавления оси в конец с использованием ...:\n {new_array_4.shape}")
# Вывод:
# Размер массива new_array_4 после добавления оси в конец с использованием ...: (3, 4, 1)

############################
###### Удаление осей #######
############################

# 2. Удаление оси размером 1 с использованием np.squeeze
# Создание массива с дополнительной осью размером 1
array_with_single_dimension = np.array([[[1, 2, 3], [4, 5, 6]]])
print("Форма массива до применения squeeze:\n", array_with_single_dimension.shape,
      "и сам массив ДО с пустой вложенностью:\n",
      array_with_single_dimension)
# Вывод:
# Форма массива до применения squeeze: (1, 2, 3)

# Применение np.squeeze для удаления избыточной оси
squeezed_array = np.squeeze(array_with_single_dimension)
print("Форма массива после применения squeeze:\n", squeezed_array.shape)
# Вывод:
# Форма массива после применения squeeze: (2, 3)
print("Сам массив уже без удной вложенности:\n", squeezed_array)

###################################
###### Объединение массивов #######
###################################

# 1. EXTEND. Объединение массивов по первой оси(ГОРИЗОНТАЛЬНОЙ ОСИ) с использованием np.hstack - принимает кортеж или список массивов и объединяет их вдоль горизонтальной оси,
# # т.е., увеличивает количество столбцов. Все входные массивы должны иметь одинаковое количество строк.
# Создание нескольких массивов
arr_1 = np.array([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
arr_2 = np.array([[4, 5, 6], [5, 6, 7], [6, 7, 8]])
# arr_3 = np.array([[7, 8, 9, 10], [8, 9, 10, 11], [9, 10, 11]])  - будет ошибка, т.к. нужно 4хмерный,  а не 3х ([9, 10, 11])
arr_3 = np.array([[7, 8, 9, 10], [8, 9, 10, 11], [9, 10, 11, 12]])

print(f"3 оси на последнем = arr_1.shape={arr_1.shape}", arr_1, sep="\n", end="\n")
print(f"3 оси на последнем = arr_2.shape={arr_2.shape}", arr_2, sep="\n", end="\n")
print(f"4 оси на последнем = arr_3.shape={arr_3.shape}", arr_3, sep="\n", end="\n")
# 3 оси на последнем = arr_1.shape=(3, 3)
# [[1 2 3]
#  [2 3 4]
#  [3 4 5]]
# 3 оси на последнем = arr_2.shape=(3, 3)
# [[4 5 6]
#  [5 6 7]
#  [6 7 8]]
# 4 оси на последнем = arr_3.shape=(3, 4)
# [[ 7  8  9 10]
#  [ 8  9 10 11]
#  [ 9 10 11 12]]

# EXTEND: Объединение массивов по первой оси (там где 3 елемента) - передаем список с массивами
hstack_array = np.hstack((arr_1, arr_2, arr_3))
print("Объединенный массив по первой оси (hstack):\n")
print(hstack_array)
print("Форма объединенного массива:\n", hstack_array.shape)
# Вывод:
# Объединенный массив по первой оси (hstack):
# [[ 1  2  3  4  5  6  7  8  9 10]
#  [ 2  3  4  5  6  7  8  9 10 11]
#  [ 3  4  5  6  7  8  9 10 11 12]]
# Форма объединенного массива: (3, 10)

# 2. EXTEND.Объединение массивов по 0 оси(ВЕРТИКАЛЬНОЙ ОСИ) с использованием np.vstack
arr_1 = np.array([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
arr_2 = np.array([[4, 5, 6], [5, 6, 7], [6, 7, 8]])
arr_3 = np.array([[7, 8, 9], [8, 9, 10], [9, 10, 11], [10, 11, 12]])
print(f"arr_1.shape={arr_1.shape}", arr_1, sep="\n", end="\n")
print(f"arr_2.shape={arr_2.shape}", arr_2, sep="\n", end="\n")
print(f"arr_3.shape={arr_3.shape}", arr_3, sep="\n", end="\n")
# arr_1.shape=(3, 3)
# [[1 2 3]
#  [2 3 4]
#  [3 4 5]]
# arr_2.shape=(3, 3)
# [[4 5 6]
#  [5 6 7]
#  [6 7 8]]
# arr_3.shape=(4, 3)
# [[ 7  8  9]
#  [ 8  9 10]
#  [ 9 10 11]
#  [10 11 12]]
new_arr = np.vstack([arr_1, arr_2, arr_3])  # массивы должны иметь одинковое кол-во елемнтов вдоль всех осей
print(new_arr.shape, new_arr)
# (10, 3) [[ 1  2  3]
#  [ 2  3  4]
#  [ 3  4  5]
#  [ 4  5  6]
#  [ 5  6  7]
#  [ 6  7  8]
#  [ 7  8  9]
#  [ 8  9 10]
#  [ 9 10 11]
#  [10 11 12]]

################################################
###### Объединение массивов. concatenate #######
################################################
#  np.concatenate необходимо помнить, что по всем осям, кроме той в которой происходит обьеденение КОЛ-ВО елементов должно совападать
arr_1 = np.empty([27, 27, 1])
arr_2 = np.empty([27, 27, 1])
arr_3 = np.empty([27, 27, 1])

print(f"arr1=arr2=arr3{arr_1}", end="\n\n")
# arr1=arr2=arr3[[[ 1.33691486e-311]
#   [ 1.33686098e-311]
#   [ 1.42933191e-320]
#   [ 1.33686092e-311]
#   [ 1.33686098e-311]
#   [ 1.33686146e-311]
#   [ 0.00000000e+000]
#   [ 0.00000000e+000]
#   [ 2.12199580e-314]
#   [ 4.24399158e-313]
#   [ 9.88131292e-324]
#   [ 1.81006241e-311]
#   [ 1.33686148e-311]
#   [ 1.33686150e-311]
#   [ 1.33685974e-311]
#   [ 1.33686147e-311]
#   [ 1.33686147e-311]
#   [ 1.33686097e-311]
#   [ 0.00000000e+000]
#   [ 0.00000000e+000]
#   [ 0.00000000e+000]
#   [ 0.00000000e+000]
#   [ 6.95250701e-310]
#   [ 0.00000000e+000]
#   [ 5.83329814e-302]
#   [ 6.12455142e-302]
#   [ 3.24635714e-319]]
#
#  [[...]]
#  ... 27 раз....
#  [[...]]
print(arr_1.shape, end="\n\n")
print(arr_2.shape, end="\n\n")
print(arr_3.shape)
# и такой оси по каждом массиву
# (27, 27, 1)
# (27, 27, 1)
# (27, 27, 1)

new_arr = np.concatenate([arr_1, arr_2, arr_3], axis=2)

print(f"но в итоге получаем обновленный еденый массив: {new_arr.shape}")
# но в итоге получаем обновленный еденый массив: (27, 27, 3)

###############################################
###### Разделение массивов .array_split #######
###############################################

arr_1 = np.array([['x_1', 'y_1'], ['x_2', 'y_2'], ['x_3', 'y_3'], ['x_4', 'y_4']])

print(arr_1.shape, arr_1, sep='\n\n')
# (4, 2)
# [['x_1' 'y_1']
#  ['x_2' 'y_2']
#  ['x_3' 'y_3']
#  ['x_4' 'y_4']]

# 1.  получить нулевую ось ПО ГОРИЗОНАЛЕ  - ['x_1', 'y_1'] - то нужно по 0 оси(ГОРИЗОНТАЛЬ)

arr_list = np.array_split(arr_1, 4,
                          axis=0)  # 2 - число на сколко частей нужно разделить массив, axis=0 - ось по которой будет разбит массив
print(arr_list)
# [array([['x_1', 'y_1']], dtype='<U3'), array([['x_2', 'y_2']], dtype='<U3'), array([['x_3', 'y_3']], dtype='<U3'), array([['x_4', 'y_4']], dtype='<U3')]

# 2.  получить нулевую ось ПО ВЕРТИКАЛЕ  - [['x_1' 'x_2' 'x_3' 'x_4']] - то нужно по первой оси(вертикаль)
arr_list_gorizont = np.array_split(arr_1, 2, axis=1)
print(arr_list_gorizont)
# [array([['x_1'],
#        ['x_2'],
#        ['x_3'],
#        ['x_4']], dtype='<U3'), array([['y_1'],
#        ['y_2'],
#        ['y_3'],
#        ['y_4']], dtype='<U3')]

# Если в данніх массивах, в одном из них поменять значение, то оно тоже отобразится на другом
arr_list[0][0] = 1
print(
    f"поменяли значние для arr_list, а оно изменилось в  arr_list_gorizont(как строка, хотя подставили туда инт):\n {arr_list_gorizont}")
#  [array([['1'],
#        ['x_2'],
#        ['x_3'],
#        ['x_4']], dtype='<U3'), array([['1'],
#        ['y_2'],
#        ['y_3'],
#        ['y_4']], dtype='<U3')]
