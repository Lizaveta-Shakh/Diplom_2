from api_methods import ApiMethods
from helpers.data_generator import *
from helpers.data import Messages


class TestGetUserOrders:
    @allure.title('Проверка получения заказов авторизованного пользователя')
    def test_get_orders_with_auth_returns_200(self, user):
        access_token = user["tokens"]["accessToken"]
        response = ApiMethods.get_user_orders(access_token)

        assert response.status_code == 200
        json_data = response.json()
        assert json_data["success"] is True
        assert "orders" in json_data
        assert isinstance(json_data["orders"], list)

    @allure.title('Проверка ошибки 401 при получении заказов без авторизации')
    def test_get_orders_without_auth_returns_401(self):
        response = ApiMethods.get_user_orders(access_token="")

        assert response.status_code == 401
        json_data = response.json()
        assert json_data["success"] is False
        assert json_data["message"] == Messages.GET_INFO_WITHOUT_AUTH_MESSAGE