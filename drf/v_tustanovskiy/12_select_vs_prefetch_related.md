условно есть логика касающая преобразованию данных(условно проперти) и мы ее выводим в сериалитор, что в свою очередь качует во вью

когда удобней ее поместить в сериазаторе, когда в модели.. основные критерии

---

есть сериализатор, который сериализирует отеле и в качестве одного из полей я должен выводить номера полей, кторые в этом отеле свободны, т.е. доступны и это происходит,т.е. у нас нет отдельной логики вывода отлея(что это значит, дай пример), то где нужно разместить логику получения этих данных, т.е. как бы подготовил эти данные перед тем как они попали б сериализатор для того что оптимизировать кол-во запросов и нагрузку на базу?


---
а почему не походит select_related, а prefetch_related лучше?

---

# Оптимизация логики получения доступных номеров в отеле для сериализатора

## Задача
Необходимо сериализировать данные об отеле и вывести список доступных номеров (номеров, которые свободны для бронирования) в одном из полей сериализатора. Логика получения свободных номеров должна быть оптимизирована для уменьшения количества запросов к базе данных и нагрузки на сервер.

## Решение

### 1. Логика получения данных через модель или менеджер

Логику получения доступных номеров лучше всего разместить на уровне модели, так как это касается сущности "Отель" и её связанных объектов. Это позволит подготовить данные на уровне модели и оптимизировать запросы, используя возможности Django ORM.

### 2. Пример реализации

#### Модель "Отель" и "Номер":

```python
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    
    # Метод для получения свободных номеров
    def get_available_rooms(self):
        return self.rooms.filter(is_available=True)

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)
```

Здесь метод `get_available_rooms` возвращает свободные номера, связанные с конкретным отелем.

#### Сериализатор "Отель":

```python
class HotelSerializer(serializers.ModelSerializer):
    available_rooms = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['name', 'location', 'available_rooms']

    def get_available_rooms(self, obj):
        # Получаем свободные номера из модели
        return [room.number for room in obj.get_available_rooms()]
```

В данном случае сериализатор использует метод модели `get_available_rooms` для получения списка свободных номеров.

#### Представление (view):

Для оптимизации мы используем `prefetch_related` для предварительной загрузки связанных номеров:

```python
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

class HotelDetailView(APIView):
    def get(self, request, hotel_id):
        # Используем prefetch_related для загрузки связанных номеров
        hotel = get_object_or_404(Hotel.objects.prefetch_related('rooms'), id=hotel_id)
        serializer = HotelSerializer(hotel)
        return Response(serializer.data)
```

Использование `prefetch_related('rooms')` позволяет минимизировать количество запросов к базе данных, загружая связанные объекты (номера) за один запрос.

### 3. Вывод

- Логика получения свободных номеров должна быть размещена на уровне **модели** для оптимизации и переиспользуемости.
- Использование `prefetch_related` позволяет **оптимизировать запросы к базе данных**.
- Сериализатор использует готовую логику для получения данных, не создавая дополнительных запросов во время сериализации.
