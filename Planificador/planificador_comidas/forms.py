from datetime import date, timedelta
from django import forms
from django.forms import BaseFormSet, ModelForm, DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.contrib import messages
from .models import Comida, Miembro, Compra, Perfil, ElementoCompra

from django.forms.formsets import BaseFormSet
from django.contrib.auth.forms import AuthenticationForm
#from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect

# Descripcion 
# formulariOs:
# LoginForm: Este formulario hereda de AuthenticationForm y se utiliza para el inicio de sesión de los usuarios. Personaliza la apariencia de los campos username y password utilizando el atributo widget.attrs.

# PerfilForm: Este formulario está vinculado al modelo Perfil y se utiliza para crear o actualizar perfiles de usuario. Los campos del formulario son cumpleanos, gustos, disgustos y extra. Al utilizar forms.ModelForm, el formulario se genera automáticamente a partir del modelo y se definen los campos y widgets correspondientes.

# MiembroForm: Este formulario está vinculado al modelo Miembro y se utiliza para crear o actualizar miembros. Los campos del formulario son perfil, nombre, edad, comida_preferida, gustos, disgustos y extra. Se utiliza forms.ModelForm para generar automáticamente el formulario a partir del modelo y se aplican atributos de clase a los campos utilizando widgets.

# ComidaForm: Este formulario está vinculado al modelo Comida y se utiliza para crear o actualizar comidas. Los campos del formulario son inicio, fin, tipo, titulo, descripcion, ingredientes, miembro y extra. Se aplican widgets personalizados a algunos campos para mejorar la experiencia del usuario. El formulario también incluye un conjunto de formularios ComidaMiembroFormSet que permite seleccionar múltiples miembros para la comida.

# ElementoCompraForm: Este formulario está vinculado al modelo ElementoCompra y se utiliza para crear o actualizar elementos de compra. Los campos del formulario son ingrediente, tipo, precio_aprox, cantidad, tipo_cantidad, extra y compra. El campo compra se muestra como un menú desplegable para seleccionar la compra relacionada.

# CompraForm: Este formulario está vinculado al modelo Compra y se utiliza para crear o actualizar compras. Los campos del formulario son fecha, comida y extra. El formulario también incluye un conjunto de formularios ElementoCompraFormSet que permite agregar múltiples elementos de compra a la compra principal.

# class LoginForm(AuthenticationForm):
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #     self.fields['username'].widget.attrs['class'] = 'form-control'
#     #     self.fields['password'].widget.attrs['class'] = 'form-control'

#     def login(request):
#         messages.error(request, 'F login')
#         if request.method == 'POST':
#                 form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 auth_login(request, user)
#                 return redirect('indexZ')
#             else:
#                 messages.error(request, 'Usuario o contraseña incorrectos')
#         else:
#             form = LoginForm()
#         return render(request, 'planificador_comidas/login.html', {'form': form})

class AltaUsuarioForm(UserCreationForm):

    class Meta:
        model = User
        fields =  ['first_name', 'last_name', 'email', 'username','password1', 'password2']

    # Check unique email
    # Email exists && account active -> email_already_registered
    # Email exists && account not active -> delete previous account and register new one
    def clean_email(self):
        email_passed = self.cleaned_data.get("email")
        email_already_registered = User.objects.filter(email = email_passed).exists()
        user_is_active = User.objects.filter(email = email_passed, is_active = 1)
        if email_already_registered and user_is_active:
            print('email_already_registered and user_is_active')
            raise forms.ValidationError("Email already registered.")
        elif email_already_registered:
            print('email_already_registered')
            User.objects.filter(email = email_passed).delete()

        return email_passed


