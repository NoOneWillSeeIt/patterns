# Ниже представлен класс описывающий собаку, она может лаять, а ещё мы можем её
# показать.


class Dog:

    def bark(self):
        """Make some noise"""
        print('Bark!')

    def display(self):
        """Show the creature"""


# Собаки бывают разных пород, некоторые из них лаят громко и грозно,
# а кто-то тихо и противно скрипит, поэтому используем наследование, чтобы
# каждый псинус мог самовыражаться.


class Beagle(Dog):

    def display(self):
        print('I am beagle!')


class Basenji(Dog):

    def bark(self):
        print('< silence >')

    def display(self):
        print('I am basenji')


class GermanShepherd(Dog):

    def bark(self):
        print('WOOF!')

    def display(self):
        print('I am a big german shepherd')


class ToyTerrier(Dog):

    def bark(self):
        print('squek!')
    
    def display(self):
        print('I am a lil toy terrier')


# Но не всегда собака издаёт мощный ГАВ, иногда даже большой пушистик может
# помолчать или попищать. Поведение одного и того же объекта может быть 
# изменяемым, поэтому это поведение нужно выделить из кода, чтобы оставить 
# только неизменяемые части внутри классов. В этом поможет стратегия


from abc import ABC, abstractclassmethod


class IBarkBehaviour(ABC):

    @abstractclassmethod
    def bark(self):
        """Make some noise"""


class SimpleBark(IBarkBehaviour):

    def bark(self):
        print('Bark!')


class MightyWoof(IBarkBehaviour):

    def bark(self):
        print('WOOF!')


class NoBark(IBarkBehaviour):
    
    def bark(self):
        print('< silence >')


class Squeak(IBarkBehaviour):

    def bark(self):
        print('squek')


# Выше описан интерфейс "лая" и разные его реализации. Осталось только 
# поменять классы собак, чтобы дать им свободу самовыражения.


class Dog:

    def __init__(self):
        self.bark_behaviour: IBarkBehaviour = SimpleBark()

    def set_bark_behaviour(self, bhv):
        self.bark_behaviour = bhv

    def bark(self):
        """Make some noise"""

    def display(self):
        """Show the creature"""


class Basenji(Dog):

    def __init__(self):
        self.bark_behaviour = NoBark()

    def display(self):
        print('I am basenji')

...


# Теперь поведение собаки задаётся при создании объекта, но его также можно 
# будет изменить во время выполнения при помощи set_bark_behaviour.

basenji_one = Basenji()
basenji_one.bark()
basenji_one.set_bark_behaviour(MightyWoof())
basenji_one.bark()

# В дальнейшем стратегия также может помочь, когда собакам пропишут новые 
# изменяемые действия