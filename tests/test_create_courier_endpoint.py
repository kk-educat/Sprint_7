import pytest
import allure

from helps import Generator
from helps import ClientAPI


class TestCreateCourier:

    @allure.title('Проверка успешного создания курьера')
    @allure.description('Передаются все обязательные поля. Ожидается возврат правильного кода ответа и тела {"ok":true}')
    def test_courier_creating_possible(self, courier_data):
        response = ClientAPI().create_courier(courier_data)
        # ПРОВЕРКА РЕЗУЛЬТАТА
        assert 201 == response.status_code
        r = response.json()
        assert True == r['ok']

    @allure.title('Проверка невозможности создать двух одинаковых курьеров')
    def test_same_courier_creating_impossible(self, courier_data):
        response_1 = ClientAPI().create_courier(courier_data)
        response_2 = ClientAPI().create_courier(courier_data)
        # ПРОВЕРКА РЕЗУЛЬТАТА
        # 1ый курьер был успешно создан
        assert 201 == response_1.status_code
        # попытка создания 2ого курьера с теми же данными завершается ошибкой
        assert 409 == response_2.status_code

    @allure.title('Проверка возврата ошибки при отсутствии одного из обязательных полей')
    @pytest.mark.parametrize('missed_element', ["login", "password"])
    def test_create_courier_no_necessarily_param_error(self, courier_data, missed_element):
        # удаляем из тела запроса один из элементов и выполняем запрос
        del courier_data[missed_element]
        response = ClientAPI().create_courier(courier_data)
        # ПРОВЕРКА РЕЗУЛЬТАТА
        assert 400 == response.status_code
        r = response.json()
        assert "Недостаточно данных для создания учетной записи" == r["message"]

    @allure.title('Проверка возврата ошибки при создании пользователя с логином, который уже есть')
    def test_existing_login_error(self, courier_data):
        # выполняем запрос на создание 1ого курьера
        response_1 = ClientAPI().create_courier(courier_data)
        # меняем все, кроме логина и выполняем запрос на создание 2ого курьера
        courier_data['password'] = Generator().generate_random_string(10)
        courier_data['first_name'] = Generator().generate_random_string(10)
        response_2 = ClientAPI().create_courier(courier_data)
        # ПРОВЕРКА РЕЗУЛЬТАТА
        # 1ый курьер был успешно создан
        assert 201 == response_1.status_code
        # попытка создания 2ого курьера с тем же логином завершается ошибкой
        assert 409 == response_2.status_code
        r = response_2.json()
        assert "Этот логин уже используется" == r["message"]
