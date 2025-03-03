import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar

# Функция для автоматической конвертации даты в нужный формат
def format_date(date_str):
    try:
        # Пробуем привести строку к дате
        date_obj = datetime.strptime(date_str, "%d%m%Y").strftime("%d.%m.%Y")
        return date_obj
    except ValueError:
        return None

# Функция для открытия календаря для выбора даты
def open_calendar(entry_widget):
    def on_selection(event):
        selected_date = cal.selection_get().strftime("%d.%m.%Y")
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, selected_date)
        top.destroy()

    top = tk.Toplevel(root)
    top.title("Выберите дату")
    cal = Calendar(top, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    cal.bind('<<CalendarSelected>>', on_selection)
    cal.pack(fill="both", expand=True)

# Функция для проверки правильности формата даты
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

# Функция для расчета разницы в днях между двумя датами
def calculate_days():
    start_date_str = entry_start.get()
    end_date_str = entry_end.get()

    # Приводим дату к правильному формату
    formatted_start_date = format_date(start_date_str)
    formatted_end_date = format_date(end_date_str)

    if not is_valid_date(formatted_start_date) or not is_valid_date(formatted_end_date):
        label_result.config(text="Некорректный формат даты. Используйте формат ДД.ММ.ГГГГ.", fg="red")
        return

    try:
        # Преобразование строк в объекты даты
        start_date = datetime.strptime(formatted_start_date, "%d.%m.%Y")
        end_date = datetime.strptime(formatted_end_date, "%d.%m.%Y")

        # Вычисление разницы в днях
        difference = abs((end_date - start_date).days)

        # Проверка на превышение 6 месяцев
        if difference > 180:
            # Выводим информацию о превышении и количество дней на разных строках
            label_result.config(
                text=f"<b style='color: red'>ПРЕВЫШЕНИЕ 6 МЕСЯЦЕВ!</b><br>{formatted_start_date} до {formatted_end_date}: {difference} дней",
                justify="left",
                font=("Helvetica", 12),
                foreground="black"
            )
        else:
            label_result.config(
                text=f"{formatted_start_date} до {formatted_end_date}: {difference} дней",
                justify="left",
                font=("Helvetica", 12),
                foreground="black"
            )
    except ValueError as e:
        label_result.config(text=str(e), fg="red")

# Создаем главное окно приложения
root = tk.Tk()
root.title("Калькулятор разницы в днях")

# Настройка главного окна
root.geometry("400x300")  # Размер окна
root.resizable(False, False)  # Запрещаем изменение размера окна

# Поле ввода начальной даты
label_start = tk.Label(root, text="Начальная дата:")
label_start.pack(pady=10)
entry_start = tk.Entry(root, width=20)
entry_start.pack()
button_start_calendar = tk.Button(root, text="Выбрать дату", command=lambda: open_calendar(entry_start))
button_start_calendar.pack(pady=(0, 15))

# Поле ввода конечной даты
label_end = tk.Label(root, text="Конечная дата:")
label_end.pack(pady=10)
entry_end = tk.Entry(root, width=20)
entry_end.pack()
button_end_calendar = tk.Button(root, text="Выбрать дату", command=lambda: open_calendar(entry_end))
button_end_calendar.pack(pady=(0, 15))

# Кнопка для запуска расчета
button_calculate = tk.Button(root, text="Рассчитать", command=calculate_days)
button_calculate.pack(pady=10)

# Метка для вывода результата
label_result = tk.Label(root, text="", font=("Helvetica", 12))
label_result.pack(pady=10)

# Запуск основного цикла приложения
root.mainloop()