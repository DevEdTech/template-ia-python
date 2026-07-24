"""Logica pura da feature de exemplo.

Sem I/O, sem argparse, sem dependencia de framework: apenas funcoes puras,
faceis de testar de forma isolada e deterministica.
"""

from __future__ import annotations

MIN_COUNT = 0
"""Valor minimo permitido para o contador."""


def increment(value: int, step: int = 1) -> int:
    """Incrementa `value` respeitando um passo positivo.

    Args:
        value: valor atual do contador.
        step: quanto somar (deve ser positivo).

    Returns:
        O novo valor apos o incremento.

    Raises:
        ValueError: se `step` nao for positivo.
    """
    if step <= 0:
        raise ValueError("step deve ser positivo")
    return value + step


def decrement(value: int, step: int = 1) -> int:
    """Decrementa `value` sem permitir resultado abaixo de `MIN_COUNT`.

    Args:
        value: valor atual do contador.
        step: quanto subtrair (deve ser positivo).

    Returns:
        O novo valor, nunca inferior a `MIN_COUNT`.

    Raises:
        ValueError: se `step` nao for positivo.
    """
    if step <= 0:
        raise ValueError("step deve ser positivo")
    return max(MIN_COUNT, value - step)
