import pytest
from helpers.data_generator import *
from api_methods import ApiMethods


@pytest.fixture (scope="function")
def user():
    data = user_data()

    # регистрация нового пользователя
    response = ApiMethods.register_new_user(data['name'], data['email'], data['password'])
    assert response.status_code == 200
    tokens = response.json()

    # те же данные для логина, что и при регистрации
    login_response = ApiMethods.login({
        'email': data['email'],
        'password': data['password']
    })
    assert login_response.status_code == 200

    yield {
        "tokens": tokens,
        "user_data": data  # сохраняем данные тут
    }

    ApiMethods.delete_user(tokens['accessToken'])