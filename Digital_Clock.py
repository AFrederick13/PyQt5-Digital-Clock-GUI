# Python Digital Clock with PyQt5

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect, QMessageBox, QDialog, QTimeEdit, QDialogButtonBox
import os
from PyQt5.QtCore import QTimer, QTime, Qt, QDate
from PyQt5.QtGui import QFont, QFontDatabase, QColor
import pygame  # For playing alarm sound


class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.time_label = QLabel(self)
        self.date_label = QLabel(self)
        self.timer = QTimer(self)
        self.alarm_time = None
        self.alarm_dialog = None
        self.set_alarm_button = QPushButton('Set Alarm', self)
        self.clear_alarm_button = QPushButton('Clear Alarm', self)

        # Initialize the mixer for sound playback.
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Digital Clock')
        self.setGeometry(700, 400, 800, 250)

        vbox = QVBoxLayout()
        # Use stretch factors to give more space to the time and date
        vbox.addWidget(self.time_label, 2)
        vbox.addWidget(self.date_label, 1)

        # --- Button Layout ---
        button_hbox = QHBoxLayout()
        button_hbox.addStretch()
        button_hbox.addWidget(self.set_alarm_button)
        button_hbox.addWidget(self.clear_alarm_button)
        button_hbox.addStretch()
        vbox.addLayout(button_hbox)

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

        # --- Button Connections and Initial State ---
        self.set_alarm_button.clicked.connect(self.set_alarm)
        self.clear_alarm_button.clicked.connect(self.clear_alarm)
        self.clear_alarm_button.setEnabled(False)

        self.setStyleSheet('''
            QWidget {
                background-color: black;
            }
            QLabel {
                color: green;
                background-color: transparent;
            }
            QLineEdit, QTimeEdit {
                background-color: #1A1A1A;
                border: 1px solid green;
                padding: 4px;
                color: green;
                border-radius: 4px;
                selection-background-color: green;
                selection-color: black;
            }
            QPushButton {
                color: green;
                background-color: #1A1A1A;
                border: 1px solid green;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2A2A2A;
            }
            QPushButton:pressed {
                background-color: #101010;
            }
            QPushButton:disabled {
                color: #4F4F4F;
                background-color: #111111;
                border-color: #4F4F4F;
            }
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
        self.set_alarm_button.setFont(my_font)
        self.clear_alarm_button.setFont(my_font)

        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.update_time()

    def update_time(self):
        now = QTime.currentTime()
        current_time = now.toString("hh:mm:ss AP")
        self.time_label.setText(current_time)
        current_date = QDate.currentDate().toString("dddd, MMMM d, yyyy")
        self.date_label.setText(current_date)

        # Check if the alarm should go off. Don't re-trigger if sound is already playing.
        if self.alarm_time and not pygame.mixer.music.get_busy():
            if now.hour() == self.alarm_time.hour() and now.minute() == self.alarm_time.minute() and now.second() == 0:
                self.trigger_alarm()

    def set_alarm(self):
        """Open a dialog to get the alarm time from the user using a 12-hour format."""
        dialog = QDialog(self)
        dialog.setWindowTitle('Set Alarm')
        layout = QVBoxLayout(dialog)

        label = QLabel("Select alarm time:")
        layout.addWidget(label)

        time_edit = QTimeEdit(dialog)
        time_edit.setDisplayFormat("hh:mm AP")
        if self.alarm_time:
            time_edit.setTime(self.alarm_time)
        else:
            time_edit.setTime(QTime.currentTime())

        # Match the digital font aesthetic but at a smaller size
        font = self.time_label.font()
        font.setPixelSize(24)
        time_edit.setFont(font)
        layout.addWidget(time_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec_() == QDialog.Accepted:
            self.alarm_time = time_edit.time()
            self.clear_alarm_button.setEnabled(True)
            QMessageBox.information(self, "Alarm Set", f"Alarm set for {self.alarm_time.toString('hh:mm AP')}.")

    def clear_alarm(self):
        """Clears the currently set alarm."""
        if self.alarm_time:
            self.alarm_time = None
            self.clear_alarm_button.setEnabled(False)
            QMessageBox.information(self, "Alarm Cleared", "The alarm has been cleared.")

    def _generate_beep(self):
        """Generates a simple beep sound as a fallback if no mp3 is found."""
        import math
        import array

        sample_rate = 44100
        duration_ms = 500
        frequency = 880.0  # A5 note
        num_samples = int(sample_rate * duration_ms / 1000.0)
        max_amplitude = 2**15 - 1  # 16-bit signed int

        # Create a mono wave
        samples = array.array('h')  # 'h' is for signed short
        for i in range(num_samples):
            angle = 2 * math.pi * i * frequency / sample_rate
            sample = int(max_amplitude * math.sin(angle))
            samples.append(sample)

        # For stereo, duplicate the sample for the second channel
        stereo_samples = array.array('h')
        for s in samples:
            stereo_samples.append(s)
            stereo_samples.append(s)

        # The buffer argument is new in pygame 2.0.0
        try:
            # Create a Sound object from the sample buffer
            sound = pygame.mixer.Sound(buffer=stereo_samples)
            return sound
        except (pygame.error, TypeError) as e:
            print(f"Warning: Could not create a fallback beep sound: {e}")
            print("Please ensure you have an 'Alarm_Music.mp3' file or a modern pygame version.")
            return None

    def trigger_alarm(self):
        """Plays the alarm sound and shows a notification."""
        if getattr(sys, 'frozen', False):
            script_dir = sys._MEIPASS
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
        # NOTE: You'll need an alarm sound file named "Alarm_Music.mp3" in the same directory.
        sound_file = os.path.join(script_dir, 'Alarm_Music.mp3')

        alarm_sound = None
        if os.path.exists(sound_file):
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play(-1)  # Play in a loop
        else:
            # If the music file is not found, play a generated beep
            alarm_sound = self._generate_beep()
            if alarm_sound:
                alarm_sound.play(loops=-1)

        self.alarm_dialog = QMessageBox(self)
        self.alarm_dialog.setIcon(QMessageBox.Information)
        self.alarm_dialog.setInformativeText("The alarm is ringing.")
        self.alarm_dialog.setWindowTitle("Alarm")
        self.alarm_dialog.setStandardButtons(QMessageBox.Ok)
        self.alarm_dialog.exec_()

        # Stop whichever sound is playing
        if alarm_sound:
            alarm_sound.stop()
        else:
            pygame.mixer.music.stop()

    def resizeEvent(self, event):
        # The VBox layout uses a 2:1 stretch factor for time:date

        # --- Time Label (gets approx. 2/3 of the space) ---
        # hh:mm:ss AP is wider, so we adjust the width divisor
        time_font_size = min(self.width() // 9, int(self.height() * (2/3) * 0.8))
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

        # --- Button Font Size ---
        button_font_size = max(10, int(date_font_size * 0.6))
        button_font = self.set_alarm_button.font()
        button_font.setPixelSize(button_font_size)
        self.set_alarm_button.setFont(button_font)
        self.clear_alarm_button.setFont(button_font)

        super().resizeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())


# project notes:

# alarm defaults to long, annoying beep when no mp3 file is found. Look into adding default alarm style mp3 file.