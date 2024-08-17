from app.common.http_methods import GET, POST
from flask import Blueprint, request

from ..controllers import OrderController
from .decorators import response, response__with_not_found


order = Blueprint('order', __name__)
controller = OrderController


@order.route('/', methods=POST)
@response
def create_order():
    return controller.create(request.json)


@order.route('/id/<_id>', methods=GET)
@response__with_not_found
def get_order_by_id(_id: int):
    return controller.get_by_id(_id)


@order.route('/', methods=GET)
@response__with_not_found
def get_orders():
    return controller.get_all()
