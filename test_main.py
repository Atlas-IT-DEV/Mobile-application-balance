from ctypes.wintypes import POINT
from http.client import responses
from datetime import datetime
import pytest
import random
import string
from copy import deepcopy
from fastapi.testclient import TestClient
from main import app
from setup.debug_info import machine
from src.utils.custom_logging import setup_logging

log = setup_logging()
client = TestClient(app)


"""

Ошибка Not Found вероятно говорит о неправильно созданном роуте, или не правильно переданным параметрам в тесты

"""


# Вспомогательная функция для генерации случайных данных
def generate_random_data(data_type, length=8):
    if data_type == "string":
        return ''.join(random.choices(string.ascii_letters, k=length))
    elif data_type == "number":
        return random.randint(1, 1000000)
    elif data_type == "datetime":
        return datetime.now()
    return None


# Вспомогательная функция для выполнения запросов
def api_request(method, url, json_data=None, headers=None):
    response = client.request(method, url, json=json_data, headers=headers)
    return response


# Вспомогательная функция для проверки статуса и получения данных
def assert_response(response, expected_status, keys=None):
    log.info("-------------------------------------")
    assert response.status_code == expected_status, \
        f"Unexpected status code: {response.status_code}, Response: {response.text}"
    if keys:
        response_data = response.json()
        if isinstance(response_data, list):
            for item in response_data:
                for key in keys:
                    assert key in item
        else:
            for key in keys:
                assert key in response_data
        return response_data
    return None


# Генерация тестовых данных для различных сущностей
def generate_test_data(entity_type):
    data_map = {
        "user": {
            "first_name": generate_random_data("string"),
            "last_name": generate_random_data("string"),
            "phone": generate_random_data("string"),
            "INN": generate_random_data("string"),
            "password": generate_random_data("string"),
            "role": "ADMIN"
        },
        "image": {
            "url": generate_random_data("string")
        },
        "fee_category": {
            "name": generate_random_data("string")
        },
        "company": {
            "name": generate_random_data("string"),
            "description": generate_random_data("string"),
            "contact": generate_random_data("string")
        },
        "sub_category": {
            "type": generate_random_data("string")
        },
        "fee": {
            "name": generate_random_data("string"),
            "description": generate_random_data("string"),
            "final_cost": generate_random_data("number"),
            "gathered_cost": generate_random_data("number"),
            "fee_category_id": None,
            "image_id": "1,2,3,4"
        },
        "subscription": {
            "user_id": None,
            "fee_id": None,
            "type_sub_id": None
        },
        "history_payment": {
            "user_id": None,
            "fee_id": None,
            "pay": generate_random_data("number"),
            "created_at": f"{generate_random_data('datetime')}"
        }
    }
    return data_map.get(entity_type)


def setup_entity(entity_type, endpoint, token):
    if entity_type == "fee":
        fee_category_id = setup_entity("fee_category", "fee_categories",
                                       token)
        fee_data = generate_test_data("fee")
        entity_data = {**fee_data,
                       "fee_category_id": fee_category_id}
    elif entity_type == "subscription":
        user_id = setup_entity("user", "users", token)
        fee_id = setup_entity("fee", "fees", token)
        type_sub_id = setup_entity("sub_category", "sub_categories", token)
        subscription_data = generate_test_data("subscription")
        entity_data = {**subscription_data,
                       "user_id": user_id,
                       "fee_id": fee_id,
                       "type_sub_id": type_sub_id}
    elif entity_type == "history_payment":
        user_id = setup_entity("user", "users", token)
        fee_id = setup_entity("fee", "fees", token)
        history_payment_data = generate_test_data("history_payment")
        entity_data = {**history_payment_data,
                       "user_id": user_id,
                       "fee_id": fee_id}
    else:
        entity_data = generate_test_data(entity_type)
    log.info(f"Creating {entity_type} with data: {entity_data}")
    response = api_request("POST", f"/{endpoint}/", json_data=entity_data,
                           headers={"Authorization": f"Bearer {token}"})
    log.info(f"POST {endpoint}/ response: {response.json()}")
    response_data = assert_response(response, 200, keys=["id"])
    return response_data["id"]


