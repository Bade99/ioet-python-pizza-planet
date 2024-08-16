import pytest


def test_get_index_service(client, index_uri):
    response = client.get(index_uri)
    pytest.assume(not response.json["error"])
