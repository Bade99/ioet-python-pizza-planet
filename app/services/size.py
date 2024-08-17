from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import SizeController
from .decorators import response, response__with_not_found


size = Blueprint('size', __name__)
controller = SizeController


@size.route('/', methods=POST)
@response
def create_size():
    return controller.create(request.json)


@size.route('/', methods=PUT)
@response
def update_size():
    return controller.update(request.json)


@size.route('/id/<_id>', methods=GET)
@response__with_not_found
def get_size_by_id(_id: int):
    return controller.get_by_id(_id)


@size.route('/', methods=GET)
@response__with_not_found
def get_sizes():
    return controller.get_all()
