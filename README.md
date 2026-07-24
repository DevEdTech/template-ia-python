# python-project-template

Template de projeto Python (aplicação de linha de comando), pensado para pessoas que constroem ferramentas com a ajuda de agentes de código. Vem com organização de pastas, padrões de qualidade, testes, **build multiplataforma (Windows, macOS e Linux)** e instruções para agentes já prontos.

## Objetivo

Dar um ponto de partida seguro e organizado para criar aplicações Python simples. Você descreve o que quer, o agente implementa seguindo as regras deste template, e você valida com um único comando.

## Quando usar

Indicado para:

- Ferramentas de linha de comando (CLI)
- Automações e scripts de processamento
- Utilitários de dados (leitura/transformação de arquivos)
- Protótipos e provas de conceito
- Pequenos serviços sem interface web
- Bibliotecas simples reutilizáveis

## Quando NÃO usar (versão 1)

- Aplicações web com front-end (use o `project-template` de React)
- Sistemas de alta criticidade ou financeiros
- Serviços que exigem autenticação real e armazenamento seguro de segredos
- Pipelines de dados de grande escala ou infraestrutura crítica
- Aplicativos móveis ou desktop com interface gráfica rica

## Pré-requisitos

- Python 3.11 ou superior (o arquivo `.python-version` indica a versão recomendada)
- [uv](https://docs.astral.sh/uv/) (recomendado) — ou `pip` + `venv` como alternativa
- git
- Um agente de código (ex.: Claude Code)

> **Por que uv?** É rápido, resolve dependências de forma determinística (`uv.lock`), gerencia o ambiente virtual e a versão do Python, e funciona igual nos três sistemas operacionais. Se preferir, tudo funciona com `pip` — veja a alternativa em cada passo.

## Criar um novo projeto a partir do template

1. Crie o repositório a partir deste template (botão "Use this template" no GitHub) ou copie a pasta.
2. Entre na pasta do projeto.
3. Instale as dependências e rode o setup:

```bash
uv sync                        # cria o .venv e instala tudo (runtime + dev)
python scripts/setup_project.py
```

Com `pip`, em vez de `uv sync`:

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -e ".[dev]"
python scripts/setup_project.py
```

O `setup_project.py` renomeia o pacote, personaliza nome e descrição, remove a feature de exemplo (opcional) e sincroniza as skills dos agentes.

## Execução

Rode a CLI de exemplo:

```bash
uv run app-template --help
uv run app-template count up
uv run app-template count show
```

Sem uv (com o ambiente ativado):

```bash
python -m app_template --help
```

## Validação

Antes de considerar qualquer alteração pronta, rode:

```bash
python scripts/dev.py validate
```

Esse comando executa, em sequência: verificação das skills, checagem de formatação, lint, checagem de tipos, testes e build. Se todos passarem, a alteração está saudável.

## Comandos

O runner `scripts/dev.py` é o equivalente cross-platform ao `npm run` — funciona igual no Windows, macOS e Linux.

| Comando                                  | O que faz                                                         |
| ---------------------------------------- | ---------------------------------------------------------------- |
| `python scripts/dev.py format`           | Formata o código com Ruff                                        |
| `python scripts/dev.py format-check`     | Confere a formatação sem alterar arquivos                        |
| `python scripts/dev.py lint`             | Verifica problemas de código com Ruff                            |
| `python scripts/dev.py lint-fix`         | Corrige automaticamente o que o Ruff conseguir                   |
| `python scripts/dev.py typecheck`        | Verifica os tipos com mypy (modo estrito)                        |
| `python scripts/dev.py test`             | Roda os testes com pytest                                        |
| `python scripts/dev.py test-cov`         | Roda os testes medindo cobertura                                 |
| `python scripts/dev.py build`            | Gera o pacote distribuível (wheel + sdist)                       |
| `python scripts/dev.py build-exe`        | Gera o executável standalone do SO atual (PyInstaller)          |
| `python scripts/dev.py sync-skills`      | Sincroniza as skills para `.claude/skills` e `.agents/skills`    |
| `python scripts/dev.py check-skills`     | Verifica se as cópias das skills estão sincronizadas             |
| `python scripts/dev.py validate`         | Roda tudo: skills, format, lint, typecheck, testes e build       |

> **Atalho Unix (opcional):** no macOS e Linux há um `Makefile` — `make validate`, `make test`, etc. No Windows, use os comandos `python scripts/dev.py <tarefa>` acima, que funcionam em qualquer sistema.

## Build para diferentes ambientes (Windows, macOS, Linux)

Há dois formatos de entrega, e o guia completo está em [docs/building.md](docs/building.md):

- **Pacote Python (wheel + sdist)** — multiplataforma por natureza. `python scripts/dev.py build` gera artefatos em `dist/` que instalam em qualquer SO com Python.
- **Executável standalone (PyInstaller)** — um binário que roda sem Python instalado. `python scripts/dev.py build-exe` gera o executável **do sistema em que você está**. Como o PyInstaller não faz cross-compilação, cada executável (Windows, macOS, Linux) precisa ser gerado no próprio sistema operacional.

## Estrutura resumida

```
src/
└── app_template/         # pacote da aplicação (renomeado no setup)
    ├── __main__.py       # permite `python -m app_template`
    ├── cli.py            # composição da CLI (app) — sem regra de negócio
    ├── features/         # cada capacidade do produto em sua pasta
    │   └── example/      # exemplo mínimo; removido/renomeado no setup
    │       ├── model.py      # lógica pura
    │       ├── services.py   # I/O e persistência
    │       └── commands.py   # ligação com a CLI
    └── shared/           # reutilizável e neutro (types, lib)
tests/                    # espelham a estrutura das features
docs/                     # esta documentação
scripts/                  # runner e utilitários cross-platform
```

Detalhes em [docs/architecture.md](docs/architecture.md).

## Como usar agentes

As regras que os agentes devem seguir ficam em dois arquivos na raiz:

- `AGENTS.md` — regras gerais válidas para qualquer agente
- `CLAUDE.md` — instruções específicas para o Claude Code

Além disso, há skills que guiam tarefas comuns. Veja [docs/agents.md](docs/agents.md).

## Como criar uma feature

1. Peça ao agente um plano: "Use a skill plan-feature para planejar...".
2. Revise o plano.
3. Peça a implementação: "Use a skill implement-feature...".
4. Crie a pasta em `src/app_template/features/<nome>` com `model.py`, `services.py`, `commands.py` e um `__init__.py` que expõe a interface pública.
5. Adicione testes em `tests/features/<nome>/`.
6. Rode `python scripts/dev.py validate`.

Regras de arquitetura em [docs/architecture.md](docs/architecture.md).

## Como registrar uma decisão

Decisões relevantes de arquitetura ou tecnologia viram um ADR (Architecture Decision Record) em `docs/decisions/`. Use o formato do primeiro registro, [0001-initial-architecture.md](docs/decisions/0001-initial-architecture.md), como modelo.

## Limitações conhecidas

- Zero dependências de runtime por padrão: a feature de exemplo usa só a biblioteca padrão.
- Sem autenticação real nem armazenamento seguro de segredos.
- Executáveis nativos precisam ser gerados no próprio SO de destino (um build por sistema).
- Voltado a aplicações simples; não substitui projetos de alta criticidade.
