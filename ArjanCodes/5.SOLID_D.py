#1.#################### [S]INGLE RESPONSIBILITY #####################
# # - каждый класс должен иметь одну и только одну причину для изменения
# # -- и причина изменений может быть **заинтересованное лицо**
# # --- т.е. если приложение разрабатывается и оно нужно АДМИНУ, ОПЕРАТОРУ и КЛИЕНТУ, то
# # --- нужно делать модули так, что б елс АДМИН попросил внести какую-то фичу, то ОНА НЕ ЛОШЛЖНА ПОВЛИЯТЬ на других **заинтересованных лиц**

# правильно назначая ответсвенность/ОБЯЗАННОСТИ обьекту
# проблема задачи была в том что что у менеджера была двойная ответсвенность..
# - он задачами управлял
# - и отвечал за начисление зп.. не правильно
# Или еще пример
# -пришем программу, которая моделириует торговлю молоком, то "где должна быть цена  о стоимости пакета мололка при ООП дизейне?"
# - цена должна ли быть классе Оредер или классе пакет Молоко?
# - если в пакете Молока, то это неправильно, ведь молоку пофиг, а диструбютер может быть разный от степени жадности, где 1$, где 2$,

# причину для изменения
# Если меняется логика конкретной функциональности, должен изменяться только тот класс, который за неё отвечает.
# Например, изменения в процессе заказа должны касаться только классов, связанных с заказом, а не с клиентом.
#  Если класс отвечает за несколько задач, то нужно Разделенить обязанности

#2.#################### [O]PEN/CLOSED #####################
# - про наследование(расшряешь функциональность потомком), а не модификацию(внутри искомого класса)
# - не про наследование, нно про расширение функциональност - КОМПОЗИЦИЯ, по сравнению наследования:
# --- плюсы(обьекты становятся не такими зависимоми друг от друга, т.е. более слабая связь между ними, как следствие
# ----- легче масштабировать и вносить новый функционал НЕ СТРОЯ огромную иерархическую структуру
# --- минусы: тот же самый плюс, если не правильно применять, то все будет разбито и не будет связи

#3.#################### [L]ISKOV SUBSTITUTION(ПОДСТАВИВ) #####################
# - инстанс родительского класса можно ВСЕГДА заменить на инстанс дочернего класса(ПОДСТАВИВ)
# - через конкретизацию атрибутов и методов в родительском классе (чтобы избежать проблем, связанных с отсутствием
# унифицированного подхода обработке данных, т.е. для возможности перебора в цикле инстансов род и дочернего класса)

#4.#################### [I]NTERFACE SEGREGATION #####################
# - Класс потомка не должен зависеть от ненужных методов родительского класса.
# - Решение:
# --- создаём миксины — небольшие классы с отдельными методами, которые наследуем только тогда, когда они нужны.т.е. подключать только нужные интрфейсы
# --- через "КОМПОЗИЦИИ" - способ построения объектов, при котором один объект включает в себя другие
# объекты(через передачу в конструктор обьекта) и использует их для выполнения своих задач. ЭТО ДАЖЕ УДОБНЕЙ ЧЕМ наследование МИКСинов.

#5.#################### [D]EPENDENCY INVERSION #####################
# 5.1 Высокоуровневые модули не должны зависеть от низкоуровневых модулей. Оба должны зависеть от абстракций.
# 5.2. Абстракция не должна зависить от реализации, А НАООБОРОТ - реализация должна зависеть от абстракции

# Стрелки свзей всікоуровнего, как и никоуровнего обе ведут ТОЛЬКО В ЄТУ АБСТРАКЦИЮ
# Низкоуровневые модули, в свою очередь, реализуют эту абстракцию. СтрелкТаким образом, можно легко заменять низкоуровневые модули,
# не изменяя код высокоуровневого модуля, поскольку он работает с абстракцией, а не с конкретной реализацией.
# Пример:
## 1.1.Работа с базой данных через ORM позволяет бизнес-логике не зависеть от конкретной базы данных (например, PostgreSQL,
# MySQL, SQLite). Вместо этого, программа обращается к абстрактным методам ORM,
# которые сами выбирают, как взаимодействовать с каждой из баз данных.
# Т.Е. ВЫСОКОУРОВНЕВЫЙ ORM ниче НЕ ЗНАЕТ о НИЗКОУРОВНЕвом sql и бд

# 2.1. Представь, что у тебя есть разные игрушечные машинки: одна работает на батарейках, а другая на солнечных панелях.
# Если ты хочешь, чтобы твой пульт управления мог управлять любой из этих машинок, не нужно менять пульт для каждой машинки.
# Вместо этого, все машинки должны использовать одну и ту же кнопку «вперёд» и «назад», которая подходит ко всем пультам.
# 2.2.Теперь бизнес-логика не зависит от конкретной базы данных, а лишь от интерфейса Database.

# 3. Броке  ры - микросервеси ненапрямую взаимдействуют друг с другом, а через некую абстракцию(брокера), при том что сервисы не подозревают о существовании друг друга

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

