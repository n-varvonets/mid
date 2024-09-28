
# Генераторы с `send()` и паттерн "Цепочка обязанностей"

## Использование метода `send()` в генераторах

Метод `send()` в генераторах используется для передачи данных в генератор во время его выполнения. Это позволяет организовать двустороннюю связь между вызывающим кодом и генератором, что делает генераторы более гибкими.

### Пример использования `send()` в реальном сценарии:

```python
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
```

### Описание:
- Первый вызов `next()` запускает генератор до первого `yield`.
- Вызов `send("Данные 1")` передает данные в генератор и возобновляет его выполнение с того места, где оно было приостановлено.

## Паттерн "Цепочка обязанностей" (Chain of Responsibility)

**Паттерн "Цепочка обязанностей"** — это поведенческий паттерн, в котором запрос передаётся по цепочке объектов, и каждый объект сам решает, обработать ли запрос или передать его дальше по цепочке.

Использование `send()` в генераторах можно связать с этим паттерном, так как генератор может принимать данные, обрабатывать их и передавать управление обратно вызывающему коду. Каждый шаг обработки может решать, что делать с данными дальше.

### Пример реализации паттерна "Цепочка обязанностей" с генераторами:

```python
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
```

### Описание:
- **`handler_one`**: обрабатывает чётные числа. Если данные не удовлетворяют условию, передает их дальше в `handler_two`.
- **`handler_two`**: обрабатывает нечётные числа или сообщает, что данные не подходят для обработки.
- Каждый генератор в цепочке решает, обрабатывать ли данные или передавать их дальше.

## Реальный пример: Телеграм-бот с использованием паттерна "Цепочка обязанностей" и генераторов

В данном примере мы создадим структуру для Телеграм-бота, который собирает уточняющие вопросы о пользователе, проверяет данные и передает их по цепочке обработчиков для валидации и обработки.

### Реальный пример Телеграм-бота с паттерном "Цепочка обязанностей" и генераторами

#### Установка зависимости
Прежде чем приступить к коду, убедитесь, что у вас установлен модуль `python-telegram-bot` для взаимодействия с API Телеграм. Установите его командой:

```bash
pip install python-telegram-bot
```

### Код примера:

```python
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Генератор для обработки имени
def name_handler():
    while True:
        message = yield
        if 'name' not in message:
            print("Запрашиваем имя...")
            yield {"question": "Как вас зовут?"}
        else:
            print(f"Имя '{message['name']}' принято")
            handler_age.send(message)

# Генератор для обработки возраста
def age_handler():
    while True:
        message = yield
        if 'age' not in message:
            print("Запрашиваем возраст...")
            yield {"question": "Сколько вам лет?"}
        else:
            age = message['age']
            if age.isdigit() and 1 <= int(age) <= 120:
                print(f"Возраст '{age}' принят")
                # Здесь можно добавить следующую логику обработки
            else:
                print(f"Неправильный возраст '{age}'. Перезапрос.")
                yield {"question": "Введите корректный возраст"}

# Инициализация обработчиков
handler_age = age_handler()
next(handler_age)  # Запуск второго обработчика

handler_name = name_handler()
next(handler_name)  # Запуск первого обработчика

# Обработка сообщений от пользователя
async def handle_message(update: Update, context):
    user_message = update.message.text
    if 'name' not in context.user_data:
        question = handler_name.send({"name": user_message})
    elif 'age' not in context.user_data:
        question = handler_age.send({"age": user_message})
    
    if question and isinstance(question, dict):
        await update.message.reply_text(question['question'])

# Основная логика бота
async def start(update: Update, context):
    await update.message.reply_text("Привет! Давай познакомимся. Как тебя зовут?")

# Создаем приложение
app = ApplicationBuilder().token("ВАШ_ТОКЕН").build()

# Добавляем обработчики команд и сообщений
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

# Запуск бота
if __name__ == "__main__":
    app.run_polling()
```

### Описание работы:

- **`name_handler()`**: Запрашивает имя пользователя и передает его в цепочку для обработки.
- **`age_handler()`**: После имени запрашивает возраст и проверяет его валидность.
- **Телеграм-бот**: С помощью генераторов и паттерна "Цепочка обязанностей" происходит последовательная обработка входящих сообщений, проверка данных и ответ пользователю.
