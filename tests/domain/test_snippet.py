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


def test_snippet_model_from_dict():
    code = uuid.uuid4()
    init_dict = {
        "code": code,
        "language": "Python",
        "title": "Replace to join",
        "description": "''.join(data)",
        "created_at": "2021-11-13"
    }


def test_snippet_model_to_dict():
    init_dict = {
        "code": uuid.uuid4(),
        "language": "Python",
        "title": "Replace to join",
        "description": "''.join(data)",
        "created_at": "2021-11-13"
    }

    snippet = Snippet.from_dict(init_dict)

    assert snippet.to_dict() == init_dict