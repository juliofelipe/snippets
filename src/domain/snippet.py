from typing import Optional
import uuid
import dataclasses
from datetime import date


@dataclasses.dataclass
class Snippet:
    code: uuid.UUID
    language: str
    title: str
    description: str
    created_at: Optional[date]

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        return dataclasses.asdict(self)