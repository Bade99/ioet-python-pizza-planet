from app.common.http_methods import GET, POST
from flask import Blueprint, request

from ..controllers import OrderController
from .base import execute, execute__with_not_found


order = Blueprint('order', __name__)
controller = OrderController


@order.route('/', methods=POST)
def create_order():
    return execute(controller.create, request.json)


@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
    return execute__with_not_found(controller.get_by_id, _id)


@order.route('/', methods=GET)
def get_orders():
    return execute__with_not_found(controller.get_all)
