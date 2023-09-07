# Паттерн одиночка представляет собой объект, который не даёт создавать 
# дополнительные экземпляры самого себя.
# Питонячьи способы сделать синглтон:
# 1. Класс

from typing import Any


class Singleton:

    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        
        # Т.к. __new__ возвращает экземпляр, то для него каждый раз будет 
        # вызываться __init__
        return cls.__instance
    
# Минусом является возможность наследования и следовательно переопределение 
# __new__ в потомках.

# 2. Декоратор

def singleton_decorator(class_):
    instance = None
    def get_instance_wrapper(*args, **kwargs):
        nonlocal instance
        if not instance:
            instance = class_(*args, **kwargs)
        return instance
    
    return get_instance_wrapper


@singleton_decorator
class A:
    ...

# Минусом такого подхода является, что type(A) покажет, что это функция, поэтому
# нельзя использовать классовые и статические методы. Также всё ещё можно 
# создать второй экземпляр через type(A())()

# 3. Метакласс

class Singleton(type):

    __instance = None

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if not self.__instance:
            self.__instance = super().__call__(*args, **kwargs)

        return self.__instance


class A(metaclass=Singleton):
    ...