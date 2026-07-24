#!/usr/bin/env python3
"""Gera um executavel standalone da aplicacao com PyInstaller.

Cross-platform: roda no Windows, macOS e Linux usando apenas stdlib para orquestrar.
IMPORTANTE: o PyInstaller NAO faz cross-compilacao. Cada executavel precisa ser
gerado NO sistema operacional de destino. Para gerar os tres (win/mac/linux) de
uma vez, use a matriz de CI em .github/workflows/build.yml.

Uso:
    python scripts/build_exe.py              # gera dist/app-template[.exe]
    python scripts/build_exe.py --name meucli

O nome do executavel e do modulo de entrada refletem o pacote `app_template`.
Ajuste ENTRY_MODULE / DEFAULT_NAME apos renomear o pacote no setup.
"""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Modulo com o bloco `if __name__ == "__main__"` que inicia a app.
ENTRY_MODULE = PROJECT_ROOT / "src" / "app_template" / "__main__.py"
DEFAULT_NAME = "app-template"


def _pyinstaller_cmd(name: str) -> list[str]:
    """Monta o comando do PyInstaller, preferindo `uv run` quando disponivel."""
    base = (
        ["uv", "run", "pyinstaller"]
        if shutil.which("uv")
        else [sys.executable, "-m", "PyInstaller"]
    )
    return [
        *base,
        "--onefile",  # um unico arquivo executavel
        "--name",
        name,
        "--paths",
        str(PROJECT_ROOT / "src"),  # garante que `app_template` seja encontrado
        "--clean",
        "--noconfirm",
        str(ENTRY_MODULE),
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gera o executavel standalone (PyInstaller).")
    parser.add_argument("--name", default=DEFAULT_NAME, help="Nome do executavel gerado.")
    args = parser.parse_args(argv)

    if not ENTRY_MODULE.exists():
        print(f"Modulo de entrada nao encontrado: {ENTRY_MODULE}", file=sys.stderr)
        return 1

    cmd = _pyinstaller_cmd(args.name)
    print(f"Sistema: {platform.system()} ({platform.machine()})")
    print(f"$ {' '.join(cmd)}", flush=True)
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, check=False)
    if result.returncode == 0:
        suffix = ".exe" if platform.system() == "Windows" else ""
        print(f"\nExecutavel gerado em: dist/{args.name}{suffix}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
