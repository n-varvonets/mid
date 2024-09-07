# 1
# some_var = None
# some_lst = [1, 0, True, [], 0, 2]
#
# # Пример использования оператора "or" для назначения значения переменной
# for el in some_lst:
#     # Если some_var ещё не установлена (None), назначаем ей текущее значение el, если оно истина
#     if not some_var:
#         some_var = el or some_var
#
# print(some_var)  # some_var примет первое значение, которое является истиной






# 3
some_var = None
some_lst = [0, None, False, '', '-First True Value-', '-Another Value-', 1]
for el in some_lst:
    some_var = some_var or el
print(some_var)  # Выведет: 'First True Value'

print('' is None)
print([] is None)