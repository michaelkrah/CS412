from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
import random

# Create your views here.

from . models import *
from django.views.generic import ListView, DetailView

# Class-based view
class ShowAllView(ListView):
  '''View to show all articles'''

  model = Article
  template_name = 'blog/show_all.html'
  context_object_name = 'articles'



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

