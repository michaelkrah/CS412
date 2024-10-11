from . import views
from django.urls import path
from django.conf import settings

urlpatterns = [
  path(r'', views.RandomArticleView.as_view(), name="random"), # views is imported file name, ShowAllView is created class, as_view is the static method that is a part of that class
  path(r'show_all', views.ShowAllView.as_view(), name="show_all"),
  path(r'article/<int:pk>', views.ArticleView.as_view(), name="article"), # Can visit a specific article
]