class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left_child = left
        self.right_child = right


class BalancedBinarySearchTree:
    def __init__(self, root_value):
        self.root = Node(root_value)

    def insert(self, inserted_value, current_node=None):
        if current_node is None:
            current_node = self.root

        if inserted_value == current_node.value:
            return

        if inserted_value < current_node.value:
            if current_node.left_child:
                self.insert(inserted_value, current_node.left_child)
            else:
                current_node.left_child = Node(inserted_value)
        else:
            if inserted_value > current_node.value:
                if current_node.right_child:
                    self.insert(inserted_value, current_node.right_child)
                else:
                    current_node.right_child = Node(inserted_value)

    def search(self, search_value, current_node=None):
        if current_node is None:
            current_node = self.root

        if search_value == current_node.value:
            return current_node
        elif search_value < current_node.value:
            return self.search(search_value, current_node.left_child) if current_node.left_child else None
        else:
            return self.search(search_value, current_node.right_child) if current_node.right_child else None

    def find_min(self, current_node):
        """
        Метод для нахождения минимального значения в дереве (наименьший узел).
        """
        while current_node.left_child:
            current_node = current_node.left_child
        return current_node

    def delete(self, value, current_node=None):
        """
        1.Поиск узла: Метод рекурсивно ищет узел, который нужно удалить.
        2.Удаление узла без потомков: Если у узла нет потомков, он удаляется просто присвоением None.
        3.Удаление узла с одним потомком: Если у узла есть только один потомок, этот потомок заменяет удаляемый узел.
        5.Удаление узла с двумя потомками: Если у узла есть два потомка:
            Находим наименьший узел в правом поддереве (successor).
            Копируем значение этого узла в удаляемый узел.
            Удаляем successor из его текущей позиции.
        """
        if current_node is None:
            current_node = self.root

        if value < current_node.value:
            if current_node.left_child:
                current_node.left_child = self.delete(value, current_node.left_child)
        elif value > current_node.value:
            if current_node.right_child:
                current_node.right_child = self.delete(value, current_node.right_child)
        else:
            # Узел найден
            # 1. Если нет потомков
            if current_node.left_child is None and current_node.right_child is None:
                current_node = None
            # 2. Если есть только один потомок
            elif current_node.left_child is None:
                current_node = current_node.right_child
            elif current_node.right_child is None:
                current_node = current_node.left_child
            # 3. Если есть два потомка
            else:
                # Находим преемника (наименьший узел в правом поддереве)
                successor = self.find_min(current_node.right_child)
                # Переносим значение преемника в текущий узел
                current_node.value = successor.value
                # Удаляем преемника из правого поддерева
                current_node.right_child = self.delete(successor.value, current_node.right_child)

        return current_node

    def display(self):
        """просто для удобности вывода принта"""
        display_tree(self.root)

#### add ####
def display_tree(node, level=0, prefix="Root: "):
    if node is not None:
        # Рекурсивный вызов для правого поддерева (оно будет выведено выше корня)
        display_tree(node.right_child, level + 1, "R--- ")

        # Вывод текущего узла
        print(" " * (4 * level) + prefix + str(node.value))

        # Рекурсивный вызов для левого поддерева (оно будет выведено ниже корня)
        display_tree(node.left_child, level + 1, "L--- ")

##########

tree = BalancedBinarySearchTree(42)

tree.insert(37)
tree.insert(20)
tree.insert(100)
tree.insert(38)
tree.insert(98)
tree.insert(156)
tree.insert(99)
tree.insert(101)

print("Initial tree:")
tree.display()

print("\nУдаление узла 100\n")
tree.delete(100)
tree.display()

