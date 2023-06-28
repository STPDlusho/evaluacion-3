from django.contrib import admin
from .models import * 
# Register your models here.
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Boleta)
admin.site.register(DetalleBoleta)