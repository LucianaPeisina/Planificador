from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views


urlpatterns = [
    # Ruta para la página principal
    path('', views.index, name='index'),

    # Rutas para el menú semanal
    path('comida/', views.comida, name='comida'),
    path('comida/nuevo/', views.agregar_comida, name='agregar_comida'),
    path('comida/<int:pk>/editar/', views.editar_comida, name='editar_comida'),
    path('comida/<int:pk>/eliminar/', views.eliminar_comida, name='eliminar_comida'),
    path("lista_comida/", views.TodasComidasListaView.as_view(), name="lista_comida"),
    path("running-lista-comidas/", views.RunningListaComidasView.as_view(),name="running_comidas",),
    path("comida/<int:comida_id>/detalles/", views.comida_detalles, name="comida-detalles"),

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


    # Rutas para elemento compra
    path('compras/<int:compra_pk>/elementos/nuevo/', views.agregar_elemento, name='agregar_elemento'),
    path('compras/<int:compra_pk>/elementos/<int:elemento_pk>/editar/', views.editar_elemento, name='editar_elemento'),
    path('compras/<int:compra_pk>/elementos/<int:elemento_pk>/eliminar/', views.eliminar_elemento, name='eliminar_elemento'),


    # Rutas para el inicio de sesión y cierre de sesión
   path('login/', views.login_view, name='login'),

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Ruta para registrar un nuevo usuario
    path('registro/', views.registro, name='registro'),
    


    path('calendarioMenu/', views.calendario_menu, name='calendarioMenu'),



#    path("calendario/", views.CalendarioViewNuevo.as_view(), name="calendario"),
 #   path("calendario/", views.CalendarioView.as_view(), name="calendarios"),


]


