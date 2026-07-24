"""Testes de comportamento da CLI da feature de exemplo.

Exercitam o ponto de entrada real (`main`) do comeco ao fim: parsing dos
argumentos, orquestracao de model + services e persistencia isolada em um
diretorio temporario (fixture `isolated_data_dir`).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app_template.cli import main


def test_show_inicia_em_zero(isolated_data_dir: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["count", "show"]) == 0
    assert capsys.readouterr().out.strip() == "0"


def test_up_incrementa_e_persiste(
    isolated_data_dir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["count", "up"]) == 0
    assert capsys.readouterr().out.strip() == "1"

    assert main(["count", "up", "--step", "2"]) == 0
    assert capsys.readouterr().out.strip() == "3"

    # Um novo processo (nova chamada) le o valor persistido.
    assert main(["count", "show"]) == 0
    assert capsys.readouterr().out.strip() == "3"


def test_down_nao_passa_de_zero(
    isolated_data_dir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["count", "down"]) == 0
    assert capsys.readouterr().out.strip() == "0"
