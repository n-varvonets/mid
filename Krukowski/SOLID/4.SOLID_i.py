#1.#################### [S]INGLE RESPONSIBILITY #####################
# # - каждый класс должен иметь одну и только одну причину для изменения (должен отвечать только за одну часть
# # функциональности системы или за выполнение одной задачи)
# # - лучше много маленьких, чем ОДИН ГИГАНТСКИЙ КЛАСС
#2.#################### [O]PEN/CLOSED #####################
# - про наследование, а не модификацию
#3.#################### [L]ISKOV SUBSTITUTION #####################
# - инстанс родительского класса можно заменить на инстанс дочернего класса
# - через конкретизацию атрибутов и методов в родительском классе (чтобы избежать проблем, связанных с отсутствием
# унифицированного подхода обработке данных, т.е. для возможности перебора в цикле инстансов род и дочернего класса)
#4.#################### [I]NTERFACE SEGREGATION #####################
# - Класс потомка не должен зависеть от ненужных методов родительского класса.
# - Решение:
# --- создаём миксины — небольшие классы с отдельными методами, которые наследуем только тогда, когда они нужны.т.е. подключать только нужные интрфейсы
# --- через композциции - способ построения объектов, при котором один объект включает в себя другие
# объекты(через передачу в конструктор обьекта) и использует их для выполнения своих задач. ЭТО ДАЖЕ УДОБНЕЙ ЧЕМ наследование МИКСинов.
#5.#################### [D]EPENDENCY INVERSION #####################
# - Высокоуровневые модули не должны зависеть от низкоуровневых модулей. Оба должны зависеть от абстракций.
# Низкоуровневые модули, в свою очередь, реализуют эту абстракцию. Таким образом, можно легко заменять низкоуровневые модули,
# не изменяя код высокоуровневого модуля, поскольку он работает с абстракцией, а не с конкретной реализацией.Пример:
# 1.Вместо того чтобы класс, отвечающий за бизнес-логику, напрямую создавал и использовал объект базы данных, он будет
# использовать интерфейс Database, который может быть реализован различными классами (например, MySQLDatabase, PostgreSQLDatabase).
# 2.Представь, что у тебя есть разные игрушечные машинки: одна работает на батарейках, а другая на солнечных панелях.
# Если ты хочешь, чтобы твой пульт управления мог управлять любой из этих машинок, не нужно менять пульт для каждой машинки.
# Вместо этого, все машинки должны использовать одну и ту же кнопку «вперёд» и «назад», которая подходит ко всем пультам.
# Теперь бизнес-логика не зависит от конкретной базы данных, а лишь от интерфейса Database.
# - dependancy injection - лучше в метод передавать другой класс, чем в классе использовать напрямую другой класс

# крепкий/добротный - принципы и правила - это все хорошо, но не стоит забывать о здравом смысле,
# т.е. нен стоит быть слишком педантичным и следовать всем правилам и довыдам

# --- Problem ---
# - клиент(класс потомка) НЕ ДОЛЖЕН зависить от методов
# - клиент(класс потомка) НЕ ДОЛЖЕН подключать методы, которые он не использует

class Creature:
    """
    РОдительский класс 'Создание' с:
    - именем
    - методами swim, walk, talk
    """
    def __init__(self, name):
        self.name = name

    def swim(self):
        pass

    def walk(self):
        pass

    def talk(self):
        print(f'My name is {self.name}')


class Human(Creature):
    """
    Клиент-человек или потомок от Creature, который умеет
    - плавать, ходить и говорить
    """
    def __init__(self, name):
        super().__init__(name)

    def swim(self):
        print(f"I'm {self.name} and I can swim")

    def walk(self):
        print(f"I'm {self.name} and I can walk")

    def talk(self):
        print(f"I'm {self.name} and I can talk")

class Fish(Creature):
    """
    Клиент-рыба или потомок от Creature, который умеет
    - ТОЛЬКО плавать
    """
    def __init__(self, name):
        super().__init__(name)

    def swim(self):
        print(f"I'm {self.name} and I can swim")

class Cat(Creature):
    """
    Клиент-кошка или потомок от Creature, который умеет
    - плавать(теоретичски, хотя она не будет этому рада) и ходить
    """
    def __init__(self, name):
        super().__init__(name)

    def swim(self):
        print(f"I'm {self.name} and I can swim")

    def walk(self):
        print(f"I'm {self.name} and I can walk")


human = Human("John Doe")
human.swim()
human.walk()
human.talk()
# I'm John Doe and I can swim
# I'm John Doe and I can walk
# I'm John Doe and I can talk

fish = Fish("Nemo")
fish.swim()
# I'm Nemo and I can swim

cat = Cat("Mr. Buttons")
cat.walk()
cat.swim()
# I'm Mr. Buttons and I can walk
# I'm Mr. Buttons and I can swim

# НО ТУТ ВОЗНИКАЕТ ПРОБЛЕМА, хотя кошка и НЕ УМЕЕТ говорить, НО МЫ МОЖЕМ ВЫЗВАТЬ ее РОДИТЕЛЬСКИЙ метод talk()
cat.talk()  # My name is Mr. Buttons
# Это и есть нарушение  INTERFACE SEGREGATION

# --- Solving ---
# 1. создадим отдельные интерфейсы для реализции конкретных действий, от котрых будем наследоваться (МИКСИНЫ).
# т.е. методы разделяются по назначению... подключать только нужные интрфейсы
class Creature:
    """
    РОдительский класс 'Создание' с:
    - именем
    - БЕЗ методов swim, walk, talk
    """
    def __init__(self, name):
        self.name = name


class SwimmerInterface:
    """
    Интрефейс для реализации плавния
    """
    def swim(self):
        print('swim_from_parent')
        pass

class WalerInterface:
    def walk(self):
        pass


class TalkerInterface:
    def talk(self):
        print(f'My name is {self.name}')


class HumanI(Creature, SwimmerInterface, WalerInterface, TalkerInterface):
    """
    НАследуем и\методы миксинов, которые можно
    - переопределить в текщем классе(swim)
    - использовать методы со значением миксина (walk, talk)
    """
    def __init__(self, name):
        super().__init__(name)

    def swim(self):
        print(f"I'm {self.name} and I can swim")

    # def walk(self):
    #     print(f"I'm {self.name} and I can walk")

    # def talk(self):
    #     print(f"I'm {self.name} and I can talk")

class FishI(Creature,  SwimmerInterface):
    """
    Через миксин даем ем ту функциональность, котору мы хотим и НЕ БОЛЬШЕ!!!!!!

    можно через SUPER()


    """
    def __init__(self, name):
        super().__init__(name)

    # def swim(self):
    #     print(f"I'm {self.name} and I can swim")


fish = FishI('fish')
fish.swim()
# swim_from_parent


# Как результат, у рыбы нету метода talk()
fish.talk()
# AttributeError: 'FishI' object has no attribute 'talk'







