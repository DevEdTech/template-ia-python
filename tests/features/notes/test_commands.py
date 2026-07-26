from __future__ import annotations

import argparse
from typing import Any

import pytest

from app_template.features.notes.commands import register_notes_commands
from app_template.features.notes.use_cases import list_notes


def test_notes_add_and_list(
    capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture, isolated_data_dir: Any
) -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")
    register_notes_commands(subparsers)

    # Add
    args_add = parser.parse_args(["notes", "add", "Minha nota CLI"])
    assert args_add.handler(args_add) == 0
    out, _ = capsys.readouterr()
    assert "adicionada com sucesso!" in out

    # List
    args_list = parser.parse_args(["notes", "list"])
    assert args_list.handler(args_list) == 0
    out, _ = capsys.readouterr()
    assert "Minha nota CLI" in out

    # Add error
    args_add_err = parser.parse_args(["notes", "add", "  "])
    assert args_add_err.handler(args_add_err) == 1
    assert "não pode ser vazio" in caplog.text


def test_notes_remove(
    capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture, isolated_data_dir: Any
) -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")
    register_notes_commands(subparsers)

    args_add = parser.parse_args(["notes", "add", "Temp"])
    args_add.handler(args_add)
    capsys.readouterr()  # consume

    notes = list_notes()
    note_id = notes[0].id

    # Remove
    args_remove = parser.parse_args(["notes", "remove", note_id])
    assert args_remove.handler(args_remove) == 0
    out, _ = capsys.readouterr()
    assert "removida com sucesso" in out

    # Remove erro
    args_remove_err = parser.parse_args(["notes", "remove", "123"])
    assert args_remove_err.handler(args_remove_err) == 1
    assert "não encontrada" in caplog.text
