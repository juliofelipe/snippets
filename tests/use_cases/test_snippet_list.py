import pytest
import uuid
from unittest import mock

from src.domain.snippet import Snippet
from src.requests.snippet_list import SnippetListRequest, build_snippet_list_request
from src.use_cases.snippet_list import snippet_list_use_case
from src.responses import ResponseTypes


@pytest.fixture
def domain_snippets():
    snippet_1 = Snippet(
        code=uuid.uuid4(),
        language="Python",
        title="Replace to join",
        description="''.join(data)",
        created_at="2021-11-13"
    )

    snippet_2 = Snippet(
        code=uuid.uuid4(),
        language="Bash",
        title="Commands Docker",
        description="sudo service docker start",
        created_at="2021-11-12"
    )

    snippet_3 = Snippet(
        code=uuid.uuid4(),
        language="Python",
        title="Code Pythonics",
        description="if data in datas: print(data)",
        created_at="2021-11-12"
    )

    snippet_4 = Snippet(
        code=uuid.uuid4(),
        language="Python",
        title="Code Pythonics",
        description="for data in datas: print(data)",
        created_at="2021-11-11"
    )

    return [snippet_1, snippet_2, snippet_3, snippet_4]


def test_snippet_list_without_parameters(domain_snippets):
    repo = mock.Mock()
    repo.list.return_value = domain_snippets

    request = build_snippet_list_request()

    response = snippet_list_use_case(repo, request)

    assert bool(response) is True
    repo.list.assert_called_with(filters=None)
    assert response.value == domain_snippets


def test_snippet_list_with_filters(domain_snippets):
    repo = mock.Mock()
    repo.list.return_value = domain_snippets

    qry_filters = {"code__eq": 5}
    request = build_snippet_list_request(filters=qry_filters)

    response = snippet_list_use_case(repo, request)

    assert bool(response) is True
    repo.list.assert_called_with(filters=qry_filters)
    assert response.value == domain_snippets


def test_room_list_handles_generic_error():
    repo = mock.Mock()
    repo.list.side_effect = Exception("Just an error message")

    request = build_snippet_list_request(filters={})

    response = snippet_list_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseTypes.SYSTEM_ERROR,
        "message": "Exception: Just an error message"
    }


def test_snippet_list_handles_bad_request():
    repo = mock.Mock()

    request = build_snippet_list_request(filters=5)

    response = snippet_list_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseTypes.PARAMETERS_ERROR,
        "message": "filters: Is not iterable"
    }