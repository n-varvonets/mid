
# Методы модели Django: Описание и триггеры

### `Методы модели` Django включают такие методы, как:

* save()
* delete()
* clean()
* full_clean()
* get_absolute_url()
* И сигналы (pre_save, post_save, pre_delete, post_delete).

# Подробное описание методов модели Django

## Класс Article

```python
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse

class Article(models.Model):
    """
    Поля title, content, author, и published_date описывают статью.
    Поле author связано с моделью Author через ForeignKey.
    Поле related_name='articles' позволяет доступ к статьям автора через author.articles.
    Метод __str__() возвращает заголовок статьи.
    Метод get_absolute_url() возвращает URL для детального просмотра статьи.
    Метод clean() выполняет валидацию данных, например, проверку длины заголовка.
    Метод save() выполняет полную валидацию перед сохранением статьи.
    Метод delete() удаляет объект статьи из базы данных.
    Метод save_related() сохраняет связанные объекты (например, автора) при сохранении статьи.
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, related_name='articles', on_delete=models.CASCADE)
    published_date = models.DateField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})

    def clean(self):
        """
        Метод clean() выполняет кастомную валидацию данных модели.
        В данном случае он проверяет, что длина заголовка статьи не меньше 5 символов.
        """
        if len(self.title) < 5:
            raise ValidationError('Заголовок должен содержать как минимум 5 символов.')

    def save(self, *args, **kwargs):
        """
        Метод save() выполняет сохранение объекта в базу данных.
        Перед сохранением вызывается метод full_clean(), который включает в себя вызов clean().
        После этого вызывается базовый метод save(), который также вызывает сигналы pre_save и post_save.
        """
        self.full_clean()  # Вызов clean() для валидации данных перед сохранением
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Метод delete() удаляет объект из базы данных.
        Перед удалением и после удаления могут быть вызваны сигналы pre_delete и post_delete соответственно.
        """
        super().delete(*args, **kwargs)

    def save_related(self, *args, **kwargs):
        """
        Метод save_related() сохраняет связанные объекты.
        Обычно вызывается автоматически и не требует ручного вызова.
        """
        super().save_related(*args, **kwargs)
```

## Порядок вызова методов модели Django

### 1. Валидация через `clean()` и `full_clean()`
- **Назначение**: Метод `clean()` Выполняет кастомную валидацию данных `на уровне модели` перед их сохранением.и, например, проверку минимальной длины заголовка. Метод `full_clean()` вызывает `clean()` и проверяет, что все поля модели содержат валидные данные.
- **Когда вызывается**: `clean()` вызывается внутри метода `full_clean()`, который, в свою очередь, вызывается перед сохранением объекта через метод `save()`.
- **Где используется**:
  - `Модели (models.py)`: Переопределяется для добавления кастомной логики валидации данных.
  - `Формы (forms.py)`: Часто вызывается внутри методов full_clean() или is_valid() для проверки данных формы перед сохранением.
  - `Админка (admin.py)`: Валидация данных в админке перед сохранением изменений.

Метод `clean(self)` в модели Django выполняет кастомную валидацию данных на уровне модели. Это гарантирует, что данные всегда валидируются, независимо от того, как они были введены (через форму, API, админку и т.д.). Логика валидации в `clean()` обеспечивает целостность данных и предотвращает их некорректное сохранение.

```python
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateField()

    def clean(self):
        """
        Проверка минимальной длины заголовка и корректности даты публикации.
        """
        if len(self.title) < 5:
            raise ValidationError('Заголовок должен содержать как минимум 5 символов.')

        if self.published_date > timezone.now().date():
            raise ValidationError('Дата публикации не может быть в будущем.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Выполняем валидацию перед сохранением
        super().save(*args, **kwargs)
```

```markdown
View/Serializer --> save() --> full_clean()  # full_clean() вызывает clean() для валидации
full_clean() --> clean()  # clean() выполняет кастомную валидацию данных
```

#### Почему использовать clean(self)?
- Универсальная валидация: Проверки в clean(self) выполняются независимо от того, как данные были получены или обработаны (через формы, админку, API и т.д.)
- Логика на уровне модели: Это проще и логичнее реализовать внутри модели, чем в каждом отдельном сериализаторе или форме.
#### Можно ли проверять поля в сериализаторе?
- Сериализаторы хороши для проверки данных, поступающих через API. `Если вы работаете исключительно с API, валидация в сериализаторе может быть достаточной.` Однако, если модель используется также в админке, в формах или в других частях системы, валидация в сериализаторе не обеспечит целостности данных на всех уровнях.


