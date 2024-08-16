def find_unmatched_brackets(expression):
    stack = []
    brackets = {')': '(', '}': '{', ']': '['}

    for i, char in enumerate(expression):
        if char in brackets.values():
            stack.append((char, i))
        elif char in brackets:
            if stack and stack[-1][0] == brackets[char]:
                stack.pop()
            else:
                # Если стек пуст или скобка не соответствует, игнорируем её и продолжаем проверку
                continue

    # Если в стеке остались незакрытые скобки, возвращаем их
    if stack:
        unmatched = ', '.join([f"'{char}' at position {pos}" for char, pos in stack])
        return f"Unmatched opening brackets: {unmatched}"

    return "All brackets are matched correctly"


# Пример использования
expression = "Demo (internal {demo2 [invalid])"
result = find_unmatched_brackets(expression)
print(result)


################################################################################################
from collections import deque


class PrinterQueue:
    def __init__(self):
        self.queue = deque()

    def add_job(self, job):
        """Добавить задачу в очередь печати"""
        self.queue.append(job)
        print(f"Добавлена задача: {job}")

    def print_job(self):
        """Распечатать следующий документ в очереди"""
        if self.queue:
            job = self.queue.popleft()
            print(f"Печать задачи: {job}")
        else:
            print("Очередь пуста, нет задач для печати.")

    def show_queue(self):
        """Показать текущую очередь печати"""
        if self.queue:
            print("Текущая очередь печати:", list(self.queue))
        else:
            print("Очередь пуста.")


# Пример использования
printer_queue = PrinterQueue()

# Добавляем задачи в очередь печати
printer_queue.add_job("Документ 1")
printer_queue.add_job("Документ 2")
printer_queue.add_job("Документ 3")

# Показать текущую очередь печати
printer_queue.show_queue()

# Печать задач
printer_queue.print_job()  # Печатает "Документ 1"
printer_queue.print_job()  # Печатает "Документ 2"

# Показать оставшиеся задачи в очереди
printer_queue.show_queue()

# Добавить еще одну задачу
printer_queue.add_job("Документ 4")

# Печать остальных задач
printer_queue.print_job()  # Печатает "Документ 3"
printer_queue.print_job()  # Печатает "Документ 4"
printer_queue.print_job()  # Сообщает, что очередь пуста
