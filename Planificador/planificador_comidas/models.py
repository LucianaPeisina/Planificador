from django.contrib.auth.models import User
from django.db import models


class Miembro(models.Model):
    nombre = models.CharField(max_length=50)
    edad = models.PositiveIntegerField()
    comida_preferida = models.CharField(max_length=50)
    gustos = models.TextField()
    disgustos = models.TextField()
    extra = models.TextField(blank=True)


class Menu(models.Model):
    TIPO_CHOICES = (
        ('D', 'Desayuno'),
        ('A', 'Almuerzo'),
        ('C', 'Cena'),
    )
    fecha = models.DateField()
    dia_semana = models.CharField(max_length=20)
    hora = models.TimeField()
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    ingredientes = models.TextField()
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE)
    extra = models.TextField(blank=True)


class Compra(models.Model):
    TIPO_CHOICES = (
        ('F', 'Frescos'),
        ('S', 'Secos'),
        ('E', 'Enlatados'),
        ('Fr', 'Frutas'),
        ('V', 'Verduras'),
        ('C', 'Carne')
    )

    CANTIDAD_CHOICES = (
        ('kg', 'Kilo'),
        ('unidad', 'Unidad'),
        ('g', 'Gramos'),
        ('l', 'Litros'),
        # agregar más opciones si es necesario
    )

    ingrediente = models.CharField(max_length=50)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    precio_aprox = models.DecimalField(max_digits=6, decimal_places=2)
    cantidad = models.DecimalField(max_digits=6, decimal_places=2)
    tipo_cantidad = models.CharField(max_length=10, choices=CANTIDAD_CHOICES)
    extra = models.TextField(blank=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)



class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
