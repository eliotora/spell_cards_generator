from PyQt6.QtCore import QAbstractTableModel, Qt

class JSONTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data_list = data
        self.keys = list(data[0].keys()) if data else []

    def rowCount(self, parent=None):
        return len(self.data_list)

    def columnCount(self, parent=None):
        return len(self.keys)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            row = self.data_list[index.row()]
            key = self.keys[index.column()]
            return str(row.get(key, ""))

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.keys[section]
            else:
                return str(section + 1)
