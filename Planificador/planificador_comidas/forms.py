from django import forms
from django.forms import BaseFormSet, ModelForm, DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.contrib import messages
from .models import Comida, Miembro, Compra, Perfil, ElementoCompra

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['cumpleanos', 'gustos', 'disgustos', 'extra']

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

    def login(self, request):
        if request.method == 'POST':
            form = self(data=request.POST)  # Corrige aquí, pasa request.POST directamente
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    return redirect('index')  
                else:
                    form.add_error(None, 'Usuario o contraseña incorrectos')
        else:
            form = self()


class MiembroForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = ['perfil','nombre', 'edad', 'comida_preferida', 'gustos', 'disgustos', 'extra']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'comida_preferida': forms.TextInput(attrs={'class': 'form-control'}),
            'gustos': forms.Textarea(attrs={'class': 'form-control'}),
            'disgustos': forms.Textarea(attrs={'class': 'form-control'}),
            'extra': forms.Textarea(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['perfil'].required = True

ComidaMiembroFormSet = formset_factory(MiembroForm, formset=BaseFormSet, extra=1)
class ComidaForm(forms.ModelForm):
    miembro = forms.ModelMultipleChoiceField(queryset=Miembro.objects.all(), widget=forms.CheckboxSelectMultiple)
    extra = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "¿Ingrese cualquier extra"}))
    miembros_formset = ComidaMiembroFormSet(prefix='miembros')

    class Meta:
        model = Comida
        fields = ['inicio', 'fin', 'tipo', 'titulo', 'descripcion', 'ingredientes', 'miembro', 'extra']

        widgets = {
            "titulo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Introduzca el título de la comida"}
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Introduzca una descripción",
                }
            ),
            "ingredientes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Introduzca los ingredientes",
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
            "extra": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Introduzca cualquier extra",
                }
            ),
        }

    def __init__(self, user, *args, **kwargs):
        super(ComidaForm, self).__init__(*args, **kwargs)
        self.fields["inicio"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["fin"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.instance.user = user

        if self.instance.pk:
            # Si se está editando una comida existente, se preseleccionan los miembros asociados
            self.fields['miembro'].initial = self.instance.miembro.all()

        # Se muestra el campo extra si la comida está marcada como "extra"
        if self.instance.extra:
            self.fields['extra'].widget.attrs['style'] = ''
        else:
            self.fields['extra'].widget.attrs['style'] = 'display:none;'

    def save(self, commit=True):
        comida = super().save(commit=False)

        # Actualizar la relación muchos a muchos con los miembros seleccionados
        if commit:
            comida.save()
            comida.miembro.set(self.cleaned_data['miembro'])

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
    comida = forms.ModelChoiceField(queryset=Comida.objects.all())

    class Meta:
        model = Compra
        fields = ['fecha', 'comida', 'extra']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elemento_compra_formset = ElementoCompraFormSet(prefix='elementos')

    def is_valid(self):
        form_valid = super().is_valid()
        formset_valid = self.elemento_compra_formset.is_valid()
        return form_valid and formset_valid

    def save(self, commit=True):
        compra = super().save(commit=False)
        if commit:
            compra.save()

            for form in self.elemento_compra_formset:
                elemento_compra = form.save(commit=False)
                elemento_compra.compra = compra
                elemento_compra.save()

        return compra
