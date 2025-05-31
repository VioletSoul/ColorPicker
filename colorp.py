import sys
import random
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QColorDialog, QListWidget,
                             QListWidgetItem, QSpinBox, QSizePolicy, QComboBox,
                             QStackedLayout)
from PyQt6.QtGui import QPixmap, QColor, QFont, QIcon
from PyQt6.QtCore import Qt

class ColorPickerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Color Picker")
        self.setFixedSize(350, 450)
        self.palette_colors = set()
        self._updating_ui = False
        self.current_mode = 'RGB'

        self._create_ui()
        self._setup_layouts()
        self._connect_signals()
        self._apply_styles()
        self._update_ui_visibility()

    def _create_ui(self):
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['RGB', 'HSV', 'HSL'])

        self.color_label = QLabel("Color: not selected")
        self.color_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.color_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        self.color_icon = QLabel()
        self.color_icon.setFixedSize(30, 30)
        self.color_icon.setStyleSheet("border: 2px solid #444; border-radius: 4px;")

        # Параметры для каждого режима: (название, диапазон, суффикс)
        self.spin_params = {
            'RGB': [('R', 0, 255, ''), ('G', 0, 255, ''), ('B', 0, 255, '')],
            'HSV': [('H', 0, 359, ''), ('S', 0, 100, '%'), ('V', 0, 100, '%')],
            'HSL': [('H', 0, 359, ''), ('S', 0, 100, '%'), ('L', 0, 100, '%')]
        }

        self.widgets = {}
        self.apply_buttons = {}

        for mode in ['RGB', 'HSV', 'HSL']:
            w = QWidget()
            layout = QHBoxLayout(w)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(4)
            spins = []
            for prefix, mn, mx, suf in self.spin_params[mode]:
                sb = QSpinBox()
                sb.setRange(mn, mx)
                sb.setPrefix(f"{prefix}: ")
                sb.setSuffix(suf)
                sb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                sb.setFixedHeight(26)
                layout.addWidget(sb)
                spins.append(sb)
            btn = QPushButton(f"Apply {mode}")
            btn.setFixedHeight(26)
            layout.addWidget(btn)
            w.setFixedHeight(32)
            self.widgets[mode] = (w, spins)
            self.apply_buttons[mode] = btn

        self.button_dialog = QPushButton("Select color")
        self.custom_palette_button = QPushButton("Generate Custom Palette")
        self.palette_label = QLabel("Saved Colors:")
        self.palette_label.setFont(QFont("Arial", 11))
        self.palette_list = QListWidget()
        self.palette_list.setFixedHeight(140)
        self.clear_button = QPushButton("Clear Palette")

    def _setup_layouts(self):
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.mode_combo)

        preview_layout = QHBoxLayout()
        preview_layout.addWidget(self.color_label)
        preview_layout.addWidget(self.color_icon)
        preview_layout.addStretch()
        main_layout.addLayout(preview_layout)

        self.input_stack = QStackedLayout()
        for mode in ['RGB', 'HSV', 'HSL']:
            self.input_stack.addWidget(self.widgets[mode][0])
        input_stack_widget = QWidget()
        input_stack_widget.setLayout(self.input_stack)
        input_stack_widget.setFixedHeight(32)
        main_layout.addWidget(input_stack_widget)

        main_layout.addWidget(self.button_dialog)
        main_layout.addWidget(self.custom_palette_button)
        main_layout.addWidget(self.palette_label)
        main_layout.addWidget(self.palette_list)
        main_layout.addWidget(self.clear_button)

    def _connect_signals(self):
        self.mode_combo.currentIndexChanged.connect(self.input_stack.setCurrentIndex)
        self.mode_combo.currentTextChanged.connect(self._update_ui_visibility)

        self.apply_buttons['RGB'].clicked.connect(self._apply_rgb)
        self.apply_buttons['HSV'].clicked.connect(self._apply_hsv)
        self.apply_buttons['HSL'].clicked.connect(self._apply_hsl)

        self.button_dialog.clicked.connect(self.choose_color_dialog)
        self.custom_palette_button.clicked.connect(self.generate_custom_palette)
        self.palette_list.itemClicked.connect(self.select_palette_color)
        self.clear_button.clicked.connect(self.clear_palette)

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget { font-family: Arial; font-size: 12px; }
            QPushButton { min-height: 26px; padding: 3px 6px; }
            QSpinBox { padding: 2px 4px; }
            QComboBox { min-height: 26px; }
            QListWidget { font-size: 11px; }
        """)

    def _update_ui_visibility(self):
        # Можно расширить при необходимости
        pass

    def _apply_rgb(self):
        r, g, b = (sb.value() for sb in self.widgets['RGB'][1])
        self.set_color(QColor(r, g, b))

    def _apply_hsv(self):
        h, s, v = (sb.value() for sb in self.widgets['HSV'][1])
        c = QColor()
        c.setHsv(h, int(s * 2.55), int(v * 2.55))
        self.set_color(c)

    def _apply_hsl(self):
        h, s, l = (sb.value() for sb in self.widgets['HSL'][1])
        c = QColor()
        c.setHsl(h, int(s * 2.55), int(l * 2.55))
        self.set_color(c)

    def set_color(self, color: QColor):
        if not color.isValid() or self._updating_ui:
            return
        self._updating_ui = True

        # RGB
        r, g, b = color.red(), color.green(), color.blue()
        for sb, val in zip(self.widgets['RGB'][1], (r, g, b)):
            sb.setValue(val)

        # HSV
        h, s, v, _ = color.getHsv()
        for sb, val in zip(self.widgets['HSV'][1], (h, round(s / 2.55), round(v / 2.55))):
            sb.setValue(val)

        # HSL
        h, s, l, _ = color.getHsl()
        for sb, val in zip(self.widgets['HSL'][1], (h, round(s / 2.55), round(l / 2.55))):
            sb.setValue(val)

        hex_code = color.name()
        self.color_label.setText(f"Color: {hex_code}  (R: {r}, G: {g}, B: {b})")
        self.color_icon.setPixmap(self.create_color_icon(color).pixmap(30, 30))
        QApplication.clipboard().setText(hex_code)

        if hex_code not in self.palette_colors:
            self._add_color_to_palette(hex_code, color)

        self._updating_ui = False

    def create_color_icon(self, color: QColor, size=20) -> QIcon:
        pixmap = QPixmap(size, size)
        pixmap.fill(color)
        return QIcon(pixmap)

    def generate_custom_palette(self):
        self.palette_list.clear()
        self.palette_colors.clear()
        colors = set()
        while len(colors) < 7:
            c = QColor(*[random.randint(0, 255) for _ in range(3)])
            if c.isValid():
                colors.add(c.name())
        for hex_code in colors:
            self._add_color_to_palette(hex_code)

    def choose_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.set_color(color)
        else:
            self.reset_color()

    def reset_color(self):
        self.color_label.setText("Color: not selected")
        self.color_icon.clear()

    def _add_color_to_palette(self, hex_code: str, color: QColor = None):
        if not color:
            color = QColor(hex_code)
        if not color.isValid():
            return
        self.palette_colors.add(hex_code)
        item = QListWidgetItem(hex_code)
        item.setIcon(self.create_color_icon(color))
        self.palette_list.addItem(item)

    def select_palette_color(self, item: QListWidgetItem):
        self.set_color(QColor(item.text()))

    def clear_palette(self):
        self.palette_list.clear()
        self.palette_colors.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorPickerApp()
    window.show()
    sys.exit(app.exec())
