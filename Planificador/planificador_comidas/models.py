from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cumpleanos = models.DateField(blank=True, null=True)
    gustos = models.TextField(blank=True)
    disgustos = models.TextField(blank=True)
    extra = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    
    


class Miembro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='miembros')
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    edad = models.PositiveIntegerField()
    comida_preferida = models.CharField(max_length=150)
    gustos = models.TextField()
    disgustos = models.TextField()
    extra = models.TextField(blank=True)
    def __str__(self):
        return self.nombre
    
    
class Menu(models.Model):
    miembros = models.ManyToManyField(Miembro, related_name='menus')
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
    extra = models.TextField(blank=True)
    def __str__(self):
        return f"{self.titulo} ({self.fecha})"

    
class Compra(models.Model): 
    fecha = models.DateField()
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    extra = models.TextField(blank=True)

    def costo_total(self):
        return sum(elemento.precio_aprox * elemento.cantidad for elemento in self.elementocompra_set.all())
    
    def __str__(self):
        return f"Compra del {self.fecha}"
    
    

class ElementoCompra(models.Model):
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE)
    
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

    def __str__(self):
        return f"{self.ingrediente} - {self.cantidad} {self.tipo_cantidad}"

    
    
    
    



