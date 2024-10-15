from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from . models import *
from django.views.generic import ListView, DetailView, CreateView
from . forms import *
from django.urls import reverse

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

class CreateProfileView(CreateView):
  '''View for users to create new profiles'''

  form_class = CreateProfileForm
  template_name = 'mini_fb/create_profile_form.html'

  # def form_valid(self, form: BaseModelForm) -> HttpResponse:
  #   profile = Profile.objects.get(pk=self.kwargs['pk'])
  #   return super().form_valid(form)

  def get_success_url(self):
    '''return the url to redirect to'''
    return reverse("profile", args=[self.object.pk])
  

class CreateStatusMessageView(CreateView):
  '''View to create new status messages'''

  form_class = CreateStatusMessageForm
  template_name = 'mini_fb/create_status_form.html'


  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    profile = Profile.objects.get(pk=self.kwargs['pk'])
    form.instance.profile = profile
    return super().form_valid(form)

  def get_success_url(self):
    '''return the url to redirect to'''
    return reverse("profile", kwargs=self.kwargs)


  def get_context_data(self, **kwargs: any) -> dict[str, any]:
      '''build dict of key value pairs'''
      # get the super class version of context data
      context = super().get_context_data(**kwargs)

      # find the article with the PK from the URL
      # self.kwargs['pk'] is finding the article PK from the URL
      profile = Profile.objects.get(pk=self.kwargs['pk'])

      # add the article to the context data
      context['profile'] = profile

      return context