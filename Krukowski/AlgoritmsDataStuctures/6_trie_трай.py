class Node:
    def __init__(self):
        # Дочерние узлы хранятся в словаре, где ключ — это символ, а значение — следующий узел(потомки)
        self.children = {}
        # Нужно как-то отмечать конец слова..  можно через звездочку одному ноду, НО
        # другой нод может продолжать слово с родителя:
        # - eco*
        # - ecoflow*
        # - economic*
        # - economical*
        # Булевый флаг, указывающий на конец слова
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        # Инициализация корневого узла
        self.root = Node()

    def insert(self, word):
        """
        Проходит по символам строки и вставляет новый узел, если его нет.
        Устанавливает флаг is_end_of_word, если вся строка вставлена.

        node — это текущий узел, в котором мы находимся.
        children — это словарь потомков текущего узла, где ключи — символы, а значения — соответствующие узлы(потомки).
        char — это текущий символ слова, который мы обрабатываем.

        Когда мы выполняем node = node.children[char], это означает:
            - Мы смотрим, есть ли у текущего узла node потомок, связанный с символом char.
            - Если такой потомок существует, мы перемещаемся к нему, то есть делаем этот узел текущим (node),
              чтобы продолжить обработку следующих символов.
        """
        # Начинаем с корня
        node = self.root
        # Проходим по каждому символу в слове
        for char in word:
            # Если текущего символа нет среди потомков узла, добавляем новый узел,
            if char not in node.children:
                # т.е. гарантирует, что у текущего узла будет потомок, связанный с текущим символом char
                node.children[char] = Node()
            # Переходим к следующему узлу - означает спуск на уровень ниже в дереве к узлу(потомку),
            # который соответствует текущему символу, с которым мы работаем.
            node = node.children[char]
        # Устанавливаем флаг, что это конец слова
        node.is_end_of_word = True

    def search(self, word):
        """
        поиск пригодится при АВТОКОМПЛИТЕ
        """
        # Начинаем с корня, т.е. с первой буквы
        node = self.root
        # Проходим по каждому символу в слове
        for char in word:
            # Если символа нет среди потомков узла, значит, слово отсутствует
            if char not in node.children:
                return False, word
            # Переходим к следующему узлу - означает спуск на уровень ниже в дереве к узлу(потомку),
            # который соответствует текущему символу, с которым мы работаем.
            node = node.children[char]
        # Возвращаем True и найденное слово, если текущий узел отмечен как конец слова
        return node.is_end_of_word, word

    def starts_with(self, prefix):
        # Начинаем с корня
        node = self.root
        # Проходим по каждому символу в префиксе
        for char in prefix:
            # Если символа нет среди потомков узла, значит, нет строки с таким префиксом
            if char not in node.children:
                return False, f'prefix={prefix}'
            # Переходим к следующему узлу - означает спуск на уровень ниже в дереве к узлу(потомку),
            # который соответствует текущему символу, с которым мы работаем.
            node = node.children[char]
        # Если все символы префикса найдены, возвращаем True
        return True, f'prefix={prefix}'

    def delete(self, word):
        # Вспомогательная функция для рекурсивного удаления
        def _delete(node, word, depth):
            # Если узел пустой, возвращаем False
            if not node:
                return False

            # Если мы находимся на последнем символе слова
            if depth == len(word):
                # Если это конец слова, снимаем флаг конца слова
                if node.is_end_of_word:
                    node.is_end_of_word = False
                # Если узел больше не имеет потомков, можно его удалить
                return len(node.children) == 0

            # Рекурсивно переходим к следующему узлу
            char = word[depth]
            if char in node.children:
                should_delete_child = _delete(node.children[char], word, depth + 1)
                # Если узел пустой и не конец другого слова, удаляем его
                if should_delete_child:
                    del node.children[char]
                    # Возвращаем True, если после удаления нет потомков
                    return len(node.children) == 0
            return False

        # Начинаем с корня и нулевой глубины
        _delete(self.root, word, 0)


# Пример использования
trie = Trie()
trie.insert("cat")
trie.insert("catty")
trie.insert("category")
trie.insert("categorizer")
trie.insert("car")
trie.insert("dog")

# Поиск слова
print(trie.search("cat"))  # True
print(trie.search("can"))  # False

# Поиск по префиксу
print(trie.starts_with("ca"))  # True
print(trie.starts_with("do"))  # True

# Удаление слова
trie.delete("car")
print(trie.search("car"))  # False
print(trie.search("cat"))  # True
