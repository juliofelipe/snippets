from collections.abc import Mapping


class SnippetListRequest:
    @classmethod
    def from_dict(cls, adict):
        return cls()

    def __bool__(self):
        return True


class SnippetListInvalidRequest:
    def __init__(self):
        self.errors = []

    def add_error(self, parameter, message):
        self.errors.append({"parameter": parameter, "message": message})

    def has_errors(self):
        return len(self.errors) > 0

    def __bool__(self):
        return False


class SnippetListValidRequest:
    def __init__(self, filters=None):
        self.filters = filters

    def __bool__(self):
        return True


def build_snippet_list_request(filters=None):
    accepted_filters = ["code__eq", "language__eq", "title__contains"]
    invalid_req = SnippetListInvalidRequest()

    if filters is not None:
        if not isinstance(filters, Mapping):
            invalid_req.add_error("filters", "Is not iterable")
            return invalid_req

        for key, value in filters.items():
            if key not in accepted_filters:
                invalid_req.add_error("filters", "Key {} cannot be used".format(key))

        if invalid_req.has_errors():
            return invalid_req

    return SnippetListValidRequest(filters=filters)
