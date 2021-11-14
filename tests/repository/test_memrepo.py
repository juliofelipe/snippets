import pytest

from src.domain.snippet import Snippet
from src.repository.memrepo import MemRepo


@pytest.fixture
def snippet_dicts():
    return [
        {
            "code": "f0ca28d5-0ba1-44cd-b47a-d19fe390d03e",
            "language": "Python",
            "title": "Replace to join",
            "description": "''.join(data)",
            "created_at": "2021-11-13",
        },
        {
            "code": "832b1bed-d4c1-4365-9397-1ba680f309a7",
            "language": "Bash",
            "title": "Commands Docker",
            "description": "sudo service docker start",
            "created_at": "2021-11-12",
        },
        {
            "code": "4119a868-2a1d-414b-9871-a3669aabd0a0",
            "language": "Python",
            "title": "Code Pythonics",
            "description": "if data in datas: print(data)",
            "created_at": "2021-11-12",
        },
        {
            "code": "b1d70ad2-717c-4e01-b550-ae9af9c5cdac",
            "language": "Python",
            "title": "Code Pythonics",
            "description": "for data in datas: print(data)",
            "created_at": "2021-11-11",
        },
    ]


def test_repository_list_without_parameters(snippet_dicts):
    repo = MemRepo(snippet_dicts)

    snippets = [Snippet.from_dict(i) for i in snippet_dicts]

    assert repo.list() == snippets


def test_repository_list_with_code_equal_filter(snippet_dicts):
    repo = MemRepo(snippet_dicts)

    snippets = repo.list(filters={"code__eq": "f0ca28d5-0ba1-44cd-b47a-d19fe390d03e"})

    assert len(snippets) == 1
    assert snippets[0].code == "f0ca28d5-0ba1-44cd-b47a-d19fe390d03e"


@pytest.mark.parametrize("language", ["Bash", "Bash"])
def test_repository_list_with_language_equal_filter(snippet_dicts, language):
    repo = MemRepo(snippet_dicts)

    snippets = repo.list(filters={"language__eq": language})

    assert len(snippets) == 1
    assert snippets[0].code == "832b1bed-d4c1-4365-9397-1ba680f309a7"


@pytest.mark.parametrize("title", ["Code Pythonics", "Code Pythonics"])
def test_repository_list_with_title_equal_filter(snippet_dicts, title):
    repo = MemRepo(snippet_dicts)

    snippets = repo.list(filters={"title__eq": title})

    assert len(snippets) == 2
    assert set([r.code for r in snippets]) == {
        "4119a868-2a1d-414b-9871-a3669aabd0a0",
        "b1d70ad2-717c-4e01-b550-ae9af9c5cdac",
    }
