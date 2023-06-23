from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminTimeWidget, AdminDateWidget
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db import transaction


class ConctactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        widgets={
            'mensaje': forms.Textarea(attrs={
                'rows':5,
                'cols':30
                }),
        }
        fields = '__all__'
        

class ProductoForm(forms.ModelForm):

    class Meta:
        model = Productos
        fields = ["nombre", "descripcion", "precio", "stock", "categoria","tendencia", "imagen"]
        

class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categorias
        fields = ["nombre","imagen"]


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ["username", "first_name","last_name","email","password1","password2"]


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nombre', 'comentario', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = False         

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'tipo', 'sexo', 'raza', 'microchip', 'foto']
        labels = {
            'nombre': 'Nombre',
            'tipo': 'Tipo de Mascota',
            'sexo': 'Género',
            'raza': 'Raza',
            'microchip': '¿Tiene microchip?',
            'foto': 'Foto',
        }
        widgets = {
            'foto': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class MascotaAdminForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'tipo', 'sexo', 'raza', 'microchip', 'foto', 'propietario']
        labels = {
            'nombre': 'Nombre',
            'tipo': 'Tipo de Mascota',
            'sexo': 'Género',
            'raza': 'Raza',
            'microchip': '¿Tiene microchip?',
            'foto': 'Foto',
            'propietario': 'Propietario',
        }
        widgets = {
            
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'microchip': forms.Select(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class AgengarHorasForm(forms.ModelForm):
    hora = forms.TimeField(widget=AdminTimeWidget(format='%H:%M'))
    dia = forms.DateField(widget=AdminDateWidget(attrs={'class': 'datepicker'}, format='%Y-%m-%d'))

    class Meta:
        model = Agengar_horas_disponibles
        fields = '__all__'



class PedirHoraForm(forms.ModelForm):
    def __init__(self, propietario, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.propietario = propietario
        self.fields['mascota'].queryset = self.propietario.mascota_set.all()
        self.fields['hora'].queryset = Agengar_horas_disponibles.objects.exclude(
            pedirhora__hora__in=PedirHora.objects.values_list('hora__id', flat=True)
        )

    class Meta:
        model = PedirHora
        fields = ['mascota', 'hora']

class NosotrosForm(forms.ModelForm):
    class Meta:
        model = Nosotros
        fields = '__all__'