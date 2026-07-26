"""Composição da interface de linha de comando da aplicação.

Responsabilidade: montar o parser de argumentos e delegar cada comando para a
feature correspondente. Não contém regra de negócio nem implementação gráfica.

A interface usa `argparse` da biblioteca padrao para manter zero dependencias de
runtime. Se um dia a complexidade justificar uma lib (ex.: Typer, Click),
registre a decisao em docs/decisions/ antes de adicionar.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence

from app_template import __version__
from app_template.features.example import register_example_commands

# Cada subcomando registra um handler: recebe os args e retorna o codigo de saida.
Handler = Callable[[argparse.Namespace], int]


def build_parser() -> argparse.ArgumentParser:
    """Constroi o parser raiz e registra os comandos de cada feature."""
    parser = argparse.ArgumentParser(
        prog="app-template",
        description="Aplicacao de exemplo do template Python.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="<comando>")
    subparsers.required = True

    # Cada feature registra seus proprios subcomandos. A camada app so orquestra.
    register_example_commands(subparsers)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Ponto de entrada da CLI. Retorna o codigo de saida do processo."""
    parser = build_parser()
    args = parser.parse_args(argv)
    # Cada subcomando define `args.handler` (ver commands.py de cada feature).
    handler: Handler = args.handler
    return handler(args)
