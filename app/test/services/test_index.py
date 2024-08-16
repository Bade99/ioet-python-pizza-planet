import pytest


def test_get_index_service(client, index_uri):
    response = client.get(index_uri)
    result = response.json
    pytest.assume(not result["error"])
    pytest.assume("version" in result)
    pytest.assume("status" in result)
