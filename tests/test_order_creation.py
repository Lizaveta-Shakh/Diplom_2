from api_methods import ApiMethods
from helpers.data_generator import *
from helpers.data import Messages


class TestOrderCreation:
    @allure.title('Проверка возмоножности создания заказа авторизованным пользователем (и ингредиентов)')
    def test_create_order_with_auth_returns_200(self, user):
        access_token = user["tokens"]["accessToken"]
        ingredients  = ApiMethods.ingredients_info()
        payload = {
            "ingredients": ingredients[:2]  #  2 любых ингредиента
        }
        response = ApiMethods.create_order(payload, access_token)

        assert response.status_code == 200
        json_data = response.json()
        assert json_data["success"] is True
        assert "order" in json_data
        assert "number" in json_data["order"]


    @allure.title('Проверка ошибки 400 при создании заказа авторизованным пользователем (без ингредиентов)')
    def test_create_order_without_ingredients_returns_400(self, user):
        access_token = user["tokens"]["accessToken"]
        payload = {
            "ingredients": []
        }
        response = ApiMethods.create_order(payload, access_token)

        assert response.status_code == 400
        json_data = response.json()
        assert json_data["success"] is False
        assert json_data["message"] == Messages.NO_ING_MESSAGE


    @allure.title('Проверка ошибки 500 при создании заказа с невалидным ID ингредиента')
    def test_create_order_with_invalid_ingredient_returns_500(self, user):
        access_token = user["tokens"]["accessToken"]
        payload = {
            "ingredients": ["invalid_ingredient_id_123"]
        }
        response = ApiMethods.create_order(payload, access_token)

        assert response.status_code == 500

    @allure.title('Проверка создания заказа без авторизации (валидные ингредиенты)')
    def test_create_order_without_auth_with_ingredients_returns_200(self):
        ingredients = ApiMethods.ingredients_info()
        payload = {
            "ingredients": ingredients[:2]
        }

        response = ApiMethods.create_order(payload, access_token="")

        assert response.status_code == 200
        json_data = response.json()
        assert json_data["success"] is True
        assert "order" in json_data

    @allure.title('Проверка ошибки 400 при создании заказа без ингредиентов и без авторизации')
    def test_create_order_without_auth_and_ingredients_returns_400(self):
        payload = {
            "ingredients": []
        }

        response = ApiMethods.create_order(payload, access_token="")

        assert response.status_code == 400
        json_data = response.json()
        assert json_data["success"] is False
        assert json_data["message"] == "Ingredient ids must be provided"

    @allure.title('Проверка ошибки 500 при создании заказа с неcуществующим id ингредиента без авторизации')
    def test_create_order_without_auth_with_invalid_ingredient_returns_500(self):
        payload = {
            "ingredients": ["invalid_ingredient_id_123"]
        }

        response = ApiMethods.create_order(payload, access_token="")

        assert response.status_code == 500