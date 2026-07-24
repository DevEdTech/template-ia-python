# Testes

## Filosofia

Testamos o **comportamento observável** da aplicação: o que entra e o que sai. Não testamos detalhes internos de implementação. Um bom teste continua passando mesmo que você reorganize o código por dentro, desde que o comportamento continue o mesmo.

## Ferramenta

Usamos **pytest**. A configuração está em `pyproject.toml` (`[tool.pytest.ini_options]`), com `pythonpath = ["src"]` para que os testes importem o pacote sem instalação extra.

## Tipos de teste

- **Unidade**: funções e lógica isoladas — principalmente o `model.py` (puro e determinístico).
- **Comportamento (end-to-end da CLI)**: exercitam o ponto de entrada real (`main`), do parsing dos argumentos até o efeito observável (saída no terminal, arquivo persistido).

## Localização

Os testes ficam em `tests/`, espelhando a estrutura das features:

```
tests/
├── conftest.py               # fixtures compartilhadas e neutras
└── features/
    └── minha-feature/
        ├── test_model.py     # lógica pura
        └── test_commands.py  # comportamento da CLI
```

> **Por que fora de `src/`?** No layout `src/`, manter os testes separados evita que eles entrem no pacote distribuído e força os testes a importarem o código como um usuário faria.

## Comandos

```bash
python scripts/dev.py test        # roda os testes uma vez
python scripts/dev.py test-cov    # roda medindo cobertura
```

Você também pode passar argumentos direto ao pytest:

```bash
python scripts/dev.py test -k nome_do_teste -v
```

## Isolamento de I/O

Testes não devem tocar em dados reais do usuário. Use `tmp_path` e `monkeypatch` do pytest para redirecionar a persistência. O template já traz a fixture `isolated_data_dir` (em `tests/conftest.py`), que aponta o diretório de dados para uma pasta temporária.

## Exemplo curto

```python
from app_template.cli import main


def test_up_incrementa(isolated_data_dir, capsys):
    assert main(["count", "up"]) == 0
    assert capsys.readouterr().out.strip() == "1"
```

O foco é no que a aplicação produz, não em como o código foi escrito por dentro.

## O que NÃO testar

- Estado interno ou nomes de variáveis.
- Detalhes de implementação de bibliotecas de terceiros.
- Casos impossíveis só para "aumentar cobertura".

## Investigar falhas

1. Leia a mensagem de erro: o pytest indica o que era esperado e o que aconteceu.
2. Rode um teste específico com `-k` e `-v` para focar.
3. Se um teste falha após uma mudança de comportamento intencional, atualize o teste para o novo comportamento esperado.
4. Se a falha for inesperada, corrija o código, não o teste.
