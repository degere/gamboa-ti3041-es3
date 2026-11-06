from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),

    # Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/incrementar/<int:producto_id>/', views.incrementar_carrito, name='incrementar_carrito'),
    path('carrito/decrementar/<int:producto_id>/', views.decrementar_carrito, name='decrementar_carrito'),
    path('carrito/quitar/<int:producto_id>/', views.quitar_carrito, name='quitar_carrito'),
    path('carrito/comprar/', views.comprar, name='comprar'),

    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='Ferreteria/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
]