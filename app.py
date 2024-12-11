import tkinter as tk
from datetime import datetime

# Константы
START_TIME = 8  # Начало рабочего дня
END_TIME = 19  # Конец рабочего дня
DAILY_SALARY = 3333  # Зарплата в день
WORK_HOURS = END_TIME - START_TIME  # Часы работы в день
SALARY_PER_SECOND = DAILY_SALARY / (WORK_HOURS * 3600)  # Сколько зарабатывается в секунду

# Функция для расчета заработанных денег с 8 утра
def calculate_salary():
    current_time = datetime.now()
    start_time = current_time.replace(hour=START_TIME, minute=0, second=0, microsecond=0)
    end_time = current_time.replace(hour=END_TIME, minute=0, second=0, microsecond=0)

    # Если текущее время раньше 8:00, заработок 0
    if current_time < start_time:
        return 0.0
    # Если текущее время после конца рабочего дня, заработок фиксированный
    elif current_time > end_time:
        return DAILY_SALARY
    else:
        # Время, прошедшее с 8:00 утра, в секундах
        elapsed_seconds = (current_time - start_time).total_seconds()
        # Считаем заработок пропорционально времени
        earned_money = elapsed_seconds * SALARY_PER_SECOND
        return earned_money

# Функция для обновления суммы в реальном времени
def update_label():
    earned_money = calculate_salary()  # Текущий заработок
    money_label.config(text=f"Заработано за сегодня: {earned_money:.2f} рублей")  # Обновляем метку
    window.after(10, update_label)  # Обновляем каждые 10 миллисекунд

# Создание графического интерфейса
window = tk.Tk()
window.title("Бабки Наськи")

# Добавление метки для отображения зарплаты
money_label = tk.Label(window, font=("Helvetica", 24), width=40, text="Заработано за сегодня: 0.00 рублей")
money_label.pack(padx=20, pady=20)

# Запуск обновления
update_label()  # Первоначальный запуск

# Запуск интерфейса
window.mainloop()