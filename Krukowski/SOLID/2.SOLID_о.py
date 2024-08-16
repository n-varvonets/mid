# [S]INGLE RESPONSIBILITY - лучше много маленьких, чем ОДИН ГИГАНТСКИЙ КЛАСС
# [O]PEN/CLOSED - про наследование, а не модификацию
# [L]ISKOV SUBSTITUTION
# [I]NTERFACE SEGREGATION
# [D]EPENDENCY INVERSION
# крепкий/добротный - принципы и правила - это все хорошо, но не стоит забывать о здравом смысле,
# т.е. нен стоит быть слишком педантичным и следовать всем правилам и довыдам

# --- Problem --- Класс можно расширять, НО НАПРЯМУЮ НЕ МОДФИЦИРОВАТЬ (НАСЛЕДОВАНИЕ)
import sys
import time

class Logger:
    def log(self, message):
        current_time = time.localtime()
        sys.stderr.write(f"{time.strftime('%Y-%b-%d %H:%M:%S', current_time)} --> {message}\n")
        # дальше к примеру,
        # 1. нужно убрать время (%H:%M:%S) по заданию на сейчас , убираем
        # sys.stderr.write(f"{time.strftime('%Y-%b-%d %H:%M:%S', current_time)} --> {message}\n")
        # 2. проходит время и нужно добавить обратно...
        # - и это как раз и нарушает Opened/Closed

logger = Logger()
logger.log('An error has happened!')

# --- Solving ---
# 1. создать инит, что б именно там задавать метку времени... и в завсимости от РИКВЕСТА пользователя,
# давать ему либо '%Y-%b-%d %H:%M:%S' либо '%Y-%b-%d'


class OpenedClosedLogger:
    def __init__(self):

        self.prefix = time.strftime('%Y-%b-%d %H:%M:%S', time.localtime())
        print(self.prefix)

    def log(self, message):
        sys.stderr.write(f"{self.prefix} --> {message}\n")


# 2. дальше если кого-то не устравивает данный класс, то создайте подкласс, который будет наследовать логгер класс,
# т.е. в исходный класс не вносить изменения
class CustomLogger(OpenedClosedLogger):
        # def __init__(self):
        #     # print(self.prefix) 1. упадет ошибка принта, т.к. не было супер() и в области видимости нет self.prefix
        #     # 2. но ниже будет перваая инициализация self.prefix, не было супер()
        #     self.prefix = time.strftime('%Y-%b-%d', time.localtime())
        #     print(self.prefix)


        def __init__(self):
            super().__init__()
            # 3. но если будет супер(), то в родильском классе пройдет инициализация self.prefix
            print(self.prefix)  # и здесь будет значение
            # а дальше просто переопределим переменную self.prefix
            self.prefix = time.strftime('%Y-%b-%d %H:%S', time.localtime())
            print(self.prefix)

logger = CustomLogger()
logger.log('An error has happened!')




