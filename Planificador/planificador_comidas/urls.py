from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views


urlpatterns = [
    # Ruta para la página principal
    path('', views.index, name='index'),

    #Rutas para Perfil
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('listado_perfiles/', views.listado_perfiles, name="listado_perfiles"),

    # Rutas para el menú semanal
    path('comida/', views.comida, name='comida'),
    path('comida/<int:pk>/editar/', views.editar_comida, name='editar_comida'),
    path('comida/<int:pk>/eliminar/', views.eliminar_comida, name='eliminar_comida'),
    
    #*** cambie en varias definiciones pq estaban mezclados los nombres:
    #*** (antes) comida-detalles <-> (despues) detalle_comida
    # #path("comida/<int:comida_id>/detalles/", views.comida_detalles, name="comida-detalles"),
    path("comida/<int:comida_id>/detalles/", views.detalle_comida, name="detalle_comida"),
    path("calendarioMenu/", views.CalendarViewNew.as_view(), name="calendarioMenu"),
    path("calenders/", views.CalendarView.as_view(), name="calendars"),



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
    # path('login/', views.login_view, name='login'),
    path('login/', views.login_request, name='login'),
    #path('logout/', views.logout_request, name='logout'),

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Ruta para registrar un nuevo usuario
    path('registro/', views.registro, name='registro'),
     


 
]


