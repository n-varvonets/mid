def two_sum(nums, target):
    # Создаем словарь для хранения индексов чисел
    num_to_index = {}

    # Проходим по каждому числу в списке nums
    for i, num in enumerate(nums):
        # complement - это разница между target и текущим числом num.
        # Она показывает, какое число необходимо найти в списке,
        # чтобы в сумме с num получилось target.
        difference = target - num  # Переименовали complement на более понятное имя difference (разница)

        # Если разница уже есть в словаре, то мы нашли пару чисел,
        # которая в сумме равна target. Возвращаем индексы этих чисел.
        if difference in num_to_index:
            return [num_to_index[difference], i]

        # Если пара не найдена, сохраняем индекс текущего числа в словарь.
        # Ключом будет само число, а значением - его индекс.
        num_to_index[num] = i

    # Если пара чисел не найдена, возвращаем пустой список
    return []

# Примеры вызова функции с разными входными данными:
# В первом примере числа 2 и 7 в сумме дают 9 (индексы [0, 1])
print(two_sum(nums=[2, 7, 11, 15], target=9))

# Во втором примере числа 2 и 4 дают в сумме 6 (индексы [1, 2])
print(two_sum(nums=[3, 2, 4], target=6))

# В третьем примере два числа 3 дают в сумме 6 (индексы [0, 1])
print(two_sum(nums=[3, 3], target=6))
