from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
import random

# Create your views here.

from . models import *
from django.views.generic import ListView, DetailView, CreateView
from . forms import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib.auth import login


# Class-based view
class ShowAllView(ListView):
  '''View to show all articles'''

  model = Article
  template_name = 'blog/show_all.html'
  context_object_name = 'articles'

  def dispatch(self, *args, **kwargs):
    '''implement to add more tracing'''

    print(f"self.request.user={self.request.user}")


    # delegate to superclass version
    return super().dispatch(*args, **kwargs)


class RandomArticleView(DetailView):
  '''Detail view shows one instance of a model'''

  model = Article
  template_name = 'blog/article.html'
  context_object_name = 'article'

  def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
    '''Returns one instance of the object to show'''

    all_articles = Article.objects.all()  # Essentially select all

    return random.choice(all_articles)
  

class ArticleView(DetailView):
  '''Show one article by its primary key'''

  model = Article
  template_name = 'blog/article.html'
  context_object_name = 'article'



class CreateArticleView(LoginRequiredMixin, CreateView): # order of superclasses depends on order that they're evaluated
  '''View to create a new article instance.'''

  form_class = CreateArticleForm
  template_name = 'blog/create_article_form.html'

  def form_valid(self, form):
    '''add some debuggin statements'''

    print(f"Form data form.cleaned_data={form.cleaned_data}")

    user = self.request.user

    form.instance.user = user 

    return super().form_valid(form)
  
  def get_login_url(self):
    '''return the url required for login'''
    return reverse('login')


class RegistrationView(CreateView):
  '''Display and process the UserCreationForm for account registration'''

  template_name = 'blog/register.html'
  form_class = UserCreationForm

  def dispatch(self, *args, **kwargs): # Method that gets called first for any generic view
    '''Handle the User creation process'''

    # we handle the post request
    if self.request.POST:
      print(f"self.request.POST: {self.request.POST}")
      
      form = UserCreationForm(self.request.POST)

      if not form.is_valid():
        return super().dispatch(*args, **kwargs)

      user = form.save()
      print("user", user)

      login(self.request, user)

      return redirect(reverse('show_all'))

    # let the superclass CreateView handle the HTTP GET:

    return super().dispatch(*args, **kwargs)