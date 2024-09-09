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


a = 256
b = 256
print(a is b)  # True, так как числа от -5 до 256 кэшируются, и a и b ссылаются на один и тот же объект.

a1 = 2572
b1 = 2572
print(a1 is b1)  # False, числа вне диапазона кэширования создают новые объекты в памяти, поэтому a1 и b1 ссылаются на разные объекты.

a2 = hash(256)
b2 = hash(256)
print(a2 is b2)  # True, результат hash(256) равен 256, а числа до 256 кэшируются, поэтому a2 и b2 ссылаются на один и тот же объект.
print(a2)  # 256
print(b2)  # 256

a3 = hash(257)
b3 = hash(257)
print(a3 is b3)  # False, результат hash(257) равен 257, но числа больше 256 не кэшируются, поэтому a3 и b3 — разные объекты.
print(a3)  # 257
print(b3)  # 257



# 3
some_var = None
some_lst = [0, None, False, '', '-First True Value-', '-Another Value-', 1]
for el in some_lst:
    some_var = some_var or el
print(some_var)  # Выведет: 'First True Value'

print('' is None)
print([] is None)