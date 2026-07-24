"""Tipos compartilhados e neutros de dominio."""

from __future__ import annotations

from typing import Literal

# Estados explicitos para operacoes que podem estar em andamento ou falhar.
AsyncStatus = Literal["idle", "loading", "success", "error"]
