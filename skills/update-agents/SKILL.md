---
name: update-agents
description: Atualiza o AGENTS.md da raiz — as regras que todo agente lê em toda sessão — quando arquitetura, comandos, testes, convenções ou fronteiras do projeto mudam; use depois que a mudança foi implementada e validada, não para o README nem para docs/.
---

# Atualizar AGENTS.md

## Finalidade

Manter o `AGENTS.md` da raiz fiel às regras que valem hoje no projeto.
Ele é carregado em toda sessão de agente: regra errada ali se propaga
para todas as tarefas seguintes.

## Quando usar

Depois que uma mudança importante foi implementada e validada. Conta como
importante a mudança que altera **como se trabalha** no projeto:

- Fronteira de arquitetura, camada nova ou regra de import.
- Divisão entre `model.py`, `services.py`, `use_cases.py` e adaptadores.
- Tarefa nova ou removida no runner `scripts/dev.py`.
- Convenção de commit, de teste ou limite de cobertura.
- Dependência aceita, proibida ou substituída.
- Pasta nova com regra própria (por exemplo `docs/entregas`).
- Regra de portabilidade entre Windows, macOS e Linux.
- ADR aprovado que muda o modo de trabalho.
- Skill nova que entra no processo obrigatório.

## Quando não usar

- Para o `README.md`: use `update-readme`.
- Para `docs/` e ADR: use `update-documentation`.
- Para o guia de acionamento das skills em `docs/agents.md`: ele é parte
  de `docs/`, e quem cuida dele é `update-documentation`.
- Para mudança que não cria nem revoga regra — correção de bug, ajuste
  de texto, refatoração interna.

## O que entra no AGENTS.md

Entra a regra imperativa, curta e verificável, que vale para **toda**
tarefa. Não entra explicação, tutorial nem histórico.

| Entra                                            | Não entra                       |
| ------------------------------------------------ | ------------------------------- |
| "`model.py` permanece puro: sem I/O."            | Como testar uma função pura     |
| "Execute `python scripts/dev.py validate`."      | O que cada etapa do validate faz|
| "Todo código novo tem type hints."               | Como configurar o mypy          |

O detalhe fica em `docs/` e o `AGENTS.md` aponta para lá. Duplicar os dois
é garantir que um vai divergir do outro.

## Processo

1. Identifique a mudança e confirme que ela já está no código, com
   `python scripts/dev.py validate` verde. Regra não documenta intenção;
   documenta o que passou a valer.
2. Leia o `AGENTS.md` atual inteiro antes de editar.
3. Decida se a mudança **cria**, **altera** ou **revoga** uma regra. Se não
   faz nenhuma das três, pare: não é caso desta skill.
4. Escreva a regra na seção existente que já trata do assunto. Só crie
   seção nova quando o assunto não couber em nenhuma; a ordem canônica das
   seções está em `assets/agents-outline.md`.
5. Remova a regra que deixou de valer. Regra morta ensina o errado.
6. Confirme que cada regra citada tem como ser verificada: por tarefa do
   `validate`, por hook do pre-commit, por revisão de diff. Se não houver
   como, diga no texto como se confere.
7. Verifique se o `CLAUDE.md` continua coerente — ele aponta para o
   `AGENTS.md` e para a ordem de leitura de `docs/`.
8. Confira à mão os comandos e caminhos citados: `check-docs` valida
   `README.md` e `docs/`, mas **não** cobre o `AGENTS.md`.
9. Rode `python scripts/dev.py validate`.

## Regras de escrita

- Uma regra por linha, no imperativo. Nada de "recomenda-se".
- Frase curta, sem adjetivo. A regra precisa caber na cabeça de quem lê.
- Sem emoji, sem seção decorativa.
- Mantenha a ordem das seções existentes; reordenar sem necessidade só
  gera diff difícil de revisar.
- Custo de contexto é real: o arquivo é lido em toda sessão. Se a regra
  não muda o comportamento do agente, ela não merece uma linha.

## Resultado esperado

- `AGENTS.md` atualizado, com as regras que valem hoje.
- Lista do que foi acrescentado, alterado e removido, com o motivo.
- Confirmação de que `CLAUDE.md` continua coerente.
- Resultado de `python scripts/dev.py validate`.
