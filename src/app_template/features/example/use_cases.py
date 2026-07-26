"""Casos de uso compartilhados pelas interfaces da feature de exemplo.

Esta camada orquestra a lógica pura de `model.py` e o I/O de `services.py`.
CLI, GUI e futuras interfaces chamam as mesmas operações.
"""

from __future__ import annotations

from app_template.features.example.model import decrement, increment
from app_template.features.example.services import load_count, save_count


def get_count() -> int:
    """Retorna o valor persistido do contador."""
    return load_count()


def increase_count(step: int = 1) -> int:
    """Incrementa, persiste e retorna o novo valor."""
    new_value = increment(load_count(), step)
    save_count(new_value)
    return new_value


def decrease_count(step: int = 1) -> int:
    """Decrementa, persiste e retorna o novo valor."""
    new_value = decrement(load_count(), step)
    save_count(new_value)
    return new_value
