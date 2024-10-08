
# Разница между `@property` и `@cached_property`

В Python существуют два основных типа свойств для классов: обычные свойства (`@property`) и кешированные свойства (`@cached_property`). Рассмотрим их различия:

## 1. `@property`

- **Каждый раз выполняется**: Свойство вычисляется при каждом доступе.
- **Пример использования**:

    ```python
    class MyClass:
        @property
        def my_property(self):
            # Этот код выполняется каждый раз, когда к свойству обращаются
            return calculate_something()
    ```

- **Когда использовать**: Подходит, если значение может изменяться и необходимо пересчитывать его при каждом обращении.

## 2. `@cached_property`

- **Один раз выполняется, потом кешируется**: Свойство вычисляется только один раз, при первом доступе. Затем результат сохраняется, и при последующих обращениях возвращается кешированное значение.
- **Пример использования**:

    ```python
    from functools import cached_property

    class MyClass:
        @cached_property
        def my_property(self):
            # Этот код выполнится только один раз, затем результат будет кеширован
            return calculate_something()
    ```

- **Когда использовать**: Полезно, если свойство является затратным для вычисления, и результат не изменяется в течение жизни объекта.

---

# Жизненный цикл объекта в Django REST Framework (DRF)

В Django REST Framework (DRF) объекты создаются и управляются при обработке запросов, как часть веб-приложения. Объекты в DRF могут быть различными сущностями, такими как:

## 1. **View (Представления)**:
   В каждом запросе DRF создает экземпляр представления для обработки запроса.
   
   - **Жизненный цикл**: Экземпляр создается для каждого входящего HTTP-запроса и уничтожается после обработки запроса (обычно после возвращения ответа). Это временный объект.
   
   - **Кеширование**: Не имеет смысла кешировать объект представления, так как он живет только в контексте одного запроса. Однако, можно кешировать результаты работы представления (например, выходные данные API), чтобы избежать повторной обработки запроса, если данные не изменились.

## 2. **Serializer (Сериализаторы)**:
   Сериализаторы используются для преобразования данных модели в JSON-формат и обратно.
   
   - **Жизненный цикл**: Экземпляры сериализаторов также создаются и используются в рамках одного запроса.
   
   - **Кеширование**: Кеширование сериализатора может быть полезно, если сериализация данных является дорогостоящей операцией (например, при работе с большими объемами данных или сложными зависимостями). Однако кешируются обычно не сами объекты сериализатора, а результат их работы (например, закешированные JSON-ответы).

## 3. **Model (Модели)**:
   Модели — это объекты, представляющие данные базы данных.
   
   - **Жизненный цикл**: Экземпляры модели существуют в памяти в течение запроса, пока на них есть ссылки. Если объект модели загружен в процессе запроса, то он будет уничтожен после завершения обработки запроса.
   
   - **Кеширование**: 
     - Кеширование объектов модели может значительно повысить производительность, особенно если эти объекты часто запрашиваются и не изменяются.
     - Пример: Можно использовать Django-кеш или внешние системы, такие как Redis, чтобы кешировать результаты сложных запросов к базе данных, тем самым избегая повторного выполнения запросов.
   
## 4. **QuerySet (Набор запросов)**:
   Набор запросов — это ленивый объект, представляющий запрос к базе данных.
   
   - **Жизненный цикл**: QuerySet выполняется только в момент обращения к данным. После выполнения запроса результатом становится список объектов модели.
   
   - **Кеширование**: QuerySet можно кешировать для повторного использования результатов сложных запросов. Это особенно актуально для дорогих запросов, которые возвращают большие наборы данных.

---

# Зачем кешировать свойства с `@cached_property`?

```python
class MySerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(source='cleaned_views_count')

class MyView(APIView):
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        log.info(f"Views: {instance.cleaned_views_count}")
        return Response({'views': instance.cleaned_views_count})
```

```python
   from functools import cached_property

   class MyClass:
       @cached_property
       def cleaned_views_count(self) -> list[int]:
           if self.creative != "video":
               return []
           if not self.views_count:
               return [0]
           return self.views_count
   ```

# Зачем кешировать свойства с `@cached_property`?

## Причины кеширования в вашем случае:
1. **Многократное использование в одном запросе**:
   - Свойство может вызываться **несколько раз** в одном запросе, например, в <u>**сериализаторе** и **представлении (view)**</u>.
   - Без кеширования метод будет пересчитываться при каждом вызове, что увеличивает нагрузку.

2. **Оптимизация производительности**:
   - Если вычисление свойства требует обращения к базе данных или выполнения других затратных операций, кеширование позволяет избежать повторных вычислений, используя один и тот же результат.

## Пример:
В сериализаторе и вью свойство `cleaned_views_count` может вызываться несколько раз:
```python
class MySerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(source='cleaned_views_count')

class MyView(APIView):
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        log.info(f"Views: {instance.cleaned_views_count}")
        return Response({'views': instance.cleaned_views_count})
```