"""Composição da interface gráfica da aplicação.

Tkinter é carregado somente ao criar a janela. Assim, instalações voltadas à
CLI não falham apenas porque o sistema não oferece o componente gráfico.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Protocol

from app_template.features.example import create_example_panel


class GuiWindow(Protocol):
    """Contrato mínimo usado pelo loop principal e pelos testes."""

    def mainloop(self) -> None:
        """Executa o loop de eventos da janela."""


class GuiUnavailableError(RuntimeError):
    """Indica que o ambiente atual não consegue abrir a GUI."""


WindowFactory = Callable[[], GuiWindow]


def build_window() -> GuiWindow:
    """Monta a janela raiz sem iniciar o loop de eventos."""
    try:
        import tkinter as tk
    except ImportError as exc:
        raise GuiUnavailableError(
            "Tkinter não está instalado neste Python. Instale o suporte Tk do sistema."
        ) from exc

    try:
        window = tk.Tk()
    except tk.TclError as exc:
        raise GuiUnavailableError(
            "não foi possível acessar um ambiente gráfico nesta sessão."
        ) from exc

    window.title("Aplicação de exemplo")
    window.minsize(360, 220)
    create_example_panel(window).pack(fill="both", expand=True)
    return window


def main(window_factory: WindowFactory | None = None) -> int:
    """Abre a GUI e retorna zero quando o loop termina normalmente."""
    factory = build_window if window_factory is None else window_factory
    try:
        window = factory()
    except GuiUnavailableError as exc:
        print(f"GUI indisponível: {exc}", file=sys.stderr)
        return 1
    window.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
