# Фасад предоставляет упрощённый интерфейс к группе объектов для работы с ними.
# В примере ниже фасад загружает картинку, изменяет её размер, а затем сохраняет 
# по заданному пути.


class NetworkLoader:

    def load_from_url(self, url: str) -> bytes:
        ...


class File:

    def __init__(self, bytes_data: bytes) -> None:
        pass

    def get_bytes(self) -> bytes:
        pass


class Image(File):

    def resize(self, width, height):
        pass


class FileManager:

    def load_bytes(self, bytes_data: bytes) -> None:
        pass

    def save_file(self, path: str) -> None:
        pass


class UrlReceiverFacade:

    def __init__(self, network_loader: NetworkLoader, 
                 file_manager: FileManager) -> None:
        self._net_loader = network_loader
        self._file_manager = file_manager

    def receive_img_and_save(self, url: str, path: str) -> None:
        net_data = self._net_loader.load_from_url(url)
        image = Image(net_data)
        image.resize(250, 250)
        self._file_manager.load_bytes(image.get_bytes())
        self._file_manager.save_file(path)


network_loader = NetworkLoader()
file_manager = FileManager()
facade = UrlReceiverFacade(network_loader, file_manager)
facade.receive_img_and_save('http://', 'c:\\users\\123.png')
