from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView, CreateView
from django.db.models import Q
from .forms import *
import json
from django.http import  JsonResponse
from django.contrib.auth.models import User
IVA_PERCENTAGE = 0.19
from django.db import IntegrityError


# Create your views here.
def index(request):
    carrusel = Carrucel.objects.all()
    categoria = Categorias.objects.exclude(imagen='')
    nosotros = Nosotros.objects.first()  # Obtén el primer registro de la tabla
    productos_en_tendencia = Productos.objects.filter(tendencia=True)
    productos_normales = Productos.objects.filter(tendencia=False)

    data = {
        'carrusel': carrusel,
        'categoria': categoria,
        'productos_en_tendencia': productos_en_tendencia,
        'productos_normales': productos_normales,
        'mostrar_mapa': True,  # Agrega esta variable al contexto
        'nosotros':nosotros,

    }
    return render(request, 'index.html', data)




# Listar productos por categoria
def productoxCategoria(request, id):
    busqueda = request.POST.get("buscador")
    productos_normales = Productos.objects.filter(categoria=id, tendencia=False)
    
    if busqueda:
        productos_normales = productos_normales.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        ).distinct()

    if id:
        productos_en_tendencia = Productos.objects.filter(categoria=id, tendencia=True)
        if productos_en_tendencia.exists():
            titulo_tendencia = 'Productos en Tendencia'
        else:
            titulo_tendencia = 'Productos Normales'
    else:
        productos_en_tendencia = Productos.objects.filter(tendencia=True)
        titulo_tendencia = 'Productos en Tendencia'

    data = {
        'titulo_tendencia': titulo_tendencia,
        'productos_en_tendencia': productos_en_tendencia,
        'productos_normales': productos_normales
    }
    return render(request, 'index.html', data)


# views productos
def detalleProducto(request, id):
    product = get_object_or_404(Productos, id=id)
    otrosProductos = Productos.objects.filter(categoria=product.categoria)
    comentarios = Comentario.objects.filter(producto=product)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.producto = product
            comentario.save()
            return redirect('veterinaria:detalleproducto', id=id)
    else:
        form = ComentarioForm()

    data = {
        'producto': product,
        'productosRelacionados': otrosProductos,
        'comentarios': comentarios,
        'form': form,
    }
    return render(request, 'producto/detalle.html', data)




@login_required(login_url='/login')
def addProducto(request):
    data = {
        'form': ProductoForm(),
        'categorias': Categorias.objects.all(),
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Registro agregado correctamente")
            return redirect(to="/listarproductos")
        else:
            data["form"] = formulario

    return render(request, 'producto/agregar.html', data)


@login_required(login_url='/login')
def listarProductos(request):
    busqueda = request.POST.get("buscador")
    lista_productos = Productos.objects.order_by('nombre')
    page = request.GET.get('page', 1)
    if busqueda:
        lista_productos = Productos.objects.filter(
            Q(nombre__icontains = busqueda) |
            Q(descripcion__icontains = busqueda)
        ).distinct()

    try:
        paginator = Paginator(lista_productos, 6)
        lista_productos = paginator.page(page)
    except:
        raise Http404

    data = {'entity': lista_productos,
            'title': 'LISTADO DE PRODUCTOS',
            'paginator': paginator
            }
    return render(request, 'producto/listar.html', data)


@login_required(login_url='/login')
def editarProducto(request, id):
    producto = get_object_or_404(Productos, id=id)
    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Registro modificado correctamente")
            return redirect(to="/listarproductos")
        data["form"] = formulario
    return render(request, 'producto/modificar.html', data)


@login_required(login_url='/login')
def deleteProducto(request, id):
    producto = get_object_or_404(Productos, id=id)
    producto.delete()
    messages.success(request, "Registro eliminado correctamente")
    return redirect(to="/listarproductos")

def nosotros(request):
    return render(request, 'nosotros.html')

# Views categorias
@login_required(login_url='/login')
def listCategorias(request):
    lista_categorias = Categorias.objects.all().order_by('nombre')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(lista_categorias, 4)
        lista_categorias = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': lista_categorias,
        'title': 'LISTADO DE CATEGORIAS',
        'paginator': paginator
    }

    return render(request, 'categoria/categorias.html', data)


@login_required(login_url='/login')
def addCategoria(request):
    data = {
        'form': CategoriaForm()
    }
    if request.method == 'POST':
        formulario = CategoriaForm(data=request.POST, files=request.FILES)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Registro agregado correctamente")
            return redirect(to="/categorias")
        else:
            data["form"] = formulario
    return render(request, 'categoria/agregar.html', data)


