from django.shortcuts import render, redirect
from .models import * 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


# Create your views here.
def cargarInicio(request):
    return render(request,'inicio.html')

def cargarCarrito (request):
    return render (request, 'carrito.html')

def cargarDetalle(request):
    return render (request, 'detalle_producto.html')

def cargarLista(request):
    return render (request, 'lista_productos.html')

def cargarBoleta(request):
    return render(request, 'boleta_confirmacion')


def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        Categoria.objects.create(nombre=nombre)
        return redirect('lista_categorias.html')
    return render(request, 'crear_categoria.html')

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'lista_categorias.html', {'categorias': categorias})

def editar_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    if request.method == 'POST':
        nombre = request.POST['nombre']
        categoria.nombre = nombre
        categoria.save()
        return redirect('lista_categorias')
    return render(request, 'editar_categoria.html', {'categoria': categoria})

def eliminar_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    categoria.delete()
    return redirect(request, 'lista_categorias')

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})

def detalle_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})

def agregar_carrito(request, producto_id):
    producto = Producto.objects.get(id=producto_id)

    # Obtener o crear el carrito de compras del usuario
    if 'carrito' not in request.session:
        request.session['carrito'] = []

    carrito = request.session['carrito']

    # Verificar si el producto ya está en el carrito
    for item in carrito:
        if item['producto_id'] == producto.id:
            # El producto ya está en el carrito, aumentar la cantidad
            item['cantidad'] += 1
            break
    else:
        # El producto no está en el carrito, agregarlo
        carrito.append({
            'producto_id': producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'cantidad': 1,
            'total': producto.precio
        })

    request.session.modified = True

    return redirect('ver_carrito')

def ver_carrito(request):
    if 'carrito' not in request.session:
        request.session['carrito'] = []

    carrito = request.session['carrito']
    total_carrito = 0

    for item in carrito:
        item['subtotal'] = item['precio'] * item['cantidad']
        total_carrito += item['subtotal']

    return render(request, 'carrito.html', {'carrito': carrito, 'total_carrito': total_carrito})

def finalizar_compra(request):
    if 'carrito' not in request.session:
        return redirect('ver_carrito')

    # Obtener los productos del carrito
    carrito = request.session['carrito']

    # Crear una nueva boleta
    boleta = Boleta.objects.create(id_cliente=request.user.cliente, total=0)

    total_general = 0

    # Crear los detalles de la boleta
    for item in carrito:
        producto = Producto.objects.get(id=item['producto_id'])
        subtotal = item['subtotal']

        DetalleBoleta.objects.create(
            id_producto=producto,
            id_boleta=boleta,
            precio=item['precio'],
            cantidad=item['cantidad'],
            total=subtotal
        )

        total_general += subtotal

    # Actualizar el total de la boleta
    boleta.total = total_general
    boleta.save()

    # Limpiar el carrito de compras
    del request.session['carrito']

    return redirect('boleta_confirmacion')

def register_view(request):
    if request.method == 'POST':
        # Obtén los datos del formulario
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Verifica si las contraseñas coinciden
        if password1 != password2:
            error_message = 'Las contraseñas no coinciden.'
            return render(request, 'register.html', {'error_message': error_message})

        # Verifica si el nombre de usuario ya está en uso
        if User.objects.filter(username=username).exists():
            error_message = 'El nombre de usuario ya está en uso.'
            return render(request, 'register.html', {'error_message': error_message})

        # Crea el usuario
        user = User.objects.create_user(username=username, password=password1, email=email)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Inicia sesión automáticamente después de crear la cuenta
        login(request, user)

        # Redirige al usuario a la página principal
        return redirect('inicio')

    return render(request, 'registration/register.html')


def login_view(request):
    if request.method == 'POST':
        # Obtén los datos del formulario
        username = request.POST['username']
        password = request.POST['password']

        # Autentica al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Inicia sesión si el usuario es autenticado correctamente
            login(request, user)
            return redirect('inicio')
        else:
            error_message = 'Nombre de usuario o contraseña incorrectos.'
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'registration/login.html')






