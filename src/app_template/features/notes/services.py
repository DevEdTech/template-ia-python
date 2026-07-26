from __future__ import annotations

import json
import os
import sys
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from pathlib import Path

from app_template.features.notes.model import Note

_STATE_FILENAME = "notes.json"
_SCHEMA_VERSION = 1
_ENV_DATA_DIR = "APP_TEMPLATE_DATA_DIR"


@dataclass(frozen=True)
class NotesSnapshot:
    notes: list[Note]
    revision: int


class NoteStorageError(RuntimeError):
    """Falha observável ao ler ou persistir notas."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


class NoteStorageConflictError(NoteStorageError):
    def __init__(self) -> None:
        super().__init__(
            "NOTE_STORAGE_CONFLICT",
            "As notas estão sendo alteradas por outro processo. Tente novamente.",
        )


def _default_data_dir() -> Path:
    override = os.environ.get(_ENV_DATA_DIR)
    if override:
        return Path(override)
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(base) / "app-template"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "app-template"
    base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(base) / "app-template"


def _state_path() -> Path:
    return _default_data_dir() / _STATE_FILENAME


def _backup_path() -> Path:
    return _state_path().with_suffix(".backup.json")


def _lock_path() -> Path:
    return _state_path().with_suffix(".lock")


@contextmanager
def _exclusive_lock() -> Iterator[None]:
    lock = _lock_path()
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise NoteStorageConflictError() from exc
    try:
        os.close(descriptor)
        yield
    finally:
        with suppress(OSError):
            lock.unlink()


def _preserve_invalid_data(raw: str) -> None:
    backup = _backup_path()
    with suppress(OSError):
        if not backup.exists():
            backup.write_text(raw, encoding="utf-8")


def _parse_notes(values: object) -> list[Note]:
    if not isinstance(values, list):
        raise NoteStorageError(
            "NOTE_STORAGE_INVALID_DATA", "O arquivo de notas está em um formato inválido."
        )
    try:
        return [Note.from_record(item) for item in values]
    except ValueError as exc:
        raise NoteStorageError(
            "NOTE_STORAGE_INVALID_DATA", "Uma ou mais notas salvas estão corrompidas."
        ) from exc


def _read_snapshot() -> tuple[NotesSnapshot, bool]:
    path = _state_path()
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return NotesSnapshot([], 0), False
    except OSError as exc:
        raise NoteStorageError(
            "NOTE_STORAGE_READ_FAILED", "Não foi possível ler as notas salvas."
        ) from exc

    try:
        data: object = json.loads(raw)
        if isinstance(data, list):
            return NotesSnapshot(_parse_notes(data), 0), True
        if not isinstance(data, dict):
            raise NoteStorageError(
                "NOTE_STORAGE_INVALID_DATA", "O arquivo de notas está em um formato inválido."
            )
        if data.get("version") != _SCHEMA_VERSION:
            raise NoteStorageError(
                "NOTE_STORAGE_INVALID_DATA",
                "A versão do arquivo de notas não é compatível com esta aplicação.",
            )
        revision = data.get("revision")
        if not isinstance(revision, int) or isinstance(revision, bool) or revision < 0:
            raise NoteStorageError(
                "NOTE_STORAGE_INVALID_DATA", "A revisão do arquivo de notas é inválida."
            )
        return NotesSnapshot(_parse_notes(data.get("notes")), revision), False
    except (json.JSONDecodeError, TypeError) as exc:
        _preserve_invalid_data(raw)
        raise NoteStorageError(
            "NOTE_STORAGE_INVALID_DATA", "O arquivo de notas está corrompido."
        ) from exc
    except NoteStorageError:
        _preserve_invalid_data(raw)
        raise


def _write_snapshot(snapshot: NotesSnapshot) -> None:
    path = _state_path()
    temporary = path.with_suffix(".tmp")
    payload = {
        "version": _SCHEMA_VERSION,
        "revision": snapshot.revision,
        "notes": [note.to_record() for note in snapshot.notes],
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        temporary.replace(path)
    except OSError as exc:
        with suppress(OSError):
            temporary.unlink(missing_ok=True)
        raise NoteStorageError(
            "NOTE_STORAGE_WRITE_FAILED", "Não foi possível salvar as notas."
        ) from exc


def load_notes_snapshot() -> NotesSnapshot:
    snapshot, legacy = _read_snapshot()
    if not legacy:
        return snapshot
    return save_notes(snapshot.notes, expected_revision=0)


def load_notes() -> list[Note]:
    return load_notes_snapshot().notes


def save_notes(notes: list[Note], expected_revision: int | None = None) -> NotesSnapshot:
    with _exclusive_lock():
        current, _legacy = _read_snapshot()
        if expected_revision is not None and current.revision != expected_revision:
            raise NoteStorageConflictError()
        snapshot = NotesSnapshot(notes, current.revision + 1)
        _write_snapshot(snapshot)
        return snapshot
