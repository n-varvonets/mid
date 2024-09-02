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



from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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
```