@login_required(login_url='/login')
def modificarCategoria(request, id):
    categoria = get_object_or_404(Categorias, id=id)

    data = {
        'form': CategoriaForm(instance=categoria)
    }
    if request.method == 'POST':
        formulario = CategoriaForm(data=request.POST, instance=categoria)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Registro modificado correctamente")
            return redirect(to="/categorias")
        else:
            data["form"] = formulario

    return render(request, 'categoria/modificar.html', data)


@login_required(login_url='/login')
def deleteCategoria(request, id):
    categoria = get_object_or_404(Categorias, id=id)
    productos = Productos.objects.filter(categoria=categoria)
    productos.delete()
    categoria.delete()
    messages.success(request, "Registro eliminado correctamente")
    return redirect(to="/categorias")

def contacto(request):
    data = {
        'form': ConctactoForm()
    }

    if request.method == 'POST':
        formulario = ConctactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Gracias por su mensaje")
        else:
            data["form"] = formulario
    return render(request, 'contacto/contacto.html', data)

def mostrar_contacto(request):
    contacto = Contacto.objects.all()
    m = {'contacto': contacto ,
        'title': 'MOSTRAR Contactos',
        }
    return render(request, 'contacto/mostrar.html',m)

def detalle_contacto(request, id):
    contacto = get_object_or_404(Contacto, id=id)
    data = {
        'contacto': contacto,
    }
    return render(request, 'contacto/detalle.html', data)

@login_required(login_url='/login')
def eliminar_contacto(request, id):
    contacto = get_object_or_404(Contacto, id=id)
    contacto.delete()
    messages.success(request, "Registro eliminado correctamente")
    return redirect(to="/listarcontacto")


def registrar(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, 'Usuario registrado correctamente')
            return redirect('/')
        else:
            data['form'] = formulario
    
    return render(request, 'auth/registrar.html', data)


# ============================ PANEL ============================

def change(request, username=None):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        password = request.POST.get('password')
        user.set_password(password)
        user.save()
        messages.success(request, 'Su Contraseña se Cambiado Correctamente ')
        return redirect('/')
    else:
        data = {'username': username}
        return render(request, 'change.html', data)



def usuario_administrar (request):
    users = User.objects.all()

    data = {
            'title': 'LISTADO DE PERSONAS INGRESADAS AL SISTEMA',
            'users': users
            }
    return render(request, 'nuevopersona/admusuario.html', data)



def solgas_usuario_detalle(request, id):
    user = User.objects.get(id=id)
    mascotas = Mascota.objects.filter(propietario=user)

    data = {
        'user': user,
        'mascotas': mascotas
    }
    return render(request, 'nuevopersona/usuariodetalle.html', data)


def usuario_administrar_eliminar (request, id):
    users = User.objects.get(id=id)
    users.delete()
    messages.success(request, 'Eliminado Correctamente al usuario')
    return redirect('/solgas/usuario/administrar/')



def crear_usuario(request):
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('/solgas/usuario/administrar/')
    return render(request, 'nuevopersona/crearusuario.html')

def usuario_administrar_modificar (request,id): 
    if request.method == 'POST':
        username = request.POST.get('username')
        users = User.objects.get(id=id)
        password = request.POST.get('password')
        users.set_password(password)
        users.save()
        return redirect('/solgas/usuario/administrar/')
    else:
        data = {'id': id}
        return render(request, 'nuevopersona/usuariomodificar.html', data)

# ============================== MASCOTAS ========================================
def mostrar_mascotas(request):
    mascotas = Mascota.objects.all()
    return render(request, 'mascotas/mostrar.html', {'mascotas': mascotas})

def adminmodificar_mascota(request, mascota_id):
    mascota = Mascota.objects.get(id=mascota_id)
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = MascotaForm(instance=mascota)
    return render(request, 'mascotas/modificar.html', {'form': form})

def detalles_mascota(request, mascota_id):
    mascota = Mascota.objects.get(id=mascota_id)
    return render(request, 'mascotas/detalle.html', {'mascota': mascota})



def registrar_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.propietario = request.user
            mascota.save()
            return redirect('/')
    else:
        form = MascotaForm()
    return render(request, 'mascotas/registro_mascota.html', {'form': form})

def crear_mascota_admin(request):
    if request.method == 'POST':
        form = MascotaAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = MascotaAdminForm()
    return render(request, 'mascotas/crear_mascota_admin.html', {'form': form})

@login_required
def eliminar_mascota(request, mascota_id):
    mascota = Mascota.objects.get(id=mascota_id)
    mascota.delete()
    messages.success(request, "Registro eliminado correctamente")
    return redirect(to="/")


