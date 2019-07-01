from django.contrib import admin

from .models import *
# Register your models here.


admin.site.register(categoria)


#crear columnas en la vista 
class ProductAdmin(admin.ModelAdmin):
    model = producto
    list_display = ['nombre','categoria', 'precio']



class StockAdmin(admin.ModelAdmin):
    model = stock
    list_display = ['producto','cantidad']

admin.site.register(producto, ProductAdmin)
admin.site.register(stock, StockAdmin)