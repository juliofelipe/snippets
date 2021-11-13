import json
from unittest import mock

from src.domain.snippet import Snippet

snippet_dict = {
    "code": "f0ca28d5-0ba1-44cd-b47a-d19fe390d03e",
    "language": "Python",
    "title": "Replace to join",
    "description": "''.join(data)",
    "created_at": "2021-11-13"
}

snippets = [Snippet.from_dict(snippet_dict)]


@mock.patch("application.rest.snippet.snippet_list_use_case")
def test_get(mock_use_case, client):
    mock_use_case.return_value = snippets

    http_response = client.get("/snippets")

    assert json.loads(http_response.data.decode("UTF-8")) == [snippet_dict]
    mock_use_case.assert_called()
    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"

