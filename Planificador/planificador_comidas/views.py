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
            messages.success(request, f'¡Tu cuenta ha sido creada, {username}!')
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
            return redirect('menu')
    else:
        form = MenuForm()
    return render(request, 'planificador_comidas/menu/agregar_menu.html', {'form': form})


@login_required
def editar_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()
            form.save_m2m()
            return redirect('menu')
    else:
        form = MenuForm(instance=menu)
    return render(request, 'planificador_comidas/menu/editar_menu.html', {'form': form})


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
            form.save()
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
            form.save()
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
            compra.save()
            return redirect('compras')
    else:
        form = CompraForm(instance=compra)
    return render(request, 'planificador_comidas/compras/editar_compra.html', {'form': form})

def eliminar_compra(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    compra.delete()
    return redirect('compras')


