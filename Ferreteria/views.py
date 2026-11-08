from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from .models import Producto
from .forms import RegistroForm, ProductoForm



def home(request):
    destacados = Producto.objects.filter(stock__gt=0).order_by('-precio')[:6]
    return render(request, 'Ferreteria/home.html', {'destacados': destacados})



def catalogo(request):
    productos = Producto.objects.all().order_by('id')
    return render(request, 'Ferreteria/catalogo.html', {'productos': productos})


# ---------- CRUD de productos (solo personal del sitio) ----------

def es_staff(user):
    return user.is_authenticated and user.is_staff


solo_staff = user_passes_test(es_staff, login_url='login')


@solo_staff
def producto_crear(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f"Producto \"{producto.nombre}\" creado correctamente.")
            return redirect('catalogo')
    else:
        form = ProductoForm()
    return render(request, 'Ferreteria/producto_form.html', {'form': form, 'titulo': 'Nuevo producto'})


@solo_staff
def producto_editar(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f"Producto \"{producto.nombre}\" actualizado.")
            return redirect('catalogo')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'Ferreteria/producto_form.html',
                  {'form': form, 'titulo': 'Editar producto', 'producto': producto})


@solo_staff
def producto_eliminar(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f"Producto \"{nombre}\" eliminado.")
        return redirect('catalogo')
    # GET: pantalla de confirmación antes de borrar
    return render(request, 'Ferreteria/producto_confirmar_eliminar.html', {'producto': producto})


def registro(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"¡Bienvenido, {user.username}! Tu cuenta fue creada.")
            return redirect('catalogo')
    else:
        form = RegistroForm()

    return render(request, 'Ferreteria/registro.html', {'form': form})



def _carrito(request):
    return request.session.get('carrito', {})


def _guardar_carrito(request, carrito):
    request.session['carrito'] = carrito
    request.session.modified = True


def _safe_next(request, default='catalogo'):
    """Devuelve la URL a la que volver, validando que sea interna."""
    next_url = request.GET.get('next') or request.POST.get('next') or ''
    if next_url.startswith('/'):
        return next_url
    return default



def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    carrito = _carrito(request)
    key = str(producto_id)
    cantidad = carrito.get(key, 0)

    if cantidad + 1 > producto.stock:
        messages.error(request, f"No hay más stock disponible de {producto.nombre}.")
    else:
        carrito[key] = cantidad + 1
        _guardar_carrito(request, carrito)
        messages.success(request, f"{producto.nombre} agregado al carrito.")

    return redirect(_safe_next(request))


def incrementar_carrito(request, producto_id):
    return agregar_carrito(request, producto_id)


def decrementar_carrito(request, producto_id):
    carrito = _carrito(request)
    key = str(producto_id)
    if key in carrito:
        if carrito[key] > 1:
            carrito[key] -= 1
        else:
            del carrito[key]
        _guardar_carrito(request, carrito)
    return redirect(_safe_next(request, default='ver_carrito'))


def quitar_carrito(request, producto_id):
    carrito = _carrito(request)
    carrito.pop(str(producto_id), None)
    _guardar_carrito(request, carrito)
    messages.info(request, "Producto eliminado del carrito.")
    return redirect(_safe_next(request, default='ver_carrito'))


def ver_carrito(request):
    carrito = _carrito(request)
    items = []
    total = 0
    for pid, cant in carrito.items():
        try:
            p = Producto.objects.get(pk=int(pid))
        except Producto.DoesNotExist:
            continue
        subtotal = p.precio * cant
        total += subtotal
        items.append({'producto': p, 'cantidad': cant, 'subtotal': subtotal})

    return render(request, 'Ferreteria/carrito.html', {'items': items, 'total': total})



@login_required
@transaction.atomic
def comprar(request):
    if request.method != 'POST':
        return redirect('ver_carrito')

    carrito = _carrito(request)

    # Descarta del carrito productos que ya fueron eliminados del catálogo
    existentes = set(str(pk) for pk in Producto.objects.filter(pk__in=[int(k) for k in carrito]).values_list('pk', flat=True))
    carrito = {k: v for k, v in carrito.items() if k in existentes}
    _guardar_carrito(request, carrito)

    if not carrito:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('catalogo')

    errores = []
    for pid, cant in carrito.items():
        p = Producto.objects.select_for_update().get(pk=int(pid))
        if p.stock < cant:
            errores.append(f"{p.nombre}: solo quedan {p.stock} unidades.")

    if errores:
        for e in errores:
            messages.error(request, e)
        return redirect('ver_carrito')


    for pid, cant in carrito.items():
        Producto.objects.filter(pk=int(pid)).update(stock=F('stock') - cant)

 
    _guardar_carrito(request, {})
    messages.success(request, "¡Compra realizada con éxito! El stock fue actualizado.")
    return redirect('catalogo')