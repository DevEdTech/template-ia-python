---
name: design-interface
description: Projeta a experiência de uma interface de CLI ou GUI deste projeto — argumentos, códigos de saída, mensagens de erro acionáveis, estados de tela e resposta sob carga; use antes de implementar interface nova ou ao revisar uma que frustra o usuário. Não use para regra de negócio nem para escolher toolkit gráfico, que é decisão arquitetural e exige ADR.
---

# Projetar interface

## Finalidade

Decidir como a pessoa interage com a aplicação antes de escrever a interface,
de forma que o resultado seja verificável: cada decisão vira comportamento
observável e testável.

## Quando usar

- Antes de implementar um comando de CLI ou uma tela de GUI.
- Ao revisar uma interface que confunde ou frustra quem usa.
- Quando os estados de erro não estão claros.

## Quando não usar

- Para regra de negócio: ela fica em `model.py`, não na interface.
- Para trocar o toolkit gráfico: é decisão arquitetural, exige ADR em
  `docs/decisions/` e o template não assume nenhuma dependência de runtime.

## Processo

1. Leia o `AGENTS.md` e confirme quais interfaces este projeto tem
   (`python scripts/dev.py show-profile`). Projetar GUI em um projeto `cli` é
   trabalho descartado.
2. Nomeie a tarefa do usuário em uma frase: o que ele quer terminar.
3. Liste as entradas necessárias e quais têm padrão razoável. Toda entrada sem
   padrão é uma pergunta que a interface precisa fazer.
4. Defina os estados observáveis: sucesso, vazio, validação, processando e
   erro. Interface sem estado de erro declarado é interface que mente.
5. Escreva as mensagens de erro: o que aconteceu, por quê e como consertar.
6. Defina o comportamento sob demora: o que o usuário vê enquanto espera.
7. Liste as decisões em uma tabela de entrada → saída observável, para virar
   teste.

## Decisões de CLI

- `--help` e `-h` sempre existem e descrevem cada argumento.
- `0` para sucesso; diferente de zero para falha (`2` para erro de uso).
- Erro vai para `stderr`, resultado para `stdout`: quem redireciona a saída
  precisa receber só o resultado.
- Sem cor nem barra de progresso obrigatórias — degrade quando a saída não for
  um terminal.
- Operação destrutiva pede confirmação, ou exige `--yes` explícito.

## Decisões de GUI

- O toolkit é Tkinter, da biblioteca padrão. Trocar exige ADR.
- O callback retorna rápido: trabalho demorado sai do loop de eventos e o
  resultado volta pelo mecanismo seguro do toolkit, nunca atualizando widget
  de uma thread de trabalho.
- Toda espera tem indicação visível de progresso.
- Controles relacionados ficam agrupados, com espaçamento e fonte legíveis.
- A janela sobrevive a redimensionamento, com `grid` ou `pack` configurados.
- Diagnóstico vai para o logger: um executável em modo windowed não tem
  terminal.

## Resultado esperado

- A tarefa do usuário em uma frase.
- Entradas, com padrões e perguntas.
- Tabela de estados observáveis e o que cada um mostra.
- Textos das mensagens de erro.
- Comportamento sob demora.
- Lista de casos para `generate-tests`.
