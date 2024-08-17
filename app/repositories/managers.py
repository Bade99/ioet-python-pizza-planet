from typing import Any, List, Optional, Sequence, Tuple

from sqlalchemy.sql import text, column

from datetime import datetime

from .models import Ingredient, Beverage, Order, OrderDetail, Size, db
from .serializers import (
    IngredientSerializer,
    BeverageSerializer,
    OrderSerializer,
    SizeSerializer,
    ma,
)


class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class OrderDetailElementManager(BaseManager):
    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return (
            cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
        )


class IngredientManager(OrderDetailElementManager):
    model = Ingredient
    serializer = IngredientSerializer


class BeverageManager(OrderDetailElementManager):
    model = Beverage
    serializer = BeverageSerializer


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all(
            (
                OrderDetail(
                    order_id=new_order._id,
                    ingredient_id=ingredient._id,
                    price=ingredient.price,
                )
                for ingredient in ingredients
            )
        )
        cls.session.add_all(
            (
                OrderDetail(
                    order_id=new_order._id,
                    beverage_id=beverage._id,
                    price=beverage.price,
                )
                for beverage in beverages
            )
        )
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f"Method not suported for {cls.__name__}")

    @classmethod
    def get_all_between(
        cls, start_date: datetime, end_date: datetime
    ) -> Tuple[Any, Optional[str]]:
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.filter(Order.date.between(start_date, end_date)).all()
        result = serializer.dump(_objects)
        return result


class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column("1")).from_statement(text("SELECT 1")).all()
