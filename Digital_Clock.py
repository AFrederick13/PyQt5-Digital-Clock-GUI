# Python Digital Clock with PyQt5

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
import os
from PyQt5.QtCore import QTimer, QTime, Qt, QDate
from PyQt5.QtGui import QFont, QFontDatabase, QColor


class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.time_label = QLabel(self)
        self.date_label = QLabel(self)
        self.timer = QTimer(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Digital Clock')
        self.setGeometry(700, 400, 800, 250)

        vbox = QVBoxLayout()
        # Use stretch factors to give more space
        vbox.addWidget(self.time_label, 2)
        vbox.addWidget(self.date_label, 1)
        self.setLayout(vbox)

        self.time_label.setAlignment(Qt.AlignCenter)
        self.date_label.setAlignment(Qt.AlignCenter)

        # Create a drop shadow effect for the text
        time_shadow = QGraphicsDropShadowEffect()
        time_shadow.setBlurRadius(8)
        time_shadow.setXOffset(0)
        time_shadow.setYOffset(0)
        time_shadow.setColor(QColor("green"))
        self.time_label.setGraphicsEffect(time_shadow)

        # Create a drop shadow effect for the date text
        date_shadow = QGraphicsDropShadowEffect()
        date_shadow.setBlurRadius(8)
        date_shadow.setXOffset(0)
        date_shadow.setYOffset(0)
        date_shadow.setColor(QColor("green"))
        self.date_label.setGraphicsEffect(date_shadow)

        self.time_label.setStyleSheet('''
            color: green;
            background-color: transparent;
        ''')
        self.date_label.setStyleSheet('''
            color: green;
            background-color: transparent;
        ''')

        self.setStyleSheet('''
            background-color: black;
        ''')

        # --- Using a relative path to make the project portable ---
        # Get the directory of the current script or the PyInstaller extracted location
        if getattr(sys, 'frozen', False):
            script_dir = sys._MEIPASS
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(script_dir, 'DS-DIGII.TTF')
        font_id = QFontDatabase.addApplicationFont(font_path)

        # Check if the font was loaded correctly
        if font_id < 0:
            print("Warning: Could not load DS-DIGI font. Using a default font.")
            my_font = QFont("Arial")  # Fallback font
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            my_font = QFont(font_family)
        self.time_label.setFont(my_font)
        self.date_label.setFont(my_font)

        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.update_time()

    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm AP")
        self.time_label.setText(current_time)
        current_date = QDate.currentDate().toString("dddd, MMMM d, yyyy")
        self.date_label.setText(current_date)

    def resizeEvent(self, event):
        # The VBox layout uses a 2:1 stretch factor for time:date

        # --- Time Label (gets approx. 2/3 of the space) ---
        time_font_size = min(self.width() // 7, int(self.height() * (9/10) * 0.8))
        time_font = self.time_label.font()
        time_font.setPixelSize(time_font_size)
        self.time_label.setFont(time_font)

        # Scale the drop shadow proportionally to the text
        time_shadow = self.time_label.graphicsEffect()
        if time_shadow:
            time_shadow.setBlurRadius(max(5, time_font_size // 12))
            time_shadow.setXOffset(0)
            time_shadow.setYOffset(0)

        # --- Date Label (gets approx. 1/3 of the space) ---
        date_font_size = min(self.width() // 18, int(self.height() * (1/3) * 0.8))
        date_font = self.date_label.font()
        date_font.setPixelSize(date_font_size)
        self.date_label.setFont(date_font)

        # Scale the drop shadow for the date
        date_shadow = self.date_label.graphicsEffect()
        if date_shadow:
            date_shadow.setBlurRadius(max(4, date_font_size // 8))
            date_shadow.setXOffset(0)
            date_shadow.setYOffset(0)

        super().resizeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())


# project notes:

#    * Customization: Adding a context menu (right-click) to change colors, toggle between 12/24-hour formats, or keep the window "Always on Top."