from . import views
from django.urls import path
from django.conf import settings

urlpatterns = [
  path(r'', views.ShowAllView.as_view(), name="show_all"), # views is imported file name, ShowAllView is created class, as_view is the static method that is a part of that class
]