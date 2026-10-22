#!/usr/bin/env python3
"""Perfil e capacidades do projeto: a unica fonte da verdade sobre o que vale aqui.

O template nasce completo, mas um projeto derivado nao precisa de tudo. Em vez
de espalhar condicionais pelos scripts e pela documentacao, o estado fica em
`.template-state.json` e todo mundo le daqui.

    profile       prototipo | padrao | rigoroso
    capabilities  o que o projeto usa (gui, cli, build_exe...)

`profile` decide o que e bloqueante; `capabilities` decide o que existe. Uma
capacidade desligada nao vira aviso: ela simplesmente nao e verificada.

A escolha de interface (`interface`) ja existia e continua valendo: este modulo
a le e a traduz em capacidades, para que haja um vocabulario so.

Cross-platform (Windows, macOS, Linux): usa apenas a stdlib.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = PROJECT_ROOT / ".template-state.json"

Profile = Literal["prototipo", "padrao", "rigoroso"]
Tier = Literal["blocking", "advisory", "off"]

PROFILES: tuple[str, ...] = ("prototipo", "padrao", "rigoroso")
DEFAULT_PROFILE: Profile = "padrao"

#: Limites de cobertura por perfil. O prototipo nao mede; o padrao protege
#: contra regressao sem virar meta; o rigoroso e o portao de producao.
COVERAGE_THRESHOLDS: dict[str, int | None] = {
    "prototipo": None,
    "padrao": 70,
    "rigoroso": 80,
}

DEFAULT_CAPABILITIES: dict[str, bool] = {
    #: Interface de linha de comando.
    "cli": True,
    #: Interface grafica (Tkinter).
    "gui": True,
    #: Executavel standalone via PyInstaller.
    "build_exe": True,
}


@dataclass(frozen=True)
class Suite:
    """Uma suite do `validate`, com o que ela exige e o que a aciona."""

    name: str
    label: str
    #: Nivel por perfil.
    tier: dict[str, Tier]
    #: Capacidade necessaria; sem ela a suite nem aparece.
    requires: str | None = None
    #: Entra no `--quick`.
    quick: bool = False
    #: Gatilhos que, ao mudar, acionam a suite em `--changed`.
    triggers: tuple[str, ...] = ()
    #: A suite aceita receber caminhos especificos.
    accepts_paths: bool = False


ALL_BLOCKING: dict[str, Tier] = {
    "prototipo": "blocking",
    "padrao": "blocking",
    "rigoroso": "blocking",
}
ADVISORY_IN_DRAFT: dict[str, Tier] = {
    "prototipo": "advisory",
    "padrao": "blocking",
    "rigoroso": "blocking",
}

SUITES: tuple[Suite, ...] = (
    Suite(
        "sync-skills",
        "Sincronizar skills",
        ADVISORY_IN_DRAFT,
        triggers=("skills",),
    ),
    Suite("check-skills", "Skills", ADVISORY_IN_DRAFT, triggers=("skills",)),
    Suite(
        "check-architecture",
        "Arquitetura",
        ALL_BLOCKING,
        quick=True,
        triggers=("src",),
    ),
    Suite("check-docs", "Documentacao", ADVISORY_IN_DRAFT, triggers=("docs",)),
    Suite(
        "format-check",
        "Formatacao",
        ADVISORY_IN_DRAFT,
        triggers=("any",),
        accepts_paths=True,
    ),
    Suite(
        "lint", "Lint", ALL_BLOCKING, quick=True, triggers=("src", "scripts"), accepts_paths=True
    ),
    Suite("typecheck", "Tipos", ALL_BLOCKING, quick=True, triggers=("src", "scripts", "config")),
    Suite("test", "Testes", ALL_BLOCKING, quick=True, triggers=("src", "scripts")),
    Suite("build", "Build", ADVISORY_IN_DRAFT, triggers=("src", "config")),
    Suite(
        "smoke-package",
        "Smoke do wheel",
        ADVISORY_IN_DRAFT,
        triggers=("src", "config"),
    ),
)

#: Suites que o `validate` nao roda, mas que o projeto conhece.
EXTERNAL_SUITES: dict[str, str] = {
    "build-exe": "Executavel standalone do SO atual",
    "audit": "Auditoria de dependencias (depende de rede)",
}


@dataclass(frozen=True)
class ProjectConfig:
    """Estado efetivo do projeto."""

    profile: str = DEFAULT_PROFILE
    capabilities: dict[str, bool] = field(default_factory=lambda: dict(DEFAULT_CAPABILITIES))
    package_name: str = "app_template"
    distribution_name: str = "python-project-template"
    display_name: str = "Python Project Template"
    interface: str = "both"

    @property
    def coverage(self) -> int | None:
        """Limite minimo de cobertura do perfil, ou None quando nao se aplica."""
        return COVERAGE_THRESHOLDS[self.profile]

    def has(self, capability: str) -> bool:
        """Se o projeto usa a capacidade informada."""
        return self.capabilities.get(capability, False)


def _read_state(root: Path) -> dict[str, object]:
    state_file = root / ".template-state.json"
    if not state_file.is_file():
        return {}
    try:
        loaded = json.loads(state_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f".template-state.json invalido: {error}") from error
    return loaded if isinstance(loaded, dict) else {}


def read_project_config(root: Path = PROJECT_ROOT) -> ProjectConfig:
    """Le perfil e capacidades efetivos do projeto."""
    state = _read_state(root)

    raw_profile = state.get("profile")
    profile = (
        raw_profile if isinstance(raw_profile, str) and raw_profile in PROFILES else DEFAULT_PROFILE
    )

    interface = state.get("interface")
    interface_name = interface if isinstance(interface, str) else "both"

    capabilities = dict(DEFAULT_CAPABILITIES)
    # A escolha de interface e a fonte para `cli` e `gui`: manter dois lugares
    # dizendo a mesma coisa so cria chance de divergirem.
    capabilities["cli"] = interface_name in {"cli", "both"}
    capabilities["gui"] = interface_name in {"gui", "both"}
    declared = state.get("capabilities")
    if isinstance(declared, dict):
        for key, value in declared.items():
            if isinstance(key, str) and isinstance(value, bool):
                capabilities[key] = value

    def text(key: str, fallback: str) -> str:
        value = state.get(key)
        return value if isinstance(value, str) and value else fallback

    return ProjectConfig(
        profile=profile,
        capabilities=capabilities,
        package_name=text("packageName", "app_template"),
        distribution_name=text("distributionName", "python-project-template"),
        display_name=text("displayName", "Python Project Template"),
        interface=interface_name,
    )


def has_capability(name: str, root: Path = PROJECT_ROOT) -> bool:
    """Atalho para consultar uma capacidade."""
    return read_project_config(root).has(name)


def resolve_suites(config: ProjectConfig) -> list[tuple[Suite, Tier, str | None]]:
    """Resolve o nivel de cada suite para o perfil e as capacidades atuais."""
    resolved: list[tuple[Suite, Tier, str | None]] = []
    for suite in SUITES:
        if suite.requires is not None and not config.has(suite.requires):
            resolved.append((suite, "off", f'capacidade "{suite.requires}" desligada'))
            continue
        resolved.append((suite, suite.tier.get(config.profile, "blocking"), None))
    return resolved


def main() -> int:
    """Imprime o estado atual, para inspecao rapida."""
    config = read_project_config()
    print(f"Perfil: {config.profile}")
    ativas = ", ".join(name for name, on in config.capabilities.items() if on) or "nenhuma"
    print(f"Capacidades: {ativas}")
    print(
        f"Cobertura: {config.coverage}%"
        if config.coverage is not None
        else "Cobertura: nao aplicada neste perfil"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
