# Итераторы глубоко интегрированы в Python, любой перебор в цикле for 
# производится через итераторы. 
# Для реализации итератора достаточно определить два магических метода: __iter__
# и __next__. В классе-коллекции по которой можно итерироваться нужно определить 
# __iter__ - метод должен возвращать объект итератора. Для самого итератора 
# __iter__ возвращает самого себя.
# __next__ возвращает следующий элемент. Когда все элементы пройдены нужно 
# бросить исключение StopIteration.
# Абстрактный пример, который не является хорошей реализацией, но показывает 
# как это работает в питоне.

class List:

    def __init__(self) -> None:
        self._list = []

    def __iter__(self):
        return Iterator(self._list)
    
    def append(self, element):
        self._list.append(element)


class Iterator:

    def __init__(self, collection: List) -> None:
        self._collection = collection
        self._current_elem = -1

    def __iter__(self):
        return self
    
    def __next__(self):
        self._current_elem += 1
        if self._current_elem == len(self._collection):
            raise StopIteration

        return self._collection[self._current_elem]


dumb_list = List()

# добавляем элементы
for i in range(20):
    dumb_list.append(i)

# вот тут работает итератор
for i in dumb_list:
    print(i)
