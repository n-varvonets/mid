##################### [S]INGLE RESPONSIBILITY #####################
# # - каждый класс должен иметь одну и только одну причину для изменения (должен отвечать только  за выполнение одной задачи
# или за одну часть функциональности системы)
# # - лучше много маленьких, чем ОДИН ГИГАНТСКИЙ КЛАСС
##################### [O]PEN/CLOSED #####################
# - про наследование, а не модификацию
##################### [L]ISKOV SUBSTITUTION #####################
# - инстанс родительского класса можно заменить на инстанс дочернего класса
# - через конкретизацию атрибутов и методов в родительском классе (чтобы избежать проблем, связанных с отсутствием
# унифицированного подхода обработке данных, т.е. для возможности перебора в цикле инстансов род и дочернего класса)
##################### [I]NTERFACE SEGREGATION #####################
# - Класс потомка не должен зависеть от ненужных методов родительского класса.
# - Решение:
# --- создаём миксины — небольшие классы с отдельными методами, которые наследуем только тогда, когда они нужны.т.е. подключать только нужные интрфейсы
# --- через композциции - способ построения объектов, при котором один объект включает в себя другие
# объекты(через передачу в конструктор обьекта) и использует их для выполнения своих задач. ЭТО ДАЖЕ УДОБНЕЙ ЧЕМ наследование МИКСинов.
##################### [D]EPENDENCY INVERSION #####################
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
# 1.1. проблема в том, что НА СЕЙЧАС есть DebitPaymentProcessorComposition, который зависит от authorizer: SMSAuthComposition,
# при том что мы знаем что использует конкртный тип 2ауф
# 1.2. а если создать АВС для DebitPaymentProcessorComposition и сказать ему реализовать метод verify, то тогда можно
# отнаследоваться от него и CreditPaymentProcessorComposition, который по своему реализует метод verify,
# НО будет выполнять одну и ту же задачу - проверить...ТО ТОГДА  Высокоуровневые модули НЕ БУДУТ зависеть от низкоуровневых модулей.

from abc import ABC, abstractmethod

class Order:
    items = []
    quantities = []
    prices = []
    status = "Open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total

class ProcessorSOLIDComposition(ABC):

    @abstractmethod
    def pay(self, order):
        pass


class SMSAuthComposition:   # no inherit

    authorized = False

    def verify_code(self, code):
        print(f"checking code {code} in correctness")
        self.authorized = True

    def is_verified(self) -> bool:
        return self.authorized


class DebitPaymentProcessorComposition(ProcessorSOLIDComposition):
    def __init__(self, security_code, authorizer: SMSAuthComposition):  # Нарушение DEPENDENCY INVERSION, потмоу что
        # данный класс ЗАВИСИТ ОТ передаваемого authorizer: SMSAuthComposition
        self.authorizer = authorizer
        self.security_code = security_code

    def pay(self, order):
        if not self.authorizer.is_verified():
            raise Exception("Not authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class CreditPaymentProcessorComposition(ProcessorSOLIDComposition):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class PayPalPaymentProcessorComposition(ProcessorSOLIDComposition):
    def __init__(self, email, authorizer: SMSAuthComposition):  # Нарушение DEPENDENCY INVERSION, потмоу что
        # данный класс ЗАВИСИТ ОТ передаваемого authorizer: SMSAuthComposition
        self.authorizer = authorizer
        self.email = email

    def pay(self, order):
        if not self.authorizer.is_verified():
            raise Exception("Not authorized")
        print("Processing PayPal payment type")
        print(f"Verifying security code: {self.email}")
        order.status = "paid"

order = Order()
order.add_item("keyboard", 1, 58)
order.add_item("SSD", 1, 150)
order.add_item("USB Cable", 2, 7)

print(order.total_price())
authorizer = SMSAuthComposition()
processor_paypal = PayPalPaymentProcessorComposition("nick@gmail.com", authorizer)
processor_paypal.authorizer.verify_code("2265")
processor_paypal.pay(order)

# --- Solution ---
# 1. делаем АБС класс от зависмого передавемого класса(SMSAuthComposition), в котором определяем методы для реализации(verify_code)

class ABCSMSAuthComposition(ABC):
    """
    делаем обьязательным  методом для все подклассов только verify_code
    """
    @abstractmethod
    def verify_code(self, code):
        pass

# 2. делаем завимый класс - сабклассом АБС
class SMSAuthCompositionDependancyInv(ABCSMSAuthComposition):

    authorized = False

    def verify_code(self, code):
        print(f"checking code {code} in correctness")
        self.authorized = True

    def is_verified(self) -> bool:
        return self.authorized

# 3. и теперь в пайпал мы можем передать не зависимый КОНКРЕТНЫЙ класс SMSAuthComposition, а его абстрацию ABCSMSAuthComposition,
# которая может реализовать 2+ типов 2auth... гланое методы должны быть реализованы в обоих типах

class PayPalPaymentProcessorCompositionDependancyInv(ProcessorSOLIDComposition):
    # def __init__(self, email, authorizer: SMSAuthComposition):  # Нарушение DEPENDENCY INVERSION
    def __init__(self, email, authorizer: ABCSMSAuthComposition):   # передаем абстракцию ABCSMSAuthComposition, НЕ НАРУШАЯ DEPENDENCY INVERSION
        self.authorizer = authorizer
        self.email = email

    def pay(self, order):
        if not self.authorizer.is_verified():
            raise Exception("Not authorized")
        print("Processing PayPal payment type")
        print(f"Verifying security code: {self.email}")
        order.status = "paid"


# 4. к примеру, я могу добавить ЕЩЕ ОДИН ТИП АВТОРИЗАЦИИ и передать его в дебит,а не пйпал

class NoneRobotAuthDependancyInv(ABCSMSAuthComposition):

    authorized = False

    def verify_code(self, code):
        print(f"checking code {code} in correctness")
        self.authorized = True

    def is_verified(self) -> bool:
        return self.authorized



class DebitPaymentProcessorCompositionDependancyInv(ProcessorSOLIDComposition):


    # def __init__(self, security_code, authorizer: SMSAuthComposition):  # Нарушение DEPENDENCY INVERSION
    def __init__(self, security_code, authorizer: NoneRobotAuthDependancyInv):   # передаем абстракцию NoneRobotAuthDependancyInv, НЕ НАРУШАЯ DEPENDENCY INVERSION
        self.authorizer = authorizer
        self.security_code = security_code

    def pay(self, order):
        if not self.authorizer.is_verified():
            raise Exception("Not authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

