# Существует объект, в который записываются данные считанные с датчиков на 
# метеостанции. Его описание выглядит так:

class WeatherData:

    def __init__(self):
        self._temperature = None
        self._humidity = None
        self._pressure = None
    
    def set_measurements(self, temperature, humidity, pressure):
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure

    @property        
    def temperature(self):
        return self._temperature
    
    @property
    def humidity(self):
        return self._humidity
    
    @property
    def pressure(self):
        return self._pressure
    
# При изменении данных в объекте нам может понадобиться обновить отображение 
# состояний текущей погоды, статистики, ближайшего прогноза. Хорошим решением 
# станет применение паттерна Наблюдатель. 
# Суть его в следующем - есть наблюдатели, которые зависят от субъекта и 
# при изменении состояния последнего получают оповещения об этом и могут 
# поменять уже своё состояние. Для текущей задачи подойдут следующие интерфейсы

from abc import ABC, abstractmethod


class IObserver(ABC):

    @abstractmethod
    def update(self, temperature, humidity, pressure):
        """Update observer condition"""


class ISubject(ABC):

    @abstractmethod
    def subscribe(self, observer: IObserver):
        """Subscribe observer for updates"""

    @abstractmethod
    def unsubscribe(self, observer: IObserver):
        """Unsubscribe observer"""

    @abstractmethod
    def notify(self):
        """Notify subs"""

# Теперь субъекту достаточно унаследовать интерфейс ISubject и реализовать его 
# методы, а наблюдателям - унаследовать IObserver и подписаться на обновления 
# субъекта

class WeatherData(ISubject):

    def __init__(self):
        self._temperature = None
        self._humidity = None
        self._pressure = None
        # Для set важно, чтобы объект в него помещаемый был хэшируемым.
        self._subscribers = set()
    
    def set_measurements(self, temperature, humidity, pressure):
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        # Данные изменились, можно уведомлять
        self.notify()

    def subscribe(self, observer: IObserver):
        self._subscribers.add(observer)

    def unsubscribe(self, observer: IObserver):
        self._subscribers.discard(observer)

    def notify(self):
        # Для наблюдателей не должно быть разницы в каком порядке их уведомлять, 
        # иначе это повышает связность кода. Также set не гарантирует порядок 
        # итерации элементов
        for observer in self._subscribers:
            observer.update(self.temperature, self.humidity, self.pressure)
    
    @property        
    def temperature(self):
        return self._temperature
    
    @property
    def humidity(self):
        return self._humidity
    
    @property
    def pressure(self):
        return self._pressure
    
# Показания с датчиков могут обновляться слишком часто, поэтому вводится 
# специальный флаг, который будет ограничивать количество оповещений 
# наблюдателей.

class WeatherData(ISubject):

    def __init__(self):
        ...
        self._state_changed = False
    
    def _set_changed(self):
        self._state_changed = True
    
    def _clear_changed(self):
        self._state_changed = False
    
    def set_measurements(self, temperature, humidity, pressure):
        # Будем оповещать наблюдателей только в случае, если температура 
        # изменилась полградуса и более
        if abs(temperature - self._temperature) >= 0.5:
            self._set_changed()
        ...

    ...

    def notify(self):
        if self.has_changed:
            for observer in self._subscribers:
                observer.update(self.temperature, self.humidity, self.pressure)

            self._clear_changed()
    
    @property        
    def has_changed(self):
        return self._state_changed
    
# Остаётся проблема с тем, что набор данных передаваемых в метод update для 
# наблюдателей может изменяться. Править набор аргументов в интерфейсе, а затем 
# в каждой реализации - трудозатратно и неправильно. Лучше передать ссылку на 
# субъект, чтобы наблюдатель мог сам получить из него нужные данные. 
# Дополнительные данные, которые захочет нам отдать субъект будем получать 
# в отдельный объект.

class IObserver(ABC):

    @abstractmethod
    def update(self, subject: ISubject, additional_args: dict = None):
        """Update observer condition"""


class CurrentCondition(IObserver):

    def update(self, subject: ISubject, additional_args: dict = None):
        if isinstance(subject, WeatherData):
            print(f'Current conditions: temperature {subject.temperature}C '\
                  f'degrees and {subject.humidity}% humidity')

class WeatherData(ISubject):

    def notify(self, additional_args = None):
        if self.has_changed:
            for observer in self._subscribers:
                observer.update(self, additional_args)

            self._clear_changed()
