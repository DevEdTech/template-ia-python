"""Ligacao da feature de exemplo com a CLI (camada `commands`).

Aqui os subcomandos sao registrados e os handlers orquestram model + services.
Nenhuma regra de negocio vive neste arquivo: a logica esta em `model` e o acesso
ao disco em `services`.
"""

from __future__ import annotations

import argparse

from app_template.features.example.model import decrement, increment
from app_template.features.example.services import load_count, save_count


def _handle_show(_args: argparse.Namespace) -> int:
    """Mostra o valor atual do contador."""
    print(load_count())
    return 0


def _handle_up(args: argparse.Namespace) -> int:
    """Incrementa e persiste o contador."""
    new_value = increment(load_count(), args.step)
    save_count(new_value)
    print(new_value)
    return 0


def _handle_down(args: argparse.Namespace) -> int:
    """Decrementa (nunca abaixo de zero) e persiste o contador."""
    new_value = decrement(load_count(), args.step)
    save_count(new_value)
    print(new_value)
    return 0


def register_example_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Registra o grupo de comandos `count` no parser raiz.

    Cada subcomando define `handler`, chamado pela camada app (cli.py).
    """
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
