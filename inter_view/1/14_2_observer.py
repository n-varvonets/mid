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

print(subject.state)  # 0
subject.state = 123  # Все подписчики получат уведомление о новом состоянии
print(subject.state)  # 123

