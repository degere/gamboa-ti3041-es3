from django.db.models import Count

from .models import Producto


def navegacion(request):
    """Categorías (con su cantidad de productos) disponibles en todas las páginas."""
    categorias = (
        Producto.objects.values('categoria')
        .annotate(total=Count('id'))
        .order_by('categoria')
    )
    return {'categorias': list(categorias)}
