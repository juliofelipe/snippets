import json
from unittest import mock

import pytest

from src.domain.snippet import Snippet
from src.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)

snippet_dict = {
    "code": "f0ca28d5-0ba1-44cd-b47a-d19fe390d03e",
    "language": "Python",
    "title": "Replace to join",
    "description": "''.join(data)",
    "created_at": "2021-11-13",
}

snippets = [Snippet.from_dict(snippet_dict)]


@mock.patch("application.rest.snippet.snippet_list_use_case")
def test_get(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(snippets)

    http_response = client.get("/snippets")

    assert json.loads(http_response.data.decode("UTF-8")) == [snippet_dict]

    mock_use_case.assert_called()
    args, kwargs = mock_use_case.call_args
    assert args[1].filters == {}

    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"


@mock.patch("application.rest.snippet.snippet_list_use_case")
def test_get_with_filters(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(snippets)

    http_response = client.get("/snippets?filter_language__eq=Java")

    assert json.loads(http_response.data.decode("UTF-8")) == [snippet_dict]

    mock_use_case.assert_called()
    args, kwargs = mock_use_case.call_args
    assert args[1].filters == {"language__eq": "Java"}

    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"


@pytest.mark.parametrize(
    "response_type, expected_status_code",
    [
        (ResponseTypes.PARAMETERS_ERROR, 400),
        (ResponseTypes.RESOURCE_ERROR, 404),
        (ResponseTypes.SYSTEM_ERROR, 500),
    ],
)
@mock.patch("application.rest.snippet.snippet_list_use_case")
def test_get_response_failures(
    mock_use_case,
    client,
    response_type,
    expected_status_code,
):
    mock_use_case.return_value = ResponseFailure(
        response_type, message="Just an error message"
    )

    http_response = client.get("/snippets?dummy_request_string")

    mock_use_case.assert_called()

    assert http_response.status_code == expected_status_code
