# Correção da auditoria de dependências

- **Data**: 2026-10-26
- **Branch**: `fix/dependency-audit-2026-10-26`
- **Plano de origem**: correção restrita autorizada na conversa.

## Objetivo e funcionalidades entregues

Eliminar os achados da [auditoria de origem](https://github.com/DevEdTech/template-ia-python/actions/runs/40319578033), preservando os gates e o comportamento do template.

## Critérios de aceite

- [x] Lock resolvido e instalação com `uv sync --locked`.
- [x] Validação completa e auditoria local sem achados.
- [x] Diff restrito às dependências afetadas e à evidência da entrega.

## Arquivos alterados

- `uv.lock`: filelock 3.32.0 → 4.2.1, virtualenv 21.7.13 → 21.14.10 e setuptools 83.0.0 → 84.1.0.
- `packaging` 26.2 → 26.3, necessário porque virtualenv exige `packaging>=26.3`.
- Este registro.

## Testes e validações executadas

Windows, Python 3.13.14. Comandos: `uv sync --locked`, `uv run --locked python scripts/dev.py validate` e `uv run --locked python scripts/dev.py audit`; todos com código de saída 0.

```text
Required test coverage of 80.0% reached. Total coverage: 87.56%
50 passed in 7.71s
Successfully built dist\python_project_template-0.0.0.tar.gz
Successfully built dist\python_project_template-0.0.0-py3-none-any.whl
Smoke test do wheel OK.
No known vulnerabilities found
```

A validação também conferiu skills, arquitetura, documentação, formato, lint e tipos. Nenhum teste novo: não houve mudança de comportamento. A primeira candidata virtualenv 21.14.9 ainda apresentou CVE-2026-113713; 21.14.10 eliminou o achado na nova auditoria.

## Fora do escopo

Runtime, código de produto, workflows, permissões, segredos, outros repositórios e atualizações Ruff/pre-commit do PR Dependabot #14.

## Limitações e pendências conhecidas

Os resultados acima são locais. Os checks Linux/Windows, hooks e Security do PR devem passar no SHA final antes do merge. CI e Security da branch principal devem ser conferidos após o merge. A auditoria reflete o banco consultado nesta data.

## Como verificar manualmente

1. Execute `uv sync --locked`.
2. Execute `uv run --locked python scripts/dev.py validate`.
3. Execute `uv run --locked python scripts/dev.py audit`; espere ausência de vulnerabilidades conhecidas.
