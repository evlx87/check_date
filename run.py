import logging
import tkinter as tk
from datetime import datetime
from tkinter.scrolledtext import ScrolledText  # Используем Text с прокруткой

# Настраиваем логирование
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S')


# Функция для автоматического распознавания и конвертации даты в нужный формат
def parse_and_format_date(date_str):
    formats_to_try = ["%d.%m.%Y", "%d%m%Y"]  # Поддерживаемые форматы дат
    for fmt in formats_to_try:
        try:
            # Пробуем распарсить дату
            date_obj = datetime.strptime(date_str, fmt).date()
            return date_obj.strftime("%d.%m.%Y"), date_obj  # Возвращаем форматированную строку и сам объект даты
        except ValueError:
            pass  # Переходим к следующему формату
    logging.error(f'Не удалось распознать дату: {date_str}')
    return None, None  # Если ни один формат не подошел, возвращаем None для обоих значений


# Функция для расчета разницы в днях между двумя датами
def calculate_days():
    start_date_str = entry_start.get().strip()
    end_date_str = entry_end.get().strip()

    # Логируем введенные даты
    logging.info(f'Получены даты: {start_date_str}, {end_date_str}')

    # Парсим и форматируем обе даты
    start_date_formatted, start_date_obj = parse_and_format_date(start_date_str)
    end_date_formatted, end_date_obj = parse_and_format_date(end_date_str)

    # Проверяем, правильно ли распарсились даты
    if start_date_obj is None or end_date_obj is None:
        result_text.config(state="normal")
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Некорректный формат даты. Используйте формат ДД.ММ.ГГГГ или ДДММГГГ.\n", 'error_red')
        result_text.config(state="disabled")
        logging.warning('Одна из дат имеет неправильный формат.')
        return

    # Проверка порядка дат
    if start_date_obj > end_date_obj:
        result_text.config(state="normal")
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Начальная дата должна быть раньше конечной!\n", 'error_red')
        result_text.config(state="disabled")
        logging.warning('Начальная дата больше конечной.')
        return

    # Вычисляем разницу в днях
    difference = abs((end_date_obj - start_date_obj).days)

    if difference > 180:
        result_text.config(state="normal")
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"ПРЕВЫШЕНИЕ 6 МЕСЯЦЕВ!\n", 'warning_orange')
        result_text.insert(tk.END, f"Количество дней между {start_date_formatted} и {end_date_formatted}: {difference}\n", 'result_black')
        result_text.config(state="disabled")
        logging.info(f'Разница в днях: {difference}. Превосходит 180 дней.')
    else:
        result_text.config(state="normal")
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Количество дней между {start_date_formatted} и {end_date_formatted}: {difference}\n", 'result_black')
        result_text.config(state="disabled")
        logging.info(f'Разница в днях: {difference}')


# Создаем главное окно приложения
root = tk.Tk()
root.title("Калькулятор разницы в днях")

# Настройка главного окна
root.geometry("400x300")  # Увеличенный размер окна для удобства чтения
root.resizable(False, False)  # Запрещаем изменение размера окна

# Поле ввода начальной даты
label_start = tk.Label(root, text="Начальная дата (ДД.ММ.ГГГГ):")
label_start.pack(pady=10)
entry_start = tk.Entry(root, width=20)
entry_start.pack()

# Поле ввода конечной даты
label_end = tk.Label(root, text="Конечная дата (ДД.ММ.ГГГГ):")
label_end.pack(pady=10)
entry_end = tk.Entry(root, width=20)
entry_end.pack()

# Кнопка для запуска расчета
button_calculate = tk.Button(root, text="Рассчитать", command=calculate_days)
button_calculate.pack(pady=10)

# Виджет для вывода результата с поддержкой стилей
result_text = ScrolledText(root, height=10, width=40, wrap=tk.WORD)
result_text.tag_configure('error_red', foreground='red')      # Красный текст для ошибок
result_text.tag_configure('warning_orange', foreground='orange')  # Оранжевый текст для предупреждений
result_text.tag_configure('result_black', foreground='black')  # Черный текст для обычных результатов
result_text.pack(pady=10)

# Запуск основного цикла приложения
root.mainloop()