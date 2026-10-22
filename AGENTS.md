# Instruções do projeto

## Perfil deste projeto

O perfil e as capacidades ficam em `.template-state.json` e decidem o que vale
aqui. Veja o estado atual com:

```bash
python scripts/dev.py show-profile
```

- **Perfil** (`prototipo` | `padrao` | `rigoroso`): define o que bloqueia e o
  que apenas avisa. Em `prototipo`, só arquitetura, lint, tipos e testes
  bloqueiam.
- **Capacidades**: o que o projeto usa. `cli` e `gui` vêm da escolha de
  interface feita no setup; uma interface removida não existe mais no disco, e
  as regras dela não se aplicam.

Uma regra abaixo que mencione capacidade desligada não se aplica. Na dúvida,
`show-profile` é a fonte da verdade, não este texto.

## Leia primeiro

1. README.md
2. docs/architecture.md
3. docs/development-process.md
4. docs/testing.md
5. docs/building.md

## Processo

Sempre, qualquer que seja o tamanho da mudança:

1. Entenda a solicitação e os critérios de aceite.
2. Inspecione os arquivos relevantes e os testes existentes.
3. Mantenha as alterações dentro do escopo solicitado.
4. Adicione ou atualize testes para mudanças de comportamento.
5. Execute `python scripts/dev.py validate` (ou `validate --changed` ao
   iterar).
6. Revise o diff final.

Para mudança que afeta vários arquivos, cria funcionalidade, altera
arquitetura ou integra serviço externo, acrescente:

7. Apresente um plano antes de escrever código (`plan-feature`).
8. Atualize a documentação afetada.
9. Registre a evidência da entrega em `docs/entregas`.

Correção pontual, ajuste de texto e mudança de uma linha param no passo 6:
plano, documentação e registro de entrega existem para trabalho que muda o
entendimento do projeto, não para toda edição.

## Arquitetura

- Organize as capacidades do produto em `src/<pacote>/features`.
- Não importe módulos internos de outra feature.
- Use a interface pública das features (o `__init__.py` de cada uma).
- Mantenha a lógica de negócio em `model.py` e a orquestração compartilhada em `use_cases.py`.
- Mantenha APIs externas e persistência atrás de serviços (`services.py`).
- Isole adaptações de interface: `commands.py` para CLI e `gui.py` para GUI
  (apenas as interfaces que este projeto tem).
- Mantenha as composições `src/<pacote>/cli.py` e `src/<pacote>/gui.py` sem
  regra de negócio.
- Mantenha `shared` neutro em relação ao domínio.
- Não adicione abstrações sem necessidade demonstrada.

## Escopo

- Não expanda o escopo além do solicitado.
- Uma funcionalidade por vez.

## Dependências

- Não adicione dependências sem explicar a necessidade.
- Prefira a biblioteca padrão (stdlib) e dependências já existentes.
- O template começa com zero dependências de runtime — mantenha assim quando possível.

## Segurança

- Nunca faça commit de segredos.

## Qualidade de código

- Todo código novo tem type hints e passa no mypy em modo estrito.
- Formatação e lint são feitos pelo Ruff (`python scripts/dev.py format` / `lint`).
- Funções e módulos públicos têm docstrings claras.
- Prefira `pathlib` a manipulação de strings de caminho.
- Escreva código portável entre Windows, macOS e Linux.
- Com a capacidade `gui`: não bloqueie o loop de eventos com I/O ou
  processamento demorado.

## Persistência e APIs

- Acesso a disco, rede ou variáveis de ambiente fica em `services.py`.
- `model.py` permanece puro: sem I/O, fácil de testar.

## Testes

- Toda mudança de comportamento deve considerar testes (pytest).
- Teste o resultado observável, não os detalhes internos.
- Com a capacidade `gui`: teste com casos de uso, controladores ou janelas
  falsas; não dependa de display real na suíte padrão.
- O limite de cobertura vem do perfil (`show-profile`); não o reduza para
  fazer passar, e não escreva teste de caso impossível para subir o número.
- Não coloque lógica em `build_window` nem em `create_*_panel`: construção de
  widget não é testável sem display real, então a lógica ali fica sem rede de
  segurança. Por isso elas também são excluídas da medição — a exclusão é
  consequência da regra, não o motivo dela.
- Ao iterar, `python scripts/dev.py validate --changed` roda só os testes que
  cobrem o que você mexeu e o que depende disso.

## Erros e diagnóstico

- Com a capacidade `cli`: erros em `stderr` e código de saída diferente de
  zero; não use o logger para falar com o usuário.
- Com a capacidade `gui`: use o logger, porque um executável em modo windowed
  não tem terminal.

## Documentação

- Toda decisão relevante atualiza a documentação ou gera um ADR.
- Toda entrega implementada gera um registro em `docs/entregas`, com
  funcionalidades, testes e o resultado real das validações.
- Mudança que cria ou revoga uma regra atualiza este `AGENTS.md`.

## Conclusão

Uma tarefa só está concluída quando todos os itens da definição de
concluído estiverem satisfeitos. A lista fica em
`docs/development-process.md` e é a única fonte da verdade.
