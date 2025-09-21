# Python Digital Clock with PyQt5

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
import os
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont, QFontDatabase


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

        self.time_label.setStyleSheet('''
            font-size: 100px;
            color: green;
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
