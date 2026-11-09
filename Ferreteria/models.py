from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=500)
    categoria = models.CharField(max_length=50)
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    imagen = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre


class ConsultaCliente(models.Model):
    """Consulta enviada por un cliente desde el formulario de contacto."""
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    mensaje = models.TextField()
    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consultas',
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'consulta de cliente'
        verbose_name_plural = 'consultas de clientes'

    def __str__(self):
        return f"{self.nombre} ({self.correo})"
