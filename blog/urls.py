from . import views
from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views # login and logout views

urlpatterns = [
  path(r'', views.RandomArticleView.as_view(), name="random"), # views is imported file name, ShowAllView is created class, as_view is the static method that is a part of that class
  path(r'show_all', views.ShowAllView.as_view(), name="show_all"),
  path(r'article/<int:pk>', views.ArticleView.as_view(), name="article"), # Can visit a specific article
  path(r'create_article', views.CreateArticleView.as_view(), name="create_article"),

  path(r'login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
  path(r'logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'),

  path(r'register/', views.RegistrationView.as_view(), name='register'),


]