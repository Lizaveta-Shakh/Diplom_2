import pytest

from api_methods import ApiMethods
from helpers.data_generator import *
from helpers.data import Messages



class TestLogin:
    @allure.title('Проверка, успешного логина с существующими данными аккаунта')
    def test_login_registered_user_data_returns_200(self, user):
        data = user['user_data']
        payload = {
            "email": data['email'],
            "password": data['password']
        }
        response = ApiMethods.login(payload)


        assert response.status_code == 200
        json_response = response.json()
        assert json_response['success'] is True


    @allure.title('Проверка, что логин с незаполненным обязательным полем возвращает ошибку')
    @pytest.mark.parametrize('fields', ['email', 'password'])
    def test_login_registered_user_data_returns_error(self, user, fields):
        data = user['user_data']
        login_data = {
            "email": data['email'],
            "password": data['password']
        }
        login_data.pop(fields)
        response = ApiMethods.login(login_data)


        assert response.status_code == 401
        json_response = response.json()
        assert json_response['message'] == Messages.INCORRECT_LOGIN_DATA_MESSAGE