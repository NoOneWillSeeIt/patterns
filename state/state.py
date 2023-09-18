# Пример паттерна состояния на основе автомата по продаже жвачки.


from abc import ABC


class IState(ABC):
    """Интерфейс состояний"""

    def __init__(self, context) -> None:
        self._context = context

    def insert_coin(self):
        ...

    def eject_coin(self):
        ...

    def turn_crank(self):
        ...

    def dispense(self):
        ...


class NoCoinState(IState):

    def insert_coin(self):
        print('coin inserted')
        self._context.set_state(self._context.get_has_coin_state())

    def eject_coin(self):
        print('no coin to eject')

    def turn_crank(self):
        print('insert coin first')

    def dispense(self):
        print('no coin = no gum')


class HasCoinState(IState):

    def insert_coin(self):
        print('there is already coin')

    def eject_coin(self):
        print('coin ejected')
        self._context.set_state(self._context.get_no_coin_state())

    def turn_crank(self):
        print('crank has turned')
        self._context.set_state(self._context.get_sold_state())

    def dispense(self):
        print('turn crank first')


class SoldState(IState):

    def insert_coin(self):
        print('take gum first')

    def eject_coin(self):
        print('no eject, gum sold - take it')

    def turn_crank(self):
        print('no double gum - take gum in dispenser')

    def dispense(self):
        print('sold')
        self._context.release_ball()
        if self._context.get_gumballs_count() > 0:
            self._context.set_state(self._context.get_no_coin_state())
        else:
            self._context.set_state(self._context.get_no_gum_state())
        

class NoGumState(IState):

    def insert_coin(self):
        print('no gum')

    def eject_coin(self):
        print('no gum')

    def turn_crank(self):
        print('no gum')

    def dispense(self):
        print('no gum')


class GumballMachine:
    """Context/Контекст на диаграмме классов"""

    def __init__(self, gumballs_count) -> None:
        self._gumballs_count = gumballs_count

        self._no_coin_state = NoCoinState(self)
        self._has_coin_state = HasCoinState(self)
        self._sold_state = SoldState(self)
        self._no_gum_state = NoGumState(self)

        if self._gumballs_count > 0:
            self._current_state = self._no_coin_state
        else:
            self._current_state = self._no_gum_state
    
    def set_state(self, new_state):
        self._current_state = new_state

    def insert_coin(self):
        self._current_state.insert_coin()

    def eject_coin(self):
        self._current_state.eject_coin()

    def turn_crank(self):
        self._current_state.turn_crank()

    def dispense(self):
        self._current_state.dispense()

    def release_ball(self):
        self._gumballs_count -= 1

    def get_gumballs_count(self):
        return self._gumballs_count
    
    def get_no_coin_state(self):
        return self._no_coin_state
    
    def get_has_coin_state(self):
        return self._has_coin_state
    
    def get_sold_state(self):
        return self._sold_state
    
    def get_no_gum_state(self):
        return self._no_gum_state
    

gumball_machine = GumballMachine(1)
gumball_machine.insert_coin()
gumball_machine.insert_coin()
gumball_machine.turn_crank()
gumball_machine.eject_coin()
gumball_machine.dispense()
gumball_machine.insert_coin()
