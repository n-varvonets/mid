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
            if current_node.right_child:
                self.insert(inserted_value, current_node.right_child)
            else:
                current_node.right_child = Node(inserted_value)

    def delete(self, deletion_value, current_node=None):
        """
        :return  В каждом рекурсивном вызове возвращаем
         - либо потомка, который должен занять место удаленного узла,
         - либо текущий узел, если удаление произошло глубже в дереве.

         Допустим, у нас есть следующее дерево, и мы хотим удалить узел со значением 70:
         1. бинарное дерево поиска до удаления узла:
                 50
                /   \
              30     70
             /  \   /  \
            20  40 60  80
                       /
                      75
                     /  \
                    72  77

         Шаг 1: Находим узел со значением 70.
         Шаг 2: Преемником узла 70 является узел 72 (наименьший в правом поддереве).
         Шаг 3: Переносим значение 72 в узел 70.
         Шаг 4: Удаляем узел 72, так как его значение уже используется.

         2. Итоговое дерево будет выглядеть так:
                 50
                /  \
              30    72
             /  \   /  \
            20  40 60  80
                      /
                     75
                       \
                        77

        https://youtu.be/occBtnLEshk?si=_LJJ82eKkjHzSN7D&t=1290
        """
        # 0. поиск начинаем с корня
        if current_node is None:
            current_node = self.root

        # return unless current_node - что значит выходим из рекурсии если узла уже нет

        #          42
        #       /      \
        #     37        100
        #    /  \     /     \
        #   20  38   98    156
        #             \     /
        #             99  101

        # 1.1. если значение меньше желаемого значения на удаление (root=42, удалить хочу 20)
        if deletion_value < current_node.value:  # рекурсивный поиск
            # для моего корня=42 (текущего_узла) будет новым ЛЕВЫМ потомок ТО, что вернет ВЫЗОВ метода delete
            # - с тем же значением на удаление(20), НО УЖЕ
            # - с left_child как новый корень(текущего_узла=37) нового вызова..
            # т.е. спустились В ПОИСКЕ НА ЛВЛ НИЖЕ
            # - и так до желаемого значения(20), т.е. потом вызов будет delete(20, 20) и возращаем нашу ноду бБЕЗ ЛЕВОГО ПОТОМКА
            # (т.е. условие not current_node.left_child) и возращаем правого потомка... НО там и правого потомка нет,
            # т.е. вернет NULL.. этот NULL вернeться на ЛВЛ ВЫШЕ(к root=37 и правого_потомка=38, А ЛЕВЫЙ СТАНЕТ = NULL, т.е. удалили 20 как и предпологалось с tree )
            current_node.left_child = self.delete(deletion_value, current_node.left_child)
            return current_node
        # 1.2. если значение больше ... (root=50, удалить хочу 101)
        elif deletion_value > current_node.value:  # рекурсивный поиск
            # аналогично с левой стороной, только вместо
            current_node.right_child = self.delete(deletion_value, current_node.right_child)
            return current_node
        # 1.3. если у текщего нода НЕТУ ЛЕВОГО потомка, то возращаем правый
        elif not current_node.left_child:  # когда левая часть  NULL
            return current_node.right_child
        # 1.4. во всех остальных слуаях будет
        else:  # когда левая часть NOT NULL  (удалить 100)
            # мы поднимаем правого  потомка для этого узла  и возращаем этот узел
            # self._lift(156, 100)
            current_node.right_child = self._lift(current_node.right_child, current_node)
            # если у левого узла есть ЛЕВЫЙ ПОТОМОК(он есть=101),
            # то для текущего_узла=156 надо установить нового левого потомка=NULL, т.е.
            # self._lift(101, 100)
            # дальше смотрим, что у него нет левого потомка
            # ЭТО ОЗНАЧАЕТ что для узла, который мы отим удалить, новым значением станет ЗНАЧЕНИЕ ТЕКУЩЕГО узла,
            # т.е. для 100 будет новым значение 101, так эе возьми правого потомка для теущего узла(NULL) и...
            # верни его, т.е. для 156 новым левым потомком будет NULL

            return current_node

    def _lift(self, current_node, node_to_delete):
        # если у текщего узла есть левый потомок, тогда левым потомком становится,
        if current_node.left_child:
            # то что вернет данный  метод lift на новом рекурсивном вызове, относительно node_to_delete
            current_node.left_child = self._lift(current_node.left_child, node_to_delete)
            return current_node
        else:
            # Переносим значение текущего узла в удаляемый узел
            node_to_delete.value = current_node.value
            # Возвращаем правого потомка текущего узла, чтобы заменить его
            return current_node.right_child

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

