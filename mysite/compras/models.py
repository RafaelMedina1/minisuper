from django.db import models
from usuario.models import usuario
from producto.models import producto

# Create your models here.

class compra(models.Model):
    user = models.ForeignKey(usuario, on_delete=models.CASCADE)
    product = models.ForeignKey(producto,  on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_total = models.DecimalField(decimal_places=2,max_length=5,max_digits = 5)
    fecha = models.DateTimeField(auto_now_add=True)

