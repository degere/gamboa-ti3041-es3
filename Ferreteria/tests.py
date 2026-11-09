from django.test import TestCase, Client
from django.urls import reverse

from .models import Producto, ConsultaCliente


class ConsultaFormularioTests(TestCase):
    """Formulario de contacto: validaciones, guardado en BD y CSRF."""

    def datos(self, **cambios):
        datos = {
            'nombre': 'Juan Pérez',
            'correo': 'juan@ejemplo.cl',
            'mensaje': 'Quisiera cotizar 20 metros de cable.',
        }
        datos.update(cambios)
        return datos

    def test_consulta_valida_se_guarda_y_confirma(self):
        r = self.client.post(reverse('contacto'), self.datos(), follow=True)
        self.assertEqual(ConsultaCliente.objects.count(), 1)
        self.assertContains(r, 'Recibimos tu consulta')

    def test_producto_de_interes_es_opcional_y_se_asocia(self):
        p = Producto.objects.create(nombre='Taladro', categoria='Electricidad', precio=42750, stock=7)
        self.client.post(reverse('contacto'), self.datos(producto=p.id))
        self.assertEqual(ConsultaCliente.objects.get().producto, p)

    def test_correo_invalido_se_rechaza(self):
        r = self.client.post(reverse('contacto'), self.datos(correo='no-es-un-correo'))
        self.assertIn('correo', r.context['form'].errors)
        self.assertEqual(ConsultaCliente.objects.count(), 0)

    def test_campos_vacios_se_rechazan(self):
        r = self.client.post(reverse('contacto'), {'nombre': '', 'correo': '', 'mensaje': ''})
        errores = r.context['form'].errors
        for campo in ('nombre', 'correo', 'mensaje'):
            self.assertIn(campo, errores)
        self.assertEqual(ConsultaCliente.objects.count(), 0)

    def test_mensaje_muy_corto_se_rechaza(self):
        r = self.client.post(reverse('contacto'), self.datos(mensaje='hola'))
        self.assertIn('mensaje', r.context['form'].errors)
        self.assertEqual(ConsultaCliente.objects.count(), 0)

    def test_formulario_incluye_token_csrf(self):
        r = self.client.get(reverse('contacto'))
        self.assertContains(r, 'csrfmiddlewaretoken')

    def test_post_sin_token_csrf_es_rechazado(self):
        cliente = Client(enforce_csrf_checks=True)
        r = cliente.post(reverse('contacto'), self.datos())
        self.assertEqual(r.status_code, 403)
        self.assertEqual(ConsultaCliente.objects.count(), 0)


class SesionProductosVisitadosTests(TestCase):
    """Sesión: se guardan los últimos 3 productos visitados, sin repetidos."""

    def setUp(self):
        self.productos = [
            Producto.objects.create(nombre=f'Producto {i}', categoria='Prueba', precio=1000, stock=5)
            for i in range(4)
        ]

    def visitar(self, producto):
        self.client.get(reverse('producto_detalle', args=[producto.id]))

    def test_guarda_solo_los_ultimos_tres_sin_repetir(self):
        p0, p1, p2, p3 = self.productos
        for p in (p0, p1, p2, p3, p1):
            self.visitar(p)
        self.assertEqual(self.client.session['visitados'], [p1.id, p3.id, p2.id])

    def test_catalogo_muestra_vistos_recientemente(self):
        self.visitar(self.productos[0])
        r = self.client.get(reverse('catalogo'))
        self.assertContains(r, 'Vistos recientemente')
