from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from datetime import date
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

# Create your models here.
class Categorias(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='categoria', blank=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = "categorias"
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']


#modelo Productos
class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imgproductos/%Y/%m/%d', blank=True)
    descripcion = models.TextField()
    precio = models.IntegerField()
    stock = models.IntegerField(null=True, default=0)
    categoria = models.ForeignKey(Categorias, on_delete=models.SET_NULL, null=True)
    tendencia = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'contacto'
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['nombre']

# Model Carrito
class Carro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Productos, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
 
    @property
    def subtotal(self):
        return self.product_qty * self.product.precio

    @property
    def iva(self):
        return self.subtotal * 0.19

    @property
    def total_neto(self):
        return self.subtotal + self.iva

  
#Favoritos
class Favorito(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	producto=models.ForeignKey(Productos,on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)

class Carrucel(models.Model):
    titulo = models.CharField(max_length=20)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='carucel')

#Mascotas
class Mascota(models.Model):
    nombre = models.CharField(max_length=500)
    tipo_mascota = [
        ('Perro (a)','Perro (a)'),
        ( 'Gato (a)', 'Gato (a)')
    ]
        
    tipo = models.CharField(max_length=10, choices=tipo_mascota, default="PERRO(A)")
    genero_mascota = [
        ('Macho','Macho'),
        ('Hembra','Hembra')        
    ]
    sexo = models.CharField(max_length=8, choices=genero_mascota, default="MACHO")
    raza = models.CharField(max_length=60, blank=True, null=True)
    tiene_chip = [
        ('Si','Si'),
        ('No','No')
    ]
    microchip = models.CharField(max_length=8, choices=tiene_chip, default="Si")
    foto = models.ImageField(upload_to='mascota')
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)    
    def __str__(self):
        return f'{self.nombre }  {self.propietario}' 

def validar_dia(value):
    dia_actual = datetime.date.today()

    if value <= dia_actual:
        raise ValidationError('Fecha no disponible')
    if value.weekday() == 6:  # 6 representa el día domingo
        raise ValidationError('Fecha disponible')

class Agengar_horas_disponibles(models.Model):
    servicio = models.CharField(max_length=200, help_text="Servicio: (Vacunas, Peluqueria, ChequeoMedico)")
    dia = models.DateField(help_text="Ingrese el día", validators=[validar_dia])
    hora = models.TimeField(help_text="Ingrese la hora")

    class Meta:
        unique_together = ('hora', 'dia')

    def clean(self):
        if self.dia.weekday() < 5:  # 0 representa el día lunes y 4 el viernes
            # Verificar horas para días de semana (lunes a viernes)
            if self.hora < datetime.time(10, 0) or self.hora > datetime.time(19, 0):
                raise ValidationError(_('Las horas disponibles de lunes a viernes son de 10:00 a 19:00.'))
        elif self.dia.weekday() == 5:  # 5 representa el día sábado
            # Verificar horas para sábados
            if self.hora < datetime.time(10, 0) or self.hora > datetime.time(18, 0):
                raise ValidationError(_('Las horas disponibles los sábados son de 10:00 a 18:00.'))

    def __str__(self):
        return f'{self.servicio} {self.dia.strftime("%b %d %Y")} {self.hora.strftime("%H:%M")}'

class PedirHora(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    hora = models.ForeignKey(Agengar_horas_disponibles, on_delete=models.CASCADE)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='horas_pedidas')

    def __str__(self):
        return f'{self.mascota} - {self.hora}'
    
class Comentario(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='comentarios')
    nombre = models.CharField(max_length=500)
    comentario = models.TextField()
    rating = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comentario

class Nosotros(models.Model):
    titulo = models.CharField(max_length=500)
    subtitulo = models.CharField(max_length=500)
    historia =  models.TextField()
    foto_doctora = models.ImageField(upload_to='nosotros')
    servicio1 = models.CharField(max_length=500)
    descripcion1  = models.TextField()
    imagen1 =  models.ImageField(upload_to='nosotros')
    servicio2 = models.CharField(max_length=500)
    descripcion2  = models.TextField()
    imagen2 =  models.ImageField(upload_to='nosotros')
    servicio3 = models.CharField(max_length=500)
    descripcion3  = models.TextField()
    imagen3 =  models.ImageField(upload_to='nosotros')
    servicio4 = models.CharField(max_length=500)
    descripcion4  = models.TextField()
    imagen4 =  models.ImageField(upload_to='nosotros')
    servicio5 = models.CharField(max_length=500)
    descripcion5  = models.TextField()
    imagen5 =  models.ImageField(upload_to='nosotros')
    servicio6 = models.CharField(max_length=500)
    descripcion6  = models.TextField()
    imagen6 =  models.ImageField(upload_to='nosotros')
    vision = models.TextField()
    mision = models.TextField()