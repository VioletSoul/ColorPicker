from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QColorDialog, QListWidget, QListWidgetItem,
                             QSpinBox, QSizePolicy, QComboBox, QStackedLayout)
from PyQt6.QtGui import QPixmap, QColor, QFont, QIcon
from PyQt6.QtCore import Qt
import sys
import random


class ColorPickerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Color Picker")
        self.resize(350, 450)
        self.setFixedSize(self.size())

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

        self.rgb_widget = QWidget()
        rgb_layout = QHBoxLayout(self.rgb_widget)
        rgb_layout.setContentsMargins(0, 0, 0, 0)
        rgb_layout.setSpacing(4)
        self.spin_r = QSpinBox()
        self._configure_spinbox(self.spin_r, "R:", 0, 255)
        self.spin_g = QSpinBox()
        self._configure_spinbox(self.spin_g, "G:", 0, 255)
        self.spin_b = QSpinBox()
        self._configure_spinbox(self.spin_b, "B:", 0, 255)
        self.button_apply_rgb = QPushButton("Apply RGB")
        self.button_apply_rgb.setFixedHeight(26)
        rgb_layout.addWidget(self.spin_r)
        rgb_layout.addWidget(self.spin_g)
        rgb_layout.addWidget(self.spin_b)
        rgb_layout.addWidget(self.button_apply_rgb)
        self.rgb_widget.setFixedHeight(32)

        self.hsv_widget = QWidget()
        hsv_layout = QHBoxLayout(self.hsv_widget)
        hsv_layout.setContentsMargins(0, 0, 0, 0)
        hsv_layout.setSpacing(4)
        self.spin_h = QSpinBox()
        self._configure_spinbox(self.spin_h, "H:", 0, 359)
        self.spin_s_hsv = QSpinBox()
        self._configure_spinbox(self.spin_s_hsv, "S:", 0, 100)
        self.spin_v = QSpinBox()
        self._configure_spinbox(self.spin_v, "V:", 0, 100)
        self.button_apply_hsv = QPushButton("Apply HSV")
        self.button_apply_hsv.setFixedHeight(26)
        hsv_layout.addWidget(self.spin_h)
        hsv_layout.addWidget(self.spin_s_hsv)
        hsv_layout.addWidget(self.spin_v)
        hsv_layout.addWidget(self.button_apply_hsv)
        self.hsv_widget.setFixedHeight(32)

        self.hsl_widget = QWidget()
        hsl_layout = QHBoxLayout(self.hsl_widget)
        hsl_layout.setContentsMargins(0, 0, 0, 0)
        hsl_layout.setSpacing(4)
        self.spin_h_hsl = QSpinBox()
        self._configure_spinbox(self.spin_h_hsl, "H:", 0, 359)
        self.spin_s_hsl = QSpinBox()
        self._configure_spinbox(self.spin_s_hsl, "S:", 0, 100)
        self.spin_l = QSpinBox()
        self._configure_spinbox(self.spin_l, "L:", 0, 100)
        self.button_apply_hsl = QPushButton("Apply HSL")
        self.button_apply_hsl.setFixedHeight(26)
        hsl_layout.addWidget(self.spin_h_hsl)
        hsl_layout.addWidget(self.spin_s_hsl)
        hsl_layout.addWidget(self.spin_l)
        hsl_layout.addWidget(self.button_apply_hsl)
        self.hsl_widget.setFixedHeight(32)

        self.button_dialog = QPushButton("Select color")
        self.custom_palette_button = QPushButton("Generate Custom Palette")
        self.palette_label = QLabel("Saved Colors:")
        self.palette_label.setFont(QFont("Arial", 11))
        self.palette_list = QListWidget()
        self.palette_list.setFixedHeight(140)
        self.clear_button = QPushButton("Clear Palette")

    def _configure_spinbox(self, spinbox, prefix, min_val, max_val):
        spinbox.setRange(min_val, max_val)
        spinbox.setPrefix(f"{prefix} ")
        spinbox.setSuffix("%" if prefix in ["S:", "V:", "L:"] else "")
        spinbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        spinbox.setFixedHeight(26)

    def _setup_layouts(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(self.mode_combo)

        preview_layout = QHBoxLayout()
        preview_layout.addWidget(self.color_label)
        preview_layout.addWidget(self.color_icon)
        preview_layout.addStretch()
        main_layout.addLayout(preview_layout)

        self.input_stack_widget = QWidget()
        self.input_stack = QStackedLayout()
        self.input_stack.setContentsMargins(0, 0, 0, 0)
        self.input_stack.setSpacing(0)
        self.input_stack_widget.setLayout(self.input_stack)

        self.input_stack.addWidget(self.rgb_widget)
        self.input_stack.addWidget(self.hsv_widget)
        self.input_stack.addWidget(self.hsl_widget)

        self.input_stack_widget.setFixedHeight(32)

        main_layout.addWidget(self.input_stack_widget)

        main_layout.addWidget(self.button_dialog)
        main_layout.addWidget(self.custom_palette_button)
        main_layout.addWidget(self.palette_label)
        main_layout.addWidget(self.palette_list)
        main_layout.addWidget(self.clear_button)

    def _connect_signals(self):
        self.mode_combo.currentIndexChanged.connect(self.input_stack.setCurrentIndex)
        self.mode_combo.currentTextChanged.connect(self._update_ui_visibility)

        self.button_apply_rgb.clicked.connect(self._apply_rgb)
        self.button_apply_hsv.clicked.connect(self._apply_hsv)
        self.button_apply_hsl.clicked.connect(self._apply_hsl)

        self.button_dialog.clicked.connect(self.choose_color_dialog)
        self.custom_palette_button.clicked.connect(self.generate_custom_palette)
        self.palette_list.itemClicked.connect(self.select_palette_color)
        self.clear_button.clicked.connect(self.clear_palette)

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 12px;
            }
            QPushButton {
                min-height: 26px;
                padding: 3px 6px;
            }
            QSpinBox {
                padding: 2px 4px;
            }
            QComboBox {
                min-height: 26px;
            }
            QListWidget {
                font-size: 11px;
            }
        """)

    def _update_ui_visibility(self):
        pass

    def _apply_rgb(self):
        color = QColor(self.spin_r.value(), self.spin_g.value(), self.spin_b.value())
        self.set_color(color)

    def _apply_hsv(self):
        color = QColor()
        color.setHsv(
            self.spin_h.value(),
            int(self.spin_s_hsv.value() * 2.55),
            int(self.spin_v.value() * 2.55)
        )
        self.set_color(color)

    def _apply_hsl(self):
        color = QColor()
        color.setHsl(
            self.spin_h_hsl.value(),
            int(self.spin_s_hsl.value() * 2.55),
            int(self.spin_l.value() * 2.55)
        )
        self.set_color(color)

    def set_color(self, color: QColor):
        if not color.isValid() or self._updating_ui:
            return

        self._updating_ui = True

        self.spin_r.setValue(color.red())
        self.spin_g.setValue(color.green())
        self.spin_b.setValue(color.blue())

        h, s, v, _ = color.getHsv()
        self.spin_h.setValue(h)
        self.spin_s_hsv.setValue(round(s / 2.55))
        self.spin_v.setValue(round(v / 2.55))

        h_hsl, s_hsl, l_hsl, _ = color.getHsl()
        self.spin_h_hsl.setValue(h_hsl)
        self.spin_s_hsl.setValue(round(s_hsl / 2.55))
        self.spin_l.setValue(round(l_hsl / 2.55))

        hex_code = color.name()
        self.color_label.setText(f"Color: {hex_code}  (R: {color.red()}, G: {color.green()}, B: {color.blue()})")
        self.color_icon.setPixmap(self.create_color_icon(color).pixmap(30, 30))
        QApplication.clipboard().setText(hex_code)

        if not self.is_color_in_palette(hex_code):
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
            r, g, b = (random.randint(0, 255) for _ in range(3))
            color = QColor(r, g, b)
            if color.isValid():
                colors.add(color.name())

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

    def is_color_in_palette(self, hex_code: str) -> bool:
        return hex_code in self.palette_colors

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
        hex_code = item.text()
        color = QColor(hex_code)
        self.set_color(color)

    def clear_palette(self):
        self.palette_list.clear()
        self.palette_colors.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorPickerApp()
    window.show()
    sys.exit(app.exec())
