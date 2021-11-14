from src.domain.snippet import Snippet


class MemRepo:
    def __init__(self, data):
        self.data = data

    def list(self, filters=None):

        result = [Snippet.from_dict(i) for i in self.data]

        if filters is None:
            return result

        if "code__eq" in filters:
            result = [r for r in result if r.code == filters["code__eq"]]

        if "language__eq" in filters:
            result = [r for r in result if r.language == filters["language__eq"]]

        if "title__eq" in filters:
            result = [r for r in result if r.title == filters["title__eq"]]

        return result
