# Различия между `has_permission` и `has_object_permission` в Django REST Framework

## Введение

В Django REST Framework для контроля доступа к API используются два основных метода: `has_permission` и `has_object_permission`. Оба этих метода проверяют, имеет ли пользователь доступ к определённому ресурсу, но они проверяют разные уровни доступа:

- **`has_permission`** проверяет **общий доступ** к представлению.
- **`has_object_permission`** проверяет **доступ к конкретному объекту**. 

### Что означает "доступ к объекту" и "общий доступ"?

- **Общий доступ (`has_permission`)**: Проверка прав на доступ к представлению в целом, без привязки к конкретному объекту. Например, у пользователя может быть право просматривать список фильмов, но это не гарантирует ему доступ к каждому отдельному фильму.
  
- **Доступ к объекту (`has_object_permission`)**: Проверка прав на доступ к конкретному объекту. Даже если пользователь имеет общий доступ к списку фильмов, он может не иметь прав на доступ к конкретному фильму (например, если фильм является приватным или связан с другим пользователем).
- `check_object_permissions` вызывается, когда нужно убедиться, что у пользователя есть права на доступ к конкретному объекту перед выполнением действия с ним.

## Примеры использования

### Пример с `has_permission`

```python
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        # Проверка, что пользователь аутентифицирован
        return request.user and request.user.is_authenticated
        
    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь владельцем объекта
        return obj.owner == request.user
    

class OrderDetailView(APIView):
    permission_classes = [IsOwner]

    def get(self, request, *args, **kwargs):
        # Получаем объект заказа
        order = self.get_object()
        
        # Проверяем права доступа к объекту
        self.check_object_permissions(request, order)
        
        # Если разрешение получено, возвращаем данные объекта
        return Response({"order": order})

    # def check_object_permissions(self, request, obj):
    #     """
    #     check_object_permissions вызывается, когда нужно убедиться, что у пользователя есть права на доступ 
    #     к конкретному объекту перед выполнением действия с ним.    
    #     """
    #     for permission in self.get_permissions():
    #         if not permission.has_object_permission(request, self, obj):
    #             raise PermissionDenied()
```
### Заключение

- **`has_permission`** проверяет общий доступ ко всему представлению, тогда как **`has_object_permission`** проверяет доступ к конкретным объектам.

---
## Работа `permission_classes` в GenericAPIView и ViewSet

### GenericAPIView

`GenericAPIView` предоставляет гибкую основу для создания представлений в DRF, позволяя вам реализовать как базовые, так и сложные проверки доступа. В `GenericAPIView` методы `has_permission` и `has_object_permission` используются следующим образом:

- **`permission_classes`**: Указываются на уровне представления. Эти классы будут применяться ко всем методам в представлении (например, `get`, `post`, `put`, `delete`).
  
- **Порядок выполнения**: Сначала вызывается `has_permission`, чтобы проверить общий доступ. Если общий доступ разрешён, при работе с конкретным объектом (например, при `retrieve`, `update`, `destroy`) вызывается `has_object_permission`.

Пример:
```python
class MyGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyModel.objects.all()
    permission_classes = [IsOwner]

    def get(self, request, *args, **kwargs):
        # Получаем объект
        obj = self.get_object()
        # Проверяем права доступа к объекту
        self.check_object_permissions(request, obj)
        return Response({"data": obj.data})
```
### ViewSet

`ViewSet` объединяет несколько методов (таких как `list`, `retrieve`, `create`, `update`, `destroy`) в одном классе, и предоставляет маршрутизацию для них. Работа с `permission_classes` в `ViewSet` схожа с `GenericAPIView`, но с некоторыми отличиями:

- **Общий доступ** (`has_permission`) проверяется при доступе к действиям, которые не привязаны к конкретному объекту (например, `list`, `create`).
  
- **Доступ к объекту** (`has_object_permission`) проверяется при доступе к действиям, связанным с конкретным объектом (например, `retrieve`, `update`, `destroy`).

#### Пример:

