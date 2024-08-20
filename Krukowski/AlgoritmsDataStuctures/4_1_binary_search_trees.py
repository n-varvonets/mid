#############################################################################
################ Реализация бинарного поиска (Binary Search) ################
#############################################################################
import time

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    steps = 0

    while left <= right: #  гарантирует, что на каждом шаге цикла будет проверен хотя бы один элемент,
        # т.е. условие было left < right, то на этапе, когда остается один элемент (например, left = right = 2),
        # этот элемент не был бы проверен, что могло бы привести к пропуску элемента.

        mid = (left + right) // 2
        steps += 1

        if arr[mid] == target:
            return mid, steps

        elif arr[mid] > target:
            right = mid - 1

        else:
            left = mid + 1

    return -1, steps  # Если элемент не найден


#########################################################################################
################ Реализация бинарного дерева поиска (Binary Search Tree) ################
#########################################################################################

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BalancedBinarySearchTree:
    def __init__(self):
        # изначально у дерева будет только корень
        self.root = None



    def sorted_array_to_bst(self, arr):
        if not arr:
            return None

        mid = len(arr) // 2
        node = TreeNode(arr[mid])

        node.left = self.sorted_array_to_bst(arr[:mid])
        node.right = self.sorted_array_to_bst(arr[mid + 1:])

        return node

    def build_tree(self, arr):
        self.root = self.sorted_array_to_bst(arr)

    def search(self, target):
        return self._search(self.root, target, 0)

    def _search(self, node, target, steps):
        if node is None:
            return False, steps

        steps += 1

        if node.data == target:
            return True, steps

        elif target < node.data:
            return self._search(node.left, target, steps)

        else:
            return self._search(node.right, target, steps)

############################################################
################ Cравнение на наборе данных ################
############################################################

import random


# Генерация отсортированного массива
data = sorted(random.sample(range(1, 100000), 10000))
target = data[random.randint(0, len(data) - 1)]

# Тестирование бинарного поиска (Binary Search)
start_time = time.time()
result, binary_search_steps = binary_search(data, target)
binary_search_time = time.time() - start_time
print(f"Binary Search - Индекс: {result}, target={target}, Шаги: {binary_search_steps}, Время: {binary_search_time} секунд")

# Создание и тестирование сбалансированного бинарного дерева поиска (Balanced Binary Search Tree)
bst = BalancedBinarySearchTree()
bst.build_tree(data)

start_time = time.time()
found, bst_steps = bst.search(target)
bst_time = time.time() - start_time
print(f"Balanced Binary Search Tree - Найдено: {found}, Шаги: {bst_steps}, Время: {bst_time} секунд")

# Ожидаемые результаты:
# 1. Бинарный поиск (Binary Search):
# - Должен быть быстрее на отсортированных массивах, так как он сразу делит массив пополам.
# Бинарное дерево поиска (Binary Search Tree):
# - Количество шагов может быть аналогично бинарному поиску,
# - но если дерево не сбалансировано,то может превратиться в список O(N).
