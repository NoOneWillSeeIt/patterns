# Декораторы применяются для расширения существующего функционала, расширяя уже 
# написанный код, но не изменяя его. Позволяет модифицировать данные до или 
# после выполнения операций декорируемого объекта.
# Позволяет гибко расширять код, но может добавить большую иерархию мелких 
# классов, разобраться в которых потом достаточно сложно.

from abc import ABC, abstractmethod


class Beverage(ABC):

    _description: str = 'Unknown beverage'

    def get_description(self) -> str:
        return self._description
    
    @abstractmethod
    def cost(self) -> float:
        ...


class Latte(Beverage):

    _description: str = 'Latte'

    def cost(self) -> float:
        return 1.5
    

class CondimentDecorator(Beverage):

    def __init__(self, beverage: Beverage):
        self._beverage = beverage

    @abstractmethod
    def get_description(self) -> str:
        ...


class Whip(CondimentDecorator):
    
    def get_description(self) -> str:
        return self._beverage.get_description() + ', Whip'
    
    def cost(self) -> float:
        return self._beverage.cost() + 0.2
    

beverage = Latte()
beverage = Whip(beverage)

print('Order: ' + beverage.get_description())
print(f'Cost: {beverage.cost()}$')
