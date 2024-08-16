from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import BeverageController
from .base import execute, execute__with_not_found


beverage = Blueprint('beverage', __name__)
controller = BeverageController


@beverage.route('/', methods=POST)
def create_beverage():
    return execute(controller.create, request.json)


@beverage.route('/', methods=PUT)
def update_beverage():
    return execute(controller.update, request.json)


@beverage.route('/id/<_id>', methods=GET)
def get_beverage_by_id(_id: int):
    return execute__with_not_found(controller.get_by_id, _id)


@beverage.route('/', methods=GET)
def get_beverages():
    return execute__with_not_found(controller.get_all)
