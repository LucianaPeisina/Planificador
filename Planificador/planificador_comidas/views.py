from calendar import month_name
from datetime import timedelta, datetime, date
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe
from django.views import generic
from django.views.generic import ListView

#from .forms import ComidaForm, MiembroForm, CompraForm, ElementoCompraForm, LoginForm, PerfilForm
from .forms import ComidaForm, MiembroForm, CompraForm, ElementoCompraForm, PerfilForm
from .models import Comida, Miembro, Compra, ElementoCompra, Perfil

from django.contrib import messages
from .forms import AltaUsuarioForm
# ...

def calendario_menu(request):
    return render(request, 'planificador_comidas/calendarioMenu.html')

def index(request):
    return render(request, 'planificador_comidas/index.html')

def registro(request):     
    if request.method == "POST":
        alta_usuario_form = AltaUsuarioForm(request.POST)
        if alta_usuario_form.is_valid():
            user = alta_usuario_form.save(commit=False)
            user.save()  #guardamos el usuario

            messages.add_message(request, messages.SUCCESS, 'Usuario dado de alta con éxito', extra_tags="tag1")
             
            login(request,user)
            messages.add_message(request, messages.SUCCESS, 'Ha iniciado sesion como: ' + alta_usuario_form.cleaned_data.get('username'), extra_tags="tag1")
                              
            return render(request, 'planificador_comidas/index.html')
    else:
        # GET
        alta_usuario_form = AltaUsuarioForm()
    
    context = {
        'form': alta_usuario_form
    }

    return render(request, 'planificador_comidas/registro.html',context) 


############    LOGIN / LOGOUT  #####################
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data= request.POST)
        if form.is_valid():
            usuario =form.cleaned_data.get('username')
            contraseña= form.cleaned_data.get('password')
            user= authenticate(username=usuario, password=contraseña)

            if user is not None:
                login(request,user)
                messages.info(request, f"Ha iniciado sesion como: {usuario}")
                return render(request, 'planificador_comidas/index.html')

    form = AuthenticationForm()
    return render(request, 'planificador_comidas/login.html',{"form": form}) 

##
def logout_request(request):
    logout(request)
    messages.info(request,"Sesion finalizada")
    return render(request, 'planificador_comidas/index.html') 

############    PERFIL  #####################
#@login_required
def editar_perfil(request):
    perfil = Perfil.objects.get(user=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'planificador_comidas/perfil/editar_perfil.html', {'form': form})

#@login_required
def perfil(request):
    perfil = request.user.perfil
    return render(request, 'planificador_comidas/perfil/perfil.html', {'perfil': perfil})

#@login_required
def listado_perfiles(request):
    context = {}

    listado = Perfil.objects.all().order_by('id')

    context['listado_perfiles'] = listado

    return render(request, 'planificador_comidas/perfil/listado_perfiles.html', context)

############    COMIDA  #####################
#@login_required
def comida(request):
    comidas = Comida.objects.all()
    return render(request, 'planificador_comidas/comida/comida.html', {'comidas': comidas})

#@login_required
def agregar_comida(request):
    if request.method == 'POST':
        form = ComidaForm(request.POST)
        if form.is_valid():
            comida = form.save(commit=False)
            comida.save()
            form.save_m2m()
            return redirect('comida')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = ComidaForm()
    return render(request, 'planificador_comidas/comida/agregar_comida.html', {'form': form})

#@login_required
def editar_comida(request, pk):
    comida = get_object_or_404(Comida, pk=pk)

    # Obtener todos los miembros relacionados con la comida actual
    miembros_actuales = comida.miembros.all()

    if request.method == 'POST':
        form = ComidaForm(request.POST, instance=comida)

        # Si el formulario es válido, actualizar la comida y sus relaciones con los miembros
        if form.is_valid():
            comida = form.save(commit=False)
            comida.save()

            # Obtener los miembros seleccionados en el formulario
            miembros_nuevos = form.cleaned_data['miembros']

            # Actualizar las relaciones de la comida con los miembros seleccionados
            for miembro in miembros_actuales:
                if miembro not in miembros_nuevos:
                    comida.miembros.remove(miembro)
            for miembro in miembros_nuevos:
                if miembro not in miembros_actuales:
                    comida.miembros.add(miembro)

            return redirect('comida')
    else:
        form = ComidaForm(instance=comida)

    return render(request, 'planificador_comidas/comida/editar_comida.html', {'form': form})

#@login_required(login_url="signup")
#def comida_detalles(request, comida_id):
def detalle_comida(request, comida_id):
    comida = Comida.objects.get(id=comida_id)
    MiembroComida = MiembroComida.objects.filter(comida=comida)
    context = {"Comida": comida, "Miembro": MiembroComida}
#    return render(request, "comida-detalles.html", context)
    return render(request, "detalle_comida.html", context)

#@login_required
def eliminar_comida(request, pk):
    comida = get_object_or_404(Comida, pk=pk)
    comida.delete()
    return redirect('comida')

