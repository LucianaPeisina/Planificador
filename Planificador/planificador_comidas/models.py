from msilib.schema import ListView
from django.contrib.auth.models import User
from django.db import models
from datetime import date, datetime
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

# Registramos los modelos
class Perfil(models.Model):
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    cumpleanos = models.DateField(null=True, blank=True)
    gustos = models.TextField(blank=True)
    disgustos = models.TextField(blank=True)
    extra = models.TextField(blank=True)

    # def __str__(self):
    #     return "%s %s %s" % (self.user, self.cumpleanos, self.gustos,)

#    list_display = ('user', 'cumpleanos', 'gustos')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()

class Miembro(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='miembros')
    cumpleanos = models.DateField(default=datetime.today)
    nombre = models.CharField(max_length=50)
    edad = models.PositiveIntegerField()
    comida_preferida = models.CharField(max_length=150)
    gustos = models.TextField()
    disgustos = models.TextField()
    extra = models.TextField()

    def __str__(self):
        return "%s %s %s" % (self.usuario, self.nombre, self.edad)

    list_display = ('usuario', 'nombre', 'edad')



class ComidaManager(models.Manager):

    def get_all_events(self, user):
        events = Comida.objects.filter(user=user, is_active=True, is_deleted=False)
        return events

    def get_running_events(self, user):
        running_events = Comida.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            fin__gte=datetime.now().date(),
        ).order_by("inicio")
        return running_events
    
class ComidaAbstract(models.Model):


    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Comida(ComidaAbstract):
    miembros = models.ManyToManyField(Miembro, related_name='comidas')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comidas")
    titulo = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField()
    TIPO_CHOICES = (
        ('D', 'Desayuno'),
        ('A', 'Almuerzo'),
        ('C', 'Cena'),
    )
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    ingredientes = models.TextField()
    extra = models.TextField(blank=True)
    inicio = models.DateTimeField()
    fin = models.DateTimeField()

    objects = ComidaManager()

    def __str__(self):
        return self.titulo

    def obtener_url(self):
        return reverse("detalle_comida", args=(self.id,))

    @property
    def obtener_html_url(self):
        url = reverse("detalle_comida", args=(self.id,))
        return f'<a href="{url}">{self.titulo}</a>'

class Compra(models.Model): 
    fecha = models.DateField()
    comida = models.ForeignKey(Comida, on_delete=models.CASCADE, null=True)
    extra = models.TextField(blank=True)

    def costo_total(self):
        return sum(elemento.precio_aprox * elemento.cantidad for elemento in self.elementocompra_set.all())
    
    def __str__(self):
        return f"Compra del {self.fecha}"
    
    

class ElementoCompra(models.Model):
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE, null=True)
    
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

    
  