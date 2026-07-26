# Arquitetura

Este documento descreve como o código do `python-project-template` é organizado para aplicações com CLI, GUI ou ambas.

## Princípios

- Organização por funcionalidades (features), não por camadas técnicas globais.
- Regra de negócio independente da interface escolhida.
- Lógica pura separada de I/O e da apresentação.
- Uma única camada de casos de uso compartilhada por CLI, GUI e futuras interfaces.
- Simplicidade primeiro: só adicionar abstrações quando houver necessidade real.
- Composições de interface e `shared` permanecem neutros em relação ao domínio.

## Documentos de produto e arquitetura

Ao iniciar um aplicativo a partir do template, usar a skill `plan-app` para definir se o produto terá CLI, GUI ou ambas. Ela cria `docs/prd.md` com o problema, os usuários, o escopo, o não escopo, os requisitos e os critérios de aceite aprovados.

Este arquivo continua sendo a fonte das decisões técnicas. A `plan-app` deve acrescentar uma seção `Decisões do produto` com interfaces, features, fluxo de dados, persistência, integrações, plataformas e distribuição. O PRD explica **o que e por que** construir; a arquitetura explica **como o sistema será organizado**.

## Layout do projeto

```
src/
└── app_template/
    ├── __init__.py
    ├── __main__.py       # entrada padrão: CLI
    ├── cli.py            # composição da interface de terminal
    ├── gui.py            # composição da interface gráfica
    ├── features/
    │   └── example/
    │       ├── __init__.py   # interface pública da feature
    │       ├── model.py      # tipos e regras puras
    │       ├── services.py   # disco, rede e ambiente
    │       ├── use_cases.py  # orquestra model + services
    │       ├── commands.py   # adapta a feature para CLI
    │       └── gui.py        # adapta a feature para GUI
    └── shared/           # utilitários neutros
tests/
├── features/             # model, casos de uso e adaptadores
└── test_gui.py           # entrada GUI sem display real
scripts/                  # runner, setup e build multiplataforma
docs/                     # documentação e ADRs
```

Projetos que usam apenas uma interface podem remover o adaptador e a composição que não se aplicam depois de registrar essa decisão no PRD e na arquitetura.

## Responsabilidades

- **`model.py`**: tipos e regras de negócio puras, sem I/O ou dependência de interface.
- **`services.py`**: acesso a disco, rede e variáveis de ambiente.
- **`use_cases.py`**: coordena model e services; oferece as mesmas operações para qualquer interface.
- **`commands.py`**: converte argumentos, saída e códigos de retorno da CLI.
- **`features/<nome>/gui.py`**: cria componentes gráficos da feature e traduz eventos em casos de uso.
- **`cli.py` e `gui.py` do pacote**: compõem a aplicação e conectam features; não contêm regra de negócio.
- **`__init__.py` da feature**: única interface pública disponível para outras partes do projeto.
- **`shared`**: peças reutilizáveis e neutras, sem conhecimento de features.

## Regras de dependência

1. Cada capacidade vive em sua própria pasta em `features/`.
2. Uma feature não importa módulos internos de outra feature.
3. Toda feature expõe sua interface pública pelo `__init__.py`.
4. Interfaces chamam casos de uso; não implementam regra de negócio nem persistência.
5. `use_cases.py` orquestra operações, mas delega regras puras a `model.py` e I/O a `services.py`.
6. Chamadas HTTP, disco e ambiente ficam em `services.py`.
7. `model.py` permanece puro e independente de Tkinter, argparse ou outro framework.
8. `shared` não depende de nenhuma feature.
9. Não adicionar dependência de runtime enquanto a stdlib resolver.
10. Não colocar credenciais no código.
11. Tratar estados observáveis de sucesso, vazio, validação, processamento e erro.
12. Não bloquear o loop de eventos da GUI com rede, disco pesado ou processamento demorado.
13. Toda mudança de comportamento considera testes.
14. Toda decisão relevante atualiza a documentação ou gera um ADR.

## Interfaces

### CLI

A composição raiz usa `argparse`. Cada feature registra seus comandos por um adaptador `commands.py`. A entrada `python -m app_template` continua abrindo a CLI por compatibilidade.

### GUI

A composição raiz `gui.py` carrega Tkinter apenas quando a janela é criada. Cada feature fornece seu próprio painel ou componente em `features/<nome>/gui.py`. A interface gráfica chama os mesmos casos de uso da CLI.

Tkinter mantém o template sem dependência Python de runtime. Algumas distribuições Linux exigem instalar o pacote Tk do sistema. Trocar o toolkit gráfico é uma decisão arquitetural e deve ser registrada.

## Processamento demorado

Callbacks gráficos devem retornar rapidamente. Para rede, arquivos grandes ou CPU intensiva, executar o trabalho fora do loop de eventos e publicar o resultado de volta com o mecanismo seguro do toolkit. Nunca atualizar widgets diretamente a partir de uma thread de trabalho.

## Acesso a APIs e disco

Todo acesso externo passa por `services.py`. Casos de uso chamam o serviço; adaptadores de CLI e GUI recebem apenas resultados ou erros que possam apresentar ao usuário. Ver [integrations.md](integrations.md).

## Type hints e qualidade

Todo código usa type hints e passa no mypy estrito. Ruff cuida de formatação e lint. As checagens fazem parte de `python scripts/dev.py validate`.

## Testes

A suíte padrão não depende de display. Model e casos de uso são testados diretamente; entradas e controladores GUI usam janelas falsas ou dependências injetadas. Detalhes em [testing.md](testing.md).

## Empacotamento e build

O pacote wheel/sdist inclui ambas as interfaces. O PyInstaller gera um executável CLI ou GUI por sistema operacional; a GUI usa modo windowed, sem console. Veja [building.md](building.md).

## Evolução incremental

Manter apenas as interfaces aprovadas para o produto. Adicionar framework, camada ou toolkit somente quando uma necessidade concreta justificar, registrando a decisão em `docs/decisions/`.
