from dataclasses import fields
from django.shortcuts import render
from django.http import HttpRequest
from .models import Restaurantes

import googlemaps
import pprint

# Create your views here.\

API_KEY = 'AIzaSyBFw1F6ZxOpsbdWsuJJAH5YhRYXMlQALtA' #Identificador en la API de Google --- YOUR API KEY

gmaps = googlemaps.Client(key=API_KEY)

#Obtencion de restaurantes cerca de la ubicacion especificada en un radio de 1000 metros
places_result = gmaps.places_nearby(location='6.246384, -75.593709', radius='1000', type='restaurant', open_now=False)
#6.280506, -75.602769
restaurantes = Restaurantes.objects.all()

#Almacenar los datos que seran usados de los restaurantes en la variable restaurantes

for place in places_result['results']:

  my_place_id = place['place_id']

  nombre = place['name']

  #Campos que seran almacenados en la base de datos
  parametros_datos = gmaps.place(place_id=my_place_id, fields= ['rating'], language="ES")

  parametros_reviews = gmaps.place(place_id=my_place_id, fields=['review'], language="ES")


  #Comentarios hechos por usuarios
  comentarios = []

  #Valoracion general del restaurante
  rating_rest = 0

  #Almacena los comentarios del restaurante dentro de la variable comentarios
  try:
    data_user = parametros_reviews['result']['reviews']

    #Por cada comentario sacado de la API de google, toma los datos necesarios
    for data in data_user:
      name = data['author_name']
      time = data['relative_time_description']
      text = data['text']
      rating = data['rating']

      comentarios.append({'name': name, 'time': time, 'text': text, 'rating': rating})
    

    rating_user = parametros_datos['result']['rating']

    rating_rest += rating_user

  except:
    None

  fields_db = {"rating": rating_rest,
                "reviews": comentarios
              }

  #Creacion del restaurante en la base de datos, en caso de existir lo actualiza
  restaurante_db = Restaurantes.objects.update_or_create(name= nombre, address= place['vicinity'], place_id = my_place_id, review = fields_db)

def home(request):
  return render(request, 'home.html', {'restaurants' : restaurantes})

def enviarRestaurante(request):

  id = request.GET['restaurant']

  my_fields = ['name', 'price_level', 'rating', 'formatted_address', 'user_ratings_total', 'review', 'place_id']

  restaurante = Restaurantes.objects.get(place_id=id)

  return render(request, 'restaurante.html', {'place_id' : id, 'restaurante' : restaurante})


def mapa(request):

  return render(request, 'mapa.html')

