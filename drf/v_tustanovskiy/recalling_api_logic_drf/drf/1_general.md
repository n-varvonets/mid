## Сериализация

- **Сериализация** — это процесс преобразования объектов (например, моделей Django) в формат для передачи или хранения (например, JSON).
```python
from django.db import models

# Пример модели Review, которая используется в ReviewSerializer
class Review(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

# Пример модели Movie, которая используется в MovieDetailSerializer
class Movie(models.Model):
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default="")
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField('Person', verbose_name="режиссер", related_name="film_director")
    actors = models.ManyToManyField('Person', verbose_name="актеры", related_name="film_actor")
    genres = models.ManyToManyField('Genre', verbose_name="жанры")
    world_premiere = models.DateField("Примьера в мире", default=models.DateField.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField("Сборы в США", default=0, help_text="указывать сумму в долларах")
    fees_in_world = models.PositiveIntegerField("Сборы в мире", default=0, help_text="указывать сумму в долларах")
    category = models.ForeignKey('Category', verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

# Пример модели Category, Person, Genre
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры

# Сериализация — это процесс преобразования объекта (например, экземпляра модели) в формат данных, 
# который может быть передан (например, JSON). В этом случае сериализатор преобразует данные моделей Movie и Review в JSON.

# Десериализация — это обратный процесс, когда данные (например, JSON) преобразуются обратно в объект модели. 
# Например, когда вы получаете JSON с отзывом и хотите создать или обновить запись в базе данных.

class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review.
    Сериализует и десериализует данные отзывов (имя, текст, родительский отзыв).
    """

    class Meta:
        model = Review  # Указываем модель, для которой создается сериализатор
        fields = ("name", "text", "parent")  # Поля модели, которые будут сериализованы и десериализованы

class MovieDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детальной информации о фильме.
    Сериализует и десериализует связанные объекты и поля фильма.
    """

    # Связанные поля сериализуются с использованием SlugRelatedField для удобного отображения слагов
    # Поля ссылаются на 'name' вместо 'slug', чтобы при сериализации вернуть человекочитаемое имя вместо слага.
    
    # 1.Поля для сериализации (GET-запрос)
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)  # many=True означает, что это поле может содержать несколько значений
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)  # Связанные отзывы сериализуются с использованием ReviewSerializer; many=True указывает, что это список отзывов

    class Meta:
        model = Movie  # Указываем модель, для которой создается сериализатор
        exclude = ("draft",)  # Поля, которые будут исключены из сериализации и десериализации

    #  2.Десериализация в данном примере не предусмотрена явно,  
        
# Опции сериализаторов:
# - read_only=True: : Поле доступно только для чтения и используется при сериализации данных (обычно для GET-запросов)
# - write_only=True и required=True: Поле доступно только для записи и используется при десериализации данных (обычно \
#  --- для POST, PUT, PATCH запросов). Это значит, что значение поля может быть передано клиентом для сохранения или \ 
#  --- обновления данных, но оно не будет включено в ответ сервера.
# - source: Источник данных для поля, если он отличается от имени поля в сериализаторе.
# - many=True: Указывает, что поле может содержать множество объектов (список).
# - slug_field: Указывает, какое поле модели использовать для представления связанных объектов.
# - fields: Определяет, какие поля модели будут включены в сериализацию и десериализацию.
# - exclude: Определяет, какие поля модели будут исключены из сериализации и десериализации.


class MovieDetailSerializerWithPostCase(serializers.ModelSerializer):
    """
    Сериализатор для детальной информации о фильме с поддержкой POST-запросов.
    Сериализует и десериализует связанные объекты и поля фильма.
    """

    # Поля для сериализации (GET-запрос)
    category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())
    directors = serializers.SlugRelatedField(slug_field="name", queryset=Person.objects.all(), many=True)
    actors = serializers.SlugRelatedField(slug_field="name", queryset=Person.objects.all(), many=True)
    genres = serializers.SlugRelatedField(slug_field="name", queryset=Genre.objects.all(), many=True)
    reviews = ReviewSerializer(many=True, read_only=True)  # Только для сериализации (GET)

    # 1. через kwargs
    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category', 'directors', 'actors', 'genres', 'reviews')
        exclude = ("draft",)
        extra_kwargs = {
            'directors': {'read_only': True},  # Это поле будет доступно только для чтения
            'actors': {'read_only': True},     # Это поле будет доступно только для чтения
            'new_directors': {'write_only': True, 'queryset': Person.objects.all()},  # Это поле будет доступно только для записи
            'new_actors': {'write_only': True, 'queryset': Person.objects.all()}      # Это поле будет доступно только для записи
        }
        
    # 2. ЯВНОЕ присваивание в validated_data Дополнительные поля для десериализации (POST/PUT-запросы)
    new_directors = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), many=True, write_only=True)
    new_actors = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), many=True, write_only=True)

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category', 'directors', 'actors', 'genres', 'reviews', 'new_directors', 'new_actors')
        exclude = ("draft",)

    def create(self, validated_data, **kwargs):
        # 1.via kwargs
        custom_param = kwargs.get('custom_param', None)
        new_directors = custom_param["new_directors"]

        # Создание фильма
        movie = Movie.objects.create(**validated_data)

        # Добавление новых режиссеров и актеров
        movie.directors.set(new_directors)
        movie.actors.set(new_actors)

        return movie

    def update(self, instance, validated_data):
        # 2. через явное присваивание
        new_directors = validated_data.pop('new_directors', None)
        new_actors = validated_data.pop('new_actors', None)

        # Обновление существующего фильма
        for key, value in validated_data.items():
            setattr(instance, key, value)

        if new_directors is not None:
            instance.directors.set(new_directors)
        if new_actors is not None:
            instance.actors.set(new_actors)

        instance.save()
        return instance
```
# Почему используется `PrimaryKeyRelatedField`?
- **PrimaryKeyRelatedField** используется для того, чтобы сериализовать и десериализовать связанные объекты по их первичному ключу (обычно это поле `id`).
- **Почему не другое поле?** 
  - **PrimaryKeyRelatedField** удобен, когда вы хотите передать или получить идентификаторы связанных объектов, а не их детализированную информацию.
  - Другие поля, такие как **SlugRelatedField** или **StringRelatedField**, могут использоваться, если вам нужно передать или получить связанный объект через его слаг или строковое представление соответственно.
- **Может ли использоваться в модели?**
  - **PrimaryKeyRelatedField** - это специальный класс, который используется только в сериализаторах. В моделях Django используется **ForeignKey** для установления отношений между объектами, что эквивалентно использованию **PrimaryKeyRelatedField** в сериализаторе.




## QuerySet

- **QuerySet** — `это запрос` к базе данных в Django, который можно фильтровать, сортировать и модифицировать.

- `QuerySet` ленивый — запрос к базе данных выполняется только тогда, когда данные действительно нужны.
  - **Не отправляют запрос в БД**: `filter()`, `exclude()`, `order_by()`, `all()` — они просто настраивают запрос.
  - **Отправляют запрос в БД**: `list()`, `count()`, `exists()`, `first()`, `last()`, `get()` — они выполняют запрос и возвращают результаты.
  - **После выполнения `запрос(QuerySet) превращается в список`** (или другой объект, например, число, в зависимости от метода) с данными, которые можно использовать в программе.

