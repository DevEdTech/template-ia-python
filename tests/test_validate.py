"""Testes do orquestrador de validacao e do grafo de dependencias.

O `--dry-run` imprime o plano sem executar nada: e assim que se verifica a
selecao de suites sem pagar o custo de rodar build e testes de verdade.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest
from scripts.dep_graph import affected_files, build_dependency_graph, covering_tests
from scripts.project_config import (
    COVERAGE_THRESHOLDS,
    DEFAULT_PROFILE,
    PROFILES,
    ProjectConfig,
    read_project_config,
    resolve_suites,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_validate(*args: str) -> subprocess.CompletedProcess[str]:
    """Executa o validate pelo runner, como uma pessoa faria."""
    return subprocess.run(  # noqa: S603
        [sys.executable, "scripts/dev.py", "validate", *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def graph_fixture(tmp_path: Path) -> Path:
    """Projeto minimo com uma cadeia de dependencias conhecida."""

    def write(rel: str, content: str) -> None:
        destino = tmp_path / rel
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(content, encoding="utf-8")

    write("src/app/__init__.py", "")
    write("src/app/shared/__init__.py", "")
    write("src/app/shared/format.py", "def limpar(v: str) -> str:\n    return v.strip()\n")
    write("src/app/features/__init__.py", "")
    write(
        "src/app/features/pedidos/__init__.py",
        "from .model import nome\n\n__all__ = ['nome']\n",
    )
    write(
        "src/app/features/pedidos/model.py",
        "from app.shared.format import limpar\n"
        "\n"
        "\n"
        "def nome(v: str) -> str:\n"
        "    return limpar(v)\n",
    )
    write(
        "src/app/features/pedidos/commands.py",
        "from .model import nome\n\n\ndef run(v: str) -> str:\n    return nome(v)\n",
    )
    write("src/app/features/outra/__init__.py", "def solto() -> int:\n    return 1\n")
    write("tests/__init__.py", "")
    write(
        "tests/test_pedidos.py",
        "from app.features.pedidos.model import nome\n"
        "\n"
        "\n"
        "def test_nome() -> None:\n"
        "    assert nome(' a ') == 'a'\n",
    )
    return tmp_path


def test_grafo_liga_quem_importa_a_quem_e_importado(graph_fixture: Path) -> None:
    dependents, _ = build_dependency_graph(graph_fixture)

    de_format = dependents.get("src/app/shared/format.py", set())
    assert "src/app/features/pedidos/model.py" in de_format

    do_modelo = dependents.get("src/app/features/pedidos/model.py", set())
    # Import relativo e reexport contam como dependencia.
    assert "src/app/features/pedidos/commands.py" in do_modelo
    assert "src/app/features/pedidos/__init__.py" in do_modelo
    assert "tests/test_pedidos.py" in do_modelo


def test_fechamento_transitivo_alcanca_dependencia_indireta(graph_fixture: Path) -> None:
    dependents, _ = build_dependency_graph(graph_fixture)
    afetados = affected_files(["src/app/shared/format.py"], dependents)

    assert "src/app/features/pedidos/model.py" in afetados, "direto"
    assert "src/app/features/pedidos/commands.py" in afetados, "indireto"
    assert "tests/test_pedidos.py" in afetados
    # Uma feature que nao participa da cadeia fica de fora.
    assert "src/app/features/outra/__init__.py" not in afetados


def test_separa_apenas_os_testes_do_conjunto_afetado() -> None:
    afetados = {"src/app/features/pedidos/model.py", "tests/test_pedidos.py"}
    assert covering_tests(afetados) == ["tests/test_pedidos.py"]


def test_cada_perfil_decide_o_que_bloqueia() -> None:
    config = ProjectConfig(capabilities={"cli": True, "gui": True, "build_exe": True})

    def tier(profile: str, name: str) -> str:
        resolved = resolve_suites(replace(config, profile=profile))
        return str(next(t for suite, t, _ in resolved if suite.name == name))

    assert tier("prototipo", "build") == "advisory"
    assert tier("padrao", "build") == "blocking"
    assert tier("prototipo", "typecheck") == "blocking", "tipos bloqueiam em todo perfil"
    assert tier("prototipo", "check-docs") == "advisory"
    assert tier("rigoroso", "check-docs") == "blocking"


def test_prototipo_nao_impoe_limite_de_cobertura() -> None:
    assert COVERAGE_THRESHOLDS["prototipo"] is None
    padrao = COVERAGE_THRESHOLDS["padrao"]
    rigoroso = COVERAGE_THRESHOLDS["rigoroso"]
    assert padrao is not None and rigoroso is not None and padrao < rigoroso


def test_interface_escolhida_define_as_capacidades(tmp_path: Path) -> None:
    (tmp_path / ".template-state.json").write_text(
        json.dumps({"interface": "cli", "profile": "rigoroso"}), encoding="utf-8"
    )
    config = read_project_config(tmp_path)

    assert config.has("cli")
    # Projeto `cli` nao tem GUI: as regras de GUI nao se aplicam a ele.
    assert not config.has("gui")
    assert config.profile == "rigoroso"


def test_estado_ausente_ou_invalido_cai_no_padrao(tmp_path: Path) -> None:
    assert read_project_config(tmp_path).profile == DEFAULT_PROFILE

    (tmp_path / ".template-state.json").write_text(
        json.dumps({"profile": "turbo"}), encoding="utf-8"
    )
    assert read_project_config(tmp_path).profile == DEFAULT_PROFILE
    assert DEFAULT_PROFILE in PROFILES


def test_list_descreve_perfil_capacidades_e_portoes() -> None:
    result = run_validate("--list")

    assert result.returncode == 0, result.stderr
    assert "Perfil:" in result.stdout
    assert "Capacidades:" in result.stdout
    assert "check-architecture" in result.stdout


def test_quick_seleciona_somente_as_suites_rapidas() -> None:
    result = run_validate("--quick", "--dry-run")

    assert result.returncode == 0, result.stderr
    assert "pytest" in result.stdout
    assert "--cov" not in result.stdout, "caminho rapido nao mede cobertura"
    assert "smoke_package" not in result.stdout


def test_only_e_skip_restringem_a_selecao() -> None:
    only = run_validate("--only", "lint", "--dry-run")
    assert only.returncode == 0, only.stderr
    assert "1 suite(s) — lint" in only.stdout

    skip = run_validate("--skip", "build", "smoke-package", "--dry-run")
    assert skip.returncode == 0, skip.stderr
    assert "smoke_package" not in skip.stdout


def test_suite_desconhecida_falha_dizendo_como_descobrir() -> None:
    result = run_validate("--only", "inexistente")

    assert result.returncode == 2
    assert "Suite desconhecida" in result.stderr
    assert "--list" in result.stderr


def test_files_deriva_o_alvo_do_grafo_sem_cobertura_global() -> None:
    result = run_validate("--files", "src/app_template/features/notes", "--dry-run")

    assert result.returncode == 0, result.stderr
    assert "Afetados por dependencia" in result.stdout
    # A composicao da CLI depende da feature e precisa entrar.
    assert "tests/test_cli.py" in result.stdout
    # Execucao parcial nao aplica cobertura global.
    assert "--cov" not in result.stdout
