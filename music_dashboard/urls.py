from . import views
from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
  path(r'', views.ShowAllProfilesView.as_view(), name="main_page"),
  path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name="profile"),
  path(r'logout/', auth_views.LogoutView.as_view(template_name='music_dashboard/logged_out.html'), name="music_dashboard_logout"),
  path(r'login/', auth_views.LoginView.as_view(template_name='music_dashboard/login.html'), name="music_dashboard_login"),
  path(r'create_profile/', views.CreateProfileView.as_view(), name="create_profile"),
] 