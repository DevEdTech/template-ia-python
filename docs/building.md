# Build e distribuição multiplataforma

Este template entrega a aplicação de duas formas. Escolha conforme quem vai usar.

| Forma                         | Precisa de Python no destino? | Multiplataforma?                        | Quando usar                                              |
| ----------------------------- | ----------------------------- | --------------------------------------- | ------------------------------------------------------- |
| Pacote (wheel + sdist)        | Sim                           | Sim, um único artefato serve a todos    | Distribuir a outros devs; publicar em um índice (PyPI)  |
| Executável (PyInstaller)      | Não                           | Não — um binário por SO                  | Entregar para quem não tem Python instalado             |

## 1. Pacote Python (wheel + sdist)

Gera artefatos em `dist/` que instalam em qualquer sistema operacional com Python compatível. O wheel deste projeto é _pure Python_, então o **mesmo arquivo** funciona no Windows, macOS e Linux.

```bash
python scripts/dev.py build
```

Isso roda `uv build` (ou `python -m build`, se não houver uv) e produz:

```
dist/
├── python_project_template-0.0.0-py3-none-any.whl
└── python_project_template-0.0.0.tar.gz
```

Instalar em outra máquina:

```bash
pip install python_project_template-0.0.0-py3-none-any.whl
app-template --help
```

## 2. Executável standalone (PyInstaller)

Gera um único binário que roda **sem Python instalado**. Ótimo para entregar a usuários finais.

```bash
python scripts/dev.py build-exe
```

Isso produz `dist/app-template` (ou `dist/app-template.exe` no Windows).

### Limitação importante: sem cross-compilação

O PyInstaller **não** gera o executável de um SO a partir de outro. Para ter os três (Windows, macOS e Linux), você precisa rodar `python scripts/dev.py build-exe` **em cada sistema** — em uma máquina (ou VM) de cada plataforma — e coletar o binário gerado em `dist/`.

### Notas por sistema

- **Windows**: o executável é um `.exe`. O antivírus pode inspecionar binários PyInstaller na primeira execução (comportamento normal).
- **macOS**: o binário não é assinado nem "notarizado" por padrão; para distribuição ampla, considere assinatura de código (fora do escopo da v1). O executável é específico da arquitetura (Intel x86_64 ou Apple Silicon arm64) do runner.
- **Linux**: o binário depende da versão da glibc do sistema onde foi gerado. Para compatibilidade ampla, gere em uma distribuição mais antiga (ou em container manylinux).

## Versão

A versão vem de `pyproject.toml` (`[project].version`) e de `src/app_template/__init__.py` (`__version__`). Mantenha os dois em sincronia ao lançar uma nova versão.

## Reprodutibilidade

Versione o `uv.lock` (ou um `requirements.txt` travado). Assim, ao gerar o build em cada sistema, o mesmo lock garante versões idênticas de dependências e builds reproduzíveis.
