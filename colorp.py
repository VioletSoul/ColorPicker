from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QColorDialog, QListWidget, QListWidgetItem,
                             QSpinBox, QSizePolicy)
from PyQt6.QtGui import QPixmap, QColor, QFont, QIcon
from PyQt6.QtCore import Qt
import sys
import random

class ColorPickerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Picker with RGB Input")
        self.resize(400, 490)  # Уменьшенная высота окна
        self.setFixedSize(self.size())

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Горизонтальный лэйаут для метки и цветного квадрата предпросмотра
        color_preview_layout = QHBoxLayout()

        self.color_label = QLabel("Color: not selected")
        self.color_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.color_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        color_preview_layout.addWidget(self.color_label)

        self.color_icon = QLabel()
        self.color_icon.setFixedSize(20, 20)  # Размер квадрата 20x20
        self.color_icon.setStyleSheet("border: 1px solid #444;")
        color_preview_layout.addWidget(self.color_icon)

        color_preview_layout.addStretch()
        main_layout.addLayout(color_preview_layout)

        self.button_dialog = QPushButton("Select color")
        self.button_dialog.clicked.connect(self.choose_color_dialog)
        main_layout.addWidget(self.button_dialog)

        rgb_layout = QHBoxLayout()
        self.spin_r = QSpinBox()
        self.spin_r.setRange(0, 255)
        self.spin_r.setPrefix("R: ")
        rgb_layout.addWidget(self.spin_r)

        self.spin_g = QSpinBox()
        self.spin_g.setRange(0, 255)
        self.spin_g.setPrefix("G: ")
        rgb_layout.addWidget(self.spin_g)

        self.spin_b = QSpinBox()
        self.spin_b.setRange(0, 255)
        self.spin_b.setPrefix("B: ")
        rgb_layout.addWidget(self.spin_b)

        self.button_apply_rgb = QPushButton("Apply RGB")
        self.button_apply_rgb.clicked.connect(self.apply_rgb_color)
        rgb_layout.addWidget(self.button_apply_rgb)

        main_layout.addLayout(rgb_layout)

        self.custom_palette_button = QPushButton("Generate Custom Palette")
        self.custom_palette_button.clicked.connect(self.generate_custom_palette)
        main_layout.addWidget(self.custom_palette_button)

        self.palette_label = QLabel("Saved Colors:")
        self.palette_label.setFont(QFont("Arial", 11))
        main_layout.addWidget(self.palette_label)

        palette_layout = QVBoxLayout()

        self.palette_list = QListWidget()
        self.palette_list.setFixedHeight(140)  # Фиксированная высота списка 140 пикселей
        self.palette_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.palette_list.itemClicked.connect(self.select_palette_color)
        palette_layout.addWidget(self.palette_list)

        self.clear_button = QPushButton("Clear Palette")
        self.clear_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.clear_button.clicked.connect(self.clear_palette)
        palette_layout.addWidget(self.clear_button)

        main_layout.addLayout(palette_layout)

    def generate_custom_palette(self):
        self.palette_list.clear()
        added = 0
        while added < 6:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = QColor(r, g, b)
            hex_code = color.name()
            if not self.is_color_in_palette(hex_code):
                self.add_color_to_palette(hex_code, color)
                added += 1

    def choose_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.set_color(color)
        else:
            self.reset_color()

    def apply_rgb_color(self):
        r = self.spin_r.value()
        g = self.spin_g.value()
        b = self.spin_b.value()
        color = QColor(r, g, b)
        self.set_color(color)

    def set_color(self, color: QColor):
        hex_code = color.name()
        r, g, b = color.red(), color.green(), color.blue()
        self.color_label.setText(f"Color: {hex_code}  (R: {r}, G: {g}, B: {b})")
        self.color_icon.setPixmap(self.create_color_pixmap(color, size=20))
        QApplication.clipboard().setText(hex_code)

        self.spin_r.setValue(r)
        self.spin_g.setValue(g)
        self.spin_b.setValue(b)

        if not self.is_color_in_palette(hex_code):
            self.add_color_to_palette(hex_code, color)

    def reset_color(self):
        self.color_label.setText("Color: not selected")
        self.color_icon.clear()

    def create_color_pixmap(self, color, size=80):
        pixmap = QPixmap(size, size)
        pixmap.fill(color)
        return pixmap

    def is_color_in_palette(self, hex_code):
        for i in range(self.palette_list.count()):
            if self.palette_list.item(i).text() == hex_code:
                return True
        return False

    def add_color_to_palette(self, hex_code, color):
        item = QListWidgetItem(hex_code)
        icon_pixmap = self.create_color_pixmap(color, size=20)
        item.setIcon(QIcon(icon_pixmap))
        self.palette_list.addItem(item)

    def select_palette_color(self, item):
        hex_code = item.text()
        color = QColor(hex_code)
        self.set_color(color)

    def clear_palette(self):
        self.palette_list.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorPickerApp()
    window.show()
    sys.exit(app.exec())
