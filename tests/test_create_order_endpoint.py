import pytest
import allure

from helps import ClientAPI


class TestCreateOrder:

    @allure.title('Проверка создания заказа с указанием черного и/или серого предпочитаемого цвета')
    @allure.description('Проверяется, что в теле ответа содержится поле track')
    @pytest.mark.parametrize('color', [["BLACK"], ["GREY"], ["BLACK", "GREY"]])
    def test_create_order_with_color_success(self, color, order_data):
        # добавляем в данные заказа опциональное поле с предпочитаемым цветом
        order_data["color"] = color
        # отправляем тестируемый запрос
        response = ClientAPI().create_order(order_data)
        # ПРОВЕРКА РЕЗУЛЬТАТА
        # проверка успешного кода создания заказа
        assert 201 == response.status_code
        # преобразуем тело ответа из формата json в python-словарь и ищем в нем поле track 
        response_data = response.json()
        assert 'track' in response_data
        # отменяем тестовый заказ по окончании проверок
        ClientAPI().cancel_order(response_data['track'])

    @allure.title('Проверка создания заказа без указания предпочитаемого цвета')
    def test_create_order_without_color_success(self, order_data):
        # отправляем тестируемый запрос
        response = ClientAPI().create_order(order_data)
        # ПРОВЕРКА РЕЗУЛЬТАТА
        assert 201 == response.status_code
        response_data = response.json()
        assert 'track' in response_data
        # отменяем тестовый заказ по окончании проверок
        ClientAPI().cancel_order(response_data['track'])
