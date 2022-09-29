from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from .models import Comentarios, Restaurantes
from .models import plato

import googlemaps
import pprint

# Create your views here.\

API_KEY = 'AIzaSyBFw1F6ZxOpsbdWsuJJAH5YhRYXMlQALtA' #Identificador en la API de Google --- YOUR API KEY

gmaps = googlemaps.Client(key=API_KEY)

#Obtencion de restaurantes cerca de la ubicacion especificada en un radio de 1000 metros

places_result = gmaps.places_nearby(location='6.280506, -75.602769', radius='1000', type='restaurant', open_now=False)
#6.280506, -75.602769 / 6.246384, -75.593709

restaurantes = Restaurantes.objects.all()

puntos_user = 100

bonos = [40,50,50,25,75,40]

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

      rating_rest += rating

      comentarios.append({'author': name, 'time': time, 'text': text, 'rating': rating})

    rating_rest /= len(data_user) if len(data_user) > 0 else 1

  except:
    None


  #Creacion del restaurante en la base de datos, en caso de existir lo actualiza

  #restaurante_db = Restaurantes.objects.get_or_create(name= nombre, address= place['vicinity'], place_id = my_place_id, rating = rating_rest)
  #comentarios_db = Comentarios.objects.get_or_create(place_id = my_place_id, reviews = comentarios)


def home(request):
  global puntos_user

  return render(request, 'home.html', {'restaurants' : restaurantes, 'puntos' : puntos_user})

def enviarRestaurante(request):
  
  global puntos_user

  id = request.GET['restaurant']

  my_fields = ['name', 'price_level', 'rating', 'formatted_address', 'user_ratings_total', 'review', 'place_id']

  restaurante = Restaurantes.objects.get(place_id=id)
  comentarios = Comentarios.objects.get(place_id=id)
  
  if request.POST:
    author = request.POST['name_user']
    text = request.POST['comentario_user']
    rating = request.POST['puntuacion_user']

    message = f'nombre: {author}\ncomentario: {text}\npuntuacion: {rating}'

    print(message)

    comentario = {"author" : author, "time" : "No definido", "text" : text, "rating" : rating}
    
    comentarios.reviews.append(comentario)

    almacenar_comentarios = []

    for coment in comentarios.reviews:
      almacenar_comentarios.append(coment)

    puntos_user += 10

    Comentarios.objects.filter(place_id = id).update(reviews = almacenar_comentarios)

  return render(request, 'restaurante.html', {'place_id' : id, 'restaurante' : restaurante, 'comentarios' : comentarios, 'puntos' : puntos_user})


def mapa(request):
  global puntos_user

  return render(request, 'mapa.html', {'puntos' : puntos_user})

def puntos(request):

  global puntos_user, bonos

  return render(request, 'puntos.html', {'puntos' : puntos_user, 'bonos': bonos})



def puntuacionTotal(comentarios):
  puntuacion_total = 0

  for datos in comentarios.reviews:

    print(datos)

    rating = int(datos['rating'])

    puntuacion_total += rating
  
  puntuacion_total /= len(comentarios.reviews) if len(comentarios.reviews) > 0 else 1

  return puntuacion_total
from django.utils.datastructures import MultiValueDictKeyError

def menu(request):
  global puntos_user

  id = request.GET['menu']
  menu = plato.objects.filter(restaurante=id)



  return render(request, 'menu.html', {'place_id' : id , 'menu' : menu, 'puntos' : puntos_user})
  