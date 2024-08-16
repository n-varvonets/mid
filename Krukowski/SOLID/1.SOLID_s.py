# [S]INGLE RESPONSIBILITY
# [O]PEN/CLOSED
# [L]ISKOV SUBSTITUTION
# [I]NTERFACE SEGREGATION
# [D]EPENDENCY INVERSION
# крепкий/добротный - принципы и правила - это все хорошо, но не стоит забывать о здравом смысле,
# т.е. нен стоит быть слишком педантичным и следовать всем правилам и довыдам

# --- Problem --- Один класс, должен иметь только одну зону ответсвенности
class ExportCsv:
    """
    Данный класс нарушает принцип # [S]INGLE RESPONSIBILITY:
    - один класс покрывает сразу две зоны ответственности:
        - он форматирует данные(def prepare)
        - и что-то куда-то пишет (def write_file(self, filename))
    """
    def __init__(self, raw_data):
        self.data = self.prepare(raw_data)

    def prepare(self, raw_data):
        result = ''
        for item in raw_data:
            new_line = ','.join(
                (
                    item['name'],
                    item['surname'],
                    item['occupation']
                )
            )
            result += f"{new_line}\n"
        return result

    def write_file(self, filename):
        with open(filename, 'w', encoding='UTF8') as f:
            f.write(self.data)


data = [
    {
        'name': 'Sherlock',
        'surname': 'Holmes',
        'occupation': 'Detective'
    },
    {
        'name': 'John',
        'surname': 'Watson',
        'occupation': 'doctor'
    },
]

exporter = ExportCsv(data)
exporter.write_file('out.csv')

# --- Solving --- Один класс, должен иметь только одну зону ответсвенности.
# Т.е. нужно разбить данный класс на два

class FormatData:
    """Класс по подготовки данных """

    def __init__(self, raw_data):
        # self.data = self.prepare(raw_data)  # изначально просто будет сырые данные
        self.raw_data = raw_data   # ччто б в def prepare использовать аттрибуты класса, а не пердавать напрямую

    # def prepare(self, raw_data):
    def prepare(self):  # берем уже параметры с класса через self
        result = ''
        for item in self.raw_data:
            new_line = ','.join(
                (
                    item['name'],
                    item['surname'],
                    item['occupation']
                )
            )
            result += f"{new_line}\n"
        return result

########################### мой вариант(до просмотра) - работает, но лучше с инит #######################
# class ExportCSV:
#     def write_file(self, data, filename):
#         with open(filename, 'w', encoding='UTF8') as f:
#             f.write(data)
#
#
# formatter = FormatData(data)
# formatted_data = formatter.prepare()
# exporter = ExportCSV()
# exporter.write_file(formatted_data, 'out.csv')
########################### end my option #######################

class FileWriter:
    def __init__(self, file_name):
        self.file_name = file_name

    def write_file(self, formatted_data):
        with open(self.file_name, 'w', encoding='UTF8') as f:
            f.write(formatted_data)


formatter = FormatData(data)
formatted_data = formatter.prepare()
exporter = FileWriter('out_2.csv')
exporter.write_file(formatted_data)

# Как результат,
# - каждый класс выполняет свою работу, т.е. имеет свою зону ответсвенности
# - т.е. НЕ НУЖНО СОЗДАВАТЬ ОДИН ГИГАНТСКИЙ КЛАСС, КОТОРЫЙ ДЕЛАЕТ ВСЕ



