from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Menu, Miembro, Compra, Perfil, ElementoCompra


class MenuForm(forms.ModelForm):
    miembro = forms.ModelMultipleChoiceField(queryset=Miembro.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Menu
        fields = ['fecha', 'dia_semana', 'hora', 'tipo', 'titulo', 'descripcion', 'ingredientes', 'miembros', 'extra']


class MiembroForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = ['nombre', 'edad', 'comida_preferida', 'gustos', 'disgustos', 'extra']


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['fecha', 'menu', 'extra']


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso")
        return email


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['cumpleanos', 'gustos', 'disgustos', 'extra']



class ElementoCompraForm(forms.ModelForm):
    class Meta:
        model = ElementoCompra
        fields = ['ingrediente', 'tipo', 'precio_aprox', 'cantidad', 'tipo_cantidad', 'extra', 'compra']
        widgets = {
            'compra': forms.Select(attrs={'class': 'form-control'}),
        }
