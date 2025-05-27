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
        self.setWindowTitle("Color Picker")  # Set window title to "Color Picker" only
        self.resize(400, 400)  # Set fixed window size width=400, height=400
        self.setFixedSize(self.size())  # Prevent window resizing by user

        main_layout = QVBoxLayout()  # Create main vertical layout for the window
        self.setLayout(main_layout)  # Set main layout to the window

        color_preview_layout = QHBoxLayout()  # Horizontal layout for color label and preview square

        self.color_label = QLabel("Color: not selected")  # Label to display hex and RGB color info
        self.color_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))  # Set font style and size
        self.color_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)  # Align vertically center and left
        color_preview_layout.addWidget(self.color_label)  # Add label to horizontal layout

        self.color_icon = QLabel()  # Label to show color preview square
        self.color_icon.setFixedSize(20, 20)  # Set fixed size same as icon in palette list (20x20 px)
        self.color_icon.setStyleSheet("border: 1px solid #444;")  # Add border around preview square
        color_preview_layout.addWidget(self.color_icon)  # Add color preview square to horizontal layout

        color_preview_layout.addStretch()  # Add stretch to push widgets to the left
        main_layout.addLayout(color_preview_layout)  # Add horizontal layout to main vertical layout

        self.button_dialog = QPushButton("Select color")  # Button to open color dialog
        self.button_dialog.clicked.connect(self.choose_color_dialog)  # Connect button click to color dialog method
        main_layout.addWidget(self.button_dialog)  # Add button to main layout

        rgb_layout = QHBoxLayout()  # Horizontal layout for RGB input spinboxes and apply button

        self.spin_r = QSpinBox()  # Spinbox for Red component input
        self.spin_r.setRange(0, 255)  # Set valid range for RGB (0-255)
        self.spin_r.setPrefix("R: ")  # Prefix label inside spinbox
        rgb_layout.addWidget(self.spin_r)  # Add spinbox to RGB layout

        self.spin_g = QSpinBox()  # Spinbox for Green component input
        self.spin_g.setRange(0, 255)  # Valid range 0-255
        self.spin_g.setPrefix("G: ")  # Prefix label
        rgb_layout.addWidget(self.spin_g)  # Add to RGB layout

        self.spin_b = QSpinBox()  # Spinbox for Blue component input
        self.spin_b.setRange(0, 255)  # Valid range 0-255
        self.spin_b.setPrefix("B: ")  # Prefix label
        rgb_layout.addWidget(self.spin_b)  # Add to RGB layout

        self.button_apply_rgb = QPushButton("Apply RGB")  # Button to apply RGB values from spinboxes
        self.button_apply_rgb.clicked.connect(self.apply_rgb_color)  # Connect click to apply RGB method
        rgb_layout.addWidget(self.button_apply_rgb)  # Add button to RGB layout

        main_layout.addLayout(rgb_layout)  # Add RGB horizontal layout to main vertical layout

        self.custom_palette_button = QPushButton("Generate Custom Palette")  # Button to generate 6 random colors
        self.custom_palette_button.clicked.connect(self.generate_custom_palette)  # Connect to palette generation method
        main_layout.addWidget(self.custom_palette_button)  # Add button to main layout

        self.palette_label = QLabel("Saved Colors:")  # Label above saved colors list
        self.palette_label.setFont(QFont("Arial", 11))  # Set font size for label
        main_layout.addWidget(self.palette_label)  # Add label to main layout

        palette_layout = QVBoxLayout()  # Vertical layout for palette list and clear button

        self.palette_list = QListWidget()  # List widget to display saved colors
        self.palette_list.setFixedHeight(140)  # Fixed height 140 px for the list to enable scrollbar if needed
        self.palette_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Expand horizontally, fixed vertically
        self.palette_list.itemClicked.connect(self.select_palette_color)  # Connect item click to color selection
        palette_layout.addWidget(self.palette_list)  # Add list to palette layout

        self.clear_button = QPushButton("Clear Palette")  # Button to clear saved colors list
        self.clear_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Expand horizontally, fixed vertically
        self.clear_button.clicked.connect(self.clear_palette)  # Connect click to clear palette method
        palette_layout.addWidget(self.clear_button)  # Add button to palette layout

        main_layout.addLayout(palette_layout)  # Add palette vertical layout to main layout

    def generate_custom_palette(self):
        self.palette_list.clear()  # Clear existing palette colors
        added = 0
        while added < 6:  # Generate exactly 6 unique random colors
            r = random.randint(0, 255)  # Random Red
            g = random.randint(0, 255)  # Random Green
            b = random.randint(0, 255)  # Random Blue
            color = QColor(r, g, b)  # Create QColor object
            hex_code = color.name()  # Get hex string like "#RRGGBB"
            if not self.is_color_in_palette(hex_code):  # Avoid duplicates
                self.add_color_to_palette(hex_code, color)  # Add to list
                added += 1

    def choose_color_dialog(self):
        color = QColorDialog.getColor()  # Open color picker dialog
        if color.isValid():  # If user selects a valid color
            self.set_color(color)  # Update UI with selected color
        else:
            self.reset_color()  # Reset if canceled

    def apply_rgb_color(self):
        r = self.spin_r.value()  # Get Red from spinbox
        g = self.spin_g.value()  # Get Green
        b = self.spin_b.value()  # Get Blue
        color = QColor(r, g, b)  # Create QColor from RGB
        self.set_color(color)  # Update UI with this color

    def set_color(self, color: QColor):
        hex_code = color.name()  # Get hex code string
        r, g, b = color.red(), color.green(), color.blue()  # Extract RGB values
        self.color_label.setText(f"Color: {hex_code}  (R: {r}, G: {g}, B: {b})")  # Update label text
        self.color_icon.setPixmap(self.create_color_pixmap(color, size=20))  # Update preview square pixmap
        QApplication.clipboard().setText(hex_code)  # Copy hex code to clipboard

        self.spin_r.setValue(r)  # Sync spinboxes with current color
        self.spin_g.setValue(g)
        self.spin_b.setValue(b)

        if not self.is_color_in_palette(hex_code):  # Add color to palette if not already present
            self.add_color_to_palette(hex_code, color)

    def reset_color(self):
        self.color_label.setText("Color: not selected")  # Reset label text
        self.color_icon.clear()  # Clear preview square

    def create_color_pixmap(self, color, size=80):
        pixmap = QPixmap(size, size)  # Create square pixmap of given size
        pixmap.fill(color)  # Fill with specified color
        return pixmap

    def is_color_in_palette(self, hex_code):
        for i in range(self.palette_list.count()):  # Iterate all items
            if self.palette_list.item(i).text() == hex_code:  # Check if hex code exists
                return True
        return False

    def add_color_to_palette(self, hex_code, color):
        item = QListWidgetItem(hex_code)  # Create new list item with hex code text
        icon_pixmap = self.create_color_pixmap(color, size=20)  # Create small color icon pixmap
        item.setIcon(QIcon(icon_pixmap))  # Set icon for item
        self.palette_list.addItem(item)  # Add item to palette list

    def select_palette_color(self, item):
        hex_code = item.text()  # Get hex code from clicked item
        color = QColor(hex_code)  # Create QColor from hex
        self.set_color(color)  # Update UI with selected color

    def clear_palette(self):
        self.palette_list.clear()  # Clear all saved colors immediately

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create QApplication instance
    window = ColorPickerApp()  # Create main window instance
    window.show()  # Show window
    sys.exit(app.exec())  # Run application event loop
