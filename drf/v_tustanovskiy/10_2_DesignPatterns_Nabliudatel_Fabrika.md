
# Паттерны проектирования: "Наблюдатель" и "Фабрика"

## Паттерн "Наблюдатель"

**Описание:**
Паттерн "Наблюдатель" позволяет объектам получать уведомления об изменении состояния другого объекта, который они "наблюдают". Центральный объект (издатель) содержит список наблюдателей и уведомляет их о событиях, вызывая их методы. В Django REST Framework этот паттерн можно использовать для реагирования на изменения в моделях данных, например, через систему сигналов Django.

**Пример использования в Django REST Framework:**

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp.models import MyModel

@receiver(post_save, sender=MyModel)
def my_model_changed(sender, instance, **kwargs):
    # Логика обработки после сохранения объекта
    pass
```

## Паттерн "Фабрика"

**Описание:**
Паттерн "Фабрика" используется для создания объектов без указания конкретных классов продуктов. Фабрика определяет метод для создания объектов, а наследники этого класса реализуют этот метод, создавая объекты различных классов. В DRF паттерн можно использовать для создания сериализаторов, представлений или объектов ответов в зависимости от контекста запроса или данных.

**Примеры использования в Django REST Framework:**

1. **Фабрика сериализаторов:**
   Можно использовать разные сериализаторы для разных типов пользователей или действий:

```python
class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_admin:
            return AdminSerializer
        return UserSerializer
```

2. **Фабрика представлений:**
   Настройка поведения API в зависимости от параметров запроса:

```python
class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return MyModelListSerializer
        elif self.action == 'retrieve':
            return MyModelDetailSerializer
        return DefaultSerializer
```

Эти паттерны помогают структурировать программы для улучшения гибкости и расширяемости, а также для автоматической обработки зависимостей и уведомлений.
