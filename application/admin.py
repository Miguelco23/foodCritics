from django.contrib import admin
from .models import Restaurantes, Comentarios, plato, Categorias

# Register your models here.

admin.site.register(Restaurantes)
admin.site.register(Comentarios)
admin.site.register(plato)
admin.site.register(Categorias)


