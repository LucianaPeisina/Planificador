from django.contrib import admin

from .models import Perfil, Miembro

# Registramos los modelos (using the decorator)
# Registramos nuevos 'display' y 'filtros'
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    pass
    list_display = ('user', 'cumpleanos', 'gustos', 'extra')
    list_filter = ('gustos', 'extra')
    fields = [('user', 'cumpleanos'), 'gustos', 'extra']

@admin.register(Miembro)
class MiembroAdmin(admin.ModelAdmin):
    pass
    list_display = ('usuario', 'nombre', 'edad')