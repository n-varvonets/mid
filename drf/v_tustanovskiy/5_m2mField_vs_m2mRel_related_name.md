
# Разница между ManyToManyRel и ManyToManyField в Django

Ключевая разница между `ManyToManyRel` и `ManyToManyField` в Django заключается в их назначении и использовании:

## 1. ManyToManyField

## ForeignKey (Внешний ключ)

- **Что это**: `ForeignKey` создает связь "многие к одному". Это означает, что много объектов могут ссылаться на один и тот же объект.

### Пример:

Представь, что у нас есть классы "Книга" и "Автор":

```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(maxlength=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
```

- **Как это работает**: Одна книга может иметь только одного автора, но один автор может написать много книг.
- **Реальная жизнь**: Представь, что одна книга всегда имеет одного автора. К примеру, "Гарри Поттер" написан Дж. К. Роулинг.

## ManyToManyField (Многие ко многим)

- **Что это**: `ManyToManyField` создает связь "многие ко многим". Это означает, что много объектов могут быть связаны с множеством других объектов.

### Пример:

Представь, что у нас есть классы "Книга" и "Жанр":

```python
class Genre(models.Model):
    name = models.CharField(maxlength=100)

class Book(models.Model):
    title = models.CharField(maxlength=100)
    genres = models.ManyToManyField(Genre)
```

- **Как это работает**: Одна книга может относиться к нескольким жанрам, и один жанр может включать много книг.
- **Реальная жизнь**: Представь, что одна книга может быть одновременно и фэнтези, и приключением, а жанр "фэнтези" может включать много разных книг.

## Подведем итоги:
- **ForeignKey**: Одна книга -> один автор, но один автор -> много книг.
- **ManyToManyField**: Одна книга -> много жанров, и один жанр -> много книг.

---

## 2. ManyToManyRel

`ManyToManyRel` обычно не используется напрямую в моделях. Это внутренний класс Django ORM, который Django автоматически создает и использует для управления отношениями в базе данных.

### Пример использования ManyToManyRel для доступа к дополнительным атрибутам (используя промежуточную модель):

```python
class Author(models.Model):
    name = models.CharField(max_length=100)
    # Поле ManyToManyField с использованием промежуточной модели AuthorBook
    books = models.ManyToManyField('Book', through='AuthorBook')

class Book(models.Model):
    title = models.CharField(maxlength=100)
    # Обратное отношение ManyToManyField с использованием той же промежуточной модели
    authors = models.ManyToManyField(Author, through='AuthorBook')

class AuthorBook(models.Model):
    # Внешние ключи на модели Author и Book
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # Дополнительное поле для хранения года публикации
    year_published = models.IntegerField()
```

### Объяснение:

- В этом примере мы определили две модели: `Author` и `Book`, которые имеют отношение "многие-ко-многим".  
- Вместо использования стандартного `ManyToManyField`, который автоматически создает таблицу связи, мы используем параметр `through` для указания промежуточной модели `AuthorBook`.
- Модель `AuthorBook` добавляет дополнительное поле `year_published`, которое хранит год публикации книги автором.

### Использование ManyToManyRel:

После того как связь между моделями определена с помощью `through`, мы можем получить доступ к промежуточной модели через атрибут `through`.

```python
# Получение доступа к объекту ManyToManyRel через промежуточную модель
many_to_many_rel = Author.books.through

# Теперь вы можете использовать это для доступа к данным в промежуточной модели, таким как year_published
author_book_records = many_to_many_rel.objects.all()
for record in author_book_records:
    print(f"Author: {record.author.name}, Book: {record.book.title}, Year Published: {record.year_published}")
```

### Комментарии:

- `ManyToManyRel` не используется напрямую разработчиком. Однако, через атрибут `through` можно получить доступ к промежуточной модели и работать с дополнительными полями этой модели.
- <u>**Это полезно в случаях, когда вам необходимо добавить дополнительные атрибуты к отношению "многие-ко-многим"**</u>, которые не могут быть выражены с помощью стандартного `ManyToManyField`.
- Важно помнить, что промежуточные модели <u>**позволяют добавлять поля, которые непосредственно не связаны с одной из моделей**</u>, но описывают свойства самого отношения.

---

## 3. related_name

Когда вы создаете отношение "многие-ко-многим" с помощью `ManyToManyField`, вы можете указать аргумент `related_name`, чтобы задать имя для обратной связи с объектами, связанными с этим полем.

### Пример:

```python
class Author(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField('Book', related_name='authors')

class Book(models.Model):
    title = models.CharField(maxlength=100)
```

### Объяснение:

- В этом примере в модели `Author` поле `books` указывает на модель `Book`, создавая отношение "многие-ко-многим".
- Аргумент `related_name='authors'` определяет имя обратного отношения от модели `Book` к модели `Author`. Это значит, что для каждой книги можно получить всех связанных с ней авторов через поле `authors`.

### Использование:

Теперь вы можете обратиться к связанным авторам через `authors` с объекта `Book`. Например:

```python
book = Book.objects.get(id=1)
authors = book.authors.all()
```

### Комментарии:

- `related_name` позволяет избежать конфликтов имен в случае, если у вас есть несколько отношений "многие-ко-многим" с одной и той же моделью.
- Оно также делает код более читаемым и позволяет логически связывать объекты в обоих направлениях отношений.
