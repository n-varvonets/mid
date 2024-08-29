
# Подробное описание использования HyperlinkedModelSerializer в Django REST Framework

## Модели:

```python
from django.db import models

class Author(models.Model):
    # как вью понимает что у автора есть гиперссылки на его статьи?
    # через (Author, related_name='articles'), что позволяет получить все статьи автора через author.articles.
    # Пользователь переходит по ссылке "http://api.example.com/authors/1/" и видит данные автора, включая гиперссылки на его статьи.
    name = models.CharField(max_length=100)

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # related_name='articles' указывает, что для модели Author будет автоматически создано свойство articles, которое возвращает все связанные статьи.
    author = models.ForeignKey(Author, related_name='articles', on_delete=models.CASCADE)
    published_date = models.DateField()

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### Комментарии к моделям:
- **Author**: Модель автора статей с одним полем `name`.
- **Article**: Модель статьи с полями `title`, `content`, `author` (внешний ключ на `Author`) и `published_date`.
- **Comment**: Модель комментария к статье с полями `article` (внешний ключ на `Article`), `content` и `created_at`.

## Сериализаторы:

```python
from rest_framework import serializers

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    # т.к. знаем что есть связь related_name
    articles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='article-detail'
    )

    class Meta:
        model = Author
        fields = ['url', 'name', 'articles']
        extra_kwargs = {
            'url': {'view_name': 'author-detail', 'lookup_field': 'pk'}
        }
```

### Комментарии к `AuthorSerializer`:
- **Описание**: `AuthorSerializer` наследуется от `HyperlinkedModelSerializer`, что позволяет использовать гиперссылки для представления данных.
- **Поля**: Включает поля `url` и `name`.
- **Дополнительные аргументы**: Указывает, что для поля `url` следует использовать представление `author-detail`, передавая в него первичный ключ (`pk`) автора.

```python
class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    # т.к. есть realted_name: модель Сomment ссылается на Article
    # и нам НУЖНО  указать  рк
    comments = serializers.HyperlinkedRelatedField(
      many=True,
      read_only=True,
      view_name='comment-detail',
      lookup_field='pk'
    )
    # т.к. есть realted_name: модель Article ссылается на Author
    # и нам НЕ нужно указать  рк
    author = serializers.HyperlinkedRelatedField(
      view_name='author-detail',
      read_only=True
    )

    class Meta:
        model = Article
        fields = ['url', 'title', 'content', 'author', 'comments', 'published_date']
        extra_kwargs = {
            'url': {'view_name': 'article-detail', 'lookup_field': 'pk'}
        }
```

### Комментарии к `ArticleSerializer`:
- **Описание**: `ArticleSerializer` также использует `HyperlinkedModelSerializer` для работы с гиперссылками.
- **Поля**: Включает поля `url`, `title`, `content`, `author`, `comments` и `published_date`.
- **Гиперссылки для связанных данных**: 
  - Поле `author` представляет связь с автором статьи через гиперссылку на `author-detail`.
  - Поле `comments` представляет связь с комментариями через гиперссылки на `comment-detail`.
- **Дополнительные аргументы**: Указывает, что для поля `url` статьи следует использовать представление `article-detail`, передавая в него первичный ключ (`pk`).

## Представления (Views):

### Пример представления `AuthorDetailView`:
```python
from rest_framework import generics
from .models import Author
from .serializers import AuthorSerializer

class AuthorDetailView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'pk'
```

### Пример `ViewSet` для статей:
```python
from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

## Важные моменты:

### 1. `related_name` и его важность:
- **`related_name`** в модели позволяет Django создать обратную связь между объектами. Например, `related_name='articles'` в модели `Article` позволяет получить все статьи автора через `author.articles`. Эта связь затем используется `HyperlinkedModelSerializer` для автоматического создания гиперссылок.

### 2. Что такое `author-detail` и почему URL выглядит так:
- **`author-detail`** — это имя URL-паттерна, которое связано с представлением `AuthorDetailView`. Django REST Framework по умолчанию генерирует URL на основе базового пути для модели, например, `authors`. Имя представления используется для создания правильного URL, но в URL используется стандартный паттерн: `authors/<pk>/`.

### 3. Зачем нужен `lookup_field='pk'`?
- **`lookup_field='pk'`** указывает, что в URL используется первичный ключ (`pk`) для поиска объекта. Это важно для того, чтобы сериализатор и представление знали, как искать объект в базе данных.

## Как это работает во вью:
- **AuthorDetailView**: Это представление отвечает за возврат данных о конкретном авторе по его `pk`. Когда клиент переходит по ссылке, например, "http://api.example.com/authors/1/", `AuthorDetailView` извлекает данные о авторе с `pk=1` и возвращает их в ответе.
- **ArticleViewSet**: Этот `ViewSet` позволяет управлять операциями CRUD (создание, чтение, обновление, удаление) для статей. Когда клиент переходит по ссылке, например, "http://api.example.com/articles/1/", возвращаются данные о статье с `pk=1`.

## Как пользователь взаимодействует с API:
- Пользователь переходит по ссылке "http://api.example.com/authors/1/" и видит данные автора, включая гиперссылки на его статьи.
- Если он переходит по ссылке на статью, например, "http://api.example.com/articles/1/", он видит данные о статье, включая гиперссылки на автора и комментарии к статье.


---


# Что произойдет, если использовать обычный ModelSerializer?

Если вы используете обычный `ModelSerializer` вместо `HyperlinkedModelSerializer`, поведение сериализации изменится следующим образом:

## 1. **Отсутствие гиперссылок:**
   - `ModelSerializer` не будет автоматически создавать гиперссылки для связанных объектов. Вместо этого он будет возвращать связанные данные в виде идентификаторов или других атрибутов, заданных в модели.
   - Например, если у вас есть связь `ForeignKey` между `Article` и `Author`, поле `author` в `ArticleSerializer`, основанном на `ModelSerializer`, будет возвращать `id` автора, а не ссылку на детальную информацию о нем.

## 2. **Пример с `ModelSerializer`:**

### Модель:
```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, related_name='articles', on_delete=models.CASCADE)
    published_date = models.DateField()
```

### Сериализатор:
```python
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'published_date']
```

### Пример ответа:
```json
{
    "id": 1,
    "title": "Sample Article",
    "content": "This is the content of the article.",
    "author": 5,  # Здесь возвращается ID автора, а не гиперссылка
    "published_date": "2024-08-30"
}
```

## 3. **Как передать гиперссылку вручную:**
   - Если вы хотите добавить гиперссылки в обычный `ModelSerializer`, это можно сделать вручную с помощью `SerializerMethodField` или `HyperlinkedRelatedField`.

### Пример с добавлением гиперссылки вручную:
```python
class ArticleSerializer(serializers.ModelSerializer):
    author_url = serializers.HyperlinkedRelatedField(
        view_name='author-detail',
        read_only=True,
        source='author'
    )

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author_url', 'published_date']
```

### Пример ответа с гиперссылкой:
```json
{
    "id": 1,
    "title": "Sample Article",
    "content": "This is the content of the article.",
    "author_url": "http://api.example.com/authors/5/",
    "published_date": "2024-08-30"
}
```

## 4. **Заключение:**
   - `ModelSerializer` подходит для случаев, когда гиперссылки на связанные объекты не требуются, и достаточно возвращать их идентификаторы или другие атрибуты.
   - Если же вам нужны гиперссылки, удобнее использовать `HyperlinkedModelSerializer`, который автоматически добавляет ссылки на связанные объекты.

