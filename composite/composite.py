# Компоновщик объединяет интерфейс объекта и группы объектов, создавая 
# древовидную структуру, в которой корень - комбинация элементов, а листьями 
# могут быть как конкретные элементы, так и дополнительные комбинации

# Пример: обычный удлинитель часто содержит несколько розеток, но в некоторые 
# из них может быть воткнут другой удлинитель, а в него другой и т.д. 
# (так делать нинада, это опасно!).
# В этом случае одна из розеток заменяется целым набором. С помощью компоновщика 
# можно описать подобный интерфейс и взаимодействие с ним.
from abc import ABC, abstractmethod
from typing import Self


class ISocketComponent(ABC):
    """компонент на диаграмме"""

    WALL_SOURCE = 'wall'

    def __init__(self, power_source = None) -> None:
        ...

    def set_power_source(self, power_source) -> None:
        raise AttributeError

    # методы уникальные для розетки

    def voltage(self):
        raise AttributeError

    def live(self):
        raise AttributeError

    def neutral(self):
        raise AttributeError

    def earth(self):
        raise AttributeError
    
    def plug(self, device):
        """Подключить устройство"""
        raise AttributeError
    
    def get_device(self):
        """Вернуть подключенное устройство, если есть"""
        raise AttributeError
    
    # методы общие для розетки и удлинителя

    def print_status(self, prefix=''):
        """Вывести статус розетки/удлинителя"""
        raise AttributeError
    
    def unplug(self):
        """Отсоединить устройство"""
        raise AttributeError
    
    @property
    def has_power(self):
        raise AttributeError
    
    def power_up(self):
        raise AttributeError
    
    def power_off(self):
        raise AttributeError
    
    # методы уникальные для удлинителя
    
    def set_outlets(self, outlet_count: int) -> None:
        """Установить розетки"""
        raise AttributeError
    
    def swap_socket(self, old_socket, new_socket) -> None:
        """Сменить розетку"""
        raise AttributeError
    
    def get_free_outlet(self) -> Self:
        """Вернуть свободную розетку"""
        raise AttributeError
    
    
class UKSocket(ISocketComponent):
    """лепесток/leaf на диаграмме"""

    def __init__(self, power_source = None) -> None:
        self._device_plugged = None
        self._power_source = power_source

    def voltage(self):
        if self.has_power:
            return 230
        return 0
    
    def live(self):
        if self.has_power:
            return 1
        return 0
    
    def neutral(self):
        if self.has_power:
            return -1
        return 0
    
    def earth(self):
        return 0
    
    @property
    def has_power(self):
        return self._power_source.has_power

    def power_up(self):
        """Если прибор подключен, то можно его включить"""
        ...

    def power_off(self):
        """Выключить подключенный прибор"""
        ...

    def plug(self, device):
        if isinstance(device, PowerStrip):
            self._power_source.swap_socket(self, device)
            device.set_power_source(self._power_source)
        else:
            self._device_plugged = device

    def get_device(self):
        return self._device_plugged

    def unplug(self):
        self._device_plugged = None

    def print_status(self, prefix = ''):
        if self.has_power:
            if self._device_plugged:
                print(f'{prefix}Got device: {self._device_plugged.name}')
            else:
                print(f'{prefix}Got power and ready')
        else:
            print(f'{prefix}No power')

    def get_free_outlet(self) -> Self:
        if self._device_plugged:
            return None
        
        return self



class PowerStrip(ISocketComponent):
    """удлинитель/composite на диаграмме"""

    def __init__(self, power_source = None) -> None:
        self._power_source = power_source
        self._outlets = []

    def print_status(self, prefix = '') -> None:
        print(f'{prefix}PowerStrip:')
        for outlet in self._outlets:
            outlet.print_status(f'{prefix}\t')

    def set_power_source(self, power_source):
        self._power_source = power_source
        if self.has_power:
            self.power_up()

    @property
    def has_power(self):
        if not self._power_source:
            return False
        
        return self._power_source == self.WALL_SOURCE or \
            self._power_source.has_power

    def power_up(self):
        for outlet in self._outlets:
            outlet.power_up()

    def power_off(self):
        for outlet in self._outlets:
            outlet.power_off()

    def set_outlets(self, outlet_count):
        self._outlets = [UKSocket(self) for i in range(outlet_count)]

    def unplug(self):
        if self._power_source and self._power_source != self.WALL_SOURCE:
            self._power_source.swap_socket(self, UKSocket(self._power_source))
        else:
            # если нет родителя, а розетку вырвали с корнем из стены
            print('Disconnected from grid, maybe house collapsed')

    def swap_socket(self, old_socket, new_socket) -> None:
        for ind in range(len(self._outlets)):
            if self._outlets[ind] == old_socket:
                self._outlets[ind] = new_socket

    def get_free_outlet(self) -> Self:
        for outlet in self._outlets:
            free_outlet = outlet.get_free_outlet()
            if free_outlet:
                return free_outlet
        
        return None


class Device:

    _device_name: str = ''

    @property
    def name(self) -> str:
        return self._device_name


class Kettle(Device):

    _device_name = 'Electric kettle'


class Iron(Device):

    _device_name = 'Iron'


class PlayStation(Device):

    _device_name = 'PlayStation'


# Розетка в стене будет набором, т.к. в стене может быть как 1 разъём для 
# подключения, так сразу несколько
wall_outlet = PowerStrip(ISocketComponent.WALL_SOURCE)
wall_outlet.set_outlets(1)

power_strip = PowerStrip()
power_strip.set_outlets(3)

free_outlet = wall_outlet.get_free_outlet()
free_outlet.plug(power_strip)

power_strip2 = PowerStrip()
power_strip2.set_outlets(3)

free_outlet = power_strip.get_free_outlet()
free_outlet.plug(power_strip2)

free_outlet = power_strip.get_free_outlet()
free_outlet.plug(Kettle())

free_outlet = power_strip2.get_free_outlet()
free_outlet.plug(Iron())

free_outlet = power_strip2.get_free_outlet()
free_outlet.plug(PlayStation())

wall_outlet.print_status()

# Для розеток и удлинителей скомпоновали общий интерфейс и создали древовидную 
# структуру. В некоторых местах методы выполняются рекрсивно, за счёт чего 
# осуществляется перебор вложенных элементов - print_status, power_up, 
# power_off, has_power. На первый взгляд метод unplug для розетки и для 
# удлинителя отличается, т.к. для розетки он отсоединяет устройство, а для 
# удлинителя - сам удлинитель. Но удлинитель - устройство с несколькими 
# розетками, которое расширяет интерфейс одной розетки, при подключении, поэтому
# становится логично, что при отключении интерфейс розетки возвращается к 
# прежнему.

# Можно было бы улучшить поиск свободной розетки или добавить метод подключения 
# в удлинитель, раз он сам выдаёт первую свободную розетку. Но мне достаточно и 
# этого.