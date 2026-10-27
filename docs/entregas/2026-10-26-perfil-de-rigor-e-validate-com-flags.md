# Perfil de rigor e validate com flags

- **Data**: 2026-10-26
- **Branch**: `master` (commits `14fb89a`, `dc50291` e `9ca155a`)
- **Plano de origem**: revisão crítica dos três templates, aprovada na conversa
- **Jira**: PD-911, PD-913, PD-914

## Objetivo

Deixar de tratar todo projeto com o mesmo rigor, e deixar de pagar o portão
inteiro de validação em cada iteração.

## Funcionalidades entregues

- **Perfil de rigor** — o projeto declara em `.template-state.json` se é
  `prototipo`, `padrao` ou `rigoroso`, e isso decide o que bloqueia o
  `validate`. O limite de cobertura passa a vir do perfil, como
  `--cov-fail-under`, em vez de número fixo no `pyproject.toml`.
- **Regras que seguem a interface escolhida** — `cli` e `gui` derivam da
  escolha feita no setup. Um projeto `cli` deixa de carregar regras de GUI no
  `AGENTS.md`: antes o setup removia o código da interface não escolhida, mas
  não as regras dela.
- **Validação sob medida** — `python scripts/dev.py validate --changed` roda só
  o que a mudança afeta, incluindo os testes dos casos de uso, adaptadores e
  composições que dependem do arquivo tocado. `--quick`, `--only`, `--skip`,
  `--files`, `--strict`, `--no-bail`, `--list` e o atalho `show-profile`
  completam o conjunto.
- **Conferência do lockfile** — `check-lockfile` pega a divergência entre
  `pyproject.toml` e `uv.lock` antes de empurrar, em vez de ela aparecer no CI
  minutos depois, em todos os jobs da matriz ao mesmo tempo.
- **Skill de interface no padrão** — `interface-design-skill` virou
  `design-interface`: estava fora de todos os padrões do próprio repositório e
  não constava do catálogo.

## Critérios de aceite

- [x] O limite de cobertura vem do perfil; `prototipo` não impõe limite.
- [x] Projeto `cli` não recebe regras de GUI, e vice-versa.
- [x] `--changed` inclui os arquivos que dependem do alterado e os testes que
      cobrem o conjunto, com import relativo e reexport resolvidos.
- [x] Execução parcial não aplica cobertura global.
- [x] Mudança de configuração cancela a seleção e roda todas as suítes.
- [x] `check-lockfile` reprova divergência real e apenas avisa quando não
      consegue conferir.
- [x] A skill renomeada passa no `check_skills.py` e aparece no catálogo.
- [x] A execução do `validate` continua concentrada no runner do `dev.py`.

## Arquivos alterados

| Arquivo                            | Mudança                                                      |
| ---------------------------------- | ------------------------------------------------------------ |
| `scripts/project_config.py`        | Catálogo de suítes, perfis, capacidades e cobertura.         |
| `scripts/dep_graph.py`             | Grafo de imports via AST e fechamento transitivo.            |
| `scripts/validate.py`              | Orquestrador do `validate`, com as flags.                    |
| `scripts/check_lockfile.py`        | Confere o `uv.lock` contra o `pyproject.toml`.               |
| `scripts/dev.py`                   | Delega o `validate`; tarefas `show-profile` e `check-lockfile`. |
| `scripts/setup_project.py`         | Flags `--profile` e `--no-build-exe`; estado com perfil.      |
| `pyproject.toml`                   | `fail_under` deixa de ser o valor efetivo; pisos elevados.   |
| `skills/design-interface/SKILL.md` | Skill renomeada e reescrita no padrão do repositório.        |
| `AGENTS.md`, `CLAUDE.md`, `README.md` | Perfil, capacidades e regras condicionais por interface.   |
| `docs/agents.md`                   | Catálogo com a skill renomeada.                              |
| `docs/development-process.md`      | Tabela das flags e as duas ressalvas.                        |
| `.github/workflows/ci.yml`         | Matriz passa a cobrir Python 3.13 e 3.14.                    |
| `uv.lock`                          | Regenerado após os pisos subirem.                            |

Volume: 21 arquivos no commit da feature (1388 inserções, 539 remoções) e 7 no
commit da correção.

## Testes

| Teste                           | Tipo     | O que cobre                                                          |
| ------------------------------- | -------- | -------------------------------------------------------------------- |
| `tests/test_validate.py`        | contrato | Grafo (reexport, `__init__.py`, dependência indireta), níveis por perfil, capacidade desligada, cada flag. |
| `tests/test_check_lockfile.py`  | contrato | Lockfile ausente, `uv` ausente, em dia, divergência, e outra falha do `uv` **não** virando divergência. |
| `tests/test_dev_runner.py`      | contrato | Toda tarefa monta um comando; `validate` continua no runner.         |

Saída da suíte:

```text
TOTAL                                           362     31     56     13    89%
Required test coverage of 70% reached. Total coverage: 88.52%
============================== 68 passed in 1.10s ==============================
```

## Validações executadas

| Comando                              | Resultado |
| ------------------------------------ | --------- |
| `python scripts/dev.py validate`     | Verde     |
| CI (4 jobs da matriz + pre-commit)   | Verde     |
| CI (Security)                        | Verde     |

```text
$ python scripts/dev.py validate
Perfil padrao: 11 suite(s) — sync-skills, check-skills, check-architecture,
check-docs, check-lockfile, format-check, lint, typecheck, test, build,
smoke-package
Verificação arquitetural OK.
Validação da documentação OK.
uv.lock em dia com o pyproject.toml.
All checks passed!
Smoke test do wheel OK.
Validacao concluida.
```

CI, em `9ca155a`:

```text
pre-commit                            success
validate (ubuntu-latest, py3.13)      success
validate (ubuntu-latest, py3.14)      success
validate (windows-latest, py3.13)     success
validate (windows-latest, py3.14)     success
```

## Fora do escopo

- Remover a duplicação entre `[dependency-groups].dev` e
  `[project.optional-dependencies].dev`: continua mantida em sincronia por
  teste, porque o pip não lê PEP 735.
- Tornar o `audit` parte do `validate`: depende de rede, e o gate local não
  deve baixar nada implicitamente.

## Limitações e pendências conhecidas

- `check-lockfile` depende do `uv`. Sem ele, a suíte avisa e não reprova — o
  CI continua sendo a rede final, com `uv sync --locked`.
- O grafo cobre imports estáticos e `from ... import`. Import construído em
  tempo de execução (`importlib` com nome montado) não aparece, e nesse caso o
  `validate` completo continua sendo o portão.

## Como verificar manualmente

1. `python scripts/dev.py show-profile` — mostra o perfil, as capacidades e o
   que bloqueia.
2. `python scripts/dev.py validate --files src/app_template/features/notes
   --dry-run` — mostra os afetados por dependência (composições da CLI e da
   GUI) e os sete testes que cobrem o conjunto.
3. Acrescente uma dependência ao `pyproject.toml` sem rodar `uv lock` e
   execute `python scripts/dev.py check-lockfile`: reprova dizendo o que fazer.
   Rode `uv lock` e ele volta a passar.
