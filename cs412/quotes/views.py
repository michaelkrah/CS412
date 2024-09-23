## /Step 5
## hw/views.py
## discription: the logic to handle URL requests
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
# Create your views here.

# def home(request):
#   ''' A function to respond to the /hw URL 
#   '''

#   response_text = f'''
#   <html>
#   <h1>Hello, world!</h1>
#   <p>This is our first django web page!</p>
#   <hr>
#   This page was generated at {time.ctime()}.
#   '''

#   return HttpResponse(response_text)

quotes_list = ["It is good to love many things, for therein lies the true strength, and whosoever loves much performs much, and can accomplish much, and what is done in love is well done.", 
              "I dream my painting and I paint my dream.",
              "Be clearly aware of the stars and infinity on high. Then life seems almost enchanted after all.",
              "...and then, I have nature and art and poetry, and if that is not enough, what is enough?",
              "There is nothing more truly artistic than to love people.",
              "A great fire burns within me, but no one stops to warm themselves at it, and passers-by only see a wisp of smoke",
              "I don't know anything with certainty, but seeing the stars makes me dream.",
              "Normality is a paved road: It’s comfortable to walk,﻿ but no flowers grow on it.",
              "I put my heart and soul into my work, and I have lost my mind in the process.",
              "I often think that the night is more alive and more richly colored than the day.",
              "The sadness will last forever.",
              "It is looking at things for a long time that ripens you and gives you a deeper meaning.",
              "There is peace even in the storm",
              "I’m trying now to exaggerate the essence of things, and to deliberately leave vague what’s obvious.",]
images_list = ["https://cdn.britannica.com/36/69636-050-81A93193/Self-Portrait-artist-panel-board-Vincent-van-Gogh-1887.jpg?w=300",
              "https://personalinterpretations.com/wp-content/uploads/2018/07/vincent-van-gogh-self-portrait-with-bandaged-ear.jpg",
              "https://collectionapi.metmuseum.org/api/collection/v1/iiif/436532/1671316/main-image",
              "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Vincent_van_Gogh_-_Self-Portrait_-_Google_Art_Project.jpg/540px-Vincent_van_Gogh_-_Self-Portrait_-_Google_Art_Project.jpg"
              ]

def quote(request):
  '''A function to respond to the /quotes URL'''
  
  # this template will present the response
  template_name = "quotes/quote.html"

  # dictionary of context variables
  context = {
    'chosen_quote': '"' + quotes_list[random.randint(0, len(quotes_list)-1)] + '"',
    'chosen_image': images_list[random.randint(0, len(images_list)-1)],
    'current_time': time.ctime(),
    'letter1' : chr(random.randint(65,90)),
    'letter2' : chr(random.randint(65,90)),
    'letter3' : chr(random.randint(65,90)),
    'number' : random.randint(1,10),
  }

  # delegate response to the template:
  return render(request, template_name, context)

def about(request):
  '''A function to respond to the /quotes/about URL'''
  
  # this template will present the response
  template_name = "quotes/about.html"

  # dictionary of context variables
  context = {
    'current_time': time.ctime(),
  }

  # delegate response to the template:
  return render(request, template_name, context)

def show_all(request):
  '''A function to respond to the /quotes/show_all URL'''

  # this template will present the response
  template_name = "quotes/show_all.html"


  # dictionary of context variables
  context = {
    'quotes_list': quotes_list,
    'images_list': images_list,
    'current_time': time.ctime(),
  }
  # delegate response to the template:
  return render(request, template_name, context)
