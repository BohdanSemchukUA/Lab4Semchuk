from openpyxl import Workbook
import pandas as pd
from datetime import datetime

try:
    # Завантаження даних з CSV-файлу
    staff_data = pd.read_csv('employees.csv')

    # Конвертація стовпця з датою народження у формат datetime
    staff_data['Дата народження'] = pd.to_datetime(staff_data['Дата народження'])

    # Обчислення віку працівників
    current_date = pd.Timestamp(datetime.now())
    staff_data['Вік'] = staff_data['Дата народження'].apply(
        lambda birth_date: current_date.year - birth_date.year - (
                (current_date.month, current_date.day) < (birth_date.month, birth_date.day))
    )

    # Розподіл на вікові категорії
    age_groups = {
        'до_18': staff_data[staff_data['Вік'] < 18],
        '18_до_45': staff_data[(staff_data['Вік'] >= 18) & (staff_data['Вік'] <= 45)],
        '46_до_70': staff_data[(staff_data['Вік'] > 45) & (staff_data['Вік'] <= 70)],
        'понад_70': staff_data[staff_data['Вік'] > 70]
    }

    # Запис у Excel-файл з кількома листами
    try:
        with pd.ExcelWriter('employees_age_groups.xlsx', engine='openpyxl') as excel_writer:
            # Запис всіх даних на окремий лист
            staff_data.to_excel(excel_writer, sheet_name='Загальні_дані', index=False)

            # Запис даних для кожної вікової категорії на окремий лист
            for group_name, group_data in age_groups.items():
                group_data.to_excel(excel_writer, sheet_name=group_name, index=False)

        print("Файл успішно створено!")

    except PermissionError:
        print("Помилка доступу: можливо, файл вже відкритий або у вас недостатньо прав для запису.")

    except OSError as os_err:
        print(f"Системна помилка: неможливо створити файл. {os_err}")

except FileNotFoundError:
    print("Помилка: CSV файл з даними не знайдено.")

except Exception as err:
    print(f"Виникла помилка: {err}")
