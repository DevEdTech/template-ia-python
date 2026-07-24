"""Testes da logica pura do contador (comportamento observavel de model)."""

from __future__ import annotations

import pytest

from app_template.features.example.model import MIN_COUNT, decrement, increment


def test_increment_soma_o_passo() -> None:
    assert increment(0) == 1
    assert increment(2, step=3) == 5


def test_decrement_nao_passa_do_minimo() -> None:
    assert decrement(1) == MIN_COUNT
    assert decrement(0) == MIN_COUNT
    assert decrement(5, step=10) == MIN_COUNT


def test_passo_invalido_gera_erro() -> None:
    with pytest.raises(ValueError):
        increment(0, step=0)
    with pytest.raises(ValueError):
        decrement(0, step=-1)
