# Python Digital Clock with PyQt5

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
import os
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont, QFontDatabase, QColor


class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.time_label = QLabel(self)
        self.timer = QTimer(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Digital Clock')
        self.setGeometry(700, 400, 500, 200)

        vbox = QVBoxLayout()
        vbox.addWidget(self.time_label)
        self.setLayout(vbox)

        self.time_label.setAlignment(Qt.AlignCenter)

        # Create a drop shadow effect for the text
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setXOffset(1)
        shadow.setYOffset(1)
        shadow.setColor(QColor("green"))
        self.time_label.setGraphicsEffect(shadow)

        self.time_label.setStyleSheet('''
            font-size: 100px;
            color: green;
            background-color: transparent;
        ''')

        self.setStyleSheet('''
            background-color: black;
        ''')

        # --- Using a relative path to make the project portable ---
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(script_dir, 'DS-DIGII.TTF')
        font_id = QFontDatabase.addApplicationFont(font_path)

        # Check if the font was loaded correctly
        if font_id < 0:
            print("Warning: Could not load DS-DIGI font. Using a default font.")
            my_font = QFont("Arial", 100)  # Fallback font
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            my_font = QFont(font_family, 100)
        self.time_label.setFont(my_font)

        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.update_time()

    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        self.time_label.setText(current_time)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())


# project notes:
#   1. Visual Enhancements
#    * Modern Aesthetics: The current "green on black" is classic but could be modernized with a subtle glow (drop shadow) or gradient.
#    * Window Transparency: A frameless, semi-transparent window would allow the clock to "float" on the desktop.
#    * Responsive Layout: The font size is hardcoded (100px). Making it scale with the window size would improve usability.

#   2. Features
#    * Date Display: Adding the current date below the time.
#    * Customization: Adding a context menu (right-click) to change colors, toggle between 12/24-hour formats, or keep the window "Always on Top."
#    * Interactive Draggable Window: If the window is frameless, you'll need logic to drag it around.

#   3. Code Quality & Project Structure
#    * Refactoring: Move the UI setup and styling into separate methods or a stylesheet file (.qss) for better readability.
#    * Error Handling: Improve font loading logic (it's already decent, but could be more robust).
#    * Packaging: You have build/ and dist/ folders, suggesting you've tried PyInstaller. I can help optimize the build script to ensure the .TTF font is bundled correctly.