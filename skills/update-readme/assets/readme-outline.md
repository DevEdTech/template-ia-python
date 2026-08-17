# nome-do-projeto

Uma frase dizendo o que é, para quem e com qual stack.

## Objetivo

O que o projeto resolve, em duas ou três frases. Sem marketing.

## Quando usar

Indicado para:

- Caso de uso 1
- Caso de uso 2

## Quando NÃO usar

- Cenário fora do escopo 1
- Cenário fora do escopo 2

## Pré-requisitos

- Python 3.13 (a versão está em `.python-version`)
- `uv` (recomendado) ou `venv` + `pip`
- git

## Instalação

```bash
uv sync
```

Sem `uv`:

```bash
python -m venv .venv
```

## Execução

```bash
uv run app-template --help
```

## Validação

Antes de considerar qualquer alteração pronta, rode:

```bash
python scripts/dev.py validate
```

Uma frase dizendo o que esse comando executa, em sequência. Em macOS e
Linux, `make validate` é um atalho para o mesmo runner.

## Verificação automática

| Workflow   | Quando             | O que faz                          |
| ---------- | ------------------ | ---------------------------------- |
| `ci`       | push, Pull Request | `validate` nos sistemas suportados |
| `security` | push, semanalmente | auditoria de dependências e segredos |

## Comandos

Todas as tarefas passam pelo runner cross-platform:

```bash
python scripts/dev.py <tarefa>
```

| Tarefa      | O que faz                          |
| ----------- | ---------------------------------- |
| `test`      | Roda a suíte de testes             |
| `lint`      | Verifica problemas de código       |
| `typecheck` | Verifica os tipos                  |
| `build`     | Gera o pacote distribuível         |
| `validate`  | Roda todos os portões de qualidade |

## Build para diferentes ambientes

Diga como gerar o artefato e por que ele precisa ser gerado no próprio
sistema de destino, quando for o caso.

## Estrutura resumida

```
src/
└── pacote/               # pacote da aplicação
    ├── cli.py            # composição da CLI — sem regra de negócio
    ├── features/         # cada capacidade do produto em sua pasta
    │   └── exemplo/
    │       ├── model.py      # lógica pura
    │       ├── services.py   # I/O e persistência
    │       └── use_cases.py  # orquestração compartilhada
    └── shared/           # reutilizável e neutro
tests/                    # espelham a estrutura das features
docs/                     # esta documentação
scripts/                  # runner e utilitários cross-platform
```

Detalhes em [docs/architecture.md](docs/architecture.md).

## Como usar agentes

As regras que os agentes devem seguir ficam em dois arquivos na raiz:

- `AGENTS.md` — regras gerais válidas para qualquer agente
- `CLAUDE.md` — instruções específicas para o Claude Code

Veja [docs/agents.md](docs/agents.md) para a lista de skills.

## Como criar uma feature

1. Peça ao agente um plano: "Use a skill plan-feature para planejar...".
2. Revise o plano.
3. Peça a implementação: "Use a skill implement-feature...".
4. Rode `python scripts/dev.py validate`.
5. Peça a evidência da entrega: "Use a skill document-delivery...".

## Como registrar uma decisão

Decisões relevantes viram um ADR em `docs/decisions/`.

## Variáveis de ambiente

Copie `.env.example` para `.env.local` e preencha os valores. Diga onde a
leitura fica concentrada.

## Limitações conhecidas

- Limitação real 1
- Limitação real 2
