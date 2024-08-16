import pytest


def test_get_report_service(client, report_uri, init_report_data):
    response = client.get(report_uri)
    pytest.assume(response.status.startswith("200"))
    report = response.json
    for report_section in [
        "top_ingredient",
        "top_beverage",
        "month_revenues",
        "top_clients",
    ]:
        pytest.assume(report_section in report)
