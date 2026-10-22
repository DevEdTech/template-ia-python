#!/usr/bin/env python3
"""Grafo de dependencias do codigo-fonte, para rodar so o que a mudanca afeta.

`validate --changed` precisa responder: mudei este arquivo, quais testes cobrem
o que depende dele? A resposta e o fechamento transitivo das arestas invertidas
(quem importa quem).

Usa a AST do Python, como `check_architecture.py`, para nao errar em import
relativo, `from ... import` ou import dentro de funcao.

Cross-platform (Windows, macOS, Linux): usa apenas a stdlib.
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIRS = ("src", "tests")
IGNORED_DIRS = {"__pycache__", ".venv", "build", "dist"}


def _python_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return [path for path in directory.rglob("*.py") if not IGNORED_DIRS.intersection(path.parts)]


def _module_name(path: Path, root: Path) -> str:
    """Nome de modulo pontilhado a partir do caminho, com `src/` como raiz."""
    relative = path.relative_to(root)
    parts = list(relative.parts)
    if parts and parts[0] == "src":
        parts = parts[1:]
    if parts and parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1].removesuffix(".py")
    return ".".join(parts)


def _imported_modules(path: Path, module: str) -> set[str]:
    """Modulos que este arquivo importa, com imports relativos resolvidos."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError):
        return set()

    # Num `__init__.py` o pacote de referencia e o proprio modulo; em qualquer
    # outro arquivo e o pai. Confundir os dois faz `from .x import y` dentro de
    # um `__init__.py` apontar um nivel acima e a aresta se perder.
    if path.name == "__init__.py":
        pacote = module
    else:
        pacote = module.rsplit(".", 1)[0] if "." in module else ""
    imported: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                if node.module:
                    imported.add(node.module)
                    imported.update(f"{node.module}.{a.name}" for a in node.names)
                continue
            # Import relativo: sobe `level - 1` niveis a partir do pacote.
            base_parts = pacote.split(".") if pacote else []
            subida = node.level - 1
            base = ".".join(base_parts[: len(base_parts) - subida]) if subida else pacote
            alvo = f"{base}.{node.module}" if node.module else base
            if alvo:
                imported.add(alvo)
                imported.update(f"{alvo}.{a.name}" for a in node.names)
    return imported


def build_dependency_graph(
    root: Path = PROJECT_ROOT, directories: tuple[str, ...] = DEFAULT_DIRS
) -> tuple[dict[str, set[str]], dict[str, str]]:
    """Monta o grafo.

    Retorna `(dependents, modules)`: `dependents` mapeia caminho -> quem o
    importa (arestas invertidas) e `modules` mapeia nome de modulo -> caminho.
    """
    files = [f for directory in directories for f in _python_files(root / directory)]
    modules: dict[str, str] = {}
    for path in files:
        modules[_module_name(path, root)] = path.relative_to(root).as_posix()

    dependents: dict[str, set[str]] = {}
    for path in files:
        origem = path.relative_to(root).as_posix()
        module = _module_name(path, root)
        for imported in _imported_modules(path, module):
            # Um import pode apontar para o modulo ou para um nome dentro dele.
            alvo = modules.get(imported) or modules.get(imported.rsplit(".", 1)[0])
            if alvo is None or alvo == origem:
                continue
            dependents.setdefault(alvo, set()).add(origem)
    return dependents, modules


def affected_files(changed: list[str], dependents: dict[str, set[str]]) -> set[str]:
    """Fechamento transitivo: os alterados mais todos que dependem deles."""
    affected = set(changed)
    queue = list(affected)
    while queue:
        current = queue.pop()
        for dependent in dependents.get(current, set()):
            if dependent in affected:
                continue
            affected.add(dependent)
            queue.append(dependent)
    return affected


def covering_tests(files: set[str]) -> list[str]:
    """Os arquivos de teste dentro de um conjunto afetado.

    O nome evita o prefixo `test` de proposito: o pytest coleta por `test*` e
    tomaria a funcao por um caso de teste.
    """
    return sorted(
        path
        for path in files
        if Path(path).name.startswith("test_") or Path(path).name.endswith("_test.py")
    )


def main(argv: list[str] | None = None) -> int:
    """Imprime o conjunto afetado pelos caminhos informados."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="caminhos alterados, relativos a raiz")
    args = parser.parse_args(argv)

    dependents, _ = build_dependency_graph()
    affected = affected_files(args.paths, dependents)
    for path in sorted(affected):
        print(path)
    testes = covering_tests(affected)
    if testes:
        print("\nTestes:", file=sys.stderr)
        for path in testes:
            print(f"  {path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