```python
# Проверка доступа к объекту: является ли пользователь владельцем объекта
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

# Проверка доступа к объекту: доступ разрешен только администраторам
class IsAdminUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff

class MyModelViewSet(viewsets.ModelViewSet):
    """
    В данном примере мы создадим `ViewSet`, где два метода будут использовать разные проверки `has_object_permission`,
    а для остальных методов будет применяться `has_permission`.
    """
    queryset = MyModel.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        # Используем IsOwner для проверки доступа к объекту
        self.permission_classes = [IsOwner]
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        return Response({"data": obj.data})

    def destroy(self, request, *args, **kwargs):
        # Используем IsAdminUser для проверки доступа к объекту
        self.permission_classes = [IsAdminUser]
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        obj.delete()
        return Response({"message": "Object deleted"})

    def list(self, request, *args, **kwargs):
        # Для этого метода используется только has_permission
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Для этого метода используется только has_permission
        return super().create(request, *args, **kwargs)
```

### Заключение

- `GenericAPIView` и `ViewSet` предоставляют разные уровни абстракции для работы с представлениями в DRF, и `permission_classes` в них работает аналогично, проверяя сначала общий доступ, а затем доступ к конкретным объектам.

---

```python
from rest_framework.routers import DefaultRouter
from .views import ActorViewSet

# Создаем роутер и регистрируем ViewSet
router = DefaultRouter()
router.register(r'actors', ActorViewSet, basename='actor')

# Маршруты, создаваемые с использованием DefaultRouter
urlpatterns = [
    path('', include(router.urls)),
]

# Какие маршруты будут созданы:
# 1. GET /actors/ - вызовет метод `list` в ActorViewSet и вернет список всех актеров.
# 2. GET /actors/{id}/ - вызовет метод `retrieve` в ActorViewSet и вернет данные конкретного актера по его ID.
# 
# Какие маршруты не будут созданы:
# 1. POST /actors/ - метод `create` не будет вызван, так как он не определен в ActorViewSet.
# 2. PUT /actors/{id}/ - метод `update` не будет вызван, так как он не определен в ActorViewSet.
# 3. DELETE /actors/{id}/ - метод `destroy` не будет вызван, так как он не определен в ActorViewSet.

# Альтернативный способ ручной настройки маршрутов
urlpatterns = [
    path('actor-set/', api.ActorViewSet.as_view({'get': 'list'})),
    path('actor-set/<int:pk>/', api.ActorViewSet.as_view({'get': 'retrieve'})),
]

# Какие маршруты будут созданы:
# 1. GET /actor-set/ - вызовет метод `list` в ActorViewSet и вернет список всех актеров.
# 2. GET /actor-set/{id}/ - вызовет метод `retrieve` в ActorViewSet и вернет данные конкретного актера по его ID.
#
# Какие маршруты не будут созданы:
# 1. POST /actor-set/ - метод `create` не будет вызван, так как он не указан в ручной настройке маршрутов.
# 2. PUT /actor-set/{id}/ - метод `update` не будет вызван, так как он не указан в ручной настройке маршрутов.
# 3. DELETE /actor-set/{id}/ - метод `destroy` не будет вызван, так как он не указан в ручной настройке маршрутов.

# Альтернативный способ 2 ручной настройки маршрутов
actor_list = api.ActorModelViewSet.as_view({
    'get': 'list',    # Обрабатывает GET-запрос для получения списка объектов (метод list)
    'post': 'create'  # Обрабатывает POST-запрос для создания нового объекта (метод create)
})



from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Вариант 1: Использование ViewSet - ручная реализация методов
class ActorViewSet(viewsets.ViewSet):
    
    # Метод для получения списка всех актеров
    def list(self, request):
        queryset = Actor.objects.all()  # Получаем все объекты Actor
        serializer = ActorListSerializer(queryset, many=True)  # Сериализуем список актеров
        return Response(serializer.data)  # Возвращаем сериализованные данные

    # Метод для получения одного конкретного актера по первичному ключу (pk)
    def retrieve(self, request, pk=None):
        queryset = Actor.objects.all()  # Получаем все объекты Actor
        actor = get_object_or_404(queryset, pk=pk)  # Получаем конкретного актера или возвращаем 404, если не найден
        serializer = ActorDetailSerializer(actor)  # Сериализуем данные об актёре
        return Response(serializer.data)  # Возвращаем сериализованные данные

# Вариант 2: Использование GenericViewSet с миксинами - автоматическая реализация методов  
# - GenericViewSet добавляет лоигку с queryset и serializer_class
# - Чтобы он стал функциональным, вы добавляете миксины, например ListModelMixin и RetrieveModelMixin для `list` и `retrieve`
class ActorGenericViewSet(mixins.ListModelMixin, 
                          mixins.RetrieveModelMixin, 
                          viewsets.GenericViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    # Этот код автоматически добавляет методы `list` и `retrieve`, не требуя их явной реализации.


# Вариант 3: Использование ModelcViewSet с миксинами - автоматическая реализация методов  
class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    
    
    #3.a указать пермишены именно на 2 эти действия
    permission_classes_by_action = {
        'update': [IsAuthorCommentEntry],  # Разрешение только для автора комментария на обновление
        'destroy': [IsAuthorCommentEntry]  # Разрешение только для автора комментария на удаление
    }
    #3.b указать пермишены - для всенх остальны акшинов будет работать эти
    permission_classes = [IsAuth] 
    @action(detail=True, methods=['get', 'put'], renderer_classes=[renderers.AdminRenderer])
    def example(self, request, *args, **kwargs):
        """
        Аргумент detail=True указывает, что это действие связано c 1 конкретным объектом, а не со списком объектов.
        Этот код можно вызвать, например, по следующему URL:

         - GET /actors/1/example/: Вернет сериализованные данные актера с ID 1.
         - PUT /actors/1/example/: Обновит данные актера с ID 1, если переданы обновленные данные (нужно добавить логику для обновления).
        
        Чтобы добавить поддержку DELETE для вашего кастомного действия, вам нужно явно указать этот метод в параметре methods:
         - methods=['get', 'put', 'delete']
        """
        # Получаем объект актера
        actor = self.get_object()

        # Сериализуем объект актера с помощью ActorDetailSerializer
        serializer = ActorDetailSerializer(actor)

        # Возвращаем сериализованные данные в ответе
        return Response(serializer.data)
    
    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def my_list(self, request, *args, **kwargs):
        """
        detail=False - т.к. ЛИСТ
        #1 указать пермишены
        """
        # Вызовем метод list из родительского класса, чтобы получить список объектов
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        #2 указать пермишены
        # Проверяем, какое действие выполняется, и устанавливаем соответствующие разрешения
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]  # Доступ только для аутентифицированных пользователей
        elif self.action == 'example':
            permission_classes = [permissions.IsAuthenticated]  # Доступ только для аутентифицированных пользователей
        else:
            permission_classes = [permissions.IsAdminUser]  # Для всех остальных действий доступ только для администраторов
        return [permission() for permission in permission_classes]  # Применяем установленные классы разрешений
```

