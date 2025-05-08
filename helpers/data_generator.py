import random
import allure
import uuid
import time

from faker import Faker

fake = Faker('en_US')

#генерируем тестовые данные

@allure.step('Генерация имя и фамилии')
def generate_random_name():
    random_name = fake.name()
    return random_name

@allure.step('Генерация пароля из цифр, макс длина 6')
def generate_random_password(length=6):
    min_value = 10**(length - 1)
    max_value = 10**length - 1
    random_number = random.randint(min_value, max_value)
    return str(random_number)

@allure.step('Генерация имейл')
def generate_random_email():
    unique_part = uuid.uuid4().hex[:8]
    random_email = f"testuser_{unique_part}@ya.com"
    return random_email

@allure.step('Генерация тестовых данных для регистрации юзера')
def create_user_data():
    name = generate_random_name()
    email = generate_random_email()
    password = generate_random_password()

    return name, email, password

@allure.step('Получаю тело запроса для регистрации юзера')
def user_data():
    name, email, password = create_user_data()
    return {
        "name": name,
        "email": email,
        "password": password
    }

@allure.step('Получаю тело запроса для логина юзера')
def user_data_login():
    data = user_data()
    return {
        "email": data["email"],
        "password": data["password"]
    }


@allure.step('Получаю тело запроса для попытки повторной регистрации')
def user_data_second_register(email, password, name):
    return {
        "email": email,
        "password": password,
        "name": name
    }

@allure.step('Генерация нового имейл для обновлени информации пользователя')
def get_email_to_update():
    unique_part = f"{uuid.uuid4().hex[:4]}{int(time.time() * 1000)}"
    new_email = f"testuser_{unique_part}@gmail.com"
    return new_email


@allure.step('Генерация нового пароля для обновления информации пользователя')
def get_password_to_update(length=6):
    min_value = 10**(length - 1)
    max_value = 10**length - 1
    new_password = random.randint(min_value, max_value)
    return str(new_password)


@allure.step('Генерация нового имени для обновлени информации пользователя')
def get_name_to_update():
    new_name = fake.name()
    return new_name
