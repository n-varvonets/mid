
# Чистая архитектура и луковая архитектура

**Чистая архитектура** — это подход к разработке, который разделяет приложение на независимые слои. Это делает код более поддерживаемым, тестируемым и гибким к изменениям. Основная идея — бизнес-логика приложения не должна зависеть от внешних систем (баз данных, фреймворков, UI).

**Луковая архитектура** — это одна из реализаций чистой архитектуры, где слои системы представлены в виде "луковицы", где каждый слой зависит от внутреннего, но не наоборот.

# Основные слои луковой архитектуры в контексте Django (MVC)

### 1. Ядро (Core) — это **модель (Model)** в Django
- **Описание**: Модель отвечает за данные и бизнес-логику. Это основа, где определяется, как хранится информация и как она обрабатывается.
- **Пример**: Модель `Product`, которая хранит данные о товаре, и логика для расчёта цены с учётом скидки.

#### Пример кода:
```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class DiscountCalculator:
    @staticmethod
    def apply_discount(product, discount_percentage):
        # Логика расчёта скидки
        return product.price * (1 - discount_percentage / 100)
```

### 2. Входные интерфейсы (Use Cases) — это **вью (View)** в Django
- **Описание**: Вью получает запросы от пользователя, передаёт данные в бизнес-логику и возвращает ответ пользователю. Она связывает модель и представление данных.
- **Пример**: API для расчёта цены товара с учётом скидки.

#### Пример кода:
```python
from rest_framework.views import APIView
from rest_framework.response import Response

# Вью для расчёта цены продукта с учётом скидки
class CalculatePriceView(APIView):
    def post(self, request):
        product_data = request.data
        product = Product(product_data['name'], product_data['price'])
        discount_percentage = product_data['discount']
        # Вызов бизнес-логики для расчёта скидки
        final_price = DiscountCalculator.apply_discount(product, discount_percentage)
        return Response({"final_price": final_price})
```

### 3. Внешние интерфейсы (Adapters) — это **сериализация данных (Serializer)** в Django
- **Описание**: Сериализаторы преобразуют данные для передачи между моделями и внешними системами (например, API).
- **Пример**: Сериализация данных о товаре для передачи через API.

#### Пример кода:
```python
from rest_framework import serializers

# Сериализатор для модели Product
class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    price = serializers.FloatField()
```

### 4. Инфраструктурный слой (Infrastructure) — это **ORM и базы данных**
- **Описание**: Этот слой отвечает за сохранение данных в базу данных и их извлечение с использованием Django ORM.
- **Пример**: Использование ORM для взаимодействия с базой данных (например, сохранение и получение данных о товаре).

#### Пример кода:
```python
from django.db import models

# Модель для работы с базой данных через Django ORM
class ProductModel(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

    # Метод для сохранения продукта в базу данных
    def save_to_db(self):
        self.save()

    # Метод для получения продукта по имени
    @classmethod
    def get_product(cls, name):
        return cls.objects.get(name=name)
```

### Пример использования всех слоёв:

```python
# Вью для работы с продуктом через API
class ProductView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            # Создание объекта Product через сериализованные данные
            product = Product(**serializer.validated_data)
            # Вызов бизнес-логики для расчёта финальной цены
            final_price = DiscountCalculator.apply_discount(product, 10)
            return Response({"final_price": final_price})
        return Response(serializer.errors)
```

### MVC в контексте Django:

1. **Model** — это модель и бизнес-логика, такие как класс `Product` и расчёт скидок.
2. **View** — это вью, которая принимает запросы от пользователя, вызывает логику и возвращает ответ, как в классе `ProductView`.
3. **Controller** — здесь это функции вью (или сериализация), которые управляют бизнес-логикой и данными.

## Пример из реальной практики

Представьте интернет-магазин:

1. В **ядре** находится логика расчёта цены товаров и применяемых скидок.
2. На уровне **входных интерфейсов** — есть функция для получения итоговой цены заказа.
3. В **адаптерах** реализован интерфейс, который сохраняет заказ в базу данных или отправляет его по API.
4. **Инфраструктурный слой** — это реализация базы данных (например, PostgreSQL) или веб-сервер (например, Django).

Если вам нужно изменить базу данных с PostgreSQL на MongoDB, это затронет только внешний слой (инфраструктуру), но не бизнес-логику или интерфейсы.
