## /Step 4 
## hw/urls.py
## description: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views

# Create a list of URLs for this app:
urlpatterns = [
  path(r'', views.quote, name="quote"), 
  path(r'about', views.about, name="about"), 
  path(r'show_all', views.show_all, name="show_all"), 


]