import json

class SnippetJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "code": str(o.code),
                "language": o.language,
                "title": o.title,
                "description": o.description,
                "created_at": o.created_at,
            }
            return to_serialize
        except AttributeError: # pragma: no cover
            return super().default(o)