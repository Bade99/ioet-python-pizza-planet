from app.common.http_methods import GET
from flask import Blueprint, request

from ..controllers import ReportController
from .base import execute__with_not_found


report = Blueprint("report", __name__)
controller = ReportController


@report.route("", methods=GET)
def get_report():
    return execute__with_not_found(
        controller.get_report,
        request.args.get("startDate"),
        request.args.get("endDate"),
    )
