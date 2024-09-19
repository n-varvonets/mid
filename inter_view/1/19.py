class MyClass:
    pass

my_instance = MyClass()
print(isinstance(my_instance, object))  # Выведет: True
print(isinstance(my_instance, type))  # Выведет: False
print(type(MyClass))  # Выведет: <class 'type'>
print(type(type))  # <class 'type'>
