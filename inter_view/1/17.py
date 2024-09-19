def data_processor():
    print("Начало обработки данных")
    while True:
        data = yield  # Ожидание новых данных
        print(f"Обработка: {data}")

# Инициализация генератора
processor = data_processor()
next(processor)  # Запуск генератора до первого yield

# Передача данных для обработки через send
processor.send("Данные 1")  # Обработка: Данные 1
processor.send("Данные 2")  # Обработка: Данные 2


# --- Пример реализации паттерна "Цепочка обязанностей" с генераторами:

def handler_one():
    while True:
        data = yield  # Ожидание данных
        if isinstance(data, int) and data % 2 == 0:
            print(f"Handler One: обработал {data} (четное)")
        else:
            print(f"Handler One: передал дальше {data}")
            handler_two.send(data)  # Передаем данные следующему обработчику

def handler_two():
    while True:
        data = yield
        if isinstance(data, int) and data % 2 != 0:
            print(f"Handler Two: обработал {data} (нечетное)")
        else:
            print(f"Handler Two: не смог обработать {data}")

# Инициализация генераторов
handler_two = handler_two()
next(handler_two)  # Запуск второго обработчика

handler_one = handler_one()
next(handler_one)  # Запуск первого обработчика

# Передача данных через цепочку обработчиков
handler_one.send(4)  # обработает handler_one
handler_one.send(7)  # передаст handler_two