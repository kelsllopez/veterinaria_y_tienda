from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
app_name='veterinaria'

urlpatterns = [
    # paths menú
    path('', views.index, name='index'),
    path('categorias/', views.listCategorias, name='categorias'),
    path('contacto/', views.contacto, name='contacto'),
    path('listarcontacto/', views.mostrar_contacto, name='listarcontacto'),
    path('detallecontacto/<id>/', views.detalle_contacto, name='detallecontacto'),
    path('deletecontacto/<id>/', views.eliminar_contacto, name='deletecontacto'),
    path('nosotros/', views.nosotros, name='nosotros'),

    path('producto/', views.detalleProducto, name='producto'),
    path('addproducto/', views.addProducto, name='addproducto'),
    path('detalleproducto/<id>/', views.detalleProducto, name='detalleproducto'),
    path('productocategoria/<id>/', views.productoxCategoria, name='productocategoria'),
    path('editproducto/<id>/', views.editarProducto, name='editproducto'),
    path('deleteProducto/<id>/', views.deleteProducto, name='deleteProducto'),
    path('listarproductos/', views.listarProductos, name='listarproductos'),
    path('addcategoria/', views.addCategoria, name='addcategoria'),
    path('editcategoria/<id>/', views.modificarCategoria, name='editcategoria'),
    path('deleteCategoria/<id>/', views.deleteCategoria, name='deleteCategoria'),
        
    # paths de autenticacion
    path('registrar/', views.registrar, name='registrar'),
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('change/', views.change),
    path('change/<username>', views.change),

    path('solgas/usuario/administrar/', views.usuario_administrar),
    path('solgas/usuario/modificar/',views.usuario_administrar_modificar),
    path('solgas/usuario/modificar/<int:id>/',views.usuario_administrar_modificar),
    path('solgas/usuario/eliminar/<int:id>/',views.usuario_administrar_eliminar),
    path('solgas_usuario_detalle/<int:id>/', views.solgas_usuario_detalle, name='solgas_usuario_detalle'),
    path('solgas/crearusuario/',views.crear_usuario),
    path('horas_pedidas/<int:user_id>/', views.horas_pedidas, name='horas_pedidas'),

    
    path('registrar_mascota/', views.registrar_mascota, name='registrar_mascota'),
    path('mis_mascotas/', views.mis_mascotas, name='mis_mascotas'),
    path('adminmodificar_mascota/<int:mascota_id>/', views.adminmodificar_mascota, name='adminmodificar_mascota'),
    path('crear_mascota_admin/', views.crear_mascota_admin, name='crear_mascota_admin'),
    path('mascota/<int:mascota_id>/', views.detalles_mascota, name='detalles_mascota'),
    path('mascota/modificar/<int:mascota_id>/', views.modificar_mascota, name='modificar_mascota'),
    path('mascota/eliminar/<int:mascota_id>/', views.eliminar_mascota, name='eliminar_mascota'),

    path('mascotas/', views.mostrar_mascotas, name='mostrar_mascotas'),

    #Paths del carrito
    path('addtocart',views.add_to_cart,name="addtocart"),
    path('cart',views.cart_page,name="cart"),
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
    path('listarcarro/', views.mostrar_carro, name='listarcarro'),
    path('limpiar_carro/', views.limpiar_carro, name='limpiar_carro'),


    path('fav',views.fav_page,name="fav"),
    path('favviewpage',views.favviewpage,name="favviewpage"),
    path('remove_fav/<str:fid>',views.remove_fav,name="remove_fav"),
    path('listarfavorito/', views.mostrar_favorito, name='listarfavorito'),

    path('procesar_compra/', views.procesar_compra, name="procesar_compra"),

   
    path('crear_hora/',views.crear_hora, name='crear_hora'),
    path('mostrar_hora/', views.mostrar_hora, name='mostrar_hora'),
    path('eliminar_hora/<int:hora_id>/', views.eliminar_hora, name='eliminar_hora'),
    path('modificar_hora/<int:hora_id>/', views.modificar_hora, name='modificar_hora'),

    path('pedirhora/', views.pedir_hora_list, name='pedir_hora_list'),
    path('pedirhora/create/', views.pedir_hora_create, name='pedir_hora_create'),
    path('pedirhora/<int:id>/', views.pedir_hora_detail, name='pedir_hora_detail'),
    path('pedirhora/<int:id>/edit/', views.pedir_hora_edit, name='pedir_hora_edit'),
    path('eliminar-hora/<int:id>/', views.eliminar_hora_propietario, name='eliminar_hora_propietario'),

    path('carrucel/', views.carrucel_list, name='carrucel_list'),
    path('carrucel/<int:id>/', views.carrucel_detail, name='carrucel_detail'),
    path('carrucel/create/', views.carrucel_create, name='carrucel_create'),
    path('carrucel/<int:id>/update/', views.carrucel_update, name='carrucel_update'),
    path('carrucel/<int:id>/delete/', views.carrucel_delete, name='carrucel_delete'),

    path('listar/', views.nosotros_list, name='list'),
    path('agregar/', views.nosotros_create, name='create'),
    path('editar/<int:pk>/', views.nosotros_update, name='update'),
    path('eliminar/<int:pk>/', views.nosotros_delete, name='delete'),
    path('mostrar/<int:pk>/', views.nosotros_detail, name='detail'),


]
