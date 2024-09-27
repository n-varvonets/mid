from datetime import date


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @staticmethod
    def fromFathersAge(name, fatherAge, fatherPersonAgeDiff):
        return Person(name, date.today().year - fatherAge + fatherPersonAgeDiff)

    @classmethod
    def fromBirthYear(cls, name, birthYear):
        return cls(name, date.today().year - birthYear)

    def display(self):
        print(self.name + "'s age is: " + str(self.age))


class Man(Person):
    sex = 'Male'


def func2(a=[], b=[]):  #
    a.append(b)
    return a,


man = Man.fromBirthYear('John', 1985)
print(isinstance(man, Man))  # True
print(type(man))  # class man

man1 = Man.fromFathersAge('John', 1965, 20)
print(isinstance(man1, Man))  # False
print(func2(['Petro']))  # (['Petro',[]], )

