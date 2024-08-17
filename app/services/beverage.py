from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import BeverageController
from .decorators import response, response__with_not_found


beverage = Blueprint('beverage', __name__)
controller = BeverageController


@beverage.route('/', methods=POST)
@response
def create_beverage():
    return controller.create(request.json)


@beverage.route('/', methods=PUT)
@response
def update_beverage():
    return controller.update(request.json)


@beverage.route('/id/<_id>', methods=GET)
@response__with_not_found
def get_beverage_by_id(_id: int):
    return controller.get_by_id(_id)


@beverage.route('/', methods=GET)
@response__with_not_found
def get_beverages():
    return controller.get_all()
