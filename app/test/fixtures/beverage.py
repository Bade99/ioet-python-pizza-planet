import pytest
from app.controllers import BeverageController
from ..utils.functions import get_random_price, get_random_string


def beverage_mock() -> dict:
    return {
        'name': get_random_string(),
        'price': get_random_price(10, 20)
    }


@pytest.fixture
def beverage_uri():
    return '/beverage/'


@pytest.fixture
def beverage():
    return beverage_mock()


@pytest.fixture
def beverages():
    return [beverage_mock() for _ in range(5)]


@pytest.fixture
def create_beverage(client, beverage_uri) -> dict:
    response = client.post(beverage_uri, json=beverage_mock())
    return response


@pytest.fixture
def create_beverages(client, beverage_uri) -> list:
    beverages = []
    for _ in range(10):
        new_beverage = client.post(beverage_uri, json=beverage_mock())
        beverages.append(new_beverage.json)
    return beverages


@pytest.fixture
def create_beverage__with_controller(beverage: dict) -> dict:
    created_beverage, _ = BeverageController.create(beverage)
    return created_beverage


@pytest.fixture
def create_beverages__with_controller(beverages: list) -> list:
    created_beverages = []
    for beverage in beverages:
        created_beverage, _ = BeverageController.create(beverage)
        created_beverages.append(created_beverage)
    return created_beverages
