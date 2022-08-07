from dataclasses import fields
from django.shortcuts import render
from django.http import HttpRequest

import googlemaps
import pprint

# Create your views here.\

API_KEY = 'AIzaSyBFw1F6ZxOpsbdWsuJJAH5YhRYXMlQALtA' #Identificador en la API de Google

gmaps = googlemaps.Client(key=API_KEY)

places_result = gmaps.places_nearby(location='6.280478,-75.602796', radius='1000', type='restaurant', open_now=False)

restaurantes = []

for place in places_result['results']:

  my_place_id = place['place_id']

  my_fields = ['name', 'price_level', 'rating', 'formatted_address']

  place_details = gmaps.place(place_id= my_place_id,fields = my_fields)

  restaurantes.append(place_details)


"""https://maps.googleapis.com/maps/api/place/photo
  ?maxwidth=400
  &photo_reference=AeJbb3fTnjebcueWbwFxCU60yJ6tpjrhF6W8Tj8hNu_s3S5G4-hgkNz7046guY4Q3sf59exPNfBrILImvjy45QQDQoXeg17LbLFOeYpX16DiUKJ9ZdsM6hpUM1IOEI4PrqoeCl3pf7pfuhSYCwwRV3aEq8t21rZKi0QNPUnogcmBdmvg7b1h
  &key=API_KEY"""

def home(request):
    return render(request, 'home.html', {'restaurants' : restaurantes})