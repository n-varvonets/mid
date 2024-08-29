
# Методы модели Django: Описание и триггеры

В Django модели предоставляют несколько ключевых методов, которые могут быть переопределены для настройки поведения объекта на различных этапах его жизненного цикла. Эти методы могут быть вызваны автоматически Django или вручную, в зависимости от контекста.

## Основные методы модели

```python
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse

class Author(models.Model):
    """
    Поле name хранит имя автора.
    Метод __str__() возвращает имя автора.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Article(models.Model):
    """
    Поля title, content, author, и published_date описывают статью.
    Поле author связано с моделью Author через ForeignKey.
    Поле related_name='articles' позволяет доступ к статьям автора через author.articles.
    Метод __str__() возвращает заголовок статьи.
    Метод get_absolute_url() возвращает URL для детального просмотра статьи.
    Метод clean() выполняет валидацию данных, например, проверку длины заголовка.
    Метод save() выполняет полную валидацию перед сохранением статьи.
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
        if len(self.title) < 5:
            raise ValidationError('Заголовок должен содержать как минимум 5 символов.')

    def save(self, *args, **kwargs):
        # Дополнительная логика перед сохранением
        self.full_clean()  # Вызов метода clean() для валидации
        super().save(*args, **kwargs)

class Comment(models.Model):
    """
    Поля article, content, и created_at описывают комментарий к статье.
    Поле article связано с моделью Article через ForeignKey.
    Поле related_name='comments' позволяет доступ к комментариям статьи через article.comments.
    Метод __str__() возвращает информацию о комментарии, включая автора и заголовок статьи.
    """
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.article.author.name} on {self.article.title}'
```

### 1. `save(self, *args, **kwargs)`
- **Описание**: Метод `save()` отвечает за сохранение объекта модели в базу данных. Он обрабатывает как создание новых объектов, так и обновление существующих.
- **Триггер**: `save()` вызывается явно при сохранении объекта через метод модели, либо автоматически, например, при сохранении объектов через сериализаторы в Django REST Framework.
- **Пример**:
    ```python
    instance = MyModel(field1='value')
    instance.save()  # Сохранение объекта в базу данных
    ```

### 2. `delete(self, *args, **kwargs)`
- **Описание**: Метод `delete()` отвечает за удаление объекта модели из базы данных.
- **Триггер**: `delete()` вызывается явно при удалении объекта через метод модели, либо автоматически при каскадном удалении объектов, связанных с этим объектом.
- **Пример**:
    ```python
    instance = MyModel.objects.get(pk=1)
    instance.delete()  # Удаление объекта из базы данных
    ```

### 3. `__str__(self)`
- **Описание**: Метод `__str__()` определяет строковое представление объекта модели. Он используется при отображении объекта в административной панели Django и других местах, где требуется строковое представление объекта.
- **Триггер**: `__str__()` вызывается автоматически, когда необходимо отобразить объект в виде строки.
- **Пример**:
    ```python
    def __str__(self):
        return self.name  # Возвращает значение поля name как строковое представление объекта
    ```

### 4. `get_absolute_url(self)`
- **Описание**: Метод `get_absolute_url()` используется для получения полного URL объекта. Обычно используется в шаблонах и представлениях для создания ссылок на объекты.
- **Триггер**: `get_absolute_url()` вызывается явно в шаблонах или представлениях, когда нужно получить URL объекта.
- **Пример**:
    ```python
    def get_absolute_url(self):
        return reverse('model_detail', kwargs={'pk': self.pk})
    ```

### 5. `clean(self)`
- **Описание**: Метод `clean()` выполняет валидацию данных объекта модели перед его сохранением. Он позволяет добавить кастомные проверки, которые будут выполнены перед сохранением объекта.
- **Триггер**: `clean()` вызывается явно перед вызовом метода `save()`, обычно через метод `full_clean()`.
- **Пример**:
    ```python
    def clean(self):
        if self.some_field < 0:
            raise ValidationError('some_field не может быть отрицательным')
    ```

### 6. `full_clean(self, *args, **kwargs)`
- **Описание**: Метод `full_clean()` выполняет полную валидацию объекта, включая вызов метода `clean()` и проверку полей модели.
- **Триггер**: `full_clean()` вызывается явно перед сохранением объекта, чтобы убедиться, что данные корректны.
- **Пример**:
    ```python
    instance = MyModel(field1=-1)
    instance.full_clean()  # Вызовет ValidationError, если в clean() прописана соответствующая логика
    ```

### 7. `save_related(self, *args, **kwargs)`
- **Описание**: Метод `save_related()` сохраняет все объекты, связанные с текущим объектом через ForeignKey или ManyToManyField.
- **Триггер**: `save_related()` вызывается автоматически в процессе сохранения объекта, если есть связанные объекты, которые также нужно сохранить.
- **Пример**:
    ```python
    instance.save_related()  # Сохраняет связанные объекты после сохранения основного объекта
    ```

## Специальные методы модели

### 8. `pre_save(sender, instance, *args, **kwargs)`
- **Описание**: Метод-сигнал `pre_save` вызывается перед сохранением объекта в базу данных.
- **Триггер**: `pre_save` вызывается автоматически Django перед тем, как будет выполнен метод `save()`.
- **Пример**:
    ```python
    from django.db.models.signals import pre_save
    from django.dispatch import receiver

    @receiver(pre_save, sender=MyModel)
    def my_model_pre_save(sender, instance, **kwargs):
        instance.field = 'Modified Value'
    ```

### 9. `post_save(sender, instance, created, *args, **kwargs)`
- **Описание**: Метод-сигнал `post_save` вызывается после сохранения объекта в базу данных.
- **Триггер**: `post_save` вызывается автоматически Django после выполнения метода `save()`.
- **Пример**:
    ```python
    from django.db.models.signals import post_save
    from django.dispatch import receiver

    @receiver(post_save, sender=MyModel)
    def my_model_post_save(sender, instance, created, **kwargs):
        if created:
            print(f'Новый объект {instance} был создан')
    ```

### 10. `pre_delete(sender, instance, *args, **kwargs)`
- **Описание**: Метод-сигнал `pre_delete` вызывается перед удалением объекта из базы данных.
- **Триггер**: `pre_delete` вызывается автоматически Django перед выполнением метода `delete()`.
- **Пример**:
    ```python
    from django.db.models.signals import pre_delete
    from django.dispatch import receiver

    @receiver(pre_delete, sender=MyModel)
    def my_model_pre_delete(sender, instance, **kwargs):
        print(f'Объект {instance} будет удален')
    ```

### 11. `post_delete(sender, instance, *args, **kwargs)`
- **Описание**: Метод-сигнал `post_delete` вызывается после удаления объекта из базы данных.
- **Триггер**: `post_delete` вызывается автоматически Django после выполнения метода `delete()`.
- **Пример**:
    ```python
    from django.db.models.signals import post_delete
    from django.dispatch import receiver

    @receiver(post_delete, sender=MyModel)
    def my_model_post_delete(sender, instance, **kwargs):
        print(f'Объект {instance} был удален')
    ```

Эти методы и сигналы обеспечивают гибкость и контроль над поведением объектов модели на разных этапах их жизненного цикла. Они могут быть использованы для настройки валидации, обработки данных перед сохранением или удаления, а также для выполнения дополнительных действий после этих операций.