############    MIEMBRO  #####################
#@login_required
def miembros(request):
    miembros = Miembro.objects.all()
    perfil = request.user.perfil
    
    return render(request, 'planificador_comidas/miembros/miembros.html', {'miembros': miembros, 'perfil': perfil})

#@login_required

def agregar_miembro(request):
    if request.method == 'POST':
        form = MiembroForm(request.POST)
        if form.is_valid():
            miembro = form.save(commit=False)
            miembro.usuario = request.user 
            miembro.save()
            return redirect('miembros')
    else:
        form = MiembroForm()
    return render(request, 'planificador_comidas/miembros/agregar_miembro.html', {'form': form})

#@login_required
def editar_miembro(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    if request.method == 'POST':
        form = MiembroForm(request.POST, instance=miembro)
        if form.is_valid():
            miembro= form.save(commit=False)
            miembro.save()
            return redirect('miembros')
    else:
        form = MiembroForm(instance=miembro)
    return render(request, 'planificador_comidas/miembros/editar_miembro.html', {'form': form, 'miembro':miembro})

#@login_required
def eliminar_miembro(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    miembro.delete()
    return redirect('miembros')

############    COMPRAS  #####################
#@login_required
def compras(request):
    compras = Compra.objects.all()
    elemento = ElementoCompra.objects.all()
    return render(request, 'planificador_comidas/compras/compras.html', {'compras': compras, 'elemento': elemento})

#@login_required
def agregar_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.save()
            return redirect('editar_compra', pk=compra.pk)
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = CompraForm()
    return render(request, 'planificador_comidas/compras/agregar_compra.html', {'form': form})

#@login_required
def editar_compra(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == 'POST':
        form = CompraForm(request.POST, instance=compra)
        if form.is_valid():
            compra=  form.save()
            compra.save
            return redirect('compras')
    else:
        form = CompraForm(instance=compra)
    return render(request, 'planificador_comidas/compras/editar_compra.html', {'form': form, 'compra':compra})

def eliminar_compra(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    compra.delete()
    return redirect('compras')

############    ELEMENTO COMPRA  #####################
def agregar_elemento(request, compra_pk):
    compra = Compra.objects.get(pk=compra_pk)
    if request.method == 'POST':
        form = ElementoCompraForm(request.POST)
        if form.is_valid():
            elemento = form.save(commit=False)
            elemento.compra = compra
            elemento.save()
            #return redirect('editar_compra', compra_pk=compra_pk)
            return redirect('editar_compra', pk=compra_pk)
    else:
        form = ElementoCompraForm()
    return render(request, 'planificador_comidas/compras/agregar_elemento.html', {'form': form, 'compra': compra})

def editar_elemento(request, compra_pk, elemento_pk):
    elemento = get_object_or_404(ElementoCompra, pk=elemento_pk)
    if request.method == 'POST':
        form = ElementoCompraForm(request.POST, instance=elemento)
        if form.is_valid():
            form.save()
            return redirect('editar_compra', pk=compra_pk)
    else:
        form = ElementoCompraForm(instance=elemento)
    return render(request, 'editar_elemento.html', {'form': form})

def eliminar_elemento(request, compra_pk, elemento_pk):
    elemento = get_object_or_404(ElementoCompra, pk=elemento_pk)
    elemento.delete()
    return redirect('compras')

############      #####################
class TodasComidasListaView(ListView):
   
    template_name = "lista_comida.html"
    model = Comida

   # def get_queryset(self):
    #    return Comida.objects.get_all_events(user=self.request.user)

class RunningListaComidasView(ListView):

    template_name = "lista_comida.html"
    model = Comida



# ...



#    def get_queryset(self):
 #       return Comida.objects.get_running_comidas(user=self.request.user)

"""
def get_fecha(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_mes(d):
    first = d.replace(day=1)
    prev_mes = first - timedelta(days=1)
    mes = "mes=" + str(prev_mes.year) + "-" + str(prev_mes.mont)
    return mes

  
def sig_mes(d):
    days_in_mes = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_mes)
    next_mes = last + timedelta(days=1)
    mes = "mes=" + str(next_mes.year) + "-" + str(next_mes.month)
    return mes


class CalendarioView(generic.ListView):
    #login_url = "signin"
    model = Comida
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_fecha(self.request.GET.get("month", None))
        cal = calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendario"] = mark_safe(html_cal)
        context["prev_mes"] = prev_mes(d)
        context["sig_mes"] = sig_mes(d)
        return context


class CalendarioViewNuevo( generic.View):
    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"
    form_class = ComidaForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        comidas = Comida.objects.get_all_events(user=request.user)
        comidas_mes = Comida.objects.get_running_events(user=request.user)
        comida_lista = []

        for comida in comidas:
            comida_lista.append
            (
                {
                    "titulo": comida.titulo,
                    "inicio": comida.inicio.strftime("%Y-%m-%dT%H:%M:%S"),
                    "fin": comida.fin.strftime("%Y-%m-%dT%H:%M:%S"),

                }
            )
        context = {"form": forms, "comidas": comida_lista,
                   "comidas_mes": comidas_mes}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarioMenu")
        context = {"form": forms}
        return render(request, self.template_name, context)

"""