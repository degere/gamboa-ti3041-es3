from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'imagen')
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria',)