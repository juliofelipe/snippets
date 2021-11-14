import pytest
from src.requests.snippet_list import build_snippet_list_request


def test_build_snippet_list_request_without_parameters():
    request = build_snippet_list_request()

    assert request.filters is None
    assert bool(request) is True


def test_build_snippet_request_with_empty_filters():
    request = build_snippet_list_request({})

    assert request.filters == {}
    assert bool(request) is True


def test_build_snippet_list_request_with_invalid_filters_parameter():
    request = build_snippet_list_request(filters=5)

    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert bool(request) is False


def test_build_snippet_list_request_with_incorrect_filter_keys():
    request = build_snippet_list_request(filters={"a": 1})

    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert bool(request) is False


@pytest.mark.parametrize("key", ["code__eq", "language__eq", "title__contains"])
def test_build_snippet_list_request_accepted_filters(key):
    filters = {key: 1}

    request = build_snippet_list_request(filters=filters)

    assert request.filters == filters
    assert bool(request) is True
