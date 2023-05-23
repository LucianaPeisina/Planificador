from msilib.schema import ListView
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

# models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cumpleanos = models.DateField(null=True, blank=True)
    gustos = models.TextField(blank=True)
    disgustos = models.TextField(blank=True)
    extra = models.TextField(blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()

class Miembro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='miembros')
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='miembros')


    nombre = models.CharField(max_length=50)
    edad = models.PositiveIntegerField()
    comida_preferida = models.CharField(max_length=150)
    gustos = models.TextField()
    disgustos = models.TextField()
    extra= models.TextField()

    


class ComidaManager(models.Manager):

    def lista_comidas(self, user):
        comidas = Comida.objects.filter(user=user, is_active=True, is_deleted=False)
        return comidas

    def obtener_running_comidas(self, user):
        running_comidas = Comida.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_comidas
    
    
class ComidaAbs(models.Model):

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Comida(ComidaAbs):

    miembros = models.ManyToManyField(Miembro, related_name='comidas')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comidas")
    titulo = models.CharField(max_length=200, unique=True)
    descripcion= models.TextField()
    TIPO_CHOICES = (
        ('D', 'Desayuno'),
        ('A', 'Almuerzo'),
        ('C', 'Cena'),
    )
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    inicio = models.DateTimeField()
    fin = models.DateTimeField()

    objects = ComidaManager()

    def __str__(self):
        return self.titulo

    def obtener_url(self):
        return reverse("comida-detalles", args=(self.id,))
    
    ingredientes = models.TextField()
    extra = models.TextField(blank=True)
    def __str__(self):
        return f"{self.titulo}"
    

    @property
    def obtener_html_url(self):
        url = reverse("comida-detalles", args=(self.id,))
        return f'<a href="{url}"> {self.titulo} </a>'

    
class Compra(models.Model): 
    fecha = models.DateField()
    comida = models.ForeignKey(Comida, on_delete=models.CASCADE)
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

    
  