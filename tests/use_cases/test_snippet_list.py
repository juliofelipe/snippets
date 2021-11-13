import pytest
import uuid
from unittest import mock

from src.domain.snippet import Snippet
from src.use_cases.snippet_list import snippet_list_use_case


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

    result = snippet_list_use_case(repo)

    repo.list.assert_called_with()
    assert result == domain_snippets