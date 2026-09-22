import random
import string
import requests
import allure

import data as d


class Generator:

    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

# класс, в который вынесены методы запросов к API тестируемого сервиса
class ClientAPI:

    @allure.step('Выполняем запрос на создание курьера')
    def create_courier(self, data):
        return requests.post(d.CREATE_COURIER_PATH, json = data)

    @allure.step('Выполняем запрос на логин курьера')
    def login_courier(self, data):
        return requests.post(d.LOGIN_COURIER_PATH, json = data)

    @allure.step('Выполняем запрос на удаление курьера')
    def delete_courier(self, courier_id):
        return requests.delete(d.DELETE_COURIER_PATH.format(courier_id))

    @allure.step('Выполняем запрос на создание заказа')
    def create_order(self, data):
        return requests.post(d.ORDERS_PATH, json = data)

    @allure.step('Выполняем запрос на отмену заказа')
    def cancel_order(self, order_track):
        return requests.put(d.CANCEL_ORDER_PATH, params = {'track': order_track})

    @allure.step('Выполняем запрос на получение списка заказов')
    def get_orders_list(self):
        return requests.get(d.ORDERS_PATH)
