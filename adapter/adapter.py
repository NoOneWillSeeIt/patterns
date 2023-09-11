# Адаптер используется для преобразования вызовов методов одного интерфейса к 
# вызовам другого интерфейса.
# Абстрактный пример: есть клиентский объект, который работает с объектами, 
# реализующимим интерфейс ITarget. Есть объект, который требуется адаптировать 
# (экземпляр Adaptee) для работы с клиентским объектом. Для этого применяем 
# адаптер, который преобразует вызовы к ITarget к вызовам к Adaptee.

from abc import ABC, abstractmethod


class ITarget(ABC):
    """Целевой интерфейс"""

    @abstractmethod
    def do_smth(self):
        ...


class Client:
    """Клиент, который взаимодействует с объектами"""

    def __init__(self, target: ITarget) -> None:
        self._target = target

    def do_smth_for_client(self):
        self._target.do_smth()


class Adaptee:
    """Класс объекты которого необходимо адаптировать"""

    def do_smth_good(self):
        print('I\'m doing smth good')


class Adapter(ITarget):

    def __init__(self, adaptee: Adaptee) -> None:
        self._adaptee = adaptee

    def do_smth(self):
        return self._adaptee.do_smth_good()
    

concrete_adaptee = Adaptee()
adapter = Adapter(concrete_adaptee)
client = Client(adapter)
client.do_smth_for_client()

# Более конкретный пример: чайник с американской вилкой требует адаптера для 
# подключения в английскую розетку

class UKSocketInterface(ABC):

    @abstractmethod
    def voltage(self):
        ...

    @abstractmethod
    def live(self):
        ...

    @abstractmethod
    def neutral(self):
        ...

    @abstractmethod
    def earth(self):
        ...
    

class UKSocket(UKSocketInterface):
    """Adaptee"""

    def voltage(self):
        return 230
    
    def live(self):
        return 1
    
    def neutral(self):
        return -1
    
    def earth(self):
        return 0
    

class USASocketInterface(ABC):
    """Target"""

    @abstractmethod
    def voltage(self):
        ...

    @abstractmethod
    def live(self):
        ...

    @abstractmethod
    def neutral(self):
        ...


class Adapter(USASocketInterface):
    """Adapter"""

    def __init__(self, socket) -> None:
        self._socket = socket

    def voltage(self):
        return 110
    
    def live(self):
        return self._socket.live()
    
    def neutral(self):
        return self._socket.neutral()
    

class ElectricKettle:
    """Client"""

    def __init__(self, power) -> None:
        self._power = power

    def boil(self):
        if self._power.voltage() > 110:
            print('Burn the kitchen')
        else:
            if self._power.live() == 1 and self._power.neutral() == -1:
                print('No power')
            else:
                print('Done!')


socket = UKSocket()
adapter = Adapter(socket)
kettle = ElectricKettle(adapter)
kettle.boil()
