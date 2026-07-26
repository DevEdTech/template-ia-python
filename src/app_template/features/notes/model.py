from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Note:
    id: str
    title: str
    created_at: str


def validate_title(title: str) -> str:
    cleaned = title.strip()
    if not cleaned:
        raise ValueError("O título da nota não pode ser vazio.")
    return cleaned


def create_note(title: str) -> Note:
    cleaned_title = validate_title(title)
    return Note(
        id=str(uuid.uuid4()),
        title=cleaned_title,
        created_at=datetime.now().isoformat(),
    )
