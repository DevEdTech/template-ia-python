#!/usr/bin/env python3
"""Runner de tarefas de desenvolvimento — cross-platform (Windows, macOS, Linux).

Equivalente ao `npm run <script>` do template web, porem em Python puro (stdlib).
Funciona identicamente nos tres sistemas operacionais: usa apenas subprocess e
o mesmo interpretador em execucao — sem shell, sem Makefile obrigatorio.

Uso:
    python scripts/dev.py <tarefa> [args...]
    python scripts/dev.py validate
    python scripts/dev.py test -k nome_do_teste

Se o `uv` estiver instalado, as ferramentas rodam via `uv run` (no ambiente do
projeto). Caso contrario, caem para `python -m <ferramenta>`, assumindo que as
dependencias de dev ja foram instaladas (veja o README).

Rode `python scripts/dev.py help` para ver todas as tarefas.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

# uv disponivel? Define como as ferramentas serao invocadas.
_HAS_UV = shutil.which("uv") is not None


def _tool(tool: str, *args: str) -> list[str]:
    """Monta o comando para rodar uma ferramenta Python (ruff, mypy, pytest...)."""
    if _HAS_UV:
        return ["uv", "run", tool, *args]
    return [sys.executable, "-m", tool, *args]


def _script(name: str, *args: str) -> list[str]:
    """Monta o comando para rodar outro script do proprio template."""
    return [sys.executable, str(SCRIPTS_DIR / name), *args]


def _build_cmd() -> list[str]:
    """Comando para gerar wheel + sdist (pacote distribuivel)."""
    if _HAS_UV:
        return ["uv", "build"]
    return [sys.executable, "-m", "build"]


def _run(cmd: Sequence[str]) -> int:
    """Executa um comando exibindo-o, retornando o codigo de saida."""
    print(f"$ {' '.join(cmd)}", flush=True)
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, check=False)
    return result.returncode


def _run_all(commands: Sequence[Sequence[str]]) -> int:
    """Executa comandos em sequencia; para no primeiro que falhar."""
    for cmd in commands:
        code = _run(cmd)
        if code != 0:
            print(f"\nFALHOU (codigo {code}): {' '.join(cmd)}", file=sys.stderr)
            return code
    return 0


# Tarefas que recebem argumentos extras (repassados a ferramenta).
def task_format(args: list[str]) -> int:
    return _run(_tool("ruff", "format", *args))


def task_format_check(args: list[str]) -> int:
    return _run(_tool("ruff", "format", "--check", *args))


def task_lint(args: list[str]) -> int:
    return _run(_tool("ruff", "check", *args))


def task_lint_fix(args: list[str]) -> int:
    return _run(_tool("ruff", "check", "--fix", *args))


def task_typecheck(args: list[str]) -> int:
    return _run(_tool("mypy", *args))


def task_test(args: list[str]) -> int:
    return _run(_tool("pytest", *args))


def task_test_cov(args: list[str]) -> int:
    return _run(_tool("pytest", "--cov", *args))


def task_build(args: list[str]) -> int:
    return _run([*_build_cmd(), *args])


def task_build_exe(args: list[str]) -> int:
    return _run(_script("build_exe.py", *args))


def task_sync_skills(args: list[str]) -> int:
    return _run(_script("sync_skills.py", *args))


def task_check_skills(args: list[str]) -> int:
    return _run(_script("check_skills.py", *args))


def task_validate(args: list[str]) -> int:
    """Porta unica de qualidade: roda tudo, na ordem, parando no primeiro erro."""
    return _run_all(
        [
            _script("check_skills.py"),
            _tool("ruff", "format", "--check"),
            _tool("ruff", "check"),
            _tool("mypy"),
            _tool("pytest"),
            _build_cmd(),
        ]
    )


# Registro de tarefas: nome -> (funcao, descricao).
TASKS = {
    "format": (task_format, "Formata o codigo com Ruff."),
    "format-check": (task_format_check, "Confere a formatacao sem alterar arquivos."),
    "lint": (task_lint, "Verifica problemas de codigo com Ruff."),
    "lint-fix": (task_lint_fix, "Corrige automaticamente o que o Ruff conseguir."),
    "typecheck": (task_typecheck, "Verifica os tipos com mypy (modo estrito)."),
    "test": (task_test, "Roda os testes com pytest."),
    "test-cov": (task_test_cov, "Roda os testes medindo cobertura."),
    "build": (task_build, "Gera o pacote distribuivel (wheel + sdist)."),
    "build-exe": (task_build_exe, "Gera o executavel standalone do SO atual."),
    "sync-skills": (task_sync_skills, "Sincroniza as skills para .claude e .agents."),
    "check-skills": (task_check_skills, "Verifica se as copias das skills batem."),
    "validate": (task_validate, "Roda tudo: skills, format, lint, types, testes, build."),
}


def print_help() -> None:
    print("Tarefas disponiveis (python scripts/dev.py <tarefa>):\n")
    width = max(len(name) for name in TASKS)
    for name, (_func, desc) in TASKS.items():
        print(f"  {name.ljust(width)}  {desc}")
    print(
        f"\nRunner: {'uv run' if _HAS_UV else 'python -m'} (uv "
        f"{'detectado' if _HAS_UV else 'nao encontrado'})."
    )


def main(argv: list[str] | None = None) -> int:
    try:
        args = list(sys.argv[1:] if argv is None else argv)
        if not args or args[0] in {"help", "-h", "--help"}:
            print_help()
            return 0

        task_name, *rest = args
        entry = TASKS.get(task_name)
        if entry is None:
            print(f"Tarefa desconhecida: {task_name!r}\n", file=sys.stderr)
            print_help()
            return 2

        func, _desc = entry
        return func(rest)
    except KeyboardInterrupt:
        print("\nCancelado pelo usuário.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
