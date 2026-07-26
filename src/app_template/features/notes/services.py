from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from app_template.logger import get_logger

logger = get_logger(__name__)

_STATE_FILENAME = "notes.json"
_ENV_DATA_DIR = "APP_TEMPLATE_DATA_DIR"


def _default_data_dir() -> Path:
    override = os.environ.get(_ENV_DATA_DIR)
    if override:
        return Path(override)

    if os.name == "nt":  # Windows
        base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(base) / "app-template"

    if sys.platform == "darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "app-template"

    base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(base) / "app-template"


def _state_path() -> Path:
    return _default_data_dir() / _STATE_FILENAME


def load_notes() -> list[dict[str, str]]:
    path = _state_path()
    try:
        raw = path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        return []
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return data
    except (json.JSONDecodeError, TypeError):
        return []
    return []


def save_notes(notes: list[dict[str, str]]) -> None:
    path = _state_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(notes), encoding="utf-8")
    except OSError as e:
        logger.warning(f"Falha ao persistir notas localmente: {e}")
