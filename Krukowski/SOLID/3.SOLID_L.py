# [S]INGLE RESPONSIBILITY - лучше много маленьких, чем ОДИН ГИГАНТСКИЙ КЛАСС
# [O]PEN/CLOSED - про наследование, а не модификацию
# [L]ISKOV SUBSTITUTION
# - инстанс родительского класса можно заменить на инстанс дочернего класса
# - конкретизацию атрибутов и методов в родительском классе (чтобы избежать проблем, связанных с отсутствием унифицированного подхода обработке данных)
# [I]NTERFACE SEGREGATION
# [D]EPENDENCY INVERSION
# крепкий/добротный - принципы и правила - это все хорошо, но не стоит забывать о здравом смысле,
# т.е. нен стоит быть слишком педантичным и следовать всем правилам и довыдам

# --- Problem --- инстанс родительского класса должен работать с инстансом сабкласса
# !!!что приводит к невозможности перебора в цикле инстансов род и дочернего
class Animal:
    def __init__(self, attrs):
        self.attributes = attrs

    def eat(self):  # ТОЛЬКО СЕЛФ в родительском
        print("Ate some food!")

class Cat(Animal):
    def eat(self, amount = 0.1):  #  СЕЛФ и еще один аттрибут в дочернем
        if amount > 0.3:
            print("Can't eat that much!")
        else:
            print("Ate some cat food!")

class Dog(Animal):
    def eat(self):  # ТОЛЬКО СЕЛФ в дочернем и нету amount
        print("Ate some dog food!")

pluto = Dog({'name': 'Pluto', 'age': 3})  # через аргументы
goofy = Dog({'name': 'Goofy', 'age': 2})    # через аргументы
leo = Cat({'Mr. Leo', 4})  # через тапл - проблема - нет требований как задать аттриубты

# PROBLEM!!!что приводит к неворзможности перебора в цикле инстансов род и дочернего
animals = (pluto, goofy)  # leo
# animals = (pluto, goofy, leo)  # TypeError: 'set' object is not subscriptable
for animal in animals:
    if animal.attributes['age'] > 2:
        print(animal.attributes['name'])

# 1.мы не можем легко заменить род.класс Animal на дочерний класс Cat, потому что у него появился новый аргумент
# 2. у нас НЕТУ ОБЩЕГО ИНТЕРФЕЙСА, что б удобно  задавать аттрибуты животным(нету инита в дочерних).
# проблема - нет требований как задать аттриубты, что приводит к ситуации невозможности замены род. класса на дочерний


# --- Solving ---
# 1. В род.классе зададим требования к аттрибутам
# 2. позовлим дочерним классам иметь аттрибут _amount, через указание его в род классе, который не будет обьязательным(приватным)
class AnimalLiskovSubstitution:
    def __init__(self, name, age):  # 1.1.не просто attrs,а конкретизируем что именно и в род.классе сделаем нужный формат
        self.attributes = {'name': name, 'age': age}

    def eat(self, _amount = 0):  # 2.добавим необязтельный аттрибут в род классе, что б его могли использовать
        print("Ate some food!")

class Cat(AnimalLiskovSubstitution):
    def __init__(self, name, age):  # 1.2. в дочернем будем делигировать инициализацию аттрибутов через род.класс, т.е. задаем требования
        super().__init__(name, age)

    def eat(self, _amount = 0.1):
        if _amount > 0.3:
            print("Can't eat that much!")
        else:
            print("Ate some cat food!")

class Dog(AnimalLiskovSubstitution):

    def __init__(self, name, age):  # 1.3. тоже самое и для еще одного дочернего
        super().__init__(name, age)

    def eat(self, _amount):  # 2.  ну и для собаки тоже добавим аттрибут... НУ А ДАЛЬШЕ САМИ РЕШАЕМ, ИСПОЛЬЗОВАТЬ ЕГО ИЛИ НЕТ
        print("Ate some dog food!")

# pluto = Dog({'name': 'Pluto', 'age': 3})  # OLD через аргументы
# goofy = Dog({'name': 'Goofy', 'age': 2})    # OLD через аргументы
pluto = Dog('Pluto', 3)  # NEW просто прокидываются значения при инициализации обьекта
goofy = Dog('Goofy', 2)    # NEW просто прокидываются значения при инициализации обьекта
leo = Cat('Mr. Leo', 4)  # NEW просто прокидываются значения при инициализации обьекта

# PROBLEM!!!теперь уже можно заменить род.инстанс на дочерний
animals = (pluto, goofy, leo)  #  НЕТУ УЖЕ - TypeError: 'set' object is not subscriptable
for animal in animals:
    if animal.attributes['age'] > 2:
        print(animal.attributes['name'])
