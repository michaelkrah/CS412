"""mini facebook urls"""

from . import views
from django.urls import path
from django.conf import settings

urlpatterns = [
  path(r'', views.ShowAllProfilesView.as_view(), name="show_all_profiles_view"), # views is imported file name, ShowAllView is created class, as_view is the static method that is a part of that class
  path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name="profile"),
  path(r'create_profile', views.CreateProfileView.as_view(), name="create_profile"),
  path(r'profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name="create_status"),
  path(r'profile/<int:pk>/update', views.UpdateProfileView.as_view(), name="update_profile"),
  path(r'status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name="delete_status"),
    path(r'status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name="update_status"),



]