class PerfilForm(forms.ModelForm):
    gustos = forms.CharField(label='Gustos: ')
    disgustos = forms.CharField(label='Desagrados:')
    extra = forms.CharField(label='Extra:')
    cumpleanos = forms.DateField(
        initial=date(date.today().year - 18, 1, 1),
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'max': (date.today() - timedelta(days=18*365)).strftime('%Y-%m-%d'),
                'min': date(date.today().year - 100, 1, 1).strftime('%Y-%m-%d'),
                
            }
        )
    )
    class Meta:
        model = Perfil
        fields = ['cumpleanos', 'gustos', 'disgustos', 'extra']


class MiembroForm(forms.ModelForm):
    cumpleanos = forms.DateField(
        initial=date(date.today().year - 18, 1, 1),
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'max': (date.today() - timedelta(days=18 * 365)).strftime('%Y-%m-%d'),
                'min': date(date.today().year - 100, 1, 1).strftime('%Y-%m-%d'),
            }
        )
    )

    class Meta:
        model = Miembro
        fields = ['nombre', 'edad', 'cumpleanos', 'comida_preferida', 'gustos', 'disgustos', 'extra']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'comida_preferida': forms.TextInput(attrs={'class': 'form-control'}),
            'gustos': forms.Textarea(attrs={'class': 'form-control'}),
            'disgustos': forms.Textarea(attrs={'class': 'form-control'}),
            'extra': forms.Textarea(attrs={'class': 'form-control'}),
        }





class ComidaMiembroFormSet(formset_factory(MiembroForm, formset=BaseFormSet, extra=1)):
    pass

class ComidaForm(forms.ModelForm):
    extra = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "style": "resize: vertical;"})
    )
    miembros = forms.ModelMultipleChoiceField(
        queryset=Miembro.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Comida
        fields = ['inicio', 'fin', 'tipo', 'titulo', 'descripcion', 'ingredientes', 'extra']

        widgets = {
            "titulo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Introduzca el título de la comida"}
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Introduzca una descripción",
                    "rows": 3,
                    "style": "resize: vertical;",
                }
            ),
            "ingredientes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Introduzca los ingredientes",
                    "rows": 3,
                    "style": "resize: vertical;",
                }
            ),
            "inicio": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "fin": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "tipo": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, user, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        super(ComidaForm, self).__init__(*args, **kwargs, initial=initial)
        self.fields["inicio"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["fin"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.instance.usuario = user

        # Filtrar los objetos Miembro disponibles para el usuario actual
        self.fields['miembros'].queryset = Miembro.objects.filter(usuario=user)

        if self.instance.pk:
            # Si se está editando una comida existente, se preseleccionan los miembros asociados
            self.fields['miembros'].initial = self.instance.miembros.all()


        # Se muestra el campo extra si la comida está marcada como "extra"
        if self.instance.extra:
            self.fields['extra'].widget.attrs['style'] = ''
        else:
            self.fields['extra'].widget.attrs['style'] = 'display:none;'

    def save(self, commit=True):
        comida = super().save(commit=False)

        if commit:
            comida.save()

        # Guardar los miembros asociados a la comida
        if self.cleaned_data.get('miembros'):
            comida.miembros.set(self.cleaned_data['miembros'])

        return comida

class ElementoCompraForm(forms.ModelForm):
    class Meta:
        model = ElementoCompra
        fields = ['ingrediente', 'tipo', 'precio_aprox', 'cantidad', 'tipo_cantidad', 'extra', 'compra']
        widgets = {
            'compra': forms.Select(attrs={'class': 'form-control'}),
        }
        
ElementoCompraFormSet = formset_factory(ElementoCompraForm, extra=1)

class CompraForm(forms.ModelForm):
    comida = forms.ModelChoiceField(queryset=Comida.objects.all(), required=False, empty_label="Sin comida")
    fecha = forms.DateField(
        initial=date.today(),
        #initial=date(date.today().year, date.today().month, date.today().day),
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'max': (date.today() + timedelta(days=1 * 365)).strftime('%Y-%m-%d'),
                'min': date(date.today().year, 1, 1).strftime('%Y-%m-%d'),
            }
        )
    )

    class Meta:
        model = Compra
        fields = ['fecha', 'comida', 'extra']
