from django import forms

from django.contrib.auth.models import User

from .models import Menu, Miembro, Compra, PerfilUsuario

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


class RegistroForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = PerfilUsuario
        fields = ('comida_preferida', 'gustos', 'disgustos')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso")
        return username



    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso")
        if PerfilUsuario.objects.filter(user__email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso")
        return email


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")

        return cleaned_data
