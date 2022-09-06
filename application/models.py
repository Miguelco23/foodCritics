from django.db import models

# Create your models here.

class Restaurantes(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    place_id = models.CharField(primary_key=True, max_length=100)
    rating = models.DecimalField(max_digits=2, decimal_places= 1)

class Comentarios(models.Model):
    place_id = models.CharField(primary_key=True, max_length=100)
    reviews = models.JSONField()