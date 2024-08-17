def find_unmatched_brackets(expression):
    stack = []
    brackets = {')': '(', '}': '{', ']': '['}
    unmatched_closing = []

    for i, char in enumerate(expression):
        if char in brackets.values():
            stack.append((char, i))
        elif char in brackets:
            if stack and stack[-1][0] == brackets[char]:
                stack.pop()
            else:
                unmatched_closing.append((char, i))

    results = []
    if stack:
        unmatched_opening = ', '.join([f"'{char}' at position {pos}" for char, pos in stack])
        results.append(f"Unmatched opening brackets: {unmatched_opening}")
    if unmatched_closing:
        unmatched_closing_brackets = ', '.join([f"'{char}' at position {pos}" for char, pos in unmatched_closing])
        results.append(f"Unmatched closing brackets: {unmatched_closing_brackets}")

    if results:
        return " | ".join(results)

    return "All brackets are matched correctly"


expression = "Demo internal {demo2 [invalid])"
result = find_unmatched_brackets(expression)
print(result)

################################################################################################
from collections import deque


class PrinterQueue:
    def __init__(self):
        # Используем deque для оптимальной работы с очередью.
        # теоретически можно использовать обычный список для реализации очереди, это будет менее эффективно.
        # Метод popleft используется для удаления элементов с начала очереди. выполняет эту операцию за постоянное время 𝑂(1)
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
