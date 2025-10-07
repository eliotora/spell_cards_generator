from PySide6.QtWidgets import QWidget

class WindowsManager(dict[str, dict[str,QWidget]]):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(WindowsManager, cls).__new__(cls)
        return cls.instance

    def get_window(self, category: str, item_name:str):
        category = category.lower()
        if not category in self:
            self[category] = {}
        return self.get(category).get(item_name, None)

    def register_window(self, category:str, item_name:str, window:QWidget):
        category = category.lower()
        if not category in self:
            self[category] = {}
        self[category][item_name] = window

    def close_window(self, category:str, item_name:str):
        self[category.lower()][item_name].close()

    def close_all_windows(self):
        for category, d in self.items():
            for item_name, window in d.items():
                window.close()