```python
from rest_framework import serializers
from .models import Actor

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'
        # Если нужно сделать поле доступным только для чтения или записи, можно использовать следующие параметры:
        read_only_fields = ['id']  # Поля, доступные только для чтения
        # extra_kwargs = {
        #     'name': {'write_only': True},  # Поля, доступные только для записи
        # }
# Пример POST запроса на создание актера
{
    "name": "Robert Downey Jr.",
    "age": 56
    # "id" не нужно передавать, так как это поле является read_only и генерируется автоматически
}

# Пример GET запроса для получения информации об актере
{
    "id": 1,
    "name": "Robert Downey Jr.",
    "age": 56
    # Поле "id" будет присутствовать в ответе, так как оно указано как read_only
}
```
---

## CUSTOM PERMISSION FOR ACTION
```python
class MixedPermission:
    """Миксин permissions для action"""
    
    def get_permissions(self):
        try:
            # Возвращает permissions, специфичные для action, если они определены
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # Если для данного action нет специфичных permissions, возвращает общие permissions
            return [permission() for permission in self.permission_classes]

# Класс ViewSet, использующий смешанные permissions
class MixedPermissionViewSetDS(MixedPermission, viewsets.ViewSet):
    pass

# Класс GenericViewSet, использующий смешанные permissions
class MixedPermissionGenericViewSetDS(MixedPermission, viewsets.GenericViewSet):
    pass

# Класс, предоставляющий действия создания, обновления и удаления с использованием смешанных permissions
class CreateUpdateDestroyDS(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.DestroyModelMixin, 
    MixedPermission, 
    viewsets.GenericViewSet
):
    pass
```
