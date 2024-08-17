import pytest
from app.controllers import SizeController
from ..utils.functions import get_random_price, get_random_string
from app.repositories.models import Size

def size_mock() -> dict:
    return {
        'name': get_random_string(),
        'price': get_random_price(.01, Size.max_price())
    }


@pytest.fixture
def size_uri():
    return '/size/'


@pytest.fixture
def size():
    return size_mock()


@pytest.fixture
def sizes():
    return [size_mock() for _ in range(5)]


@pytest.fixture
def create_size(client, size_uri: str) -> dict:
    response = client.post(size_uri, json=size_mock())
    return response


@pytest.fixture
def create_sizes(client, size_uri: str) -> list:
    sizes = []
    for _ in range(10):
        new_size = client.post(size_uri, json=size_mock())
        sizes.append(new_size.json)
    return sizes


@pytest.fixture
def create_size__with_controller(size: dict) -> dict:
    created_size, _ = SizeController.create(size)
    return created_size


@pytest.fixture
def create_sizes__with_controller(sizes: list) -> list:
    created_sizes = []
    for size in sizes:
        created_size, _ = SizeController.create(size)
        created_sizes.append(created_size)
    return created_sizes
