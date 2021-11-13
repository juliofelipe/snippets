import uuid
import datetime

from src.domain.snippet import Snippet


def test_snippet_model_init():
    code = uuid.uuid4()
    snippet = Snippet(
        code,
        language="Python",
        title="Replace to join",
        description="''.join(data)",
        created_at="2021-11-13"
    )

    assert snippet.code == code
    assert snippet.language == "Python"
    assert snippet.title == "Replace to join"
    assert snippet.description == "''.join(data)"
    assert snippet.created_at == "2021-11-13"