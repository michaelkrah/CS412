## restaurant/urls.py
## description: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views

# Create a list of URLs for this app:
urlpatterns = [

  path(r'', views.main, name="main"), 
  path(r'order', views.order, name="order"), 
  path(r'confirmation', views.confirmation, name="confirmation"), 
  # path(r'about', views.about, name="about"), 
  # path(r'show_all', views.show_all, name="show_all"), 

]