### 2. Метод `save()` и сигналы `pre_save` и `post_save`
- **Порядок**:
  1. **`full_clean()`**: Первым делом, внутри метода `save()`, вызывается `full_clean()`, который включает в себя вызов `clean()` для валидации данных.
  2. **Сигнал `pre_save`**: После успешной валидации данных вызывается сигнал `pre_save`, который может быть использован для выполнения дополнительных действий перед сохранением.
  3. **Сохранение данных**: Далее объект сохраняется в базу данных через базовый метод `save()`.
  4. **Сигнал `post_save`**: После успешного сохранения вызывается сигнал `post_save`, который используется для выполнения действий после сохранения, например, отправка уведомлений.


- **Назначение**: Сохраняет объект модели в базу данных.
- **Где используется**: Сохраняет объект модели в базу данных.
  - `Представления (views.py)`: Вручную для сохранения объектов перед отправкой ответа.
  - `Сериализаторы (serializers.py)`: Для создания и обновления объектов через API.
  - `Модели (models.py)`: Можно переопределить для добавления кастомной логики перед сохранением.
  - `Команды управления (management/commands)`: Для программного создания или обновления объектов.

```markdown
save() --> full_clean()  # Первым вызывается full_clean() для валидации
full_clean() --> clean()  # Затем вызывается clean() для выполнения кастомной валидации
save() --> pre_save()  # После валидации вызывается сигнал pre_save
save() --> post_save()  # После сохранения вызывается сигнал post_save
```

```python
# views.py
from django.shortcuts import render
from .models import Article

def article_update(request, pk):
    article = Article.objects.get(pk=pk)
    article.title = "Updated Title"
    article.save()  # Вручную сохраняем изменения в базе данных
    return render(request, 'article_detail.html', {'article': article})

# serializers.py
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'author']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()  # Сохраняем изменения через сериализатор
        return instance
```

### 3. Метод `delete()` и сигналы `pre_delete` и `post_delete`
- **Назначение**: Метод `delete()` удаляет объект из базы данных. Он также может вызывать сигналы `pre_delete` перед удалением и `post_delete` после удаления.
- **Когда вызывается**: `delete()` вызывается вручную при необходимости удаления объекта, например, через ViewSet или в админке Django.

```markdown
delete() --> pre_delete()  # Сигнал pre_delete вызывается перед удалением объекта
delete() --> post_delete()  # Сигнал post_delete вызывается после удаления объекта
```

### 4. Метод `save_related()`
- **Назначение**: Метод `save_related()` сохраняет все связанные объекты модели (например, связанные через ForeignKey или ManyToManyField).
- **Когда вызывается**: Обычно вызывается автоматически в процессе сохранения основного объекта, если он имеет связанные объекты, которые также нужно сохранить.
- **Где используется**:
  - `Модели (models.py)`: Автоматически вызывается при сохранении основного объекта. Можно переопределить для добавления дополнительной логики.
  - `Сериализаторы (serializers.py)`: Когда связанный объект также должен быть сохранен, например, при создании или обновлении через API.
```markdown
save() --> save_related()  # save_related() вызывается автоматически при сохранении связей
```
```python
# models.py
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, related_name='articles', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_related()  # Сохраняет связанные объекты, например, автора или теги

# serializers.py
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'author']

    def create(self, validated_data):
        article = Article.objects.create(**validated_data)
        article.save_related()  # Пример вызова save_related в сериализаторе
        return article
```

## Пример использования методов

# Пример использования методов модели Django

## 1. `get_absolute_url()`
- **Назначение**: Возвращает полный URL для объекта модели.
- **Где используется**:
  - **Шаблоны (`templates`)**: В шаблонах, для создания ссылок на объекты модели. Например, ссылка на детальное представление статьи.
  - **Представления (`views.py`)**: В представлениях для редиректов после создания или обновления объекта.
  - **Сериализаторы (`serializers.py`)**: Для генерации URL в API ответах.
  - **Админка (`admin.py`)**: Для создания ссылок в интерфейсе администратора.
  
- **Пример**:
```python
  # views.py
  from django.shortcuts import redirect

  def article_create(request):
      if form.is_valid():
          article = form.save()
          return redirect(article.get_absolute_url())  # Использование get_absolute_url для редиректа на страницу статьи
```

```python
# Пример кода, демонстрирующий, как могут вызываться методы модели Article:

# Создание и сохранение статьи
article = Article(title="Test", content="This is a test article", author=author_instance)
article.save()  # Вызовет full_clean(), затем save(), затем сигналы pre_save и post_save

# Получение строкового представления статьи
print(article)  # Вызывает __str__()

# Получение URL статьи
url = article.get_absolute_url()  # Вызывает get_absolute_url()

# Валидация данных статьи
try:
    article.clean()  # Выполняет кастомную валидацию, например, проверку длины заголовка
except ValidationError as e:
    print(e)

# Удаление статьи
article.delete()  # Вызывает delete(), затем сигналы pre_delete и post_delete

# Сохранение связанных объектов
article.save_related()  # Обычно вызывается автоматически,
# но может быть переопределено для кастомной логики

```


