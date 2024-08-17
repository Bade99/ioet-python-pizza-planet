import pytest
from typing import Optional, List
from app.controllers import OrderController
from datetime import datetime
import random
from ..utils.functions import (shuffle_list, get_random_sequence,
                               get_random_string)


def client_data_mock() -> dict:
    return {
        'client_address': get_random_string(),
        'client_dni': str(random.randint(1000000, 9999999999)),
        'client_name': get_random_string(),
        'client_phone': get_random_sequence()
    }


@pytest.fixture
def order_uri():
    return '/order/'


@pytest.fixture
def client_data():
    return client_data_mock()


@pytest.fixture
def prepare_order(create_ingredients: list, create_size: dict, client_data: dict) -> dict:
    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    size_id = create_size.json.get('_id')
    return {
        **client_data,
        'ingredients': ingredients,
        'size_id': size_id
    }


@pytest.fixture
def create_order(client, order_uri: str, prepare_order: dict):
    return client.post(order_uri, json=prepare_order)


@pytest.fixture
def create_orders(
    client, order_uri: str, create_ingredients: list, create_beverages: list,
        create_sizes: list) -> list:
    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    beverages = [beverage.get('_id') for beverage in create_beverages]
    sizes = [size.get('_id') for size in create_sizes]
    orders = []
    for _ in range(10):
        new_order = client.post(order_uri, json={
            **client_data_mock(),
            'ingredients': shuffle_list(ingredients)[:5],
            'beverages': shuffle_list(beverages)[:5],
            'size_id': shuffle_list(sizes)[0]
        })
        orders.append(new_order.json)
    return orders


def create_order__with_controller(
    ingredients: List[dict],
    beverages: List[dict],
    size: dict,
    client_data: dict,
    date: Optional[datetime] = None,
):
    ingredients = [ingredient.get("_id") for ingredient in ingredients]
    beverages = [beverage.get("_id") for beverage in beverages]
    size_id = size.get("_id")
    order = {
        **client_data,
        "ingredients": ingredients,
        "beverages": beverages,
        "size_id": size_id,
    }
    if date:
        order["date"] = date
    created_order, error = OrderController.create(order)
    return order, created_order, error
