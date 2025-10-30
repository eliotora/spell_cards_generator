from PySide6.QtWidgets import QWidget, QSpinBox, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

class CoinWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.coins = {}
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()

        title = QLabel("COINS", alignment=Qt.AlignmentFlag.AlignCenter)

        h_layout = QHBoxLayout()


        for i, coin_type in enumerate(["CP", "SP", "EP", "GP", "PP"]):
            coin_layout = QVBoxLayout()
            coin_label = QLabel(coin_type, alignment=Qt.AlignmentFlag.AlignCenter)
            coin_spin = QSpinBox()
            coin_spin.wheelEvent = lambda event: event.ignore()
            coin_spin.setMinimum(0)

            coin_layout.addWidget(coin_label)
            coin_layout.addWidget(coin_spin)
            h_layout.addLayout(coin_layout)
            self.coins[coin_type] = (coin_label, coin_spin)

        layout.addWidget(title)
        layout.addLayout(h_layout)

        return layout




