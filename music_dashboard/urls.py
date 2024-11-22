from . import views
from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
  path(r'', views.SongsListView.as_view(), name="main_page"),

] 