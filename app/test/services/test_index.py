import pytest

from app.services.index import get_index


def test_get_index_service(client, index_uri):
    response = client.get(index_uri)
    pytest.assume(not response.json["error"])