from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import SizeController
from .base import execute, execute__with_not_found


size = Blueprint('size', __name__)
controller = SizeController


@size.route('/', methods=POST)
def create_size():
    return execute(controller.create, request.json)


@size.route('/', methods=PUT)
def update_size():
    return execute(controller.update, request.json)


@size.route('/id/<_id>', methods=GET)
def get_size_by_id(_id: int):
    return execute__with_not_found(controller.get_by_id, _id)


@size.route('/', methods=GET)
def get_sizes():
    return execute__with_not_found(controller.get_all)
