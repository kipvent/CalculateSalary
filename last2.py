from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QSlider, QComboBox, QDialog, QTextEdit
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import QTimer, Qt, QEvent, QPoint, QUrl, QSize
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimedia import QMediaPlaylist
import sys
import os
def resource_path(relative_path):
    """Получает путь к ресурсу в .exe или рядом с .py"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(resource_path("relax_music1.mp3"))))
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(resource_path("relax_music2.mp3"))))
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(resource_path("relax_music3.mp3"))))
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(resource_path("relax_music4.mp3"))))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
 
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Калькулятор зарплаты для медитации")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(resource_path("program_icon.ico")))  # Задаём иконку для программы

        # Фоновое изображение
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap(resource_path("relax_background.jpg")))
        self.background.setScaledContents(True)

        # Шапка программы (с разноцветным текстом)
        self.header_white = QLabel("Калькулятор зарплаты для", self)
        self.header_white.setFont(QFont("Helvetica", 10, QFont.Bold))
        self.header_white.setStyleSheet("color: white; background: transparent;")

        self.header_black = QLabel("медитации", self)
        self.header_black.setFont(QFont("Helvetica", 10, QFont.Bold))
        self.header_black.setStyleSheet("color: black; background: transparent;")

        self.header_white.mousePressEvent = self.start_drag
        self.header_white.mouseMoveEvent = self.move_window
        self.header_black.mousePressEvent = self.start_drag
        self.header_black.mouseMoveEvent = self.move_window

        # Кнопки свернуть/закрыть
        self.minimize_button = QPushButton("_", self)
        self.minimize_button.clicked.connect(self.showMinimized)

        self.close_button = QPushButton("X", self)
        self.close_button.clicked.connect(self.close)

        # Поле ввода зарплаты
        self.salary_input = QLineEdit(self)
        self.salary_input.setPlaceholderText("Введите зарплату в месяц")
        self.salary_input.setFont(QFont("Helvetica", 8))  # Уменьшен шрифт до 8

        # Метки "С" и "До"
        self.start_time_label = QLabel("С", self)
        self.start_time_label.setFont(QFont("Helvetica", 12, QFont.Bold))
        self.start_time_label.setStyleSheet("color: black;")

        self.start_time_box = QComboBox(self)
        self.start_time_box.addItems([str(i) for i in range(0, 24)])
        self.start_time_box.setFont(QFont("Helvetica", 12))
        self.start_time_box.setCurrentIndex(8)

        self.end_time_label = QLabel("До", self)
        self.end_time_label.setFont(QFont("Helvetica", 12, QFont.Bold))
        self.end_time_label.setStyleSheet("color: black;")

        self.end_time_box = QComboBox(self)
        self.end_time_box.addItems([str(i) for i in range(0, 24)])
        self.end_time_box.setFont(QFont("Helvetica", 12))
        self.end_time_box.setCurrentIndex(19)

        # Кнопка "Ваша зарплата"
        self.update_button = QPushButton("Ваша зарплата", self)
        self.update_button.setFont(QFont("Helvetica", 9))  # Уменьшен шрифт
        self.update_button.clicked.connect(self.update_salary)  # Связь кнопки с обработчиком

        # Заработок за сегодня
        self.daily_label = QLabel("Заработано за сегодня: 0.00 рублей", self)
        self.daily_label.setFont(QFont("Helvetica", 14, QFont.Bold))
        self.daily_label.setStyleSheet("color: black;")

        # Заработок за месяц
        self.monthly_label = QLabel("Заработано за месяц: 0.00 рублей", self)
        self.monthly_label.setFont(QFont("Helvetica", 14, QFont.Bold))
        self.monthly_label.setStyleSheet("color: black;")

        # Музыкальные кнопки
        self.prev_button = QPushButton(self)
        self.prev_button.setIcon(QIcon(resource_path(("prev_icon.png"))))
        self.prev_button.setStyleSheet("border: none;")
        self.prev_button.clicked.connect(self.previous_track)

        self.play_button = QPushButton(self)
        self.play_button.setIcon(QIcon(resource_path(("music_off.png"))))
        self.play_button.setStyleSheet("border: none;")
        self.play_button.clicked.connect(self.toggle_music)

        self.next_button = QPushButton(self)
        self.next_button.setIcon(QIcon(resource_path(("next_icon.png"))))
        self.next_button.setStyleSheet("border: none;")
        self.next_button.clicked.connect(self.next_track)

        # Ползунок громкости
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setValue(30)
        self.volume_slider.valueChanged.connect(self.set_volume)

        # Кнопка "Поблагодарить"
        self.thank_button = QPushButton(self)
        self.thank_button.setIcon(QIcon(resource_path(("thanks_icon.png"))))
        self.thank_button.setStyleSheet("border: none;")
        self.thank_button.clicked.connect(self.show_thank_dialog)

        # Таймер для обновления
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(100)

        self.resizeEvent(None)  # Инициализация размеров

    def resizeEvent(self, event):
        """Автоматическое позиционирование элементов при изменении размеров окна."""
        self.background.setGeometry(0, 0, self.width(), self.height())
        self.header_white.setGeometry(10, 10, int(self.width() // 2.5), 30)  # Приведено к int
        self.header_black.setGeometry(self.header_white.x() + self.header_white.width() + 5, 10, int(self.width() // 5), 30)
        self.minimize_button.setGeometry(self.width() - 60, 10, 20, 20)
        self.close_button.setGeometry(self.width() - 30, 10, 20, 20)

        self.salary_input.setGeometry(50, 50, int(self.width() // 4), 30)
        self.start_time_label.setGeometry(int(self.width() // 3 + 12), 50, 60, 30)
        self.start_time_box.setGeometry(int(self.width() // 3 + 30), 50, 60, 30)
        self.end_time_label.setGeometry(int(self.width() // 3 + 95), 50, 60, 30)
        self.end_time_box.setGeometry(int(self.width() // 3 + 130), 50, 60, 30)

        self.update_button.setGeometry(50, 100, int(self.width() // 4), 30)
        self.daily_label.setGeometry(50, 180, self.width() - 50, 30)  # Расширено
        self.monthly_label.setGeometry(50, 225, self.width() - 50, 30)  # Расширено

        self.prev_button.setGeometry(int(self.width() // 2 - 65), 100, 30, 30)
        self.play_button.setGeometry(int(self.width() // 2 - 35), 100, 30, 30)
        self.next_button.setGeometry(int(self.width() // 2), 100, 30, 30)
        self.volume_slider.setGeometry(int(self.width() // 2 + 50), 100, 100, 30)  # Смещено вправо
        self.thank_button.setGeometry(self.width() - 50, self.height() - 50, 50, 50)  # Перемещена в угол


    def start_drag(self, event):
        self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def move_window(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)

    def toggle_music(self):
        self.music_on = not self.music_on
        if self.music_on:
            self.play_button.setIcon(QIcon(resource_path(("music_on.png"))))
            self.player.play()
        else:
            self.play_button.setIcon(QIcon(resource_path(("music_off.png"))))
            self.player.pause()

    def previous_track(self):
        self.playlist.previous()

    def next_track(self):
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
        thank_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = SalaryCalculator()
    calculator.show()
    sys.exit(app.exec_())
