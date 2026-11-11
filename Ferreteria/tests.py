from django.test import TestCase, Client
from django.urls import reverse

from .models import Producto, ConsultaCliente
from .templatetags.formato import clp


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


class FormatoPreciosTests(TestCase):
    def test_clp_agrega_puntos_de_miles(self):
        self.assertEqual(clp(475), '$475')
        self.assertEqual(clp(11875), '$11.875')
        self.assertEqual(clp(1234567), '$1.234.567')


class CatalogoFiltrosTests(TestCase):
    """Buscador, filtro por categoría, solo con stock y orden del catálogo."""

    def setUp(self):
        Producto.objects.create(nombre='Martillo', categoria='Herramientas', precio=11875, stock=15)
        Producto.objects.create(nombre='Taladro', categoria='Electricidad', precio=42750, stock=0)
        Producto.objects.create(nombre='Cable', categoria='Electricidad', precio=11685, stock=20)

    def nombres(self, **parametros):
        r = self.client.get(reverse('catalogo'), parametros)
        return [p.nombre for p in r.context['productos']]

    def test_busqueda_por_nombre(self):
        self.assertEqual(self.nombres(q='marti'), ['Martillo'])

    def test_filtro_por_categoria(self):
        self.assertCountEqual(self.nombres(categoria='Electricidad'), ['Taladro', 'Cable'])

    def test_solo_con_stock_oculta_agotados(self):
        self.assertNotIn('Taladro', self.nombres(stock='1'))

    def test_catalogo_muestra_las_categorias_como_opciones(self):
        r = self.client.get(reverse('catalogo'))
        self.assertContains(r, 'cat-chips')
        self.assertContains(r, '?categoria=Electricidad')

    def test_las_categorias_no_aparecen_fuera_del_catalogo(self):
        r = self.client.get(reverse('contacto'))
        self.assertNotContains(r, 'cat-chips')
        self.assertNotContains(r, '?categoria=Electricidad')

    def test_orden_por_precio_descendente(self):
        self.assertEqual(self.nombres(orden='precio_desc'), ['Taladro', 'Martillo', 'Cable'])


class InicioYAutenticacionTests(TestCase):
    """Inicio solo ofrece iniciar sesión; el registro se alcanza desde el login."""

    def test_inicio_anonimo_ofrece_iniciar_sesion_pero_no_registro(self):
        r = self.client.get(reverse('home'))
        self.assertContains(r, reverse('login'))
        self.assertNotContains(r, reverse('registro'))

    def test_login_ofrece_enlace_a_registro(self):
        r = self.client.get(reverse('login'))
        self.assertContains(r, reverse('registro'))

    def test_inicio_incluye_carruseles(self):
        Producto.objects.create(nombre='Martillo', categoria='Herramientas', precio=11875, stock=15)
        r = self.client.get(reverse('home'))
        self.assertContains(r, 'data-hero')
        self.assertContains(r, 'data-carrusel')

