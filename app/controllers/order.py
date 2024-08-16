from sqlalchemy.exc import SQLAlchemyError

from ..common.utils import check_required_keys
from datetime import datetime
from ..repositories.managers import (
    IngredientManager,
    BeverageManager,
    OrderManager,
    SizeManager,
)
from .base import BaseController


class OrderController(BaseController):
    manager = OrderManager
    __required_info = (
        "client_name",
        "client_dni",
        "client_address",
        "client_phone",
        "size_id",
    )

    @staticmethod
    def calculate_order_price(size_price: float, ingredients: list, beverages: list):
        price = (
            size_price
            + sum(ingredient.price for ingredient in ingredients)
            + sum(beverage.price for beverage in beverages)
        )
        return round(price, 2)

    @classmethod
    def create(cls, order: dict):
        current_order = order.copy()
        if not check_required_keys(cls.__required_info, current_order):
            return None, "Invalid order payload"

        size_id = current_order.get("size_id")
        size = SizeManager.get_by_id(size_id)

        if not size:
            return None, "Invalid size for Order"

        ingredient_ids = current_order.pop("ingredients", [])
        beverage_ids = current_order.pop("beverages", [])
        try:
            ingredients = IngredientManager.get_by_id_list(ingredient_ids)
            beverages = BeverageManager.get_by_id_list(beverage_ids)
            price = cls.calculate_order_price(size.get("price"), ingredients, beverages)
            order_with_price = {**current_order, "total_price": price}
            return cls.manager.create(order_with_price, ingredients, beverages), None
        except (SQLAlchemyError, ValueError, RuntimeError) as ex:
            return None, str(ex)

    @classmethod
    def get_all_between(cls, start_date: str, end_date: str):
        try:
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
            return cls.manager.get_all_between(start, end), None
        except (SQLAlchemyError, ValueError, RuntimeError) as ex:
            return None, str(ex)
