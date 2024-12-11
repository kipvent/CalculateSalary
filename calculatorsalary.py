import tkinter as tk
from datetime import datetime, timedelta

# Константы
START_TIME = 8  # Начало рабочего дня
END_TIME = 19  # Конец рабочего дня
DAILY_SALARY = 3333  # Зарплата в день
WORK_HOURS = END_TIME - START_TIME  # Часы работы в день
SALARY_PER_SECOND = DAILY_SALARY / (WORK_HOURS * 3600)  # Сколько зарабатывается в секунду

# Функция для расчета заработанных денег с 8 утра за текущий день
def calculate_daily_salary():
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

# Функция для расчета заработанных денег за месяц
def calculate_monthly_salary():
    current_time = datetime.now()
    # Сколько дней прошло с начала месяца
    start_of_month = current_time.replace(day=1, hour=START_TIME, minute=0, second=0, microsecond=0)
    end_of_today = current_time.replace(hour=END_TIME, minute=0, second=0, microsecond=0)

    # Общее число дней в текущем месяце (до сегодняшнего дня включительно)
    days_passed = (current_time - start_of_month).days + 1

    # Если текущий день не закончен, корректируем сумму заработанных денег
    if current_time < end_of_today:
        monthly_salary = DAILY_SALARY * (days_passed - 1) + calculate_daily_salary()
    else:
        monthly_salary = DAILY_SALARY * days_passed

    return monthly_salary

# Функция для обновления суммы заработка в реальном времени
def update_labels():
    daily_earned = calculate_daily_salary()  # Заработок за день
    monthly_earned = calculate_monthly_salary()  # Заработок за месяц

    # Обновляем метки
    daily_label.config(text=f"Заработано за сегодня: {daily_earned:.2f} рублей")
    monthly_label.config(text=f"Заработано за месяц: {monthly_earned:.2f} рублей")
    
    window.after(10, update_labels)  # Обновляем каждые 10 миллисекунд

# Создание графического интерфейса
window = tk.Tk()
window.title("Калькулятор зарплаты для сотрудника")

# Метка для отображения заработка за день
daily_label = tk.Label(window, font=("Helvetica", 24), width=40, text="Заработано за сегодня: 0.00 рублей")
daily_label.pack(padx=20, pady=10)

# Метка для отображения заработка за месяц
monthly_label = tk.Label(window, font=("Helvetica", 24), width=40, text="Заработано за месяц: 0.00 рублей")
monthly_label.pack(padx=20, pady=10)

# Запуск обновления
update_labels()  # Первоначальный запуск

# Запуск интерфейса
window.mainloop()
