## /Step 4 
## hw/urls.py
## description: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views

# Create a list of URLs for this app:
urlpatterns = [
  path(r'', views.home, name="home"), ## First URL
  path(r'about', views.about, name="about"), ## First URL

]