from dataclasses import fields
from django.shortcuts import render
from django.http import HttpRequest

import googlemaps
import pprint

# Create your views here.\

API_KEY = 'AIzaSyBFw1F6ZxOpsbdWsuJJAH5YhRYXMlQALtA' #Identificador en la API de Google --- YOUR API KEY

gmaps = googlemaps.Client(key=API_KEY)

#Obtencion de restaurantes cerca de la ubicacion especificada en un radio de 1000 metros

places_result = gmaps.places_nearby(location='6.181976, -75.575254', radius='1000', type='restaurant', open_now=False)

restaurantes = []

#Almacenar los datos que seran usados de los restaurantes en la variable restaurantes

for place in places_result['results']:

  my_place_id = place['place_id']

  my_fields = ['name', 'price_level', 'rating', 'formatted_address', 'user_ratings_total', 'review', 'place_id']

  place_details = gmaps.place(place_id= my_place_id,fields = my_fields, language='ES')

  restaurantes.append(place_details)

def home(request):
  return render(request, 'home.html', {'restaurants' : restaurantes})

def enviarRestaurante(request):

  id = request.GET['restaurant']

  my_fields = ['name', 'price_level', 'rating', 'formatted_address', 'user_ratings_total', 'review', 'place_id']

  restaurante = gmaps.place(place_id = id, fields= my_fields, language='ES')

  return render(request, 'restaurante.html', {'place_id' : id, 'restaurante' : restaurante})
