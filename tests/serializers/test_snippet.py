import json

import uuid
from src.domain.snippet import Snippet
from src.serializers.snippet import SnippetJsonEncoder


def test_serializers_domain_snippet():
    code = uuid.uuid4()

    snippet = Snippet(
        code=code,
        language="Python",
        title="Replace to join",
        description="''.join(data)",
        created_at="2021-11-13"
    )

    expected_json = f"""
        {{
            "code": "{code}",
            "language": "Python",
            "title": "Replace to join",
            "description": "''.join(data)",
            "created_at": "2021-11-13"
        }}
    """

    json_snippet = json.dumps(snippet, cls=SnippetJsonEncoder)
    
    assert json.loads(json_snippet) == json.loads(expected_json)

    