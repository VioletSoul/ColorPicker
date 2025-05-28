from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QColorDialog, QListWidget, QListWidgetItem,
                             QSpinBox, QSizePolicy)  # Import necessary PyQt6 widgets and classes
from PyQt6.QtGui import QPixmap, QColor, QFont, QIcon  # Import GUI related classes
from PyQt6.QtCore import Qt  # Import Qt core constants
import sys  # Import system module for application exit
import random  # Import random module for palette generation


class ColorPickerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Picker")  # Set window title
        self.resize(400, 400)  # Set initial window size
        self.setFixedSize(self.size())  # Fix window size to prevent resizing

        self.palette_colors = set()  # Set to store palette colors for fast lookup

        self._create_ui()  # Create UI elements
        self._setup_layouts()  # Setup layouts and add widgets
        self._connect_signals()  # Connect signals to slots
        self._apply_styles()  # Apply basic stylesheet

    def _create_ui(self):
        # Create label to show selected color info
        self.color_label = QLabel("Color: not selected")  # Label for color info
        self.color_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))  # Set font style and size
        self.color_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)  # Align left and vertically center

        # Label to show color preview square
        self.color_icon = QLabel()  # Color preview icon
        self.color_icon.setFixedSize(20, 20)  # Fixed size for preview square
        self.color_icon.setStyleSheet("border: 1px solid #444;")  # Add border around preview

        self.button_dialog = QPushButton("Select color")  # Button to open QColorDialog

        # Spinboxes for RGB input with prefixes
        self.spin_r = QSpinBox()  # Spinbox for Red component
        self.spin_r.setRange(0, 255)  # Valid RGB range
        self.spin_r.setPrefix("R: ")  # Prefix inside spinbox

        self.spin_g = QSpinBox()  # Spinbox for Green component
        self.spin_g.setRange(0, 255)
        self.spin_g.setPrefix("G: ")

        self.spin_b = QSpinBox()  # Spinbox for Blue component
        self.spin_b.setRange(0, 255)
        self.spin_b.setPrefix("B: ")

        self.button_apply_rgb = QPushButton("Apply RGB")  # Button to apply RGB values from spinboxes

        self.custom_palette_button = QPushButton("Generate Custom Palette")  # Button to generate random palette

        self.palette_label = QLabel("Saved Colors:")  # Label above palette list
        self.palette_label.setFont(QFont("Arial", 11))  # Font size for palette label

        self.palette_list = QListWidget()  # List widget to display saved colors
        self.palette_list.setFixedHeight(140)  # Fixed height to allow scrollbar if needed
        self.palette_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Expand horizontally, fixed vertically

        self.clear_button = QPushButton("Clear Palette")  # Button to clear saved colors
        self.clear_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Expand horizontally, fixed vertically

    def _setup_layouts(self):
        main_layout = QVBoxLayout()  # Main vertical layout for the window
        self.setLayout(main_layout)  # Set main layout

        color_preview_layout = QHBoxLayout()  # Horizontal layout for label and preview
        color_preview_layout.addWidget(self.color_label)  # Add color info label
        color_preview_layout.addWidget(self.color_icon)  # Add color preview square
        color_preview_layout.addStretch()  # Add stretch to push widgets to the left
        main_layout.addLayout(color_preview_layout)  # Add preview layout to main layout

        main_layout.addWidget(self.button_dialog)  # Add color dialog button

        rgb_layout = QHBoxLayout()  # Layout for RGB spinboxes and apply button
        rgb_layout.addWidget(self.spin_r)  # Add Red spinbox
        rgb_layout.addWidget(self.spin_g)  # Add Green spinbox
        rgb_layout.addWidget(self.spin_b)  # Add Blue spinbox
        rgb_layout.addWidget(self.button_apply_rgb)  # Add apply RGB button
        main_layout.addLayout(rgb_layout)  # Add RGB layout to main layout

        main_layout.addWidget(self.custom_palette_button)  # Add generate palette button
        main_layout.addWidget(self.palette_label)  # Add palette label

        palette_layout = QVBoxLayout()  # Layout for palette list and clear button
        palette_layout.addWidget(self.palette_list)  # Add palette list widget
        palette_layout.addWidget(self.clear_button)  # Add clear palette button
        main_layout.addLayout(palette_layout)  # Add palette layout to main layout

    def _connect_signals(self):
        self.button_dialog.clicked.connect(self.choose_color_dialog)  # Connect color dialog button
        self.button_apply_rgb.clicked.connect(self.apply_rgb_color)  # Connect apply RGB button
        self.custom_palette_button.clicked.connect(self.generate_custom_palette)  # Connect generate palette button
        self.palette_list.itemClicked.connect(self.select_palette_color)  # Connect palette item click
        self.clear_button.clicked.connect(self.clear_palette)  # Connect clear palette button

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 12px;
            }
            QPushButton {
                min-height: 25px;
            }
        """)  # Basic stylesheet for consistent look

    def create_color_icon(self, color: QColor, size=20) -> QIcon:
        pixmap = QPixmap(size, size)  # Create square pixmap of given size
        pixmap.fill(color)  # Fill with specified color
        return QIcon(pixmap)  # Return QIcon from pixmap

    def generate_custom_palette(self):
        self.palette_list.clear()  # Clear existing palette
        self.palette_colors.clear()  # Clear internal color set

        colors = set()  # Temporary set to hold unique colors
        while len(colors) < 6:  # Generate 6 unique colors
            r, g, b = (random.randint(0, 255) for _ in range(3))  # Random RGB values
            color = QColor(r, g, b)
            if color.isValid():
                colors.add(color.name())  # Add hex code to set

        for hex_code in colors:
            self._add_color_to_palette(hex_code)  # Add each unique color to palette

    def choose_color_dialog(self):
        color = QColorDialog.getColor()  # Open color picker dialog
        if color.isValid():
            self.set_color(color)  # Set selected color
        else:
            self.reset_color()  # Reset if canceled

    def apply_rgb_color(self):
        r = self.spin_r.value()  # Get Red value from spinbox
        g = self.spin_g.value()  # Get Green value
        b = self.spin_b.value()  # Get Blue value
        color = QColor(r, g, b)  # Create QColor from RGB
        self.set_color(color)  # Set color

    def set_color(self, color: QColor):
        if not color.isValid():
            return  # Ignore invalid colors

        hex_code = color.name()  # Get hex code string
        r, g, b = color.red(), color.green(), color.blue()  # Extract RGB components
        self.color_label.setText(f"Color: {hex_code}  (R: {r}, G: {g}, B: {b})")  # Update label text
        self.color_icon.setPixmap(self.create_color_icon(color).pixmap(20, 20))  # Update preview icon

        QApplication.clipboard().setText(hex_code)  # Copy hex code to clipboard

        # Update spinboxes only if values differ to avoid unnecessary signals
        if self.spin_r.value() != r:
            self.spin_r.setValue(r)
        if self.spin_g.value() != g:
            self.spin_g.setValue(g)
        if self.spin_b.value() != b:
            self.spin_b.setValue(b)

        if not self.is_color_in_palette(hex_code):
            self._add_color_to_palette(hex_code)  # Add new color to palette if not present

    def reset_color(self):
        self.color_label.setText("Color: not selected")  # Reset label text
        self.color_icon.clear()  # Clear color preview icon

    def is_color_in_palette(self, hex_code: str) -> bool:
        return hex_code in self.palette_colors  # Fast lookup in set

    def _add_color_to_palette(self, hex_code: str):
        color = QColor(hex_code)
        if not color.isValid():
            return  # Ignore invalid colors
        self.palette_colors.add(hex_code)  # Add hex code to internal set
        item = QListWidgetItem(hex_code)  # Create list item with hex code text
        item.setIcon(self.create_color_icon(color))  # Set color icon for item
        self.palette_list.addItem(item)  # Add item to palette list

    def select_palette_color(self, item: QListWidgetItem):
        hex_code = item.text()  # Get hex code from clicked item
        color = QColor(hex_code)  # Create QColor from hex
        self.set_color(color)  # Set selected color

    def clear_palette(self):
        self.palette_list.clear()  # Clear all items from palette list
        self.palette_colors.clear()  # Clear internal color set


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create QApplication instance
    window = ColorPickerApp()  # Create main window instance
    window.show()  # Show window
    sys.exit(app.exec())  # Run application event loop
