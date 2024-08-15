import pytest

from datetime import datetime
from app.controllers.order import OrderController
from app.test.controllers.test_order import __create_sizes_and_ingredients, __order


@pytest.fixture
def report_uri():
    return "/report?startDate=2024-01-01&endDate=2024-08-15"

@pytest.fixture
def init_report_data(ingredients, sizes, client_data):
    new_sizes, new_ingredients = __create_sizes_and_ingredients(
        ingredients, sizes
    )
    order = __order(new_ingredients, new_sizes[0], client_data, datetime(2024, 3, 3))
    OrderController.create(order)