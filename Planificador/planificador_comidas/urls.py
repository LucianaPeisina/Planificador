from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views


urlpatterns = [
    # Ruta para la página principal
    path('', views.index, name='index'),

    # Rutas para el menú semanal
    path('menu/', views.menu, name='menu'),
    path('menu/nuevo/', views.nuevo_menu, name='agregar_menu'),
    path('menu/<int:pk>/editar/', views.editar_menu, name='editar_menu'),
    path('menu/<int:pk>/eliminar/', views.eliminar_menu, name='eliminar_menu'),

    # Rutas para los miembros de la familia
    path('miembros/', views.miembros, name='miembros'),
    path('miembros/nuevo/', views.agregar_miembro, name='agregar_miembro'),
    path('miembros/<int:pk>/editar/', views.editar_miembro, name='editar_miembro'),
    path('miembros/<int:pk>/eliminar/', views.eliminar_miembro, name='eliminar_miembro'),

    # Rutas para las compras
    path('compras/', views.compras, name='compras'),
    path('compras/nuevo/', views.agregar_compra, name='agregar_compra'),
    path('compras/<int:pk>/editar/', views.editar_compra, name='editar_compra'),
    path('compras/<int:pk>/eliminar/', views.eliminar_compra, name='eliminar_compra'),

    # Rutas para el inicio de sesión y cierre de sesión
    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Ruta para registrar un nuevo usuario
    path('registro/', views.registro, name='registro'),
    
    # Ruta para eliminar un usuario
    path('eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),


]
