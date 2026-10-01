from .content import EMPRESA, SOLUCOES


def empresa(request):
    """Disponibiliza dados da empresa e das soluções em todos os templates."""
    return {"empresa": EMPRESA, "menu_solucoes": SOLUCOES}
