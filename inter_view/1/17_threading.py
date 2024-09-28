import os
import threading
import time
from threading import Thread
from tkinter import *
from tkinter import ttk


# multithreading - многопоточность, подходит для IO-bound задач, использует ОС, страдает от GIL
# Полезно для ускорения выполнения задач или для того, чтобы текущий поток занялся другой задачей
# Любая программа имеет минимум один процесс и один поток

def waiting(timeout):
    while timeout > 0:
        timeout -= 1
        time.sleep(1)  # Ожидание 1 секунду
    print("OK")  # Печатает 'OK' после завершения ожидания


def thread_wait(timeout):
    """
    тот же самая логика.. он візівает функцию waiting, НО через thread

    """
    thread = Thread(target=waiting, args=(timeout,), daemon=True)  # Создание потока с функцией waiting
    # True = фоновым поток - выполняться в фоновом режиме, но которые не должны блокировать завершение программы.
    thread.start()  # Запуск потока
    return thread  # Возврат потока для возможного дальнейшего использования


# Глобальный счетчик в виде списка с одним элементом (для модификации внутри функций)
counter = [0]


def inc():
    """
    Увеличивает глобальный счетчик на 1 с паузой в 0.1 секунды.
    """
    c = counter[0]  # Чтение текущего значения счетчика
    time.sleep(0.1)  # Небольшая пауза в 0.1 секунды
    counter[0] = c + 1  # Увеличение значения счетчика на 1


def info():
    """
    Выводит информацию о текущем процессе и потоке.
    """
    pid = os.getpid()  # Получение ID текущего процесса
    name = threading.current_thread().name  # Получение имени текущего потока
    print(f"Process {pid}, name {name}")  # Печать информации о процессе и потоке


if __name__ == '__main__':
    # Создание графического интерфейса на базе Tkinter
    tk = Tk()

    # Кнопка "WAIT" выполняет функцию ожидания в основном потоке
    button1 = ttk.Button(tk, text="WAIT", command=lambda: waiting(3))  # Ожидание 3 секунды
    button1.pack(side=LEFT)  # Размещение кнопки слева

    # Кнопка "THREAD" запускает ожидание в отдельном потоке
    button2 = ttk.Button(tk, text="THREAD", command=lambda: thread_wait(3))  # Ожидание 3 секунды в новом потоке
    button2.pack(side=LEFT)  # Размещение кнопки слева

    # Запуск главного цикла Tkinter для отображения окна с кнопками
    tk.mainloop()

    # Закомментированный код для демонстрации работы с потоками
    # Создает 10 потоков, каждый из которых выводит информацию о процессе и потоке
    # threads = [Thread(target=info, daemon=True) for _ in range(10)]  # Создание 10 потоков
    # for t in threads:
    #     t.start()  # Запуск всех потоков
    # for t in threads:
    #     t.join()  # Ожидание завершения всех потоков
    # print(counter)  # Печать значения счетчика после работы потоков
    # info()  # Вызов функции info для текущего потока
