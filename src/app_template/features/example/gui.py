"""Adaptador Tkinter da feature de exemplo.

O módulo não cria janelas nem importa Tkinter durante a inicialização do pacote.
Isso mantém CLI, testes e builds de pacote utilizáveis em ambientes sem GUI.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from app_template.features.example.use_cases import (
    decrease_count,
    get_count,
    increase_count,
)

if TYPE_CHECKING:
    import tkinter as tk
    from tkinter import ttk


def create_example_panel(parent: tk.Misc) -> ttk.Frame:
    """Cria o painel do contador e conecta seus eventos aos casos de uso."""
    import tkinter as tk
    from tkinter import ttk

    panel = ttk.Frame(parent, padding=24)
    value = tk.StringVar(master=panel, value=str(get_count()))

    ttk.Label(panel, text="Contador atual").grid(row=0, column=0, columnspan=3, pady=(0, 8))
    ttk.Label(panel, textvariable=value, font=("", 24, "bold")).grid(
        row=1,
        column=0,
        columnspan=3,
        pady=(0, 16),
    )

    def run(action: Callable[[], int]) -> None:
        value.set(str(action()))

    ttk.Button(panel, text="Diminuir", command=lambda: run(decrease_count)).grid(
        row=2,
        column=0,
        padx=4,
    )
    ttk.Button(panel, text="Atualizar", command=lambda: value.set(str(get_count()))).grid(
        row=2,
        column=1,
        padx=4,
    )
    ttk.Button(panel, text="Aumentar", command=lambda: run(increase_count)).grid(
        row=2,
        column=2,
        padx=4,
    )
    return panel
