from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=500)
    categoria = models.CharField(max_length=50)
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    imagen = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre