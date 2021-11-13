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