from typing import List


# Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
# You may assume that each input would have exactly one solution, and you may not use the same element twice.
# You can return the answer in any order.

# Example 1:
# Input: nums = [2,7,11,15], target = 9
# Output: [0,1]
# Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

# Example 2:
# Input: nums = [3,2,4], target = 6
# Output: [1,2]

# Example 3:
# Input: nums = [3,3], target = 6
# Output: [0,1]


class Solution:
    """
    Объяснение решения:
    Внешний цикл: Проходит по каждому элементу массива nums. Переменная i представляет текущий индекс первого элемента пары.

    Внутренний цикл:
        Проверяет каждый элемент массива после текущего элемента, рассматриваемого
        во внешнем цикле (j — индекс второго элемента пары).

    Проверка суммы:
        Для каждой пары элементов nums[i] и nums[j] проверяется, равна ли их сумма значению target.
         Если равна, возвращаются индексы этих двух элементов в виде списка [i, j].

    Пример работы:
        Если nums = [2, 7, 11, 15] и target = 9, то на первой итерации (i=0, j=1) будет проверено, равна
        ли сумма nums[0] + nums[1] = 2 + 7 = 9 значению target. Поскольку это так, возвращается [0, 1].
    """

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Проходим по каждому элементу массива
        for i in range(len(nums)):
            # Для каждого элемента проверяем все последующие элементы
            for j in range(i + 1, len(nums)):
                # Если сумма текущей пары равна target, возвращаем их индексы
                if nums[i] + nums[j] == target:
                    return [i, j]
        # Если решение не найдено (хотя по условию задачи оно всегда есть), можно вернуть пустой список или бросить исключение
        return []


class Solution:
    """
    Объяснение решения:
    Словарь num_to_index:
        Мы будем использовать словарь для хранения чисел, которые мы уже видели,
        и их индексов. Ключом словаря будет само число, а значением — его индекс в массиве nums.

    Проход по массиву nums:
        Мы перебираем каждый элемент массива nums. Для каждого элемента вычисляем, какое число (complement)
        нужно найти, чтобы сумма текущего числа и complement дала target.

    Проверка на наличие complement:
        Если это число (complement) уже встречалось ранее и было записано в словарь num_to_index,
        то мы нашли решение. Возвращаем индексы этого числа и текущего элемента.

    Сохранение числа в словарь:
        Если число не найдено, мы добавляем текущий элемент и его индекс в словарь,
        чтобы проверить на следующих итерациях.

    Пример работы:
        Если nums = [2, 7, 11, 15] и target = 9, то на первой итерации num = 2, complement = 7.
        Так как 7 нет в словаре, мы добавляем 2 в словарь. На следующей итерации num = 7, complement = 2,
        и 2 уже есть в словаре, значит, решение найдено, и мы возвращаем индексы [0, 1].
    """

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Создаем словарь для хранения чисел и их индексов
        num_to_index = {}

        # Проходим по каждому элементу списка nums
        for i, num in enumerate(nums):
            # Вычисляем число, которое нужно найти, чтобы в сумме получить target
            complement = target - num

            # Проверяем, есть ли это число в словаре
            if complement in num_to_index:
                # Если есть, возвращаем текущий индекс и индекс найденного числа
                return [num_to_index[complement], i]

            # Если нужного числа нет, сохраняем текущий элемент и его индекс в словарь
            num_to_index[num] = i

        # Если решение не найдено (хотя по условию задачи оно всегда есть), можно вернуть пустой список или бросить исключение
        return []


nums = [2, 7, 11, 15]
target = 9

s = Solution()
print(s.twoSum(nums, target))

class A:
    def method(self):
        print("Method in A")

class B(A):
    def method(self):
        print("Method in B")
        super().method()

class C(A):
    def method(self):
        print("Method in C")
        super().method()

class D(B, C):
    def method(self):
        print("Method in D")
        super().method()

d = D()
d.method()

print(D.__mro__)
