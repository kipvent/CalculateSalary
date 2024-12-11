from datetime import datetime  # Импорт datetime
from PyQt5.QtWidgets import (
    QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QSlider, QComboBox, QDialog, QTextEdit
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import QTimer, Qt, QEvent, QPoint, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimedia import QMediaPlaylist
import sys
import os


class SalaryCalculator(QWidget):
    def __init__(self):
        super().__init__()

        # Зарплата по умолчанию
        self.monthly_salary = 150000
        self.daily_salary = self.monthly_salary / 30
        self.salary_per_second = self.daily_salary / (11 * 3600)  # 11 часов (8:00–19:00)
        self.music_on = False  # Состояние музыки

        # Медиа-плеер
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(os.path.abspath("relax_music1.mp3"))))
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(os.path.abspath("relax_music2.mp3"))))
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(os.path.abspath("relax_music3.mp3"))))
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(os.path.abspath("relax_music4.mp3"))))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Калькулятор зарплаты для медитации")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon("program_icon.png"))  # Задаём иконку для программы

        # Фоновое изображение
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap("relax_background.jpg").scaled(600, 400, Qt.KeepAspectRatioByExpanding))
        self.background.setGeometry(0, 0, 600, 400)

        # Шапка программы (с разноцветным текстом)
        self.header_white = QLabel("Калькулятор зарплаты для", self)
        self.header_white.setFont(QFont("Helvetica", 9, QFont.Bold))
        self.header_white.setStyleSheet("color: white; background: transparent;")
        self.header_white.setGeometry(10, 0, 250, 30)

        self.header_black = QLabel("медитации", self)
        self.header_black.setFont(QFont("Helvetica", 9, QFont.Bold))
        self.header_black.setStyleSheet("color: white; background: transparent;")
        self.header_black.setGeometry(238, 0, 330, 30)

        self.header_white.mousePressEvent = self.start_drag
        self.header_white.mouseMoveEvent = self.move_window
        self.header_black.mousePressEvent = self.start_drag
        self.header_black.mouseMoveEvent = self.move_window

        # Кнопки свернуть/закрыть
        self.minimize_button = QPushButton("_", self)
        self.minimize_button.setGeometry(540, 10, 20, 20)
        self.minimize_button.clicked.connect(self.showMinimized)

        self.close_button = QPushButton("X", self)
        self.close_button.setGeometry(570, 10, 20, 20)
        self.close_button.clicked.connect(self.close)

        # Поле ввода зарплаты
        self.salary_input = QLineEdit(self)
        self.salary_input.setPlaceholderText("Введите зарплату в месяц")
        self.salary_input.setFont(QFont("Helvetica", 14))
        self.salary_input.setGeometry(50, 35, 200, 30)

        # Метки "С" и "До"
        self.start_time_label = QLabel("С", self)
        self.start_time_label.setFont(QFont("Helvetica", 12, QFont.Bold))
        self.start_time_label.setStyleSheet("color: black;")
        self.start_time_label.setGeometry(270, 35, 50, 30)

        self.start_time_box = QComboBox(self)
        self.start_time_box.addItems([str(i) for i in range(0, 24)])
        self.start_time_box.setFont(QFont("Helvetica", 12))
        self.start_time_box.setGeometry(300, 35, 65, 30)  # Чуть уменьшена ширина
        self.start_time_box.setCurrentIndex(8)  # По умолчанию 8:00

        self.end_time_label = QLabel("До", self)
        self.end_time_label.setFont(QFont("Helvetica", 12, QFont.Bold))
        self.end_time_label.setStyleSheet("color: black;")
        self.end_time_label.setGeometry(380, 35, 50, 30)

        self.end_time_box = QComboBox(self)
        self.end_time_box.addItems([str(i) for i in range(0, 24)])
        self.end_time_box.setFont(QFont("Helvetica", 12))
        self.end_time_box.setGeometry(410, 35, 65, 30)  # Чуть уменьшена ширина
        self.end_time_box.setCurrentIndex(19)  # По умолчанию 19:00

        # Кнопка "Ваша зарплата"
        self.update_button = QPushButton("Ваша зарплата", self)
        self.update_button.setFont(QFont("Helvetica", 12))
        self.update_button.setGeometry(50, 80, 200, 30)
        self.update_button.clicked.connect(self.update_salary)

        # Заработок за сегодня
        self.daily_label = QLabel("Заработано за сегодня: 0.00 рублей", self)
        self.daily_label.setFont(QFont("Helvetica", 14, QFont.Bold))
        self.daily_label.setStyleSheet("color: black;")
        self.daily_label.setGeometry(50, 140, 500, 30)

        # Заработок за месяц
        self.monthly_label = QLabel("Заработано за месяц: 0.00 рублей", self)
        self.monthly_label.setFont(QFont("Helvetica", 14, QFont.Bold))
        self.monthly_label.setStyleSheet("color: black;")
        self.monthly_label.setGeometry(50, 180, 500, 30)

        # Музыкальные кнопки
        self.prev_button = QPushButton(self)
        self.prev_button.setIcon(QIcon("prev_icon.png"))
        self.prev_button.setGeometry(260, 80, 30, 30)
        self.prev_button.setStyleSheet("border: none;")
        self.prev_button.clicked.connect(self.previous_track)

        self.play_button = QPushButton(self)
        self.play_button.setIcon(QIcon("music_off.png"))
        self.play_button.setGeometry(300, 80, 30, 30)
        self.play_button.setStyleSheet("border: none;")
        self.play_button.clicked.connect(self.toggle_music)

        self.next_button = QPushButton(self)
        self.next_button.setIcon(QIcon("next_icon.png"))
        self.next_button.setGeometry(340, 80, 30, 30)
        self.next_button.setStyleSheet("border: none;")
        self.next_button.clicked.connect(self.next_track)

        # Ползунок громкости
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setGeometry(370, 80, 140, 30)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)

        # Кнопка "Поблагодарить"
        self.thank_button = QPushButton(self)
        self.thank_button.setIcon(QIcon("thanks_icon.png"))
        self.thank_button.setGeometry(550, 350, 50, 50)
        self.thank_button.setStyleSheet("border: none;")
        self.thank_button.clicked.connect(self.show_thank_dialog)

        # Таймер для обновления
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(100)

    def start_drag(self, event):
        self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def move_window(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)

    def toggle_music(self):
        self.music_on = not self.music_on
        if self.music_on:
            self.play_button.setIcon(QIcon("music_on.png"))
            self.player.play()
        else:
            self.play_button.setIcon(QIcon("music_off.png"))
            self.player.pause()

    def previous_track(self):
        """Переключение на предыдущий трек."""
        self.playlist.previous()

    def next_track(self):
        """Переключение на следующий трек."""
        self.playlist.next()

    def set_volume(self, value):
        self.player.setVolume(value)

    def update_labels(self):
        daily_earned = self.calculate_daily_salary()
        monthly_earned = self.calculate_monthly_salary()
        self.daily_label.setText(f"Заработано за сегодня: {daily_earned:.2f} рублей")
        self.monthly_label.setText(f"Заработано за месяц: {monthly_earned:.2f} рублей")

    def update_salary(self):
        try:
            self.monthly_salary = float(self.salary_input.text())
            self.daily_salary = self.monthly_salary / 30
            self.salary_per_second = self.daily_salary / (11 * 3600)
        except ValueError:
            self.salary_input.setPlaceholderText("Введите число!")

    def calculate_daily_salary(self):
        current_time = datetime.now()
        start_hour = int(self.start_time_box.currentText())
        end_hour = int(self.end_time_box.currentText())
        start_time = current_time.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        end_time = current_time.replace(hour=end_hour, minute=0, second=0, microsecond=0)

        if current_time < start_time:
            return 0.0
        elif current_time > end_time:
            return self.daily_salary
        else:
            elapsed_seconds = (current_time - start_time).total_seconds()
            return elapsed_seconds * self.salary_per_second

    def calculate_monthly_salary(self):
        current_time = datetime.now()
        start_of_month = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        days_passed = (current_time - start_of_month).days + 1
        return (self.daily_salary * (days_passed - 1)) + self.calculate_daily_salary()

    def show_thank_dialog(self):
        thank_dialog = QDialog(self)
        thank_dialog.setWindowTitle("Поблагодарить")
        thank_dialog.setGeometry(200, 200, 300, 200)
        thank_label = QTextEdit(thank_dialog)
        thank_label.setText(
            "Поблагодарить ©keepvent\n\nЮмани:\n4100118453538130\n\nUSDT:\n0x8910F7BF7D2208Da754Db25157c385802D455B12\n\nEmail:\nkeepwindy@yandex.ru"
        )
        thank_label.setReadOnly(True)
        thank_label.setGeometry(10, 10, 280, 180)
        thank_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = SalaryCalculator()
    calculator.show()
    sys.exit(app.exec_())
