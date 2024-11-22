from django.shortcuts import render

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

from datetime import date

class SongsListView(ListView):
  '''View to display list of voter data.'''

  template_name = 'music_dashboard/songs.html'
  model = Profile
  context_object_name = 'voters'

  paginate_by = 100

  def get_context_data(self, **kwargs: any):
      '''add data to the context object, including graphs'''

      context = super().get_context_data(**kwargs)

      birth_years = [i for i in range(1924, 2007)]
      context['birth_years'] = birth_years

      return context
