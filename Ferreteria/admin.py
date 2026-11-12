from django.contrib import admin
from .models import Producto, ConsultaCliente

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'imagen')
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria',)


@admin.register(ConsultaCliente)
class ConsultaClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'producto', 'fecha', 'solucionado')
    list_filter = ('fecha', 'producto__categoria', 'solucionado')
    search_fields = ('nombre', 'correo', 'mensaje')
    readonly_fields = ('fecha',)

