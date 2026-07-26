"""Adaptador da feature de exemplo para a interface de linha de comando.

Os handlers convertem argumentos e saídas da CLI. A orquestração compartilhada
com outras interfaces vive em `use_cases.py`.
"""

from __future__ import annotations

import argparse

from app_template.features.example.use_cases import (
    decrease_count,
    get_count,
    increase_count,
)


def _handle_show(_args: argparse.Namespace) -> int:
    """Mostra o valor atual do contador."""
    print(get_count())
    return 0


def _handle_up(args: argparse.Namespace) -> int:
    """Incrementa e persiste o contador."""
    print(increase_count(args.step))
    return 0


def _handle_down(args: argparse.Namespace) -> int:
    """Decrementa e persiste o contador."""
    print(decrease_count(args.step))
    return 0


def register_example_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Registra o grupo de comandos `count` no parser raiz."""
    count = subparsers.add_parser("count", help="Contador de exemplo persistente.")
    count_actions = count.add_subparsers(dest="action", metavar="<acao>")
    count_actions.required = True

    show = count_actions.add_parser("show", help="Mostra o valor atual.")
    show.set_defaults(handler=_handle_show)

    up = count_actions.add_parser("up", help="Incrementa o contador.")
    up.add_argument("--step", type=int, default=1, help="Passo (padrao: 1).")
    up.set_defaults(handler=_handle_up)

    down = count_actions.add_parser("down", help="Decrementa o contador.")
    down.add_argument("--step", type=int, default=1, help="Passo (padrao: 1).")
    down.set_defaults(handler=_handle_down)
