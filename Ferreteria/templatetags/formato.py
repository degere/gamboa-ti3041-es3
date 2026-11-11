from django import template

register = template.Library()


@register.filter
def clp(valor):
    """Formatea un número como pesos chilenos: 11875 -> $11.875"""
    try:
        return "$" + f"{int(valor):,}".replace(",", ".")
    except (TypeError, ValueError):
        return valor
