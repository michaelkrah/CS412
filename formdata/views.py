from django.shortcuts import render, redirect

# Create your views here.

def show_form(request):
  """Show HTML form to the client"""
  
  template_name = 'formdata/form.html'

  return render(request, template_name)

def submit(request):
  """Handle form submission, read out form data, generate a response"""

  template_name = 'formdata/confirmation.html'

  print(request)
  # read the form data into python variables

  if request.POST:

    # read the form data into python variables:
    name = request.POST['name']
    favorite_color = request.POST['favorite_color']

    # package the data up to be used in response
    context = {
      'name': name,
      'favorite_color': favorite_color,
    }

    return render(request, template_name, context)


  return redirect("show_form")