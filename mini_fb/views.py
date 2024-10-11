from django.shortcuts import render

# Create your views here.

from . models import *
from django.views.generic import ListView, DetailView

# Class-based view
class ShowAllProfilesView(ListView):
  '''View to show all profiles'''

  model = Profile
  template_name = 'mini_fb/show_all_profiles.html'
  context_object_name = 'profiles'


class ShowProfilePageView(DetailView):
  '''View to display an individual profile'''

  model = Profile
  template_name = 'mini_fb/show_profile.html'
  context_object_name = 'profile'

