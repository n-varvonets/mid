# Конкурентность (concurrency) - запуск на выполнение сразу нескольких задач (не обязательно в 1 момент времени выполняется несколько). Зависит от ПО.

# Параллельность (parallel) - конкурентность, когда 2+ задачи выполняются одновременно. Зависит от железа.

# thread-safe - потокобезопасность, означает что при работе с объектом не возникают известные проблемы при работе с конкурентностью.

# GIL (Global Interpreter Lock) - глобальная блокировка интерпретатора.

# Задачи могут быть:
# CPU-bound - зависит от мощности процессора
# IO-bound - зависит от системы ввода/вывода

# threading - IO-bound задачи
# asyncio - IO-bound задачи
# multiprocessing - любые задачи
import threading
import time

import requests

def activity():
    # for e in range(1000_000):
    #     abs(round(e * 2 / 122) + e * 3.14)   # Time: 3.21024155616760254 seconds

    res = requests.get("https://www.google.com/")  # Time: 0.21024155616760254 seconds
    return res

def run(threaded=False):
    start = time.time()
    if not threaded:
        for e in range(10):
            activity()
    else:
        threads = [threading.Thread(target=activity, daemon=True) for _ in range(10)]
        for e in threads:
            e.start()
        for e in threads:
            e.join()

    end = time.time()
    print(f'Time: {end - start} seconds')


if __name__ == '__main__':
    run(threaded=True)
    # run(threaded=False)