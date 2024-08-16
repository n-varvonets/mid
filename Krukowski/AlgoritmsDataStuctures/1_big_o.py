def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    steps = 0
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1, steps

def binary_search_recursive(arr, target, left, right, steps=0):
    steps += 1
    if left > right:
        return -1, steps
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid, steps
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right, steps)
    else:
        return binary_search_recursive(arr, target, left, mid - 1, steps)

arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
target = 7

result, steps = binary_search(arr, target)
result_rec, steps_rec = binary_search_recursive(arr, target, 0, len(arr) - 1)

if result != -1:
    print(f"Элемент найден на позиции {result} за {steps} шагов (итеративный поиск).")
else:
    print(f"Элемент не найден после {steps} шагов (итеративный поиск).")

if result_rec != -1:
    print(f"Элемент REC найден на позиции {result_rec} за {steps_rec} шагов (рекурсивный поиск).")
else:
    print(f"Элемент REC не найден после {steps_rec} шагов (рекурсивный поиск).")


##########################################################################################################
def linear_search(arr, target):
    # Проходим по каждому элементу массива
    for index, element in enumerate(arr):
        # Если текущий элемент равен искомому, возвращаем его индекс
        if element == target:
            return index
    # Возвращаем -1, если элемент не найден
    return -1


def selection_sort(arr):
    n = len(arr)
    # Проходим по всему массиву
    for i in range(n):
        # Предполагаем, что текущий элемент минимальный
        min_index = i
        # Ищем минимальный элемент в оставшейся части массива
        for j in range(i+1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        # Меняем местами текущий элемент с найденным минимальным
        arr[i], arr[min_index] = arr[min_index], arr[i]
    # Возвращаем отсортированный массив
    return arr

def bubble_sort(arr):
    n = len(arr)
    # Проходим по всему массиву
    for i in range(n):
        # Внутренний цикл для сравнения соседних элементов
        for j in range(0, n-i-1):
            # Если текущий элемент больше следующего, меняем их местами
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    # Возвращаем отсортированный массив
    return arr




