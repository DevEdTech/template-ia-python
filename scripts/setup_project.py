#!/usr/bin/env python3
"""Personaliza um novo projeto criado a partir deste template.

Uso: `python scripts/setup_project.py`.

O nome do arquivo evita `setup.py` de proposito, para nao se confundir com o
antigo script de empacotamento do distutils/setuptools.

O script e interativo. Em ambiente sem TTY (CI, pipes) ele apenas explica o uso
e sai com codigo 0, sem falhar.

O que ele faz:
  - Renomeia o pacote `app_template` e os comandos/distribuição `app-template`.
  - Atualiza name/description no pyproject.toml e o titulo do README.
  - (Opcional) remove a feature de exemplo e reinicia o tasks.md.
  - (Opcional) sincroniza as skills.

Cross-platform (Windows, macOS, Linux): usa apenas a stdlib.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

# Placeholders originais do template.
PLACEHOLDER_DIST = "python-project-template"  # nome da distribuicao e do comando base
PLACEHOLDER_PKG = "app_template"  # pacote importavel (src/app_template)
PLACEHOLDER_CLI = "app-template"  # comando de console
PLACEHOLDER_ENV = "APP_TEMPLATE_"  # prefixo de variaveis de ambiente


def log(msg: str) -> None:
    print(msg)


def slugify_package(name: str) -> str:
    """Converte um nome de projeto em um nome de pacote Python valido."""
    pkg = re.sub(r"[^0-9a-zA-Z_]+", "_", name.strip().lower()).strip("_")
    if not pkg or not pkg[0].isalpha():
        pkg = f"app_{pkg}" if pkg else "app"
    return pkg


def iter_target_files() -> list[Path]:
    """Arquivos onde os placeholders devem ser substituidos."""
    targets: list[Path] = []
    for base in ("src", "tests", "scripts"):
        targets.extend((PROJECT_ROOT / base).rglob("*.py"))
    for name in ("pyproject.toml", "README.md"):
        f = PROJECT_ROOT / name
        if f.exists():
            targets.append(f)
    return targets


def replace_in_files(project_name: str, package_name: str) -> None:
    """Substitui os placeholders (import, cli, dist, env) em todos os arquivos."""
    env_prefix = f"{package_name.upper()}_"
    replacements = {
        PLACEHOLDER_PKG: package_name,
        PLACEHOLDER_CLI: project_name,
        PLACEHOLDER_DIST: project_name,
        PLACEHOLDER_ENV: env_prefix,
    }
    for file in iter_target_files():
        text = file.read_text(encoding="utf-8")
        new_text = text
        for old, new in replacements.items():
            new_text = new_text.replace(old, new)
        if new_text != text:
            file.write_text(new_text, encoding="utf-8")
            log(f"  atualizado: {file.relative_to(PROJECT_ROOT)}")


def rename_package_dir(package_name: str) -> None:
    """Renomeia src/app_template para src/<package_name>."""
    old_dir = PROJECT_ROOT / "src" / PLACEHOLDER_PKG
    new_dir = PROJECT_ROOT / "src" / package_name
    if package_name == PLACEHOLDER_PKG:
        return
    if not old_dir.exists():
        log(f"Aviso: pacote {old_dir} nao encontrado; pulando rename.")
        return
    if new_dir.exists():
        log(f"Aviso: {new_dir} ja existe; pulando rename para nao sobrescrever.")
        return
    old_dir.rename(new_dir)
    log(f"Pacote renomeado: src/{PLACEHOLDER_PKG} -> src/{package_name}")


def update_pyproject_metadata(description: str) -> None:
    """Atualiza a description no pyproject.toml (name ja foi trocado por token)."""
    if not description:
        return
    file = PROJECT_ROOT / "pyproject.toml"
    text = file.read_text(encoding="utf-8")
    new_text = re.sub(
        r'(?m)^description = ".*"$',
        f'description = "{description}"',
        text,
        count=1,
    )
    if new_text != text:
        file.write_text(new_text, encoding="utf-8")
        log("pyproject.toml: description atualizada.")


def remove_example_feature() -> None:
    feature = PROJECT_ROOT / "src" / "app_template" / "features" / "example"
    # Pode ja ter sido renomeado; procura tambem o novo diretorio.
    if not feature.exists():
        candidates = list((PROJECT_ROOT / "src").glob("*/features/example"))
        if candidates:
            feature = candidates[0]
    tests_feature = PROJECT_ROOT / "tests" / "features" / "example"

    if feature.exists():
        shutil.rmtree(feature)
        log(f"Feature de exemplo removida: {feature.relative_to(PROJECT_ROOT)}")
    if tests_feature.exists():
        shutil.rmtree(tests_feature)
        log(f"Testes de exemplo removidos: {tests_feature.relative_to(PROJECT_ROOT)}")
    log("Atencao: ajuste cli.py, gui.py e o __init__ de features para nao importar o exemplo.")


def init_docs() -> None:
    template = (
        "# Tarefas\n\n"
        "Registre aqui as tarefas do projeto.\n\n"
        "## A fazer\n\n## Em andamento\n\n## Concluido\n"
    )
    (PROJECT_ROOT / "tasks.md").write_text(template, encoding="utf-8")
    log("tasks.md reiniciado para um estado limpo.")


def run_sync_skills() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "sync_skills.py")],
        cwd=PROJECT_ROOT,
        check=False,
    )
    if result.returncode != 0:
        log("Aviso: a sincronizacao de skills terminou com erro.")


def is_yes(answer: str, default_yes: bool) -> bool:
    normalized = answer.strip().lower()
    if normalized == "":
        return default_yes
    return normalized in {"s", "sim", "y", "yes"}


def explain_usage_and_exit() -> int:
    log("Setup do template (modo nao interativo detectado).\n")
    log("Este script personaliza um novo projeto e precisa de um terminal")
    log("interativo (TTY) para as perguntas. Rode em um terminal:\n")
    log("  python scripts/setup_project.py\n")
    log("Ou forneca argumentos via linha de comando para rodar automaticamente:")
    log('  python scripts/setup_project.py --name "meu-app" --description "Meu app" --remove-example\n')
    log("Para apenas sincronizar as skills:\n")
    log("  python scripts/dev.py sync-skills")
    return 0


def apply_changes(
    project_name: str,
    package_name: str,
    description: str,
    remove_example: bool,
    do_init_docs: bool,
    do_sync: bool,
) -> None:
    log("\nAplicando alteracoes...\n")

    # 1) Renomeia o diretorio do pacote antes de reescrever os arquivos.
    rename_package_dir(package_name)
    # 2) Substitui placeholders (import/cli/dist/env) em todos os arquivos.
    replace_in_files(project_name, package_name)
    # 3) Atualiza a description no pyproject.
    update_pyproject_metadata(description)

    if remove_example:
        remove_example_feature()
    if do_init_docs:
        init_docs()
    if do_sync:
        log("\nSincronizando skills...")
        run_sync_skills()

    log("\nSetup concluido. Proximos passos:")
    log('  1. Instale as dependencias:  uv sync  (ou: pip install -e ".[dev]")')
    log("  2. Valide o projeto:         python scripts/dev.py validate")
    log("  3. Rode a CLI:               uv run app-template --help")
    log("  4. Rode a GUI:               uv run app-template-gui")


def main() -> int:
    parser = argparse.ArgumentParser(description="Personaliza o template para um novo projeto.")
    parser.add_argument("--name", type=str, help="Nome do projeto (ex.: meu-app)")
    parser.add_argument("--description", type=str, help="Descricao do projeto")
    parser.add_argument("--remove-example", action="store_true", help="Remove a feature de exemplo")
    parser.add_argument("--init-docs", action="store_true", help="Reinicia tasks.md")
    parser.add_argument("--no-sync-skills", action="store_true", help="Pula a sincronizacao de skills")
    
    args, _ = parser.parse_known_args()
    has_args = any([args.name, args.description, args.remove_example, args.init_docs, args.no_sync_skills])
    
    if has_args:
        log("Configuracao via argumentos de linha de comando detectada.\n")
        project_name = args.name.strip() if args.name else PLACEHOLDER_DIST
        package_name = slugify_package(project_name)
        log(f'  -> pacote importavel: "{package_name}"\n')
        
        apply_changes(
            project_name,
            package_name,
            args.description.strip() if args.description else "",
            args.remove_example,
            args.init_docs,
            not args.no_sync_skills
        )
        return 0

    if not sys.stdin.isatty():
        return explain_usage_and_exit()

    log("Configuracao do novo projeto a partir do template.\n")

    name_raw = input("Nome do projeto (ex.: meu-app): ").strip()
    project_name = name_raw or PLACEHOLDER_DIST
    package_name = slugify_package(project_name)
    log(f'  -> pacote importavel: "{package_name}"\n')

    description = input("Descricao do projeto: ").strip()
    remove_example = is_yes(input("Remover feature de exemplo? (s/N): "), False)
    do_init_docs = is_yes(input("Reiniciar tasks.md? (s/N): "), False)
    do_sync = is_yes(input("Sincronizar skills? (S/n): "), True)

    apply_changes(project_name, package_name, description, remove_example, do_init_docs, do_sync)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nSetup cancelado.")
        raise SystemExit(130) from None
