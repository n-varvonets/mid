# Django Rest Framework: GenericAPIView и метод get_object()

## Класс GenericAPIView

Базовый класс для всех APIView в Django Rest Framework, который предоставляет базовую функциональность для работы с queryset и сериализатором.

### Основные атрибуты класса

- **`queryset`**:
  - Определяет набор данных (queryset), с которым будет работать представление. Обычно это объекты из базы данных, которые будут фильтроваться и передаваться в сериализатор.

- **`serializer_class`**:
  - Указывает класс сериализатора, который будет использоваться для преобразования и валидации данных. Например, сериализация данных модели в формат JSON или обратно.

- **`lookup_field`**:
  - Поле, по которому будет производиться поиск объекта в базе данных. По умолчанию это `pk` (первичный ключ), но может быть изменено, например, на `slug`.

- **`lookup_url_kwarg`**:
  - Ключевое слово, извлекаемое из URL, по которому будет производиться поиск объекта. Если не указано, используется значение из `lookup_field`.

- **`permission_classes`**:
  - Список классов разрешений, которые определяют, какие права доступа должен иметь пользователь для взаимодействия с представлением.

### Пример кода

```python
from rest_framework import generics

class GenericAPIView(generics.GenericAPIView):
    """
    Базовый класс для всех APIView в Django Rest Framework, 
    который предоставляет базовую функциональность для работы с queryset и serializer.
    """

    # Атрибуты класса
    queryset = None  # Определяет queryset, с которым будет работать представление
    serializer_class = None  # Указывает на класс сериализатора, который будет использоваться для валидации и преобразования данных
    lookup_field = 'pk'  # Поле, по которому будет производиться поиск объекта в базе данных
    lookup_url_kwarg = None  # Ключевое слово из URL, по которому будет производиться поиск объекта. Если не задано, используется значение lookup_field
    permission_classes = []  # Список классов разрешений, которые будут проверяться при доступе к этому представлению

    def get_queryset(self):
        """
        Возвращает queryset, с которым будет работать представление.
        Если queryset не определен, выбрасывается ошибка.
        """
        if self.queryset is None:
            raise AssertionError(
                "Provide a valid queryset."
            )
        return self.queryset.all()

    def get_serializer(self, *args, **kwargs):
        """
        Возвращает экземпляр сериализатора, который будет использоваться для валидации и преобразования данных.
        """
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_object(self):
        """
        Возвращает объект, который будет отображаться в представлении.
        Этот метод можно переопределить, если необходимо использовать нестандартные лукапы или фильтрацию queryset.
        """

        # Получаем queryset, который будем фильтровать
        queryset = self.filter_queryset(self.get_queryset())

        # Определяем имя аргумента, используемого для поиска объекта в базе данных (lookup)
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        # Убедимся, что этот аргумент присутствует в словаре kwargs, иначе вызовем ошибку
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' % (
                self.__class__.__name__, lookup_url_kwarg
            )
        )

        # Формируем словарь фильтрации, используя значение из kwargs
        # filter_kwargs содержит поле поиска (например, pk) и его значение из URL
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        # Пытаемся получить объект из базы данных, соответствующий фильтру
        # Если объект не найден, возвращаем ошибку 404
        obj = get_object_or_404(queryset, **filter_kwargs)

        # Проверяем права доступа пользователя к данному объекту
        self.check_object_permissions(self.request, obj)

        # Возвращаем найденный объект
        return obj
        
```

# Основные атрибуты класса GenericAPIView:

## queryset:
Определяет набор данных (queryset), с которым будет работать представление. Обычно это объекты из базы данных, которые будут фильтроваться и передаваться в сериализатор.

## serializer_class:
Указывает класс сериализатора, который будет использоваться для преобразования и валидации данных. Например, сериализация данных модели в формат JSON или обратно.

## lookup_field:
Поле, по которому будет производиться поиск объекта в базе данных. По умолчанию это `pk` (первичный ключ), но может быть изменено, например, на `slug`.

## lookup_url_kwarg:
Ключевое слово, извлекаемое из URL, по которому будет производиться поиск объекта. Если не указано, используется значение из `lookup_field`.
- Пример использования `lookup_url_kwarg`:

```python
from rest_framework import generics
from .models import Movie
from .serializers import MovieSerializer

class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'slug'  # Поиск будет происходить по полю 'slug'
    lookup_url_kwarg = 'movie_slug'  # Ключевое слово, извлекаемое из URL

# Пример URL pattern в urls.py:
# path('movies/<movie_slug>/', MovieDetailView.as_view(), name='movie-detail')

# В этом случае, при обращении к URL /movies/inception/,
# 'inception' будет передан в представление как 'movie_slug',
# и объект будет найден в базе данных по полю 'slug'.
```
## permission_classes:
Список классов разрешений, которые определяют, какие права доступа должен иметь пользователь для взаимодействия с представлением.

# Краткое описание метода get_object:
Метод `get_object()` используется для извлечения конкретного объекта из базы данных на основе параметров, переданных через URL. Этот метод выполняет поиск (лукап) объекта, проверяет права доступа к нему и возвращает объект или выбрасывает ошибку, если объект не найден или доступ к нему запрещен.

Этот код является основой для создания более сложных API в Django Rest Framework, где вам может потребоваться кастомизировать процесс поиска и фильтрации объектов, а также работы с сериализаторами.
