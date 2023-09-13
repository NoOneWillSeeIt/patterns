# Шаблонный метод представляет собой скелет алгоритма, некотрые части которого
# должны реализовываться субклассами, а некоторые части могут быть 
# необязательными.
# Абстрактный пример:

from abc import ABC, abstractmethod


class TemplateClass(ABC):

    def template_method(self):
        """Шаблонный метод, в наследниках не меняется"""
        self.prepare_data()
        self.do_smth()
        if self.hook():
            self.prepare_answer()

    def do_smth(self):
        """фиксированный алгоритм, в наследниках не меняется"""

    def hook(self):
        """Необязательный перехватчик, который реализуется по надобности"""
        return False

    @abstractmethod
    def prepare_data(self):
        """метод обязательный для переопределения в субклассах"""

    def prepare_answer(self):
        """необязательный метод, зависящий от перехватчика"""


class ConcreteClass(TemplateClass):

    def prepare_data(self):
        """метод переопределён, теперь алгоритм будет работать"""


class ConcreteClass2(TemplateClass):

    def prepare_data(self):
        """метод переопределён, теперь алгоритм будет работать"""

    def hook(self):
        """Необязательный перехватчик, результат зависит от ввода 
        пользователя"""
        ans = input('Need beautiful data output? y/n: ')
        return ans == 'y'

    def prepare_answer(self):
        """Делаем красивости"""


############################################################################
# Чуть более конкретный пример:
# Есть два класса...

class Coffee:

    def make_coffee(self):
        self.boil_water()
        self.brew_coffee_grinds()
        self.pour_in_cup()
        self.add_sugar_and_milk()


class Tea:

    def prepare_tea(self):
        self.boil_water()
        self.put_teabag_in_cup()
        self.pour_in_cup()
        self.add_lemon()

# Есть схожие пункты в приготовлении, можно объединить их в одном классе

class Beverage(ABC):

    def prepare_beverage(self):
        self.boil_water()
        self.brew()
        self.pour_in_cup()
        self.add_condiments()

    def boil_water(self):
        print('Boiling water!')

    def pour_in_cup(self):
        print('Pouring in cup')

    @abstractmethod
    def brew(self):
        ...

    @abstractmethod
    def add_condiments(self):
        ...


class Coffee(Beverage):

    def brew(self):
        print('Putting few spoons of coffee')

    def add_condiments(self):
        print('Adding sugar and milk')


class Tea(Beverage):

    def brew(self):
        print('Steeping teabag')

    def add_condiments(self):
        print('Adding lemon')

# Теперь чаю и кофе достаточно переопределить пару методов. Также можно добавить
# несколько перехватчиков, например спрашивать пользователя о добавках прежде, 
# чем добавлять их
