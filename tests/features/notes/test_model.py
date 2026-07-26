from __future__ import annotations

import pytest

from app_template.features.notes.model import create_note, validate_title


def test_validate_title_valid() -> None:
    assert validate_title("  Minha nota  ") == "Minha nota"


def test_validate_title_empty() -> None:
    with pytest.raises(ValueError, match="não pode ser vazio"):
        validate_title("   ")


def test_create_note() -> None:
    note = create_note("Teste")
    assert note.title == "Teste"
    assert note.id is not None
    assert note.created_at is not None
