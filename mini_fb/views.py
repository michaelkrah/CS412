from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from . models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from . forms import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib.auth import login


from django.shortcuts import get_object_or_404, redirect


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
  

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
  '''View to create new status messages'''

  form_class = CreateStatusMessageForm
  template_name = 'mini_fb/create_status_form.html'


  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    profile = self.get_object()
    form.instance.profile = profile
    print(f"Form data form.cleaned_data={form.cleaned_data}")

    sm = form.save()
    files = self.request.FILES.getlist('files')
    print("Files for images", files)
    for file in files:
      print("before creation", sm.pk)
      img = Image()
      img.status_message = sm
      img.image_file = file
      img.save()
      print("After", img)


    return super().form_valid(form)
  
  def dispatch(self, request, *args, **kwargs):
    
    profile = self.get_object()
    if profile.user != request.user:
        return redirect(reverse('show_all_profiles_view'))
    return super().dispatch(request, *args, **kwargs)

  
  def get_login_url(self):
    return reverse('show_all_profiles_view')

  def get_success_url(self):
    '''return the url to redirect to'''
    profile_pk = self.get_object().pk
    return reverse("profile", kwargs={"pk": profile_pk})

  def get_context_data(self, **kwargs: any) -> dict[str, any]:
      '''build dict of key value pairs'''
      # get the super class version of context data
      context = super().get_context_data(**kwargs)

      # find the article with the PK from the URL
      # self.kwargs['pk'] is finding the article f from the URL
      profile = self.get_object()

      # add the article to the context data
      context['profile'] = profile

      return context
  
  def get_object(self):
    return get_object_or_404(Profile, user=self.request.user)
  

class UpdateProfileView(LoginRequiredMixin, UpdateView):
  '''view to update a profile'''
  model = Profile
  form_class = UpdateProfileForm
  template_name = 'mini_fb/update_profile_form.html'
  
  def get_success_url(self):
    profile_pk = self.get_object().pk
    return reverse("profile", kwargs={"pk": profile_pk})
    

  def dispatch(self, request, *args, **kwargs):
    profile = self.get_object()
    if profile.user != request.user:
        return redirect(reverse('show_all_profiles_view'))
    return super().dispatch(request, *args, **kwargs)
  
  
  def get_login_url(self):
    return reverse('show_all_profiles_view')
  
  def get_object(self):

    return get_object_or_404(Profile, user=self.request.user)

    # profile = self.get_object()
    # user = User.objects.filter(profile=profile)
    # return super().get_object(queryset)



class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
  '''view to delete a status message'''
  model = StatusMessage
  template_name = "mini_fb/delete_status_form.html"
  context_object_name = "status_message"

  def get_success_url(self):

    profile = self.object.profile
    return reverse("profile", kwargs={"pk":profile.pk})
  

  def dispatch(self, request, *args, **kwargs):
    statusmessage = self.get_object()
    profile = statusmessage.profile
    if profile.user != request.user:
        return redirect(reverse('show_all_profiles_view'))
    return super().dispatch(request, *args, **kwargs)

  def get_login_url(self):
    return reverse('show_all_profiles_view')
  
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
  '''view to update a status message'''
  model = StatusMessage
  form_class = UpdateStatusMessageForm
  template_name = "mini_fb/update_status_form.html"
  content_object_name = "status_message"

  def get_success_url(self):

    profile = self.object.profile
    return reverse("profile", kwargs={"pk":profile.pk})
  

  def dispatch(self, request, *args, **kwargs):
    profile = self.get_object().profile
    if profile.user != request.user:
        return redirect(reverse('show_all_profiles_view'))
    return super().dispatch(request, *args, **kwargs)


  def get_login_url(self):
    return reverse('show_all_profiles_view')


class CreateFriendView(LoginRequiredMixin, View):
  '''view to create a friendship between two profiles'''


  def dispatch(self, request, *args, **kwargs):
      profile = self.get_object()
      other_id = self.kwargs.get('other_pk')

      other_profile = get_object_or_404(Profile, pk=other_id)

      if profile.user != request.user:
        return redirect(reverse('show_all_profiles_view'))


      profile.add_friend(other_profile)


      profile_pk = self.get_object().pk
      return redirect(reverse('profile', kwargs={"pk":profile_pk}))

  def get_login_url(self):
    return reverse('show_all_profiles_view')
  
  def get_object(self):
    return get_object_or_404(Profile, user=self.request.user)

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
  '''view to display friend suggestions'''
  
  model = Profile
  template_name = 'mini_fb/friend_suggestions.html'
  context_object_name = 'profile'


  def dispatch(self, request, *args, **kwargs):
    profile = self.get_object()
    if profile.user != request.user:
        return redirect(reverse('show_all_profiles_view'))
    return super().dispatch(request, *args, **kwargs)

  def get_login_url(self):
    return reverse('show_all_profiles_view')
  
  def get_object(self):
    return get_object_or_404(Profile, user=self.request.user)

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
  '''view to display friend suggestions'''
  
  model = Profile
  template_name = 'mini_fb/news_feed.html'
  context_object_name = 'profile'


  def dispatch(self, request, *args, **kwargs):
    profile = self.get_object()
    if profile.user != request.user:
        return redirect(reverse('show_all_profiles_view'))
    return super().dispatch(request, *args, **kwargs)

  def get_login_url(self):
    return reverse('show_all_profiles_view')


  def get_object(self):
    return get_object_or_404(Profile, user=self.request.user)
