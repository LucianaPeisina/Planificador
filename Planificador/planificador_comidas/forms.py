from django import forms
from .models import Menu, Miembro, Compra

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['fecha', 'dia_semana', 'hora', 'tipo', 'titulo', 'descripcion', 'ingredientes', 'miembro', 'extra']

class MiembroForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = ['nombre', 'edad', 'comida_preferida', 'gustos', 'disgustos', 'extra']

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['ingrediente', 'tipo', 'precio_aprox', 'cantidad', 'tipo_cantidad', 'extra', 'menu']
