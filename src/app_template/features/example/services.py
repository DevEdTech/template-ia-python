"""Adaptador de persistencia da feature de exemplo.

Todo acesso ao disco fica isolado aqui (camada de services), nunca diretamente
no model (logica pura) nem nos adaptadores de interface. Assim, trocar o meio de persistencia
nao afeta a logica nem os comandos.

O contador e salvo em um arquivo JSON dentro do diretorio de dados do usuario,
resolvido de forma portavel entre Windows, macOS e Linux.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_STATE_FILENAME = "counter.json"
_ENV_DATA_DIR = "APP_TEMPLATE_DATA_DIR"


def _default_data_dir() -> Path:
    """Resolve o diretorio de dados do usuario de forma portavel.

    - Windows: %LOCALAPPDATA%\\app-template
    - macOS:   ~/Library/Application Support/app-template
    - Linux:   $XDG_DATA_HOME/app-template ou ~/.local/share/app-template

    Pode ser sobrescrito pela variavel de ambiente `APP_TEMPLATE_DATA_DIR`.
    """
    override = os.environ.get(_ENV_DATA_DIR)
    if override:
        return Path(override)

    if os.name == "nt":  # Windows
        base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(base) / "app-template"

    if sys.platform == "darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "app-template"

    # Linux e demais Unix
    base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(base) / "app-template"


def _state_path() -> Path:
    return _default_data_dir() / _STATE_FILENAME


def load_count() -> int:
    """Le o contador persistido. Retorna 0 se ausente ou invalido."""
    path = _state_path()
    try:
        raw = path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        return 0
    try:
        data = json.loads(raw)
        value = data["count"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return 0
    return value if isinstance(value, int) else 0


def save_count(value: int) -> None:
    """Persiste o valor atual do contador, criando o diretorio se preciso."""
    path = _state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"count": value}), encoding="utf-8")
