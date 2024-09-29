from django.shortcuts import render
import time
import random
from django.shortcuts import redirect


# Create your views here.

def main(request):
  '''A function to respond to the /main URL'''
  
  # this template will present the response
  template_name = "restaurant/main.html"

  context = {'current_time': time.ctime(),}

  # delegate response to the template:
  return render(request, template_name, context)

def order(request):
  '''A function to respond to the /order URL'''
  
  # this template will present the response
  template_name = "restaurant/order.html"

  context = {'special': "Cold cheese $17 ",
             'current_time': time.ctime(),}

  # delegate response to the template:
  return render(request, template_name, context)


def confirmation(request):
  '''A function to respond to the /confirmation URL'''

  # SHOULD NOT BE HERE UNLESS ALLOWED
  
  # this template will present the response
  template_name = "restaurant/confirmation.html"

  context = {'current_time': time.ctime(),}
  print("This is the request", request)
  print("This is the request", request.POST)

    # read the form data into python variables

  if request.POST:
      
      entire_order = []
      cost = {"Cheese Pizza": 10, "Pepperoni Pizza": 12, "Vegetable Pizza": 11, "Meat Pizza": 13, "special": 17}
      for item in request.POST:
         if item not in ['special_instructions', 'name', 
                         'phone', 'email', 'csrfmiddlewaretoken']:
            entire_order.append(item)

      total = 0
      for item in entire_order:
        if item in cost:
          total += cost[item]

      # read the form data into python variables:
      name = request.POST['name']
      email = request.POST['email']
      phone = request.POST['phone']
      special_instructions = request.POST['special_instructions']

      current_time = time.time()
      minutes = random.randint(30, 60) * 60
      ready_at = current_time + minutes
      ready_at = time.ctime(ready_at)

      context = {
        'current_time': time.ctime(),
        'name': name,
        'email': email,
        'phone': phone,
        'special_instructions': special_instructions,
        'entire_order': entire_order,
        'ready_at': ready_at,
        'total': total

      }

      return render(request, template_name, context)


  return redirect("order")