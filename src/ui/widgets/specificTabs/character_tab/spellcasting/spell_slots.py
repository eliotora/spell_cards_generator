from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QCheckBox, QSpinBox
from PySide6.QtCore import Qt

class SpellSlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()

        title = QLabel("SPELL SLOTS", alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)

        h_layout = QHBoxLayout()

        g_layouts = [QGridLayout() for _ in range(3)]
        for i, nbr in enumerate([4,3,3,3,3,2,2,1,1]):
            if i % 3 == 0:
                current_layout = g_layouts[i//3]
                total_label = QLabel("Total")
                current_layout.addWidget(total_label, 0, 1, Qt.AlignmentFlag.AlignCenter)
                total_label = QLabel("Expended")
                current_layout.addWidget(total_label, 0, 2, Qt.AlignmentFlag.AlignLeft)
            level_label = QLabel(f"Level {i+1}")
            current_layout.addWidget(level_label, i%3+1, 0, Qt.AlignmentFlag.AlignCenter)
            total_line_edit = QSpinBox()
            total_line_edit.setMaximum(nbr)
            total_line_edit.setMinimum(0)
            total_line_edit.wheelEvent = lambda event: event.ignore()
            current_layout.addWidget(total_line_edit, i%3+1, 1)
            checkbox_layout = QHBoxLayout()
            for j in range(nbr):
                chkbx = QCheckBox()
                checkbox_layout.addWidget(chkbx, alignment=Qt.AlignmentFlag.AlignLeft)
            checkbox_layout.addStretch()
            current_layout.addLayout(checkbox_layout, i%3+1, 2)

        h_layout.addLayout(g_layouts[0])
        h_layout.addLayout(g_layouts[1])
        h_layout.addLayout(g_layouts[2])

        layout.addLayout(h_layout)

        return layout

    def update_display(self):
        self.modifier_edit.setText(f"+{self.modifier}" if self.modifier >= 0 else f"{self.modifier}")
        self.save_dc.setText(f"{8 + self.modifier + self.profiency}")
        self.modifier_edit.setText(f"+{self.modifier + self.profiency}" if self.modifier + self.profiency >= 0 else f"{self.modifier + self.profiency}")

    def update_modifier(self, value:int):
        self.modifier = value
        self.update_display()

    def update_proficency(self, value:int):
        self.profiency = value
        self.update_display()
