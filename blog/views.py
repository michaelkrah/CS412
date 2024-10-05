from django.shortcuts import render

# Create your views here.

from . models import *
from django.views.generic import ListView

# Class-based view
class ShowAllView(ListView):
  '''View to show all articles'''

  model = Article
  template_name = 'blog/show_all.html'
  context_object_name = 'articles'

