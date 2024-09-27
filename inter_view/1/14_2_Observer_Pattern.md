
# Паттерн Наблюдатель (Observer Pattern)

## Описание

**Назначение**: Паттерн Наблюдатель используется для создания системы подписки, которая позволяет объектам получать уведомления об изменениях в других объектах.

**Принцип работы**: В этом паттерне субъект хранит список своих наблюдателей и уведомляет их об изменениях своего состояния. Наблюдатели подписываются на субъект, чтобы автоматически получать обновления.

## Пример реализации на Python

```python
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self):
        for observer in self._observers:
            observer.update(self)

class ConcreteSubject(Subject):
    def __init__(self, state=0):
        super().__init__()
        self._state = state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.notify()

class Observer:
    def update(self, subject):
        pass

class ConcreteObserver(Observer):
    def update(self, subject):
        print(f'Наблюдатель получил новое состояние: {subject.state}')

# Пример использования
subject = ConcreteSubject()

observer_a = ConcreteObserver()
observer_b = ConcreteObserver()

subject.attach(observer_a)
subject.attach(observer_b)

subject.state = 123  # Все подписчики получат уведомление о новом состоянии
```

## Как использовать

1. Создайте объект `ConcreteSubject`.
2. Создайте один или несколько объектов `ConcreteObserver`.
3. Подключите наблюдателей к субъекту с помощью метода `attach`.
4. Измените состояние субъекта.

Когда состояние субъекта изменяется, все подписанные наблюдатели автоматически уведомляются.

## Применение

Этот паттерн часто используется в программировании GUI, системах реального времени, где нужно обеспечивать актуальность данных у нескольких получателей.
