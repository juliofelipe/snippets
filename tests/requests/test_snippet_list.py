from src.requests.snippet_list import SnippetListRequest


def test_build_snippet_list_request_without_parameters():
    request = SnippetListRequest()

    assert bool(request) is True