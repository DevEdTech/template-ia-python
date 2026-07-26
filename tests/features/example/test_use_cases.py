"""Testes dos casos de uso compartilhados pelas interfaces."""

from __future__ import annotations

from pathlib import Path

from app_template.features.example import decrease_count, get_count, increase_count


def test_casos_de_uso_compartilham_persistencia(isolated_data_dir: Path) -> None:
    assert get_count() == 0
    assert increase_count() == 1
    assert increase_count(step=2) == 3
    assert decrease_count(step=5) == 0
    assert get_count() == 0
