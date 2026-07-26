from __future__ import annotations

from app_template.features.notes.model import Note, create_note
from app_template.features.notes.services import load_notes, save_notes


def list_notes() -> list[Note]:
    raw_notes = load_notes()
    return [Note(id=n["id"], title=n["title"], created_at=n["created_at"]) for n in raw_notes]


def add_note(title: str) -> Note:
    note = create_note(title)
    raw_notes = load_notes()
    raw_notes.append(
        {
            "id": note.id,
            "title": note.title,
            "created_at": note.created_at,
        }
    )
    save_notes(raw_notes)
    return note


def remove_note(note_id: str) -> bool:
    raw_notes = load_notes()
    filtered_notes = [n for n in raw_notes if n["id"] != note_id]
    if len(filtered_notes) == len(raw_notes):
        return False
    save_notes(filtered_notes)
    return True
