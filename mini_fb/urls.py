"""mini facebook urls"""

from . import views
from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
  path(r'', views.ShowAllProfilesView.as_view(), name="show_all_profiles_view"), # views is imported file name, ShowAllView is created class, as_view is the static method that is a part of that class
  path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name="profile"),
  path(r'create_profile', views.CreateProfileView.as_view(), name="create_profile"),
  path(r'profile/create_status', views.CreateStatusMessageView.as_view(), name="create_status"),
  path(r'profile/update', views.UpdateProfileView.as_view(), name="update_profile"),
  path(r'status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name="delete_status"),
  path(r'status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name="update_status"),
  path(r'profile/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name="add_friend"),
  path(r'profile/friend_suggestions', views.ShowFriendSuggestionsView.as_view(), name="friend_suggestions"),
  path(r'profile/news_feed', views.ShowNewsFeedView.as_view(), name="news_feed"),

  path(r'login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='mini_fb_login'),
  path(r'logout/', auth_views.LogoutView.as_view(next_page='show_all_profiles_view'), name='mini_fb_logout'),

]