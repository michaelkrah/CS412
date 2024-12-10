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
  path(r'feed/', views.ShowFeedView.as_view(), name="feed"),
  path(r'profile/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name="music_dashboard_add_friend"),
  path(r'profile/upload_listens', views.UploadData.as_view(), name="music_dashboard_upload_listens"),
  path(r'songs', views.SongsListView.as_view(), name="songs"),
  path(r'artist/<int:pk>', views.ArtistDetail.as_view(), name="artist"),
  path(r'profile/update', views.EditProfileView.as_view(), name="edit_profile"),
  path(r'profile/create_playlist', views.CreatePlaylistView.as_view(), name="create_playlist"),
  path(r'profile/modify_playlist/<int:pk>', views.UpdatePlaylistView.as_view(), name="update_playlist"),
  path(r'playlist/<int:pk>', views.PlaylistDetail.as_view(), name="playlist"),
  path(r'delete_playlist/<int:pk>', views.DeletePlaylist.as_view(), name="delete_playlist"),
  path(r'delete_playlist_song/<int:pk>', views.DeletePlaylistSong.as_view(), name="delete_playlist_song"),

]