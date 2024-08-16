##################### [S]INGLE RESPONSIBILITY #####################
# # - каждый класс должен иметь одну и только одну причину для изменения (должен отвечать только за одну часть
# # функциональности системы или за выполнение одной задачи)
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
# 1. auth_sms
# 1.1. добавлили auth_sms к PaymentProcessor
# 1.2. как в DebitPaymentProcessor, который меняет флаг при ретурне + в инит self.verified = False
# 1.3. как в PayPalPaymentProcessor, который меняет флаг при ретурне + в инит self.verified = False
# 1.4. но CreditPaymentProcessor не будет иметь auth_sms --> raise exeption
# 2. в PayPalPaymentProcessor добавили проверку флага на self.verified = True

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
class PaymentProcessor(ABC):

    @abstractmethod
    def auth_sms(self, code):
        pass

    @abstractmethod
    def pay(self, order):
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code
        self.verified = False

    def auth_sms(self, code):
        print(f"Verifing SMS code {code}")
        self.verified = True

    def pay(self, order):
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    def auth_sms(self, code):
        raise Exception("Credit card payment don't support SMS auth")   #  By some reason Credit doesn't support auth

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class PayPalPaymentProcessor(PaymentProcessor):
    def __init__(self, email):
        self.email = email
        self.verified = False

    def auth_sms(self, code):
        print(f"Verifing SMS code {code}")
        self.verified = True
    def pay(self, order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing PayPal payment type")
        print(f"Verifying security code: {self.email}")
        order.status = "paid"

processor = PayPalPaymentProcessor("hello_world@gmail.com")

#####################################################################################
# Problem - не все сабклассы, поддерживают auth_sms #################################
# --- Solution_1 ЧЕРЕЗ МИКСИНЫ--- , поэтому лучше создать отдельные интерфейсы ДЛЯ этого (МИКСИНЫ)##
#####################################################################################

# 1.1. уберем из АВС необходимый метод
# 1.2. Создадим миксинотнаследуваемого от начального АВС
# 1.3. добавим через наследование миксин с ауф фичей там где нужно(DebitPaymentProcessor и PayPalPaymentProcessor)
# 2. уберем УЖЕ НЕНУЖНЫЙ метод auth_sms с CreditPaymentProcessor

class PaymentProcessorSOLID(ABC):

    @abstractmethod
    def pay(self, order):
        pass


class AuthSolidMixin(PaymentProcessorSOLID):
    @abstractmethod
    def auth_sms(self, code):
        pass


class DebitPaymentProcessor(AuthSolidMixin):
    def __init__(self, security_code):
        self.security_code = security_code
        self.verified = False

    def auth_sms(self, code):
        print(f"Verifing SMS code {code}")
        self.verified = True

    def pay(self, order):
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    # def auth_sms(self, code):
    #     raise Exception("Credit card payment don't support SMS auth")   # теперь он нам не нужен и это будет работать

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class PayPalPaymentProcessor(AuthSolidMixin):
    def __init__(self, email):
        self.email = email
        self.verified = False

    def auth_sms(self, code):
        print(f"Verifing SMS code {code}")
        self.verified = True
    def pay(self, order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing PayPal payment type")
        print(f"Verifying security code: {self.email}")
        order.status = "paid"


# Как результат, нету общего интерфейса мы разделил его по сабклассам

# --- Solution_2 ЧЕРЕЗ КОМПОЗИЦИИ---
# 1. у нас есть auth_sms метод в AuthSolidMixin, НО мы так же можем создать отдельный класс КОМПОЗИЦИЯ с одной логикической задачей, но с двумя методами:
# - подверждает верфикацию, т.е. делает self.verified = Тру
# - проверкой, является ли обьект self.verified = Тру --> bool
# 2.КОМПОЗАЦИЯ это когда создаешь класс и передаешь его как параметр при инициализации, что б он умел использовать
# методы и аттрибуты нпередаваемого класса


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

# We don't need it anymore
# class AuthSolidMixin(PaymentProcessorSOLID):
#     @abstractmethod
#     def auth_sms(self, code):
#         pass

class DebitPaymentProcessorComposition(ProcessorSOLIDComposition):  # get ABC with pay method only
    def __init__(self, security_code, authorizer: SMSAuthComposition):
        self.authorizer = authorizer  # передаем обьект КОМПОЗИТОРА
        self.security_code = security_code
        # self.verified = False  # - больше не нужно, потмоу что КОМПОЗИТОР возращает бул значение

    # - больше не нужно, потмоу что КОМПОЗИТОР иммет данный метод
    # def auth_sms(self, code):
    #     print(f"Verifing SMS code {code}")
    #     self.verified = True

    def pay(self, order):
        # if not self.verified: - больше не нужно, потмоу что КОМПОЗИТОР иммет данный метод
        #     raise Exception("Not authorized")
        if not self.authorizer.is_verified():
            raise Exception("Not authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class CreditPaymentProcessorComposition(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    # def auth_sms(self, code):
    #     raise Exception("Credit card payment don't support SMS auth")   # теперь он нам не нужен и это будет работать

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class PayPalPaymentProcessorComposition(ProcessorSOLIDComposition):  # get ABC with pay method only
    def __init__(self, email, authorizer: SMSAuthComposition):
        self.authorizer = authorizer  # передаем обьект КОМПОЗИТОРА
        self.email = email
        # self.verified = False  # - больше не нужно, потмоу что КОМПОЗИТОР возращает бул значение

    # - больше не нужно, потмоу что КОМПОЗИТОР иммет данный метод
    # def auth_sms(self, code):
    #     print(f"Verifing SMS code {code}")
    #     self.verified = True

    def pay(self, order):
        # if not self.verified: - больше не нужно, потмоу что КОМПОЗИТОР иммет данный метод
        #     raise Exception("Not authorized")
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

###################################### SIMPLE EXAMPLE OF COMPOSTION #################################
class Engine:
    def start(self):
        print("Engine started")


class Car:
    def __init__(self, engine):
        self.engine = engine  # здесь через контруктор передаем другой обьект

    def drive(self):
        self.engine.start()   # здесь композиции использования
        print("Car is moving")


engine = Engine()
car = Car(engine)
car.drive()
###########################################################################################





