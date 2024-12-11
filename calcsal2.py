from PyQt5.QtWidgets import (
    QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QSlider, QComboBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QTimer, Qt
from datetime import datetime


class SalaryCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.monthly_salary = 150000
        self.daily_salary = self.monthly_salary / 30
        self.salary_per_second = self.daily_salary / (8 * 3600)  # 8 часов в день

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Калькулятор зарплаты для медитации")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Фоновое изображение
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap("relax_background.jpg").scaled(600, 400, Qt.KeepAspectRatioByExpanding))
        self.background.setGeometry(0, 0, 600, 400)

        # Поле ввода зарплаты
        self.salary_input = QLineEdit(self)
        self.salary_input.setPlaceholderText("Введите зарплату в месяц")
        self.salary_input.setFont(QFont("Helvetica", 14))
        self.salary_input.setGeometry(50, 30, 200, 30)

        # Метки "С" и "До"
        self.start_time_label = QLabel("С", self)
        self.start_time_label.setFont(QFont("Helvetica", 12, QFont.Bold))
        self.start_time_label.setStyleSheet("color: black;")
        self.start_time_label.setGeometry(270, 30, 50, 30)

        self.start_time_box = QComboBox(self)
        self.start_time_box.addItems([str(i) for i in range(0, 24)])
        self.start_time_box.setFont(QFont("Helvetica", 12))
        self.start_time_box.setGeometry(300, 30, 50, 30)
        self.start_time_box.setCurrentIndex(8)

        self.end_time_label = QLabel("До", self)
        self.end_time_label.setFont(QFont("Helvetica", 12, QFont.Bold))
        self.end_time_label.setStyleSheet("color: black;")
        self.end_time_label.setGeometry(370, 30, 50, 30)

        self.end_time_box = QComboBox(self)
        self.end_time_box.addItems([str(i) for i in range(0, 24)])
        self.end_time_box.setFont(QFont("Helvetica", 12))
        self.end_time_box.setGeometry(400, 30, 50, 30)
        self.end_time_box.setCurrentIndex(17)

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

        # Регулировка громкости
        self.volume_label = QLabel("Громкость", self)
        self.volume_label.setFont(QFont("Helvetica", 10))
        self.volume_label.setStyleSheet("color: black;")
        self.volume_label.setGeometry(270, 80, 80, 30)

        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setGeometry(340, 80, 200, 30)

        # Кнопка "Поблагодарить"
        self.thank_button = QPushButton("❤", self)
        self.thank_button.setFont(QFont("Helvetica", 16))
        self.thank_button.setGeometry(550, 10, 40, 40)

        # Таймер для обновления
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(100)

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
        return self.daily_salary * days_passed

    def update_labels(self):
        daily_earned = self.calculate_daily_salary()
        monthly_earned = self.calculate_monthly_salary()
        self.daily_label.setText(f"Заработано за сегодня: {daily_earned:.2f} рублей")
        self.monthly_label.setText(f"Заработано за месяц: {monthly_earned:.2f} рублей")

    def update_salary(self):
        try:
            self.monthly_salary = float(self.salary_input.text())
            self.daily_salary = self.monthly_salary / 30
            self.salary_per_second = self.daily_salary / (8 * 3600)
        except ValueError:
            self.salary_input.setPlaceholderText("Введите число!")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    calculator = SalaryCalculator()
    calculator.show()
    sys.exit(app.exec_())
