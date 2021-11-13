from src.domain.snippet import Snippet

class MemRepo:
    def __init__(self, data):
        self.data = data

    def list(self):
        return [Snippet.from_dict(i) for i in self.data]