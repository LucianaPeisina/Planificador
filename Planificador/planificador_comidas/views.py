from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse

from django.contrib.auth import login, authenticate


from .models import Menu, Miembro, Compra
from .forms import MenuForm, MiembroForm, CompraForm


def index(request):
    return render(request, 'planificador_comidas/index.html')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'planificador_comidas/login.html')



def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            messages.success(request, f'¡Tu cuenta ha sido creada, {username}!')
            login(request, user)
            return redirect('login')
            
    else:
        form = UserCreationForm()
    return render(request, 'planificador_comidas/registro.html', {'form': form})


@login_required
def menu(request):
    menus = Menu.objects.all()
    return render(request, 'planificador_comidas/menu/menu.html', {'menus': menus})


@login_required
def agregar_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()
            form.save_m2m()
            return redirect('menus')
    else:
        form = MenuForm()
    return render(request, 'planificador_comidas/menus/agregar_menu.html', {'form': form})


@login_required
def editar_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)

    # Obtener todos los miembros relacionados con el menú actual
    miembros_actuales = menu.miembros.all()

    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)

        # Si el formulario es válido, actualizar el menú y sus relaciones con los miembros
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()

            # Obtener los miembros seleccionados en el formulario
            miembros_nuevos = form.cleaned_data['miembros']

            # Actualizar las relaciones del menú con los miembros seleccionados
            for miembro in miembros_actuales:
                if miembro not in miembros_nuevos:
                    menu.miembros.remove(miembro)
            for miembro in miembros_nuevos:
                if miembro not in miembros_actuales:
                    menu.miembros.add(miembro)

            return redirect('menus')
    else:
        form = MenuForm(instance=menu)

    return render(request, 'planificador_comidas/menus/editar_menu.html', {'form': form})

@login_required
def eliminar_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    menu.delete()
    return redirect('menu')


@login_required
def miembros(request):
    miembros = Miembro.objects.all()
    return render(request, 'planificador_comidas/miembros/miembros.html', {'miembros': miembros})


@login_required
def agregar_miembro(request):
    if request.method == 'POST':
        form = MiembroForm(request.POST)
        if form.is_valid():
            miembro = form.save(commit=False)
            miembro.user = request.user
            miembro.save()
            return redirect('miembros')
    else:
        form = MiembroForm()
    return render(request, 'planificador_comidas/miembros/agregar_miembro.html', {'form': form})


@login_required
def editar_miembro(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    if request.method == 'POST':
        form = MiembroForm(request.POST, instance=miembro)
        if form.is_valid():
            form.save()
            return redirect('miembros')
    else:
        form = MiembroForm(instance=miembro)
    return render(request, 'planificador_comidas/miembros/editar_miembro.html', {'form': form})


@login_required
def eliminar_miembro(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    miembro.delete()
    return redirect('miembros')


@login_required
def compras(request):
    compras = Compra.objects.all()
    return render(request, 'planificador_comidas/compras/compras.html', {'compras': compras})


@login_required
def agregar_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.menu = form.cleaned_data['menu']
            compra.save()
            return redirect('compras')
    else:
        form = CompraForm()
    return render(request, 'planificador_comidas/compras/agregar_compra.html', {'form': form})


@login_required
def editar_compra(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == 'POST':
        form = CompraForm(request.POST, instance=compra)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.menu = form.cleaned_data['menu']
            compra.save()

            return redirect('compras')
    else:
        form = CompraForm(instance=compra)
    return render(request, 'planificador_comidas/compras/editar_compra.html', {'form': form})


def eliminar_compra(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    compra.delete()
    return redirect('compras')


