import pytest

from api_methods import ApiMethods
from helpers.data_generator import *
from helpers.data import Messages



class TestReg:
    @allure.title('Проверка, что курьера можно создать')
    def test_register_user_returns_success(self):
        data = user_data()
        response = ApiMethods.register_new_user(data['name'], data['email'], data['password'])

        assert response.status_code == 200
        json_response = response.json()

        assert json_response['success'] is True
        assert 'accessToken' in json_response and 'refreshToken' in json_response
        assert json_response['user']['email'] == data['email']
        assert json_response['user']['name'] == data['name']


    @allure.title('Проверка появления ошибки 403 User already exists при попытке зарегестрировать существующего пользователя')
    def test_register_existing_user_returns_error(self,user):
        existing_user_data = user['user_data']
        second_registration = user_data_second_register(
            existing_user_data['email'], existing_user_data['password'], existing_user_data['name']
        )
        response = ApiMethods.register_new_user(
            second_registration['name'],
            second_registration['email'],
            second_registration['password']
        )

        assert response.status_code == 403
        json_response = response.json()
        assert json_response['message'] == Messages.ACCOUNT_EXIST_MESSAGE


    @allure.title('Проверка появления ошибки 403 Email, password and name are required fields при оставлении при регистрации одного из полей пустым')
    @pytest.mark.parametrize('empty_field', ['name', 'email', 'password'])
    def test_register_empty_field_returns_error(self, empty_field):
        data = user_data()
        data[empty_field] = ""
        response = ApiMethods.register_new_user(data['name'], data['email'], data['password'])

        assert response.status_code == 403
        json_response = response.json()
        assert json_response['message'] == Messages.REG_EMPTY_FIELD_MESSAGE