# Функция для удаления сущности
def teardown_entity(endpoint, entity_id, token):
    response = api_request("DELETE", f"/{endpoint}/{entity_id}",
                           headers={"Authorization": f"Bearer {token}"})
    assert_response(response, 200)


# Токен доступа администратора
access_token = None
admin_data = []


def create_admin():
    global access_token
    admin_data.append(generate_test_data("user"))
    response = api_request("POST", "/signup/", json_data=admin_data[0])
    access_token = response.json()["access_token"]


# Инициализация администратора
create_admin()


@pytest.mark.parametrize("entity_type, endpoint, expected_keys", [
    ("user", "users", ["first_name",
                       "last_name",
                       "phone",
                       "INN",
                       "password"]),
    ("image", "images", ["url"]),
    ("fee_category", "fee_categories", ["name"]),
    ("company", "companies", ["name"]),
    ("sub_category", "sub_categories", ["type"]),
    ("fee", "fees", ["name"]),
    ("subscription", "subscriptions", ["user_id",
                                       "fee_id",
                                       "type_sub_id"]),
    ("history_payment", "history_payments", ["user_id",
                                             "fee_id",
                                             "pay",
                                             "created_at"]),
])
def test_create_and_get_entity(entity_type, endpoint, expected_keys):
    log.info("-------------------------------------")
    log.info(f"entity_type: {entity_type}, endpoint: {endpoint}, expected_keys: {expected_keys}")
    entity_id = setup_entity(entity_type, endpoint, access_token)
    response = api_request("GET", f"/{endpoint}/")
    assert_response(response, 200, keys=["id"] + expected_keys)
    response = api_request("GET", f"/{endpoint}/{entity_type}_id/{entity_id}")
    assert_response(response, 200, keys=["id"] + expected_keys)
    teardown_entity(endpoint, entity_id, access_token)


@pytest.mark.parametrize("entity_type, endpoint, update_data", [
    ("user", "users", {"first_name": generate_random_data("string"),
                       "last_name": generate_random_data("string"),
                       "phone": generate_random_data("string"),
                       "INN": generate_random_data("string"),
                       "password": generate_random_data("string")}),
    ("image", "images", {"url": generate_random_data("string")}),
    ("fee_category", "fee_categories", {"name": generate_random_data("string")}),
    ("company", "companies", {"name": generate_random_data("string")}),
    ("sub_category", "sub_categories", {"type": generate_random_data("string")}),
    ("fee", "fees", {"name": generate_random_data("string"),
                     "description": generate_random_data("string"),
                     "final_cost": generate_random_data("number"),
                     "gathered_cost": generate_random_data("number")}),
    ("subscription", "subscriptions", {"id": 23}),
    ("history_payment", "history_payments", {"pay": generate_random_data("number")}),
])
def test_update_entity(entity_type, endpoint, update_data):
    log.info("-------------------------------------")
    log.info(f"entity_type: {entity_type}, endpoint: {endpoint}, update_data: {update_data}")
    entity_id = setup_entity(entity_type, endpoint, access_token)
    response = api_request("GET", f"/{endpoint}/{entity_type}_id/{entity_id}")
    test_data = response.json()
    response = api_request("PUT", f"/{endpoint}/{entity_id}", json_data=test_data,
                           headers={"Authorization": f"Bearer {access_token}"})
    assert_response(response, 200)
    updated_data = deepcopy(test_data)
    updated_data.update(update_data)
    response = api_request("PUT", f"/{endpoint}/{entity_id}", json_data=updated_data,
                           headers={"Authorization": f"Bearer {access_token}"})
    assert_response(response, 200)
    teardown_entity(endpoint, entity_id, access_token)


# Удаление администратора
def del_admin():
    phone = admin_data[0].get("phone")
    print(phone)
    response = api_request("GET", f"/users/phone/{phone}",
                           headers={"Authorization": f"Bearer {access_token}"})
    admin = response.json()
    teardown_entity("users", admin["id"], access_token)


del_admin()
