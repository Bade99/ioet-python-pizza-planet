from app.common.http_methods import GET
from flask import Blueprint, request

from ..controllers import ReportController
from .decorators import response__with_not_found


report = Blueprint("report", __name__)
controller = ReportController


@report.route("", methods=GET)
@response__with_not_found
def get_report():
    return controller.get_report(
        request.args.get("startDate"), request.args.get("endDate")
    )
