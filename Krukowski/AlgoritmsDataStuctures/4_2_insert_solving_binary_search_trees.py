
class Node:
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left_child = left
        self.right_child = right

def display_tree(node, level=0, prefix="Root: "):
    if node is not None:
        # Рекурсивный вызов для правого поддерева (оно будет выведено выше корня)
        display_tree(node.right_child, level + 1, "R--- ")

        # Вывод текущего узла
        print(" " * (4 * level) + prefix + str(node.value))

        # Рекурсивный вызов для левого поддерева (оно будет выведено ниже корня)
        display_tree(node.left_child, level + 1, "L--- ")

class BalancedBinarySearchTree:
    def __init__(self, root_value):
        # изначально у дерева будет только корень, который при иницилизации, будет иметь середину - ОДИН УЗЕЛ
        self.root = Node(root_value)

    def insert(self, inserted_value, current_node=None):
        """
        1.Нам придется использовать рекурсию потмоу что
        - каждый раз мы спускаемся на уровень ниже,
          следовательно каждый раз root будет как буд-то бы новым.

        2.1.PROBLEM: заключается в том, что вам нужно передать текущий узел (Node),
        с которым вы работаете, в рекурсивный вызов метода insert.
        2.2.SOLVING: если текущий узел (current_node) не указан, метод начинает с корня дерева
        """
        # 0. Если текущий узел не передан, начинаем с корня
        if current_node is None:
            current_node = self.root

        # 1.т.к. не может быть дублирующих значений, то просто выйдем из рекурсии
        if inserted_value == current_node.value:
            return

        # 2. когда вставляемое значение меньше значенияч текущего узла(current_node),ТО ВСТАВЛЕМ его СЛЕВА
        if inserted_value < current_node.value:
            # 2.1. Нужно проверить, занято тaм или нет
            # - если занято,
            if current_node.left_child:
                # то РЕКУРСИВНО вызываем этот же метод ЕЩЕ РАЗ, НО ТОЛЬКО в качестве новго корня будет УЖЕ left_child
                # и прокидываем в него значение, которое хотим вставим в BTC (inserted_value)
                self.insert(inserted_value, current_node.left_child)
            # 2.2. если же свободно, значит всен просто - добавляем наше inserted_value
            else:
                # ERROR
                # current_node.left_child = inserted_value
                # НО НЕ ПРОСТО ДАЕМ ЕМУ ЗНАЧЕНИЕ(а создаем обьект со связями left and right),
                # т.к. у inserted_value должны быть тоже связи left and right

                current_node.left_child = Node(inserted_value)

        # 3. Последний кейс, когда значение больше и по аналогии
        else:
            # 3.1. Нужно проверить, занято тaм или нет
            if current_node.right_child:
                self.insert(inserted_value, current_node.right_child)
            # 3.2. a если свободно, то..
            else:
                current_node.right_child = Node(inserted_value)

    def search(self, search_value, current_node=None):
        """
        простой метод, по аналогии с инсертом и вот почему
        O(logN), в отличии от линейного O(N) массива
        """
        if current_node is None:
            current_node = self.root

        # Если узел с нужным значением найден, возвращаем его
        if search_value == current_node.value:
            return current_node

        # Ищем в левом поддереве
        elif search_value < current_node.value:
            if current_node.left_child:
                return self.search(search_value, current_node.left_child)
            else:
                return None

        # Ищем в правом поддереве
        else:
            if current_node.right_child:
                return self.search(search_value, current_node.right_child)
            else:
                return None

    def display(self):
        """просто для удобности вывода принта"""
        display_tree(self.root)


tree = BalancedBinarySearchTree(42)

tree.insert(30)
tree.insert(43)
tree.insert(100)
tree.insert(44)
tree.insert(41)
tree.insert(44) # дублирующее значение

tree.display()


result = tree.search(100)
if result:
    print(f"Value {result.value} found in the tree.")
else:
    print("Value not found in the tree.")

