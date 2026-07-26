"""Tipos compartilhados e neutros de dominio."""

from __future__ import annotations

# Adicione tipos compartilhados aqui (ex: enums, protocols globais)
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E", bound=Exception)


@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T


@dataclass(frozen=True)
class Err(Generic[E]):
    error: E


Result = Ok[T] | Err[E]
