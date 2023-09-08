# Паттерн Команда отделяет объект, выдающий запросы, от объекта, который умеет 
# эти запросы выполнять.

from abc import ABC, abstractmethod


class Invoker:

    def set_command(self):
        ...


class ICommand(ABC):

    @abstractmethod
    def execute(self):
        ...    


class Receiver:

    def do_smth(self):
        ...


class CommandExample(ICommand):

    def __init__(self, receiver_obj: Receiver) -> None:
        self.receiver = receiver_obj

    def execute(self):
        ...    

# В примере выше выполнение каких-то функций объектом-исполнителем 
# инкапсулировано от инициатора за интерфейсом команды. Инициатор только 
# располагает набором команд и вызывает их по мере необходимости через 
# известный ему интерфейс.
# Более наглядный пример:

class NoCommand(ICommand):
    """Заглушка"""

    def execute(self):
        pass


class MusicPlayer:
    """Receiver/исполнитель"""

    def play(self):
        print('playing music')


class PlayMusicCommand(ICommand):
    """Команда включения музыки"""

    def __init__(self, receiver_obj) -> None:
        self._receiver = receiver_obj
        
    def execute(self):
        self._receiver.play()


class ButtonPanel:  
    """Invoker/инициатор"""

    button_quantity = 10

    def __init__(self) -> None:
        # Сначала заполним действиями-пустышками с подходящим интерфейсом
        self.buttons = [NoCommand] * self.button_quantity

    def handle_btn_pressed(self, idx):
        self.buttons[idx].execute()

    def set_command(self, idx, command: ICommand):
        self.buttons[idx] = command

# Панель с кнопками и музыкальный плеер живут отдельно и независимо друг от 
# друга
btn_panel = ButtonPanel()
music_player = MusicPlayer()

# Инкапсулируем проигрывание музыки плеером в команду
play_music_command = PlayMusicCommand(music_player)

# Теперь при нажатии на 2 (0, 1, ...) кнопку будет включаться проигрывание 
# музыки
btn_panel.set_command(1, play_music_command)
btn_panel.handle_btn_pressed(1)

# Панелей с кнопками может быть несколько, команды на проигрывание могут идти 
# из разных источников, но приходить они будут через единый интерфейс и о 
# подробностях реализации ничего знать не будут
