import requests
import allure
from helpers.URLS import Urls

class ApiMethods:
    @staticmethod
    @allure.step('Регистрация нового пользователя')
    def register_new_user(name, email, password):
        url = Urls.CREATING_USER
        data = {
            'email': email,
            'password': password,
            'name': name
        }
        response = requests.post(url, json=data)
        return response


    @staticmethod
    @allure.step('Удаление существующего юзера')
    def delete_user(access_token):
        url = Urls.USER_ACC
        headers = {"Authorization": f"Bearer {access_token}"}
        delete_response = requests.delete(url, headers=headers)
        return delete_response


    @staticmethod
    @allure.step('Авторизация пользователя')
    def login(login_data):
        url = Urls.LOGIN_USER
        login_response = requests.post(url, json = login_data)
        return login_response

    @staticmethod
    @allure.step('Изменение данных аккаунта')
    def user_data_change(updated_info, access_token):
        url = Urls.USER_ACC
        headers = {"Authorization": access_token}
        change_response = requests.patch(url, json = updated_info, headers=headers)
        return change_response

    @staticmethod
    @allure.step('Получение данных об ингредиентах')
    def ingredients_info():
        url = Urls.INGREDIENTS
        ingredient_response = requests.get(url)
        return [item["_id"] for item in ingredient_response.json().get("data", [])]

    @staticmethod
    @allure.step('Создание заказа')
    def create_order(payload, access_token):
        url = Urls.CREATE_ORDER
        headers = {"Authorization": access_token}
        response_order = requests.post(url, json=payload, headers=headers)
        return response_order

    @staticmethod
    @allure.step('Получение заказов пользователя')
    def get_user_orders(access_token):
        url = Urls.USER_ORDERS
        headers = {"Authorization": access_token}
        response_get_orders = requests.get(url, headers=headers)
        return response_get_orders