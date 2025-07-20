from PyQt6.QtCore import QObject, pyqtSignal

class SharedDict(QObject):
    categoryChanged = pyqtSignal(str, list)

    def __init__(self):
        super().__init__()
        self._data: dict[str, list[str]] = {}

    def add_item(self, key: str, item:str):
        if key not in self._data:
            self._data[key] = []
        if item and item not in self._data[key]:
            self._data[key].append(item)
            self.categoryChanged.emit(key, self._data[key])

    def remove_item(self, key: str, item:str):
        if key in self._data and item in self._data[key]:
            self._data[key].remove(item)
            self.categoryChanged.emit(key, self._data[key])

    def get_list(self, key: str) -> list[str]:
        return list(self._data.get(key, []))

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def add_list(self, key, list):
        self._data[key] = list