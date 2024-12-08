from django.shortcuts import render
from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile
from . forms import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib.auth import login
from django.urls import reverse

from datetime import date

class ShowAllProfilesView(ListView):
  '''View to show all profiles'''

  model = Profile
  template_name = 'music_dashboard/show_all_profiles.html'
  context_object_name = 'profiles'


class ShowProfilePageView(DetailView):
  '''View to display an individual profile'''

  model = Profile
  template_name = 'music_dashboard/show_profile.html'
  context_object_name = 'profile'

class CreateProfileView(CreateView):
  '''View to create a profile and associate it with a user'''
  form_class = CreateProfileForm

  template_name = 'music_dashboard/create_profile.html'

  def form_valid(self, form: BaseModelForm) -> HttpResponse:

    user_form = UserCreationForm(self.request.POST)
    if user_form.is_valid():
        user = user_form.save()
        form.instance.user = user
        return super().form_valid(form)
    return self.form_invalid(form)

  def get_context_data(self, **kwargs: Any):
    context = super().get_context_data(**kwargs)
    context['user_creation_form'] = UserCreationForm()
    return context

  def get_success_url(self):
    '''return the url to redirect to'''
    return reverse("profile", args=[self.object.pk])


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
