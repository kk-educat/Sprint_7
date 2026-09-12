import pytest
import copy

from helps import Generator
from helps import ClientAPI


@pytest.fixture
def courier_data():
    # генерируем логин, пароль и имя
    login = Generator().generate_random_string(10)
    password = Generator().generate_random_string(10)
    first_name = Generator().generate_random_string(10)
    # подготавливаем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    # возвращаем копию словаря payload
    # если тест-кейс изменит payload под себя, исходный словарь в фикстуре останется неизменным
    yield copy.deepcopy(payload)
    # пытаемся залогинить курьера
    del payload["firstName"]
    login_response = ClientAPI().login_courier(payload)
    if login_response.status_code == 200:
        # получаем id курьера
        login_response_data = login_response.json()
        id = login_response_data['id']
        # удаляем курьера по id
        ClientAPI().delete_courier(id)

@pytest.fixture
def order_data():
    payload = {
        "firstName": "Vasya",
        "lastName": "Sidorov",
        "address": "Vysotsky str., 4",
        "metroStation": 2,
        "phone": "+7 908 123 45 67",
        "rentTime": 8,
        "deliveryDate": "2026-10-07",
        "comment": "No comments"
    }
    return payload
