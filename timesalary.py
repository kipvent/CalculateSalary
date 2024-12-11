import tkinter as tk
from datetime import datetime

# Константы
START_TIME = 8  # Начало рабочего дня
END_TIME = 19  # Конец рабочего дня
DAILY_SALARY = 5000  # Зарплата за день
WORK_HOURS = END_TIME - START_TIME  # Часы работы в день
SALARY_PER_HOUR = DAILY_SALARY / WORK_HOURS  # Сколько зарабатывается в час
SECONDS_IN_HOUR = 3600  # Секунд в одном часе

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
        earned_money = (elapsed_seconds / (WORK_HOURS * SECONDS_IN_HOUR)) * DAILY_SALARY
        return earned_money

# Функция для анимации плавного увеличения числа
def animate_salary(target_amount):
    current_amount = float(money_label.cget("text").replace("Заработано за сегодня: ", "").replace(" рублей", ""))
    step = (target_amount - current_amount) / 20  # Делаем 20 шагов до новой суммы

    def update_animation():
        nonlocal current_amount
        if current_amount < target_amount:
            current_amount += step  # Увеличиваем текущую сумму
            if current_amount > target_amount:
                current_amount = target_amount  # Ограничиваем сумму
            money_label.config(text=f"Заработано за сегодня: {current_amount:.2f} рублей")
            window.after(10, update_animation)  # Обновляем каждые 10 миллисекунд
        else:
            money_label.config(text=f"Заработано за сегодня: {target_amount:.2f} рублей")  # Финальное значение

    update_animation()  # Запуск анимации

# Обновление данных в интерфейсе
def update_label():
    earned_money = calculate_salary()  # Вычисляем заработок
    animate_salary(earned_money)  # Запускаем анимацию для текущей суммы
    window.after(1000, update_label)  # Обновляем каждую секунду

# Создание графического интерфейса
window = tk.Tk()
window.title("Калькулятор зарплаты")

# Добавление метки для отображения зарплаты
money_label = tk.Label(window, font=("Helvetica", 24), width=40, text="Заработано за сегодня: 0.00 рублей")
money_label.pack(padx=20, pady=20)

# Запуск обновления
update_label()  # Первоначальный запуск

# Запуск интерфейса
window.mainloop()
