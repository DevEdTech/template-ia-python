# Atualização de dependências (Dependabot)

- **Data**: 2026-08-25
- **Branch**: `claude/merge-prs-delivery-docs-00fasm`
- **Plano de origem**: PRs abertos automaticamente pelo Dependabot (#4 e #6)

## Objetivo

Manter as dependências de desenvolvimento e as actions do CI atualizadas,
incorporando as duas atualizações que o Dependabot já havia proposto e
validado no GitHub, sem alterar comportamento do projeto.

## Funcionalidades entregues

- **CI mais resiliente** — o workflow passa a instalar o uv pela
  `astral-sh/setup-uv@v10.0.1` (antes `v9.0.0`), que tolera timeouts
  transitórios ao buscar o manifesto de versões.
- **Ferramentas de desenvolvimento atualizadas** — `ruff`, `mypy`,
  `pyinstaller` e `pre-commit` passam a exigir as versões mínimas mais
  recentes (correções de bugs upstream), sem mudança de configuração.

## Critérios de aceite

- [x] PR #4 (`astral-sh/setup-uv` 9.0.0 → 10.0.1) mergeado, com os checks
      de CI verdes.
- [x] PR #6 (grupo `python-minor-and-patch`: ruff, mypy, pyinstaller,
      pre-commit) mergeado, com os checks de CI verdes.
- [x] `python scripts/dev.py validate` verde após o merge.

## Arquivos alterados

| Arquivo                          | Mudança                                                    |
| --------------------------------- | ----------------------------------------------------------- |
| `.github/workflows/ci.yml`        | `astral-sh/setup-uv` de v9.0.0 para v10.0.1 (2 ocorrências). |
| `.github/workflows/security.yml`  | `astral-sh/setup-uv` de v9.0.0 para v10.0.1.                 |
| `pyproject.toml`                  | `ruff>=0.16.4`, `mypy>=2.3.1`, `pyinstaller>=6.22.2`, `pre-commit>=4.6.2` nos dois grupos `dev`. |
| `uv.lock`                         | Lockfile regenerado para as novas versões.                  |

## Testes

Nenhum teste novo — a entrega não altera código de produto, apenas
versões de dependências e de action do CI. A suíte existente cobre a
regressão.

Saída da suíte:

```text
tests/features/notes/test_commands.py .....                              [ 10%]
tests/features/notes/test_gui.py ..                                      [ 14%]
tests/features/notes/test_model.py ......                                [ 26%]
tests/features/notes/test_services.py ........                           [ 42%]
tests/features/notes/test_use_cases.py ..                                [ 46%]
tests/test_architecture_check.py ....                                    [ 54%]
tests/test_cli.py .....                                                  [ 64%]
tests/test_docs_check.py ..                                              [ 68%]
tests/test_generate_feature.py ..                                        [ 72%]
tests/test_gui.py ..                                                     [ 76%]
tests/test_lib.py ...                                                    [ 82%]
tests/test_logger.py ....                                                [ 90%]
tests/test_packaging.py ..                                               [ 94%]
tests/test_setup_project.py ...                                          [100%]

Required test coverage of 80.0% reached. Total coverage: 88.52%
50 passed in 3.32s
```

## Validações executadas

| Comando                          | Resultado |
| --------------------------------- | --------- |
| `python scripts/dev.py validate`  | Verde     |

```text
$ scripts/sync_skills.py -> Sincronizacao concluida com sucesso.
$ scripts/check_skills.py -> Verificacao de skills OK: 12 skill(s) validada(s) e sincronizada(s).
$ scripts/check_architecture.py -> Verificação arquitetural OK.
$ scripts/check_docs.py -> Validação da documentação OK.
$ uv run ruff format --check -> 82 files already formatted
$ uv run ruff check -> All checks passed!
$ uv run mypy -> Success: no issues found in 42 source files
$ uv run pytest --cov -> 50 passed in 3.32s (cobertura total 88.52%)
$ uv build -> wheel e sdist gerados com sucesso
$ uv run python scripts/smoke_package.py -> Smoke test do wheel OK.
```

Além disso, cada PR já havia passado individualmente nos checks do GitHub
Actions antes do merge: `validate (ubuntu-latest, py3.13)`,
`validate (windows-latest, py3.13)`, `pre-commit`,
`Auditoria de dependências` e `Varredura de segredos`.

## Fora do escopo

- Atualizações major de dependências (nenhuma foi proposta pelo
  Dependabot nesta leva).
- Revisão do `dependabot.yml` ou das políticas de agrupamento de PRs.

## Limitações e pendências conhecidas

Nenhuma limitação conhecida. Não há diferença de comportamento entre
sistemas operacionais introduzida por esta entrega — ambos os runners
(`ubuntu-latest` e `windows-latest`) passaram nos checks de CI.

## Como verificar manualmente

1. Rode `python scripts/dev.py validate` na raiz do projeto.
2. Confirme que todas as etapas (skills, arquitetura, docs, lint, tipos,
   testes, build e smoke test) terminam em verde.
