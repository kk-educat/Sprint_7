import pytest
import allure

from helps import ClientAPI


class TestLoginCourier:

    @allure.title('Проверка успешной авторизации курьера')
    @allure.description('Передаются все обязательные поля. Ожидается возврат id')
    def test_courier_login_success(self, courier_data):
        # создаем курьера
        response = ClientAPI().create_courier(courier_data)
        assert 201 == response.status_code
        # подготовка необходимых для логина данных
        payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        # отправляем тестируемый запрос
        response = ClientAPI().login_courier(payload)
        # ПРОВЕРКА РЕЗУЛЬТАТА
        assert 200 == response.status_code
        response_data = response.json()
        assert 'id' in response_data

    @allure.title('Проверка возврата ошибки на запрос без одного из полей')
    @pytest.mark.parametrize('missed_element', ['login', 'password'])
    def test_no_necessarily_param_error(self, courier_data, missed_element):
        # создаем курьера
        response = ClientAPI().create_courier(courier_data)
        assert 201 == response.status_code
        # подготовка необходимых для логина данных
        payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        # удаляем одно из обязательных полей из данных (из тела запроса)
        del payload[missed_element]
        # отправляем тестируемый запрос
        response = ClientAPI().login_courier(payload)
        # ПРОВЕРКА РЕЗУЛЬТАТА
        assert 400 == response.status_code
        response_data = response.json()
        assert 'Недостаточно данных для входа' == response_data['message']

    @allure.title('Проверка возврата ошибки при указании неправильного логина или пароля')
    @allure.description('Указание неправильного логина фактически является также кейсом проверки авторизации несуществующего пользователя')
    @pytest.mark.parametrize('wrong_element', ['login', 'password'])
    def test_wrong_auth_data_error(self, courier_data, wrong_element):
        # создаем курьера
        response = ClientAPI().create_courier(courier_data)
        assert 201 == response.status_code
        # подготовка необходимых для логина данных
        payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        # меняем одно из полей логин/пароль на некорректное
        payload[wrong_element] = 'wrong_auth_data'
        # отправляем тестируемый запрос
        response = ClientAPI().login_courier(payload)
        # ПРОВЕРКА РЕЗУЛЬТАТА
        assert 404 == response.status_code
        response_data = response.json()
        assert 'Учетная запись не найдена' == response_data['message']
