
# Django REST Framework: Привязка авторизованного пользователя при создании объекта
### Вопрос:
- как сохранить обьект и автоматичски привязать к нему авторизированного пользователя
- т.е. есть поле (owner/author/creator), то как его автоматически создать через сериализатор



# Методы сериализаторов в Django REST Framework

В Django REST Framework сериализаторы предоставляют несколько ключевых методов, которые могут быть переопределены для настройки поведения сериализации и десериализации данных. Каждый из этих методов играет свою роль в процессе преобразования данных и сохранения объектов.

## 1. `to_representation(self, instance)`

Этот метод отвечает за преобразование объекта модели в формат данных Python (например, словари и списки), который затем будет преобразован в JSON или другой формат для передачи через API. Этот метод вызывается при чтении данных, например, при возврате данных в ответ на запрос GET.

### Пример использования:

```python
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.username  # Преобразуем объект пользователя в его имя
        return representation
```

## 2. `to_internal_value(self, data)`

Этот метод преобразует входные данные (например, JSON) в формат, который сериализатор может использовать для валидации и сохранения данных. Метод используется при получении данных от клиента, таких как POST-запросы.

### Пример использования:

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        if 'title' in internal_value:
            internal_value['title'] = internal_value['title'].capitalize()  # Преобразуем заголовок в формат с заглавной буквы
        return internal_value
```

## 3. `validate(self, attrs)`

Этот метод выполняет валидацию всех полей данных. Он используется для выполнения кроссполевой валидации, то есть проверки взаимосвязанных данных между разными полями.

### Пример использования:

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'author']

    def validate(self, attrs):
        if 'badword' in attrs['title'].lower():
            raise serializers.ValidationError("Недопустимое слово в заголовке")
        return attrs
```

## 4. `create(self, validated_data)`

Метод `create` используется для создания нового объекта модели на основе проверенных данных. Этот метод вызывается, когда данные проходят валидацию и сохраняются через сериализатор.

### Пример использования:

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'author']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
```

В данном примере метод `create` переопределяется для автоматической установки текущего авторизованного пользователя в качестве автора создаваемой статьи.


## 5. `update(self, instance, validated_data)`

Метод `update` используется для обновления существующего объекта модели на основе проверенных данных. Этот метод вызывается, когда данные проходят валидацию и обновляют объект через сериализатор.

### Пример использования:

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'author']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
```

В этом примере метод `update` получает существующий объект `instance` и проверенные данные `validated_data`. 
Он обновляет поля `title` и `content` объекта, если они присутствуют в проверенных данных, и сохраняет изменения в базе данных. 
Метод затем возвращает обновленный объект.

Таким образом, метод `update` позволяет частично обновлять объект модели, сохраняя остальные поля неизменными.

## Почему метод `create` подходит для привязки авторизованного пользователя?

Метод `create` вызывается, когда создается новый объект через сериализатор. Это делает его идеальным местом для установки дополнительных данных, таких как текущий авторизованный пользователь, поскольку:

- **Инициализация нового объекта:** В момент вызова `create`, новый объект еще не создан, и мы можем добавить дополнительные поля или изменить данные перед созданием.
- **Контроль данных:** Мы можем модифицировать данные до их передачи модели, например, добавить текущего пользователя в качестве владельца (owner).
- **Логика привязки:** Поскольку метод вызывается только при создании новых объектов, он идеально подходит для добавления логики, связанной с инициализацией новых объектов, например, автоматической привязки пользователя.

## Пример реализации

Ниже приведен пример реализации сериализатора, который автоматически устанавливает текущего пользователя в качестве владельца объекта при его создании.

### Модель

```python
from django.contrib.auth.models import User
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
```

### Сериализатор

```python
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

```

### ViewSet

```python
from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.permissions import IsAuthenticated

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

## Пояснение

- **Модель `Article`** имеет поле `author`, которое связано с моделью `User`.
- **Сериализатор `ArticleSerializer`** переопределяет метод `create`, чтобы автоматически установить текущего авторизованного пользователя как автора статьи.
- **ViewSet `ArticleViewSet`** использует `perform_create`, чтобы вызвать метод `save` у сериализатора с переданным пользователем.

Таким образом, каждый раз, когда создается новый объект `Article` через этот сериализатор и ViewSet, он будет автоматически связан с текущим авторизованным пользователем.
