from django.urls import path
from .import views

urlpatterns = [ 
    path('inicio', views.cargarInicio, name='inicio'),
    path('carrito', views.cargarCarrito, name='carrito'),
    path('detalle', views.cargarDetalle, name='detalle'),
    path('lista', views.cargarLista, name='lista'),
    path('boleta', views.cargarBoleta, name='boleta'),
    path('categoria', views.lista_categorias, name='categoria'),
    path('listaProductos', views.lista_productos, name='listaProductos'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]