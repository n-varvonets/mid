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
# - более высокуровневые модули, не должны зависить от более низкоуровевых модулей,
# - а в идеале они должны зависиь от абстракций, при том что
# -- абракции не должны зависить от делателей,а наооборот.. детали должны зависить от абстракций
import sys
import time


# 1. Есть два класса, которые умеют печатать сообщения
# - либо в терминал
# - либо в файл
# 2. Есть логер класс  с
# - автодатой, как префикс
# - и два метода, которые "печатают мсдж в НУЖНОЕ МЕСТО(используя чужие классы)" - ЭТО и есть нарушение DEPENDENCY INVERSION...почему?
class TerminalPrinter:
    def write(self, msg):
        sys.stderr.write(f"{msg}\n")

class FilePrinter:
    def write(self, msg):
        with open('log.txt', 'a+', encoding='UTF8') as f:
            f.write(f"{msg}\n")

class Logger:
    """
    Потмому что данный класс ЗАВИСИТ от 2х ДРУГИХ классов,
    и нету какой-то абстрацкции которая умеет печатать и ВСЕ!

    Т.е. должын обьязатолкьо:
    - классы TerminalPrinter и FilePrinter
    - так у них обьязательно должно быть реализованы по методу write...
    т.е. очень много деталей и класс Logger зависит от других деталей
    """
    def __init__(self):
        self.prefix = time.strftime('%Y-%b-%d %H:%M:%S', time.localtime())

    def log_stderr(self, message):
        TerminalPrinter().write(f"{self.prefix} {message}")

    def log_file(self, message):
        FilePrinter().write(f"{self.prefix} {message}")

# --- Solving ---
# 1. TerminalPrinter и FilePrinter - не трогаем, т.к. они не нарушают никаких принципов(SOLI..)
# 2. класс логер будет приниманать абстрацкцию, а не зависит от абстракции

class LoggerSOLID:

    def __init__(self):
        self.prefix = time.strftime('%Y-%b-%d %H:%M:%S', time.localtime())

    def log(self, message, printer):  # printer - абстракция общего действия напчеатать(один в терминал, второй в файл)
        """"
        - у абстракции должен быть реализован метод write()
        - т.е. нам не важно что это будет за к
        ласс, главное что б передваемый класс реализовыал метод write()
        - в программе можно создать таких классов сколько угодно
        """
        # printer.write(f"{self.prefix} {message}")
        printer().write(f"{self.prefix} {message}") # !!! WARN. что б этот метод сработал, нам нужно
        print(f"file {self.prefix} was created")
        # класс FilePrinter вызвать(инициализровать->сделать инстанс)

    # def log_stderr(self, message):
    #     TerminalPrinter().write(f"{self.prefix} {message}")
    #
    # def log_file(self, message):
    #     FilePrinter().write(f"{self.prefix} {message}")


logger = LoggerSOLID()
# logger.log_file('starting_program')  # куже не нужен спецефический метод log_file
logger.log('starting_program', FilePrinter)   # а просто указать интерфейс через какой печатать