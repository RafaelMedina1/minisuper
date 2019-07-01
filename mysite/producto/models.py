from django.db import models

# Create your models here.

class categoria (models.Model):
    nombre = models.CharField(max_length=60)

    def __str__(self):
         return self.nombre

class producto (models.Model):
    nombre = models.CharField(max_length=60)
    categoria = models.ForeignKey(categoria,blank=True, on_delete=models.CASCADE)
    precio = models.DecimalField(decimal_places=2,max_length=5, max_digits = 5)
    imagen = models.ImageField(upload_to='media')

    def __str__(self):
         return self.nombre

class stock (models.Model):
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

