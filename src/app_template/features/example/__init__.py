# ============================================================================
# FEATURE DE EXEMPLO
#
# Esta pasta (`features/example`) existe apenas para demonstrar a estrutura e as
# convencoes do template. Ela DEVE SER REMOVIDA ou RENOMEADA durante o setup.
#
# Regras respeitadas aqui e que valem para toda feature:
# - Outras features NAO importam arquivos internos desta (so este __init__.py).
# - Model e puro; services concentra I/O; use_cases orquestra ambos.
# - Adaptadores de CLI e GUI apenas traduzem interacoes da interface.
# ============================================================================
"""Feature de exemplo: contador persistente compartilhado por CLI e GUI."""

from app_template.features.example.commands import register_example_commands
from app_template.features.example.gui import create_example_panel
from app_template.features.example.model import MIN_COUNT, decrement, increment
from app_template.features.example.use_cases import (
    decrease_count,
    get_count,
    increase_count,
)

__all__ = [
    "MIN_COUNT",
    "create_example_panel",
    "decrease_count",
    "decrement",
    "get_count",
    "increase_count",
    "increment",
    "register_example_commands",
]
