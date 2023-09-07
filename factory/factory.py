# Есть код готовки пиццы

from abc import ABC, abstractmethod


class Pizza(ABC):
    
    def prepare(self):
        ...

    def bake(self):
        ...

    def cut(self):
        ...

    def box(self):
        ...


class PepperoniPizza(Pizza):
    ...


class CheesePizza(Pizza):
    ...


def order_pizza(pizza_type: str) -> Pizza:
    pizza = None
    if pizza_type == 'pepperoni':
        pizza = PepperoniPizza()
    elif pizza_type == 'cheese':
        pizza = CheesePizza()

    pizza.prepare()
    pizza.bake()
    pizza.cut()
    pizza.box()

    return pizza

# Если меняется набор пиццы для приготовления, то необходимо будет поменять 
# метод order_pizza, а это не даёт закрыть его от изменений, хотя у него есть 
# неизменяемые аспекты. Для этого можно использовать фабрику - класс/метод, 
# который в зависимости от параметров вернёт необходимый объект.

class SimplePizzaFactory:
    
    @staticmethod
    def create_pizza(pizza_type: str) -> Pizza:
        pizza = None
        if pizza_type == 'pepperoni':
            pizza = PepperoniPizza()
        elif pizza_type == 'cheese':
            pizza = CheesePizza()

        return pizza

# ИЛИ оформить это обычным методом, в любом случае выбор конкретной реализации 
# класса Pizza инкапсулирован и теперь метод order_pizza можно закрыть от 
# изменений. Этот приём называется "простой фабрикой" и не является полноценным 
# паттерном, но может быть достаточно полезен

def order_pizza(pizza_type: str) -> Pizza:

    pizza = SimplePizzaFactory.create_pizza(pizza_type)
    pizza.prepare()
    pizza.bake()
    pizza.cut()
    pizza.box()

    return pizza

# Расширяем бизнес, теперь могут быть несколько пиццерий, которые готовят 
# одну и ту же пиццу, но в своём стиле и с небольшими изменениями.

class PizzaStore(ABC):

    def order_pizza(self, pizza_type: str) -> Pizza:

        pizza = self.create_pizza(pizza_type)
        pizza.prepare()
        pizza.bake()
        pizza.cut()
        pizza.box()

        return pizza
    
    @abstractmethod
    def create_pizza(self, pizza_type: str) -> Pizza:
        ...


class NYStylePepperoni(Pizza):
    ...

class NYStyleCheese(Pizza):
    ...

class ChicagoStylePepperoni(Pizza):
    ...

class ChicagoStyleCheese(Pizza):
    ...


class NYPizzaStore(PizzaStore):

    def create_pizza(self, pizza_type: str) -> Pizza:
        pizza = None
        if pizza_type == 'pepperoni':
            pizza = NYStylePepperoni()
        elif pizza_type == 'cheese':
            pizza = NYStyleCheese()

        return pizza
    

class ChicagoPizzaStore(PizzaStore):

    def create_pizza(self, pizza_type: str) -> Pizza:
        pizza = None
        if pizza_type == 'pepperoni':
            pizza = ChicagoStylePepperoni()
        elif pizza_type == 'cheese':
            pizza = ChicagoStyleCheese()

        return pizza

# Здесь используется паттерн Фабричный метод. Он определяет интерфейс создания 
# объекта, но позволяет субклассам выбрать класс создаваемого экземпляра. 
# Таким образом, Фабричный Метод делегирует операцию создания 
# экземпляра субклассам. 
# Т.е. в каждой нашей пиццерии есть неизменный процесс приготовления пиццы для 
# заказа, но сама пицца может отличаться, поэтому субклассам необходимо 
# реализовать только фабричный метод - все остальные части магазина неизменны.

# Пиццы делаются из одних компонентов, но в разных регионах используются разные 
# реализации этих компонентов. Фабрика поможет работать с семействами 
# ингредиентов и будет нести ответственность за создание каждого ингредиента.

class Dough(ABC):
    ...

class Sauce(ABC):
    ...

class CheesePizza(ABC):
    ...

class PepperoniPizza(ABC):
    ...


class PizzaIngredientFactory(ABC):
    
    @abstractmethod
    def create_dough(self) -> Dough:
        ...
    
    @abstractmethod
    def create_sauce(self) -> Sauce:
        ...

    @abstractmethod
    def create_cheese(self) -> CheesePizza:
        ...

    @abstractmethod
    def create_pepperoni(self) -> PepperoniPizza:
        ...


class NYPizzaIngredientFactory(PizzaIngredientFactory):

    def create_dough(self) -> Dough:
        return ThinCrustDough()
    
    def create_sauce(self) -> Sauce:
        return MarinaraSauce()
    
    def create_cheese(self) -> CheesePizza:
        return ReggianoCheese()
    
    def create_pepperoni(self) -> PepperoniPizza:
        return SlicedPepperoni()
    

class Pizza(ABC):

    @abstractmethod
    def prepare(self):
        ...
    
    def bake(self):
        ...

    def cut(self):
        ...

    def box(self):
        ...


class CheesePizza(Pizza):

    def __init__(self, ingredient_factory: PizzaIngredientFactory) -> None:
        self._ingredient_factory = ingredient_factory
    
    def prepare(self):
        dough = self._ingredient_factory.create_dough()
        sauce = self._ingredient_factory.create_sauce()
        cheese = self._ingredient_factory.create_cheese()


class NYPizzaStore(PizzaStore):

    def create_pizza(self, pizza_type: str) -> Pizza:
        pizza = None
        ingredient_factory = NYPizzaIngredientFactory()
        if pizza_type == 'cheese':
            pizza = CheesePizza(ingredient_factory)
        ...

        return pizza

# Это было применение паттерна Абстрактная Фабрика. Она предоставляет интерфейс 
# создания семейств взаимосвязанных или взаимозависимых объектов без указания 
# их конкретных классов. 
# Задача Абстрактной Фабрики — определить интерфейс для создания набора 
# продуктов. Каждый метод этого интерфейса отвечает за создание конкретного 
# продукта, и мы реализуем субкласс Абстрактной Фабрики, который предоставляет 
# эти реализации. Таким образом, паттерн фабричный метод являются естественным 
# способом реализации методов продуктов в абстрактных фабриках.
