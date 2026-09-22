import allure

from helps import ClientAPI


class TestGetOrdersList:
    
    @allure.title('Проверка получения списка заказов')
    @allure.description('Проверяем, что в теле ответа возвращается список заказов (поле orders)')
    def test_get_orders_list_success(self):
        # отправляем тестируемый запрос
        response = ClientAPI().get_orders_list()
        # ПРОВЕРКА РЕЗУЛЬТАТА
        assert 200 == response.status_code 
        response_data = response.json()
        assert 'orders' in response_data
