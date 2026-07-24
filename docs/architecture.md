# Arquitetura

Este documento descreve como o código do `python-project-template` é organizado e as regras que mantêm o projeto simples e sustentável.

## Princípios

- Organização por funcionalidades (features), não por camadas técnicas.
- Cada parte tem uma responsabilidade clara.
- Simplicidade primeiro: só adicione abstração quando houver necessidade real.
- Regra de negócio fica nas features; a base (`cli` e `shared`) permanece neutra.
- Lógica pura separada de I/O: facilita testar e trocar implementações.

## Layout do projeto

Usamos o **layout `src/`** (padrão moderno em Python): o código importável vive em `src/`, e os testes ficam em uma árvore `tests/` que espelha as features.

```
src/
└── app_template/         # pacote da aplicação (renomeado no setup)
    ├── __init__.py
    ├── __main__.py       # ponto de entrada para `python -m app_template`
    ├── cli.py            # composição da CLI: monta o parser e delega — sem regra de negócio
    ├── features/         # cada capacidade do produto em sua própria pasta
    │   └── example/      # exemplo mínimo; removido/renomeado no setup
    └── shared/           # reutilizável e neutro: types, lib
tests/
└── features/
    └── example/          # testes espelham a estrutura da feature
scripts/                  # runner de tarefas e utilitários (cross-platform)
docs/                     # esta documentação
```

Uma feature típica:

```
features/minha-feature/
├── __init__.py     # interface pública da feature
├── model.py        # tipos e lógica de negócio (funções puras, sem I/O)
├── services.py     # acesso a disco, rede, variáveis de ambiente
└── commands.py     # ligação com a CLI (registra subcomandos, orquestra model + services)
```

## Responsabilidades

- **cli.py (`app`)**: monta a aplicação. Cria o parser de argumentos e registra os comandos de cada feature. Não contém regra de negócio.
- **features/**: cada capacidade do produto (ex.: "exportar relatório"). Reúne tudo que aquela funcionalidade precisa.
- **shared/**: peças reutilizáveis e neutras (tipos genéricos, utilitários). Não conhece nenhuma feature específica.
- **tests/**: espelham as features; testam o comportamento observável.

## Camadas dentro de uma feature

- **model.py** — lógica pura. Sem I/O, sem `argparse`, sem rede. Funções determinísticas, fáceis de testar isoladamente.
- **services.py** — todo o I/O: leitura/escrita em disco, chamadas HTTP, leitura de variáveis de ambiente. Isola os efeitos colaterais.
- **commands.py** — registra os subcomandos da CLI e orquestra `model` + `services`. Não contém regra de negócio própria.
- **`__init__.py`** — expõe a interface pública da feature. É o único ponto que outras partes do código podem importar.

## Regras de dependência

1. Cada funcionalidade tem sua própria pasta em `features/`.
2. Uma feature não importa módulos internos de outra feature.
3. Uma feature expõe sua interface pública pelo `__init__.py`.
4. Chamadas HTTP e acesso a disco ficam em `services.py`, nunca no `model` nem no `commands`.
5. Leitura de variáveis de ambiente fica em `services.py`.
6. `model.py` é puro: sem I/O, sem dependência de framework.
7. `shared` é neutro: não depende de nenhuma feature.
8. Não crie abstrações sem necessidade concreta.
9. Sem dependências de runtime enquanto a stdlib resolver.
10. Nenhuma credencial no código.
11. Estados explícitos: trate sucesso, erro e vazio de forma clara.
12. Toda mudança de comportamento considera os testes.
13. Toda decisão relevante atualiza a documentação ou gera um ADR.

## Acesso a APIs e disco

Todo acesso a recursos externos (rede, disco, ambiente) passa por `services.py` dentro da feature. Os comandos chamam o serviço; nunca fazem I/O diretamente. Isso concentra o tratamento de erros e facilita substituir a fonte por dados fake nos testes. Veja [integrations.md](integrations.md).

## Type hints e qualidade

Todo o código usa type hints e passa no **mypy em modo estrito**. O **Ruff** cuida de formatação e lint. Essas checagens fazem parte de `python scripts/dev.py validate`.

## Testes

Os testes ficam em `tests/`, espelhando a estrutura das features. Testam o comportamento observável. Detalhes em [testing.md](testing.md).

## Empacotamento e build

O projeto usa `pyproject.toml` (PEP 621) com o backend `hatchling` e layout `src/`. Há duas formas de entrega — pacote (wheel/sdist) e executável standalone (PyInstaller) — descritas em [building.md](building.md).

## Evolução incremental

O template começa simples de propósito. Adicione estrutura, bibliotecas ou camadas apenas quando um problema real aparecer, e registre a mudança em um ADR (`docs/decisions/`).