@login_required
def mis_mascotas(request):
    mascotas = Mascota.objects.filter(propietario=request.user)
    return render(request, 'nuevopersona/mis_mascotas.html', {'mascotas': mascotas})

def modificar_mascota(request, mascota_id):
    mascota = Mascota.objects.get(id=mascota_id)

    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('/mis_mascotas')
    else:
        form = MascotaForm(instance=mascota)

    return render(request, 'nuevopersona/modificar_mascota.html', {'form': form})

# Acciones carrito
# ============================ CARRO DE COMPRA ============================

def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      #print(request.user.id)
      product_status=Productos.objects.get(id=product_id)
      if product_status:
        if Carro.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'El Producto ya esta ingresado al carro de compras'}, status=200)
        else:
          if product_status.stock>=product_qty:
            Carro.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'El Producto se agrego al carro de compra'}, status=200)
          else:
            return JsonResponse({'status':'Product stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)

def mostrar_carro(request):
    cart = Carro.objects.all()
    m = {'cart': cart, 'title': 'MOSTRAR CARRO DE COMPRAS'}
    return render(request, 'carrito/mostrar.html', m)

def cart_page(request):
    if request.user.is_authenticated:
        cart = Carro.objects.filter(user=request.user)
        subtotal = 0
        iva = 0
        total_neto = 0

        for item in cart:
            subtotal += item.subtotal
            iva += item.iva

        total_neto = subtotal + iva

        context = {
            'cart': cart,
            'subtotal': subtotal,
            'iva': iva,
            'total_neto': total_neto,
        }

        return render(request, "carrito/cart.html", context)
    else:
        return redirect("/")

def remove_cart(request, cid):
    cartitem = Carro.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")

def limpiar_carro(request):
    if request.user.is_authenticated:
        Carro.objects.filter(user=request.user).delete()
        return redirect("/cart")
    else:
        return redirect("/")
# ============================ GUARDAR FAVORITOS ============================
def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      producto_id=data['pid']
      producto_status=Productos.objects.get(id=producto_id)
      if producto_status:
         if Favorito.objects.filter(user=request.user.id,producto_id=producto_id):
          return JsonResponse({'status':'El Producto ya existe en la session de favoritos'}, status=200)
         else:
          Favorito.objects.create(user=request.user,producto_id=producto_id)
          return JsonResponse({'status':'El PRoducto ya se agrego a Favoritos'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)

def mostrar_favorito(request):
    fav = Favorito.objects.all()
    m = {'fav': fav ,
        'title': 'MOSTRAR PRODUCTOS FAVORITOS',
        }
    return render(request, 'favoritos/mostrar.html',m)

def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favorito.objects.filter(user=request.user)
    return render(request,"favoritos/fav.html",{"fav":fav})
  else:
    return redirect("/")
 
def remove_fav(request,fid):
  item=Favorito.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")



def procesar_compra(request):
    rawcart = Carro.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product_qty:
            Carro.objects.delete(id=item.id)

    cartitems = Carro.objects.filter(user=request.user)
    cart_total_price = 0
    cart_iva = 0
    for item in cartitems:
        cart_total_price += item.product.precio * item.product_qty
        cart_iva += item.product.precio * item.product_qty * IVA_PERCENTAGE

    cart_total_neto = cart_total_price + cart_iva
    
    context = {
        'cartitems': cartitems,
        'cart_total_price': cart_total_price,
        'cart_iva': cart_iva,
        'cart_total_neto': cart_total_neto
    }
    
    return render(request, 'carrito/checkout.html', context)

def crear_hora(request):
    if request.method == 'POST':
        form = AgengarHorasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('veterinaria:mostrar_hora')
    else:
        form = AgengarHorasForm()
    return render(request, 'agendar/crear_hora.html', {'form': form})

def mostrar_hora(request):
    horas = Agengar_horas_disponibles.objects.all()
    return render(request, 'agendar/mostrar_hora.html', {'horas': horas})

def eliminar_hora(request, hora_id):
    hora = Agengar_horas_disponibles.objects.get(id=hora_id)
    if request.method == 'POST':
        hora.delete()
        return redirect('veterinaria:mostrar_hora')
    return render(request, 'agendar/eliminar_hora.html', {'hora': hora})

def modificar_hora(request, hora_id):
    hora = Agengar_horas_disponibles.objects.get(id=hora_id)
    if request.method == 'POST':
        form = AgengarHorasForm(request.POST, instance=hora)
        if form.is_valid():
            form.save()
            return redirect('veterinaria:mostrar_hora')
    else:
        form = AgengarHorasForm(instance=hora)
    return render(request, 'agendar/modificar_hora.html', {'form': form, 'hora': hora})

#pedir hora
def pedir_hora_list(request):
    pedirhoras = PedirHora.objects.all()
    return render(request, 'pedirhora/pedirhora_list.html', {'pedirhoras': pedirhoras})

def pedir_hora_detail(request, id):
    pedirhora = get_object_or_404(PedirHora, id=id)
    return render(request, 'pedirhora/pedirhora_detail.html', {'pedirhora': pedirhora})

@login_required
def pedir_hora_create(request):
    propietario = request.user

    if request.method == 'POST':
        form = PedirHoraForm(propietario, request.POST)
        if form.is_valid():
            pedir_hora = form.save(commit=False)
            pedir_hora.propietario = propietario
            pedir_hora.save()
            return redirect('veterinaria:pedir_hora_list')
    else:
        form = PedirHoraForm(propietario)
    
    context = {
        'form': form
    }
    
    return render(request, 'pedirhora/pedirhora_create.html', context)


def pedir_hora_edit(request, id):
    pedirhora = get_object_or_404(PedirHora, id=id)
    if request.method == 'POST':
        form = PedirHoraForm(request.POST, instance=pedirhora)
        if form.is_valid():
            form.save()
            return redirect('veterinaria:pedir_hora_list')
    else:
        form = PedirHoraForm(instance=pedirhora)
    return render(request, 'pedirhora/pedirhora_edit.html', {'form': form, 'pedirhora': pedirhora})


def eliminar_hora_propietario(request, id):
    hora = get_object_or_404(PedirHora, id=id, propietario=request.user)
    hora.delete()
    return redirect('veterinaria:pedir_hora_list')

#carucel

def carrucel_list(request):
    carruceles = Carrucel.objects.all()
    return render(request, 'carrucel/list.html', {'carruceles': carruceles})

def carrucel_detail(request, id):
    carrucel = get_object_or_404(Carrucel, id=id)
    return render(request, 'carrucel/detail.html', {'carrucel': carrucel})

def carrucel_create(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        imagen = request.FILES['imagen']
        carrucel = Carrucel(titulo=titulo, descripcion=descripcion, imagen=imagen)
        carrucel.save()
        return redirect('veterinaria:carrucel_list')
    return render(request, 'carrucel/create.html')

def carrucel_update(request, id):
    carrucel = get_object_or_404(Carrucel, id=id)
    if request.method == 'POST':
        carrucel.titulo = request.POST['titulo']
        carrucel.descripcion = request.POST['descripcion']
        if 'imagen' in request.FILES:
            carrucel.imagen = request.FILES['imagen']
        carrucel.save()
        return redirect('veterinaria:carrucel_list')
    return render(request, 'carrucel/update.html', {'carrucel': carrucel})

def carrucel_delete(request, id):
    carrucel = get_object_or_404(Carrucel, id=id)
    if request.method == 'POST':
        carrucel.delete()
        return redirect('veterinaria:carrucel_list')
    return render(request, 'carrucel/delete.html', {'carrucel': carrucel})

@login_required
def horas_pedidas(request, user_id):
    user_horas_pedidas = PedirHora.objects.filter(propietario_id=user_id)
    return render(request, 'pedirhora/horas_pedidas.html', {'horas_pedidas': user_horas_pedidas})


#nosotros
def nosotros_list(request):
    nosotros = Nosotros.objects.all()
    return render(request, 'nosotros/nosotros_list.html', {'nosotros': nosotros})

def nosotros_create(request):
    if request.method == 'POST':
        form = NosotrosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('veterinaria:list')
    else:
        form = NosotrosForm()
    return render(request, 'nosotros/nosotros_form.html', {'form': form})

def nosotros_update(request, pk):
    nosotros = get_object_or_404(Nosotros, pk=pk)
    if request.method == 'POST':
        form = NosotrosForm(request.POST, request.FILES, instance=nosotros)
        if form.is_valid():
            form.save()
            return redirect('veterinaria:list')
    else:
        form = NosotrosForm(instance=nosotros)
    return render(request, 'nosotros/nosotros_form.html', {'form': form})

def nosotros_detail(request, pk):
    nosotros = get_object_or_404(Nosotros, pk=pk)
    return render(request, 'nosotros/nosotros_detail.html', {'nosotros': nosotros})


def nosotros_delete(request, pk):
    nosotros = get_object_or_404(Nosotros, pk=pk)
    nosotros.delete()
    return redirect('veterinaria:list')
