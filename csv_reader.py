import matplotlib.pyplot as plt
import pandas as pd

try:
    # Завантаження даних із CSV-файлу
    staff_df = pd.read_csv('employees.csv')

    # Підрахунок загальної кількості чоловіків та жінок
    gender_distribution = staff_df['Стать'].value_counts()
    print(f"Загальна кількість чоловіків: {gender_distribution.get('Чоловік', 0)}")
    print(f"Загальна кількість жінок: {gender_distribution.get('Жінка', 0)}")

    # Візуалізація гендерного розподілу
    gender_distribution.plot(kind='bar', title='Гендерний склад працівників')
    plt.xlabel('Стать')
    plt.ylabel('Кількість працівників')
    plt.show()

    # Обробка вікових даних
    staff_df['Дата народження'] = pd.to_datetime(staff_df['Дата народження'])
    current_date = pd.Timestamp.now()
    staff_df['Вік'] = staff_df['Дата народження'].apply(
        lambda birth_date: current_date.year - birth_date.year - (
            (current_date.month, current_date.day) < (birth_date.month, birth_date.day))
    )

    # Поділ на вікові групи
    age_groups = {
        'молодші_18': staff_df[staff_df['Вік'] < 18],
        '18_до_45': staff_df[(staff_df['Вік'] >= 18) & (staff_df['Вік'] <= 45)],
        '46_до_70': staff_df[(staff_df['Вік'] > 45) & (staff_df['Вік'] <= 70)],
        'понад_70': staff_df[staff_df['Вік'] > 70]
    }

    # Виведення кількості співробітників у кожній віковій групі та розподіл за статтю
    for age_group_name, group_data in age_groups.items():
        male_count = group_data[group_data['Стать'] == 'Чоловік'].shape[0]
        female_count = group_data[group_data['Стать'] == 'Жінка'].shape[0]
        print(f"{age_group_name}: {len(group_data)} співробітників")
        print(f"  - Кількість чоловіків: {male_count}")
        print(f"  - Кількість жінок: {female_count}")

        # Графік для гендерного поділу в межах кожної вікової групи
        group_data['Стать'].value_counts().plot(kind='bar', title=f'Гендерний склад у групі {age_group_name}')
        plt.xlabel('Стать')
        plt.ylabel('Кількість')
        plt.show()

except FileNotFoundError:
    print("Помилка: файл CSV не знайдено!")

except Exception as error:
    print(f"Виникла непередбачувана помилка: {error}")
