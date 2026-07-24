# ============================================================================
# FEATURE DE EXEMPLO
#
# Esta pasta (`features/example`) existe apenas para demonstrar a estrutura e as
# convencoes do template (model / services / commands + __init__ como interface
# publica). Ela DEVE SER REMOVIDA ou RENOMEADA durante o setup do seu projeto.
#
# Regras respeitadas aqui e que valem para toda feature:
# - Outras features NAO importam arquivos internos desta (so este __init__.py).
# - A interface publica da feature e exposta exclusivamente por este arquivo.
# ============================================================================
"""Feature de exemplo: um contador persistente exposto como subcomando da CLI."""

from app_template.features.example.commands import register_example_commands
from app_template.features.example.model import MIN_COUNT, decrement, increment

__all__ = ["MIN_COUNT", "decrement", "increment", "register_example_commands"]
