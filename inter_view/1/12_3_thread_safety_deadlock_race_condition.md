
# Потокобезопасность в программировании

Когда несколько потоков работают с общими данными, важно обеспечить **потокобезопасность**, чтобы избежать конфликтов, таких как **взаимоблокировки** и **состояния гонки**. Рассмотрим эти проблемы более подробно.

## 1. Взаимоблокировка (Deadlock)

**Взаимоблокировка** возникает, когда два (или более) потока блокируются, ожидая друг друга для освобождения ресурса, что приводит к ситуации, когда ни один из них не может продолжить выполнение. Каждый поток удерживает ресурс и ожидает освобождения другого, что приводит к бесконечному ожиданию.

### Пример:
- **Поток 1** захватывает **Ресурс A** и ждёт, пока **Поток 2** освободит **Ресурс B**.
- **Поток 2** захватывает **Ресурс B** и ждёт, пока **Поток 1** освободит **Ресурс A**.

#### Визуализация:

```
Поток 1 ----> Ресурс A -----> ждет -----> Ресурс B
Поток 2 ----> Ресурс B -----> ждет -----> Ресурс A
```

### Пример на Python:
```python
import threading

lock_a = threading.Lock()
lock_b = threading.Lock()

def thread1():
    with lock_a:
        print("Поток 1 захватил Ресурс A")
        with lock_b:
            print("Поток 1 захватил Ресурс B")

def thread2():
    with lock_b:
        print("Поток 2 захватил Ресурс B")
        with lock_a:
            print("Поток 2 захватил Ресурс A")

t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)

t1.start()
t2.start()

t1.join()
t2.join()
```
В этом примере есть риск взаимоблокировки, если потоки попытаются захватить ресурсы в разном порядке.

### Как избежать взаимоблокировки:
1. **Порядок блокировок**: Все потоки должны захватывать ресурсы в одном и том же порядке.
2. **Тайм-ауты**: Устанавливать тайм-ауты для захвата ресурсов, чтобы поток не зависал в ожидании слишком долго.
3. **Блокировки с проверкой**: Использовать функции вроде `try_lock`, чтобы проверять возможность захвата ресурса.

## 2. Состояние гонки (Race Condition)

**Состояние гонки** возникает, когда несколько потоков одновременно пытаются изменить общий ресурс, и результат зависит от порядка выполнения этих потоков. В результате поведение программы становится непредсказуемым, так как разные потоки могут записывать или читать данные в неправильный момент.

### Пример:
- **Поток 1** читает значение переменной.
- **Поток 2** изменяет эту переменную до того, как **Поток 1** успел завершить операцию.
- В результате переменная может иметь неверное значение или состояние.

### Пример на Python:
```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1

threads = []
for i in range(10):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Значение счетчика: {counter}")
```

### Как избежать состояния гонки:
1. **Использование блокировок (Locks)**: Обеспечить, что только один поток может изменять данные в любой момент времени.
2. **Семафоры и другие синхронизационные примитивы**: Управление доступом к общим ресурсам.
3. **Иммутабельность данных**: Использование неизменяемых данных, которые не могут быть изменены другими потоками.

--- 


# Семафоры

**Семафор** — это примитив синхронизации, который используется для ограничения количества потоков или процессов, получающих доступ к ресурсу одновременно.

## Как это работает?
- Семафор имеет счетчик доступных разрешений.
- Когда поток получает доступ к ресурсу, счетчик уменьшается.
- Когда счетчик достигает нуля, следующие потоки должны ждать, пока другие не освободят ресурс.

### Пример на Python:

```python
import threading
import time

# Семафор с 3 разрешениями
semaphore = threading.Semaphore(3)

def access_resource(thread_id):
    print(f"Поток {thread_id} пытается получить доступ к ресурсу.")
    
    # Запрашиваем доступ к ресурсу (счётчик уменьшается)
    semaphore.acquire()
    
    print(f"Поток {thread_id} получил доступ к ресурсу.")
    time.sleep(2)  # Имитируем работу с ресурсом
    
    print(f"Поток {thread_id} освобождает ресурс.")
    
    # Освобождаем ресурс (счётчик увеличивается)
    semaphore.release()

# Создаем 5 потоков, пытающихся получить доступ к ресурсу
threads = []
for i in range(5):
    t = threading.Thread(target=access_resource, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

### Основные моменты:
1. **`Semaphore(3)`**: Разрешает одновременно 3 потока.
2. **`acquire()`**: Поток захватывает ресурс, уменьшая счётчик.
3. **`release()`**: Поток освобождает ресурс, увеличивая счётчик.
4. Потоки, которым не хватает разрешений, ждут, пока ресурс освободится.

