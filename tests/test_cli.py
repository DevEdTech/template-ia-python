"""Testes da composição da CLI: parsing, despacho e códigos de saída."""

from __future__ import annotations

import importlib
from typing import Any

import pytest

from app_template.cli import build_parser, main


def test_sem_comando_mostra_ajuda_e_sai_com_zero(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    out, _ = capsys.readouterr()
    assert "<comando>" in out


def test_version_reporta_a_versao_do_pacote(capsys: pytest.CaptureFixture[str]) -> None:
    from app_template import __version__

    with pytest.raises(SystemExit) as exit_info:
        main(["--version"])

    assert exit_info.value.code == 0
    out, _ = capsys.readouterr()
    assert __version__ in out


def test_parser_registra_os_comandos_das_features() -> None:
    parser = build_parser()

    args = parser.parse_args(["notes", "list"])
    assert hasattr(args, "handler")


def test_main_despacha_para_a_feature(
    capsys: pytest.CaptureFixture[str], isolated_data_dir: Any
) -> None:
    assert main(["notes", "add", "Nota via CLI"]) == 0
    capsys.readouterr()

    assert main(["notes", "list"]) == 0
    out, _ = capsys.readouterr()
    assert "Nota via CLI" in out


def test_main_propaga_codigo_de_erro_da_feature(
    capsys: pytest.CaptureFixture[str], isolated_data_dir: Any
) -> None:
    assert main(["notes", "add", "   "]) == 1
    _, err = capsys.readouterr()
    assert "Erro:" in err


def test_modulo_de_execucao_reexporta_a_entrada() -> None:
    """`python -m app_template` precisa continuar apontando para a CLI."""
    module = importlib.import_module("app_template.__main__")

    assert module.main is main
