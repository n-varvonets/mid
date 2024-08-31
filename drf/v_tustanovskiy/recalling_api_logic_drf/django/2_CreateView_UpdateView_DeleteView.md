
# Django Views: CreateView, UpdateView, DeleteView

## CreateView

- **Назначение**:
  - Представление, используемое для создания нового объекта в базе данных.
  
- **Особенности**:
  - Основано на **ModelFormMixin**, который обрабатывает логику создания и сохранения формы.
  - Автоматически подгружает шаблон формы и обрабатывает её отправку.
  - После успешного создания объекта перенаправляет на заданный URL (определяется через `get_success_url()`).

- **Пример использования**:
  ```python
  from django.views.generic import CreateView
  from .models import Movie

  class MovieCreateView(CreateView):
      model = Movie
      fields = ['title', 'description', 'year']
      template_name = 'movie_form.html'
      success_url = '/movies/'
  ```

## UpdateView

- **Назначение**:
  - Представление, используемое для обновления существующего объекта в базе данных.
  
- **Особенности**:
  - Основано на **ModelFormMixin**, который обрабатывает логику обновления и сохранения формы.
  - Автоматически загружает данные объекта в форму для редактирования.
  - После успешного обновления объекта перенаправляет на заданный URL (определяется через `get_success_url()`).

- **Пример использования**:
  ```python
  from django.views.generic import UpdateView
  from .models import Movie

  class MovieUpdateView(UpdateView):
      model = Movie
      fields = ['title', 'description', 'year']
      template_name = 'movie_form.html'
      success_url = '/movies/'
  ```

## DeleteView

- **Назначение**:
  - Представление, используемое для удаления существующего объекта из базы данных.
  
- **Особенности**:
  - Основано на **SingleObjectMixin**, который обрабатывает логику получения и удаления объекта.
  - Автоматически подгружает подтверждающий шаблон перед удалением.
  - После успешного удаления объекта перенаправляет на заданный URL (определяется через `get_success_url()`).

- **Пример использования**:
  ```python
  from django.views.generic import DeleteView
  from .models import Movie

  class MovieDeleteView(DeleteView):
      model = Movie
      template_name = 'movie_confirm_delete.html'
      success_url = '/movies/'
  ```
