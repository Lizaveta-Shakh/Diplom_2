import pytest

from api_methods import ApiMethods
from helpers.data_generator import *
from helpers.data import Messages


class TestUserDataChange:

    @allure.title('Проверка изменения поля {field} авторизованного пользователя')
    @pytest.mark.parametrize("field, generator", [
        ("email", get_email_to_update),
        ("name", get_name_to_update)
    ])
    def test_update_user_field_with_auth_returns_200(self, user, field, generator):
        access_token = user["tokens"]["accessToken"]
        new_value = generator()
        payload = {field: new_value}

        response = ApiMethods.user_data_change(payload, access_token)

        assert response.status_code == 200
        json_data = response.json()
        assert json_data['success'] is True
        assert json_data['user'][field] == new_value


    @allure.title('Проверка изменения данных авторизованного пользователя - пароль')
    def test_update_user_password_with_auth_returns_200(self, user):
        access_token = user["tokens"]["accessToken"]
        new_password = get_password_to_update()
        payload = {"password": new_password}
        response = ApiMethods.user_data_change(payload, access_token)

        assert response.status_code == 200
        json_response = response.json()
        assert json_response['success'] is True
   # пароль не возвращается в ответе

    @allure.title('Проверка невозможности изменения данных без авторизации - имя, почта, пароль')
    @pytest.mark.parametrize("field, generator", [
        ("email", get_email_to_update),
        ("name", get_name_to_update),
        ("password", get_password_to_update)
    ])
    def test_update_user_data_unauthorized_returns_401(self, field, generator):
        new_value = generator()
        payload = {field: new_value}
        response = ApiMethods.user_data_change(payload, access_token="")

        assert response.status_code == 401
        json_data = response.json()
        assert json_data["success"] is False
        assert json_data["message"] == Messages.CHANGE_DATA_WITHOUT_LOGIN_MESSAGE