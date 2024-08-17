import pytest
from typing import Callable
from app.controllers import OrderController
from app.test.utils.functions import get_random_choice, shuffle_list
from app.test.fixtures.order import create_order__with_controller


def test_create(
    app,
    create_size__with_controller: Callable,
    create_ingredients__with_controller: Callable,
    create_beverages__with_controller: Callable,
    client_data: dict,
):
    created_size = create_size__with_controller
    created_ingredients = create_ingredients__with_controller
    created_beverages = create_beverages__with_controller
    order, created_order, error = create_order__with_controller(
        created_ingredients, created_beverages, created_size, client_data)
    size_id = order.pop("size_id", None)
    ingredient_ids = order.pop("ingredients", [])
    beverage_ids = order.pop("beverages", [])
    pytest.assume(error is None)
    for param, value in order.items():
        pytest.assume(param in created_order)
        pytest.assume(value == created_order[param])
        pytest.assume(created_order["_id"])
        pytest.assume(size_id == created_order["size"]["_id"])

        ingredients_in_detail = set(
            item["ingredient"]["_id"]
            for item in created_order["detail"]
            if item["ingredient"]
        )
        pytest.assume(not ingredients_in_detail.difference(ingredient_ids))

        beverages_in_detail = set(
            item["beverage"]["_id"]
            for item in created_order["detail"]
            if item["beverage"]
        )
        pytest.assume(not beverages_in_detail.difference(beverage_ids))


def test_create__missing_keys_returns_error(app):
    order = {"invalid_key": "invalid_value"}
    created_order, error = OrderController.create(order)
    pytest.assume(error)


def test_create_invalid_size_returns_error(app, client_data: dict):
    invalid_size = {"size_id": "invalid_size_id"}
    order = {**client_data, **invalid_size}
    created_order, error = OrderController.create(order)
    pytest.assume(error)


def test_calculate_order_price(
    app,
    create_size__with_controller: Callable,
    create_ingredients__with_controller: Callable,
    create_beverages__with_controller: Callable,
    client_data: dict,
):
    created_size = create_size__with_controller
    created_ingredients = create_ingredients__with_controller
    created_beverages = create_beverages__with_controller
    order, created_order, error = create_order__with_controller(
        created_ingredients, created_beverages, created_size, client_data)
    pytest.assume(
        created_order["total_price"]
        == round(
            created_size["price"]
            + sum(ingredient["price"] for ingredient in created_ingredients)
            + sum(beverage["price"] for beverage in created_beverages),
            2,
        )
    )


def test_get_by_id(
    app,
    create_size__with_controller: Callable,
    create_ingredients__with_controller: Callable,
    create_beverages__with_controller: Callable,
    client_data: dict,
):
    created_size = create_size__with_controller
    created_ingredients = create_ingredients__with_controller
    created_beverages = create_beverages__with_controller
    order, created_order, error = create_order__with_controller(
        created_ingredients, created_beverages, created_size, client_data)
    order_from_db, error = OrderController.get_by_id(created_order["_id"])
    size_id = order.pop("size_id", None)
    ingredient_ids = order.pop("ingredients", [])
    beverage_ids = order.pop("beverages", [])
    pytest.assume(error is None)
    for param, value in created_order.items():
        pytest.assume(order_from_db[param] == value)
        pytest.assume(size_id == created_order["size"]["_id"])

        ingredients_in_detail = set(
            item["ingredient"]["_id"] for item in created_order["detail"] if item["ingredient"]
        )
        pytest.assume(not ingredients_in_detail.difference(ingredient_ids))
        beverages_in_detail = set(
            item["beverage"]["_id"] for item in created_order["detail"] if item["beverage"]
        )
        pytest.assume(not beverages_in_detail.difference(beverage_ids))


def test_get_all(
    app,
    create_sizes__with_controller: Callable,
    create_ingredients__with_controller: Callable,
    create_beverages__with_controller: Callable,
    client_data: dict,
):
    created_sizes = create_sizes__with_controller
    created_ingredients = create_ingredients__with_controller
    created_beverages = create_beverages__with_controller
    created_orders = []
    for _ in range(5):
        order, created_order, _ = create_order__with_controller(
            shuffle_list(created_ingredients)[:3],
            shuffle_list(created_beverages)[:3],
            get_random_choice(created_sizes),
            client_data,
        )
        created_orders.append(created_order)

    orders_from_db, error = OrderController.get_all()
    searchable_orders = {db_order["_id"]: db_order for db_order in orders_from_db}
    pytest.assume(error is None)
    for created_order in created_orders:
        current_id = created_order["_id"]
        assert current_id in searchable_orders
        for param, value in created_order.items():
            pytest.assume(searchable_orders[current_id][param] == value)


def test_get_all_between__invalid_date_returns_error(app):
    orders_from_db, error = OrderController.get_all_between(
        "invalid_date", "invalid_date"
    )
    pytest.assume(error)
