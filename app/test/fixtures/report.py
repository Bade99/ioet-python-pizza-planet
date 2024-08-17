import pytest
from typing import Callable
from datetime import datetime
from app.test.fixtures.order import create_order__with_controller


@pytest.fixture
def report_uri():
    return "/report?startDate=2024-01-01&endDate=2024-08-15"


@pytest.fixture
def init_report_data(
    create_size__with_controller: Callable,
    create_ingredients__with_controller: Callable,
    create_beverages__with_controller: Callable,
    client_data: dict,
):
    created_size = create_size__with_controller
    created_ingredients = create_ingredients__with_controller
    created_beverages = create_beverages__with_controller
    create_order__with_controller(created_ingredients, created_beverages,
                                  created_size, client_data, datetime(2024, 3, 3))
