from django.urls import path
from .import views

urlpatterns = [ 
    path('', views.cargarInicio),
    path('carro', views.cargarCarrito),
    path('detalle', views.cargarDetalle),
    path('lista', views.cargarLista),
    path('boleta', views.cargarBoleta),
    path('categoria', views.lista_categorias),
    path('listaProductos', views.lista_productos)
]