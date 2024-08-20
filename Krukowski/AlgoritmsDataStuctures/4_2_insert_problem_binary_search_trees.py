
class Node:
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left_child = left
        self.right_child = right


class BalancedBinarySearchTree:
    def __init__(self, root_value):
        # изначально у дерева будет только корень, который при иницилизации, будет иметь середину - ОДИН УЗЕЛ
        self.root = Node(root_value)

    def insert(self, inserted_value):
        """
        Нам придется использовать рекурсию потмоу что
        - каждый раз мы спускаемся на уровень ниже,
          следовательно каждый раз root будет как буд-то бы новым.
        :return:
        """
        # 1.т.к. не может быть дублирующих значений, то просто выйдем из рекурсии
        if inserted_value == self.root.value:
            return

        # 2. когда вставляемое значение меньше значенияч текущего узла(current_node),ТО ВСТАВЛЕМ его СЛЕВА
        if inserted_value < self.root.value:
            # 2.1. Нужно проверить, занято том или нет
            # - если занято,
            if self.root.left_child:
                # то РЕКУРСИВНО вызываем этот же метод ЕЩЕ РАЗ, НО ТОЛЬКО в качестве новго корня будет УЖЕ left_child
                # и прокидываем в него значение, которое хотим вставим в BTC (inserted_value)
                self.insert(inserted_value, )



# PROBLEM
"""
пишу BTC
остановился на месте что в б рекурсивно вызвать метод инссерт и прокинуть в него левый корень, но что-то не понять как именно это сделать.. 
"""
