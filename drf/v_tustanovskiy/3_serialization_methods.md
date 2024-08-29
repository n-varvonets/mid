
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

### Последовательность вызова:
1. `to_representation` вызывается в процессе сериализации данных, т.е. при возврате данных через API (например, при запросах GET).
2. Контроль передается на уровень формата данных, который может быть преобразован в JSON и отправлен в ответе.

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

### Последовательность вызова:
1. `to_internal_value` вызывается при десериализации данных, т.е. когда клиент отправляет данные на сервер (например, при POST-запросе).
2. Контроль передается следующему этапу — валидации данных (методы `validate_<field>` и `validate`).

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

### Последовательность вызова:
1. `validate` вызывается после `to_internal_value`, когда данные готовы к валидации.
2. Контроль передается на этап сохранения данных (методы `create` или `update`).

## 4. `validate_<field>(self, value)`

Этот метод отвечает за валидацию конкретного поля. Например, вы можете создать метод `validate_title`, который будет вызываться для валидации значения поля `title`.

### Пример использования:

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def validate_title(self, value):
        if 'badword' in value.lower():
            raise serializers.ValidationError("Недопустимое слово в заголовке")
        return value
```

### Последовательность вызова:
1. `validate_<field>` вызывается в процессе валидации данных на уровне конкретного поля, до вызова общего метода `validate`.
2. После успешной валидации поле передается дальше для кроссполевой валидации (метод `validate`).

## 5. `validate_value(self, value)`

Метод `validate_value` может быть использован для валидации значения, но его отличие от `to_internal_value` и `validate` в том, что он, как правило, используется в случае необходимости валидировать значение до того, как оно будет преобразовано сериализатором или до валидации всего объекта. Этот метод вызывается вручную и не является частью стандартной цепочки вызовов.

### Пример использования:

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def validate_value(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Значение слишком короткое")
        return value
```

### Последовательность вызова:
1. `validate_value` вызывается вручную, когда нужно проверить отдельное значение перед тем, как оно будет передано на дальнейшую обработку.
2. Контроль может быть передан на этапы десериализации (`to_internal_value`) или валидации (`validate`).

## 6. `create(self, validated_data)`

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

### Последовательность вызова:
1. `create` вызывается после успешной валидации данных.
2. Контроль передается на уровень модели для создания нового объекта.

## 7. `update(self, instance, validated_data)`

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

### Последовательность вызова:
1. `update` вызывается после успешной валидации данных и используется для обновления существующего объекта.
2. Контроль передается на уровень модели для сохранения обновленного объекта.


## Пример вызова методов сериализатора

```python
# Предположим, что мы получили данные через запрос POST и хотим обработать их через сериализатор.
# В этом примере мы будем создавать новую статью.

data = {'title': 'My New Article', 'content': 'This is the content of the article.'}

# Создаем экземпляр сериализатора с данными
serializer = ArticleSerializer(data=data)

# Вызываем метод is_valid, который последовательно вызовет методы to_internal_value, validate_<field>, validate
if serializer.is_valid():
    # Если данные валидны, вызывается метод create или update, в зависимости от контекста
    article = serializer.save()

    # вернуть сериализованные данные, следует вызвать serializer.data, который за
    # кулисами вызовет to_representation для преобразования объекта модели в формат данных
    return Response(serializer.data, status=201)

#  Если же возвращаются ошибки или другие данные, не связанные с сериализацией объекта модели,
#  to_representation не будет задействован.
return Response(serializer.errors, status=400)
```

### Последовательность выполнения:
1. `to_internal_value` вызывается первым при инициализации сериализатора с данными.
2. `validate_<field>` и `validate` вызываются после `to_internal_value` во время выполнения `is_valid()`.
3. Если данные прошли валидацию, вызывается метод `save()`, который внутри себя вызовет либо `create`, либо `update` в зависимости от того, передан ли в сериализатор объект `instance`.
4. При успешном сохранении объекта, для возврата данных используется `serializer.data`. Этот атрибут инициирует вызов `to_representation`, который преобразует объект модели обратно в сериализованный формат данных для ответа. 
   1. Если `is_valid()` возвращает False, то в ответ возвращаются ошибки валидации через `serializer.errors`. В этом случае `to_representation` **не вызывается**, так как данные, возвращаемые в errors, не требуют сериализации объекта модели.


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
