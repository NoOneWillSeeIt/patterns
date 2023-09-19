# Заместитель может выполнять разные роли и по разному применяться в зависимости 
# от поставленной задачи: имитировать локальный объект, когда на самом деле 
# объект к которому требуется обратиться находится на удалённом сервере
# (удалённый заместитель), в качестве виртуального объекта-заглушки, который
# ожидает загрузки данных(виртуальный заместитель, в примере ниже как раз он) 
# и т.д.

class IconInterface:

    def get_height(self) -> int:
        ...

    def get_width(self) -> int:
        ...

    def draw(self) -> None:
        ...


class ImageIcon(IconInterface):

    def __init__(self, binary_data) -> None:
        self._binary_data = binary_data


    def get_height(self) -> int:
        # Получить высоту изображения
        ...

    def get_width(self) -> int:
        # Получить высоту изображения
        ...

    def draw(self) -> None:
        # Отрисовать изображение
        ...


class ProxyIcon(IconInterface):

    def __init__(self, url: str) -> None:
        self._url = url
        self._image: ImageIcon = None

    def get_height(self) -> int:
        if self._image is None:
            return 600
        
        self._image.get_height()

    def get_width(self) -> int:
        if self._image is None:
            return 800
        
        self._image.get_width()

    def set_image_icon(self, image_icon):
        self._image = image_icon

    def draw(self) -> None:
        if self._image is None:
            print('Loading image')
            load_image(self, self._url)

        self._image.draw()


def load_image(proxy, url):
    """Грузим картинку в отдельном потоке
        потом проставляем картинку в прокси через set_image_icon
    """
    ...


# создаём объект, который будем отрисовывать в ожидании данных от удалённого 
# сервера
image = ProxyIcon('localhost:8080')
# отрисовываем объект-заглушку
image.draw()
...
# через некоторое время изображение уже может быть загружено
image.draw()