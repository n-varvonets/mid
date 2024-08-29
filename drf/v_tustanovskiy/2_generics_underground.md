1. знати подкопотную логику всех генерикс.. list, retrive и т.д.... что и за чем вызывается подкапотом.. 
типо в какой момент и что вызывается(фильтер,класс).
оно помагает кастомизировать всю логику и что б не писать во вью всю логику с нуля, т.е. иметь понимания что под
капотом есть строчка, которую можно переписать. т.е. знат что за что отвечает и в какой момент это тригерится.


# Django REST Framework: Подкапотная логика Generic Views

Django REST Framework предоставляет множество стандартных представлений (Generic Views), которые можно использовать для построения API. Понимание того, как они работают под капотом, позволяет легко их кастомизировать и адаптировать к потребностям вашего приложения.

## Пример модели

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title
```

Эта модель описывает книгу с такими полями, как `title`, `author`, `published_date` и `isbn`.

## Generic Views: Подкапотная логика

### 1. `ListAPIView`
- **Описание**: `ListAPIView` используется для возврата списка объектов. Этот класс предоставляет методы для фильтрации, сортировки и поиска.
- **Подкапотная логика**:
    - **`get_queryset()`**: Этот метод вызывается для получения QuerySet, который затем будет передан в сериализатор. Вы можете переопределить его, чтобы настроить возвращаемые данные.
    - **`filter_queryset(queryset)`**: Этот метод применяется после получения QuerySet. Он отвечает за фильтрацию данных в соответствии с запросами (например, через URL-параметры).
    - **`paginate_queryset(queryset)`**: Если включена пагинация, этот метод разбивает QuerySet на страницы.
    - **`get_serializer()`**: Возвращает экземпляр сериализатора, который будет использоваться для преобразования QuerySet в JSON или другой формат.
    - **`list(request, *args, **kwargs)`**: Основной метод, который обрабатывает запрос и возвращает список объектов. Вызывает методы выше в следующей последовательности:
        1. `get_queryset()`
        2. `filter_queryset(queryset)`
        3. `paginate_queryset(queryset)`
        4. `get_serializer()`
        5. `return Response(serializer.data)`

### Пример реализации:
```python
from rest_framework.generics import ListAPIView
from .models import Book
from .serializers import BookSerializer

class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

### 2. `RetrieveAPIView`
- **Описание**: `RetrieveAPIView` используется для возврата одного объекта на основе его уникального идентификатора.
- **Подкапотная логика**:
    - **`get_object()`**: Этот метод извлекает объект из базы данных на основе переданного идентификатора. Вы можете переопределить его для кастомной логики извлечения объекта.
    - **`get_serializer()`**: Возвращает экземпляр сериализатора для преобразования объекта в нужный формат.
    - **`retrieve(request, *args, **kwargs)`**: Основной метод, который вызывает `get_object()` и `get_serializer()` для возврата данных.
        1. `get_object()`
        2. `get_serializer()`
        3. `return Response(serializer.data)`

### Пример реализации:
```python
from rest_framework.generics import RetrieveAPIView
from .models import Book
from .serializers import BookSerializer

class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

### 3. `CreateAPIView`
- **Описание**: `CreateAPIView` используется для создания нового объекта.
- **Подкапотная логика**:
    - **`get_serializer()`**: Возвращает экземпляр сериализатора, который будет использоваться для десериализации входных данных.
    - **`perform_create(serializer)`**: Этот метод вызывает `serializer.save()` для сохранения нового объекта в базе данных. Вы можете переопределить его, чтобы добавить кастомную логику перед сохранением.
    - **`create(request, *args, **kwargs)`**: Основной метод, который обрабатывает запрос, вызывает `perform_create()` и возвращает данные нового объекта.
        1. `get_serializer()`
        2. `serializer.is_valid()`
        3. `perform_create(serializer)`
        4. `return Response(serializer.data)`

### Пример реализации:
```python
from rest_framework.generics import CreateAPIView
from .models import Book
from .serializers import BookSerializer

class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

### 4. `UpdateAPIView`
- **Описание**: `UpdateAPIView` используется для обновления существующего объекта.
- **Подкапотная логика**:
    - **`get_object()`**: Извлекает объект для обновления.
    - **`get_serializer()`**: Возвращает экземпляр сериализатора для обновления объекта.
    - **`perform_update(serializer)`**: Этот метод вызывает `serializer.save()` для сохранения изменений в объекте. Вы можете кастомизировать этот процесс.
    - **`update(request, *args, **kwargs)`**: Основной метод, который вызывает `perform_update()` и возвращает обновленные данные объекта.
        1. `get_object()`
        2. `get_serializer()`
        3. `serializer.is_valid()`
        4. `perform_update(serializer)`
        5. `return Response(serializer.data)`

### Пример реализации:
```python
from rest_framework.generics import UpdateAPIView
from .models import Book
from .serializers import BookSerializer

class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

### 5. `DestroyAPIView`
- **Описание**: `DestroyAPIView` используется для удаления объекта.
- **Подкапотная логика**:
    - **`get_object()`**: Извлекает объект для удаления.
    - **`perform_destroy(instance)`**: Этот метод вызывает `instance.delete()` для удаления объекта из базы данных.
    - **`destroy(request, *args, **kwargs)`**: Основной метод, который вызывает `perform_destroy()` и возвращает подтверждение удаления.
        1. `get_object()`
        2. `perform_destroy(instance)`
        3. `return Response(status=204)`

### Пример реализации:
```python
from rest_framework.generics import DestroyAPIView
from .models import Book

class BookDeleteView(DestroyAPIView):
    queryset = Book.objects.all()
```

## Заключение

Эти Generic Views предоставляют мощный набор инструментов для быстрого создания API в Django REST Framework. Понимание их подкапотной логики помогает легко адаптировать и кастомизировать представления, не создавая их с нуля. Вы можете переопределить ключевые методы, такие как `get_queryset()`, `get_object()`, `perform_create()`, и другие, чтобы реализовать свою собственную бизнес-логику.
