from django import forms
from django.forms import ModelForm, DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import formset_factory

from .models import Comida, Miembro, Compra, Perfil, ElementoCompra

from django.forms import formset_factory


class MiembroForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = ['nombre', 'edad', 'comida_preferida', 'gustos', 'disgustos', 'extra']


ComidaMiembroFormSet = formset_factory(MiembroForm, extra=1)


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
