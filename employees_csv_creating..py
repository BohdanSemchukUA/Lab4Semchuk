import csv
import random
from faker import Faker

# Ініціалізація Faker для української мови
fake = Faker('uk_UA')

# Оновлений словник для вибору по батькові
patronymic_names = {
    'male': [
        'Данилович, Олександрович, Ярославович, Борисович, Тарасович, Євгенович',
        'Костянтинович', 'Максимович', 'Назарович', 'Олександрович', 'Павлович', 'Романович',
        'Святославович', 'Тарасович', 'Юрійович', 'Ярославович', 'Ілліч', 'Степанович'
    ],
    'female': [
        'Ярославівна', 'Анатоліївна', 'Іллівна', 'Данилівна', 'Павлівна', 'Євгенівна',
        'Костянтинівна', 'Максимівна', 'Назарівна', 'Олександрівна', 'Павлівна', 'Романівна',
        'Святославівна', 'Тарасівна', 'Юріївна', 'Ярославівна', 'Іллівна', 'Степанівна'
    ]
}


# Генерація випадкового по батькові на основі статі
def get_patronymic(gender):
    return random.choice(patronymic_names[gender])


# Генерація даних про одного працівника
def create_employee(gender):
    if gender == 'male':
        first_name = fake.first_name_male()
        last_name = fake.last_name_male()
        middle_name = get_patronymic('male')
        gender_label = 'Чоловік'
    else:
        first_name = fake.first_name_female()
        last_name = fake.last_name_female()
        middle_name = get_patronymic('female')
        gender_label = 'Жінка'

    birth_date = fake.date_of_birth(minimum_age=16, maximum_age=86)
    position = fake.job()
    city = fake.city()
    address = fake.address()
    phone_number = fake.phone_number()
    email_address = fake.email()

    return [last_name, first_name, middle_name, gender_label, birth_date, position, city, address, phone_number,
            email_address]


# Створення CSV-файлу з даними працівників
def generate_employee_csv(output_filename, total_count=2000, male_ratio=0.6):
    male_count = int(total_count * male_ratio)  # Кількість чоловіків
    female_count = total_count - male_count  # Кількість жінок
    employee_list = []

    # Генерація даних для чоловіків
    for _ in range(male_count):
        employee_list.append(create_employee('male'))

    # Генерація даних для жінок
    for _ in range(female_count):
        employee_list.append(create_employee('female'))

    # Змішування даних для випадкового порядку записів
    random.shuffle(employee_list)

    # Запис у CSV-файл
    with open(output_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            'Прізвище', 'Ім’я', 'По батькові', 'Стать', 'Дата народження',
            'Посада', 'Місто проживання', 'Адреса проживання', 'Телефон', 'Email'
        ])
        csv_writer.writerows(employee_list)


# Виклик функції для створення файлу з працівниками
generate_employee_csv('employees.csv')
