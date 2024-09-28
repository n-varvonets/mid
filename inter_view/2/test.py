# Task1
# product
# id  company_id
# 1   2
# 2   1
# 3   1
#
# company
# id
# 1
# 2
#
# Suppose you would like to order companies from company table by number of products that they have in product table?


# SELECT company.id, COUNT(product.id) AS product_count  -- Выбираем ID компании и считаем количество продуктов для каждой компании
# FROM company
# LEFT JOIN product ON company.id = product.company_id   -- Присоединяем таблицу продуктов к таблице компаний, используя company_id, чтобы включить все компании
# GROUP BY company.id                                    -- Группируем результаты по ID компании для агрегирования количества продуктов для каждой компании
# ORDER BY product_count DESC;                           -- Сортируем компании по количеству продуктов в порядке убывания


# Task2
# Implement @square decorator that will put the result function to the power of two?
def square(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result ** 2
    return wrapper


# Task3
# Suppose that you need to parse a file with several JSON written in a row and you need to separate them for future processing?
# Create a function that as input will receive string of several JSON merged together and as output will receive list of dictionaries?
# Input
# {“hello”: 1}{“good bye”: 2}
import json


def separate_string_to_types(json_string: str):
    result_list = []

    json_string = json_string.replace('“', '"').replace('”', '"')
    list_separate_json = json_string.replace("}{", "},{")
    list_separate_json = f"[{list_separate_json}]"

    json_objects = json.loads(list_separate_json)

    result_list.append(json_objects)

    print(result_list)


separate_string_to_types('{“hello”: 1}{“good bye”: 2}')
