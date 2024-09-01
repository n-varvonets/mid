
# Сравнение двух способов задания полей для десериализации

## Пример 1: Использование `extra_kwargs`

```python
extra_kwargs = {
    'new_directors': {'write_only': True, 'queryset': Person.objects.all()},
    'new_actors': {'write_only': True, 'queryset': Person.objects.all()}
}
```

## Пример 2: Определение полей напрямую

```python
# Дополнительные поля, которые будут использоваться только для десериализации (POST/PUT)
new_directors = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), many=True, write_only=True)
new_actors = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), many=True, write_only=True)
```

## Похожие черты:
- Оба способа указывают, что поля `new_directors` и `new_actors` являются полями для десериализации (например, при обработке POST/PUT запросов).
- В обоих примерах используется `PrimaryKeyRelatedField` для работы с связанными объектами, и оба указывают, что эти поля доступны только для записи (`write_only=True`).

## Различия:
- **Синтаксис**: В примере 1 поля `new_directors` и `new_actors` задаются через `extra_kwargs` в `Meta` классе, что предоставляет вам гибкость в изменении или добавлении настроек полей без необходимости явно их определять в сериализаторе. В примере 2 эти поля явно определены в классе сериализатора.
- **Область применения**: В примере 2 поля `new_directors` и `new_actors` будут сразу доступны в контексте сериализатора и их можно использовать напрямую в методах `create` или `update`. В примере 1 эти поля будут добавлены автоматически на основе `extra_kwargs`, что может быть удобно для переопределения стандартного поведения сериализатора.

## Когда использовать `extra_kwargs`?
- Если вам нужно добавить или изменить свойства существующих полей, не создавая их вручную.
- Если вы хотите переопределить свойства полей, унаследованных от базового сериализатора.

## Когда использовать явное определение полей?
- Если вы хотите явно определить логику работы с этими полями и иметь прямой доступ к ним в методах `create` или `update`.

# Зачем используется `queryset`?

**`queryset` в контексте `PrimaryKeyRelatedField`:**

- **Зачем нужен `queryset`?** 
  - `queryset` в `PrimaryKeyRelatedField` используется для указания набора данных, из которого могут быть выбраны связанные объекты. В данном случае, он определяет возможные объекты, которые могут быть связаны с `new_directors` и `new_actors`.
  - `queryset=Person.objects.all()` указывает, что поле `new_directors` и `new_actors` может содержать только тех людей, которые существуют в базе данных в модели `Person`. Это обеспечивает валидацию входных данных при десериализации: если указанный ID не существует в этом queryset, будет выброшена ошибка валидации.

- **Где это используется?**
  - Когда вы отправляете данные через POST/PUT запрос, например, в формате JSON, и хотите связать новые данные с объектами в модели, `queryset` проверяет, что все указанные идентификаторы (IDs) действительно существуют в базе данных.
  - В методах `create` и `update` сериализатора, когда вы сохраняете объект, `PrimaryKeyRelatedField` использует `queryset` для преобразования переданных ID в фактические объекты модели, которые затем сохраняются в базе данных.

## Пример использования `queryset` при сохранении:

```python
def create(self, validated_data):
    # Извлечение данных для новых режиссеров и актеров
    new_directors = validated_data.pop('new_directors', [])
    new_actors = validated_data.pop('new_actors', [])

    # Создание фильма
    movie = Movie.objects.create(**validated_data)

    # Добавление новых режиссеров и актеров
    movie.directors.set(new_directors)  # `set` использует объекты, найденные через `queryset`
    movie.actors.set(new_actors)

    return movie
```

## Подведение итогов:
- **`queryset`** определяет набор данных, с которым поле может работать, и выполняет валидацию при десериализации.
- При сохранении в базу данных данные из `PrimaryKeyRelatedField` используются для поиска объектов в базе данных, которые затем связываются с сохраняемым объектом.
- Выбор между `extra_kwargs` и явным определением полей зависит от того, насколько гибким и контролируемым должно быть поведение сериализатора.


### Пример POST-запроса для создания фильма

Предположим, у вас есть две записи в таблице `Person`:

- **Person 1**: ID = 1, name = "James Cameron"
- **Person 2**: ID = 2, name = "Arnold Schwarzenegger"

Теперь вы хотите создать новый фильм и связать его с этими двумя лицами как с режиссером и актером.

#### JSON-данные для POST-запроса:

```json
{
    "title": "Terminator 2: Judgment Day",
    "new_directors": [1],  # ID режиссера James Cameron
    "new_actors": [2]      # ID актера Arnold Schwarzenegger
}
```

### Описание полей:
- `title:` Название фильма.
- `new_directors:` Список ID режиссеров, которые будут связаны с фильмом.
- `new_actors:` Список ID актеров, которые будут связаны с фильмом.  

**В этом примере фильм "Terminator 2: Judgment Day" будет создан и связан с режиссером с ID 1 и актером с ID 2.**


### Что произойдет после запроса:
- Django Rest Framework проверит, существуют ли указанные ID режиссеров и актеров.  
- Если валидация пройдет успешно, фильм будет создан, и связи с режиссером и актерами будут установлены.

------

----

# Вопрос
- разве не проще в валидейт дата добавь эти атрибуты через поиск в кверисет, и таким образом что в create and update попдает уже  `validated_data` уже с нашими аттрибутами?

### Использование `validate` для добавления атрибутов в `validated_data`

Можно оптимизировать процесс добавления связанных объектов (например, режиссеров и актеров) в `validated_data` на этапе валидации, чтобы методы `create` и `update` получали уже готовые объекты. Это позволяет избежать дублирования кода и сделать его чище.


```python
class MovieDetailSerializer(serializers.ModelSerializer):
    new_directors = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    new_actors = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category', 'directors', 'actors', 'genres', 'reviews', 'new_directors', 'new_actors')

    def validate(self, data):
        # Преобразуем ID режиссеров и актеров в объекты Person
        if 'new_directors' in data:
            data['new_directors'] = Person.objects.filter(id__in=data['new_directors'])
        if 'new_actors' in data:
            data['new_actors'] = Person.objects.filter(id__in=data['new_actors'])
        return data

    def create(self, validated_data):
        new_directors = validated_data.pop('new_directors', [])
        new_actors = validated_data.pop('new_actors', [])
        movie = Movie.objects.create(**validated_data)
        movie.directors.set(new_directors)
        movie.actors.set(new_actors)
        return movie

    def update(self, instance, validated_data):
        new_directors = validated_data.pop('new_directors', None)
        new_actors = validated_data.pop('new_actors', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if new_directors is not None:
            instance.directors.set(new_directors)
        if new_actors is not None:
            instance.actors.set(new_actors)
        instance.save()
        return instance
```

