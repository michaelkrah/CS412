from django.shortcuts import render
from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from .models import Profile, Listen, Song, Artist, PlaylistSong
from . forms import *
import json


from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.utils.timezone import make_aware


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib.auth import login
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect


from datetime import date

class ShowAllProfilesView(ListView):
  '''View to show all profiles'''

  model = Profile
  template_name = 'music_dashboard/show_all_profiles.html'
  context_object_name = 'profiles'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    request_user_profile = None

    if self.request.user.is_authenticated:
      try:
          request_user_profile = self.request.user.get_profile()
      except ObjectDoesNotExist:
          pass
       
    context['request_user_profile'] = request_user_profile
    return context
    


class ShowProfilePageView(DetailView):
  '''View to display an individual profile'''

  model = Profile
  template_name = 'music_dashboard/show_profile.html'
  context_object_name = 'profile'

  def get_context_data(self, **kwargs):
    '''checks if a profile page is friends with the logged in user'''
    context = super().get_context_data(**kwargs)
    request_user_profile = None
    request_user_friends = []

    profile = self.get_object()

    request_user_profile = None
    is_friend = False

    if self.request.user.is_authenticated:
        try:
            request_user_profile = self.request.user.get_profile()
            request_user_friends = request_user_profile.get_friends()

            is_friend = request_user_profile.is_friend(profile)
            print("is_friend", is_friend)
        except ObjectDoesNotExist:
            pass
        

    listens = profile.get_listens()

    listens = listens.order_by('-time')[:50]

    playlists = profile.get_playlists()



    context['request_user_profile'] = request_user_profile
    context['request_user_is_friend_with_profile'] = is_friend
    context['last_50_listens'] = listens
    context['playlists'] = playlists
    return context


class CreateProfileView(CreateView):
  '''View to create a profile and associate it with a user'''
  form_class = CreateProfileForm

  template_name = 'music_dashboard/create_profile.html'

  def form_valid(self, form: BaseModelForm) -> HttpResponse:

    user_form = UserCreationForm(self.request.POST)
    if user_form.is_valid():
        user = user_form.save()
        form.instance.user = user
        return super().form_valid(form)
    return self.form_invalid(form)

  def get_context_data(self, **kwargs: Any):
    context = super().get_context_data(**kwargs)
    context['user_creation_form'] = UserCreationForm()
    return context

  def get_success_url(self):
    '''return the url to redirect to'''
    return reverse("profile", args=[self.object.pk])


class SongsListView(ListView):
  '''View to display list of voter data.'''

  template_name = 'music_dashboard/songs.html'
  model = Song
  context_object_name = 'songs'

  paginate_by = 100

  def get_context_data(self, **kwargs: any):
      '''add data to the context object, including graphs'''

      context = super().get_context_data(**kwargs)

      return context
  
  def get_queryset(self) -> QuerySet[any]:
    qs = super().get_queryset()
    
    if "song_name" in self.request.GET:
      song_name = self.request.GET['song_name']
      if song_name:
        qs=qs.filter(name__iexact=song_name)
    
    if "artist_name" in self.request.GET:
      artist_name = self.request.GET['artist_name']
      if artist_name:
        qs=qs.filter(artist__name__icontains=artist_name)

    
    if "min_release_date" in self.request.GET:
      min_date = self.request.GET['min_release_date']
      if min_date:
          qs = qs.filter(release_date__gte=min_date)

    if "max_release_date" in self.request.GET:
        max_date = self.request.GET['max_release_date']
        if max_date:
            qs = qs.filter(release_date__lte=max_date)

    return qs



class CreateFriendView(LoginRequiredMixin, View):
  '''view to create a friend relationship between two profiles'''

  def dispatch(self, request, *args, **kwargs):
    
    if not request.user.is_authenticated:
      return redirect('main_page')

    profile = self.get_object()
    other_id = self.kwargs.get('other_pk')

    other_profile = get_object_or_404(Profile, pk=other_id)

    if profile.user != request.user:
      return redirect(reverse('main_page'))


    profile.add_friend(other_profile)


    profile_pk = self.get_object().pk
    return redirect(reverse('profile', kwargs={"pk":profile_pk}))

  def get_login_url(self):
    return reverse('main_page')
  
  def get_object(self):
    return get_object_or_404(Profile, user=self.request.user)



class ShowFeedView(ListView):
  '''view to display friend suggestions'''
  
  model = Profile
  template_name = 'music_dashboard/feed.html'
  context_object_name = 'profile'


class UploadData(View):
   
   def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main_page')
        
        profile = request.user.get_profile()

        uploaded_file = request.FILES.get('json_file')
        if not uploaded_file:
            return redirect('main_page')

        try:
            Listen.objects.all().delete()
            data = json.load(uploaded_file)
            for record in data:
              ms_played = record.get("msPlayed")
              if ms_played > 15000: # Only add a track if it's been played for longer than 30 seconds
                track_name = record.get("trackName", "Unknown Track")
                date=record.get("endTime")
                datetime_obj = datetime.strptime(date, "%Y-%m-%d %H:%M")
                datetime_obj = make_aware(datetime_obj)
                time_listened = ms_played
                song_db_results = list(Song.objects.filter(name=track_name))
                if len(song_db_results) == 0: # if the track doesn't exist in the database, we can't process it so skip
                  pass
                else:
                  song = song_db_results[0]
                  listen = Listen(song=song,
                                   profile=profile,
                                   time=datetime_obj,
                                   time_listened=time_listened
                                   )
                  listen_db_results = list(Listen.objects.filter(time=datetime_obj))
                  if len(listen_db_results) == 0:
                    listen.save()

                  else:
                     print("duplicate music, can't listen to two things at the same time")
                  

        except json.JSONDecodeError:
            return redirect('main_page')
        
        return redirect("profile", pk=profile.pk)



class ArtistDetail(DetailView):
  '''View to display an individual artist, showing all their songs and albums'''

  model = Artist
  template_name = 'music_dashboard/artist.html'
  context_object_name = 'artist'

  def get_context_data(self, **kwargs):
    '''gets necessary songs and albums linked to an artist to display on the detail view'''
    context = super().get_context_data(**kwargs)

    artist = self.object
        
    # Retrieve the songs for this artist
    songs = artist.get_songs() 
    albums = artist.get_albums()

    # Add songs to the context
    context['songs'] = songs
    context['albums'] = albums
    
    return context


class EditProfileView(LoginRequiredMixin, UpdateView):
  '''view to edit a profile'''
  model = Profile
  form_class = EditProfileForm
  template_name = 'music_dashboard/edit_profile_form.html'
  
  def get_success_url(self):
    profile_pk = self.get_object().pk
    return reverse("profile", kwargs={"pk": profile_pk})


  def dispatch(self, request, *args, **kwargs):
    profile = self.get_object()
    if profile.user != request.user:
        return redirect(reverse('main_page'))
    return super().dispatch(request, *args, **kwargs)
  
  
  def get_login_url(self):
    return reverse('main_page')
  
  def get_object(self):
    return get_object_or_404(Profile, user=self.request.user)

class CreatePlaylistView(LoginRequiredMixin, CreateView):
  '''view to create an initial playlist and correctly associate it with a profile'''

  form_class = CreatePlaylistForm
  template_name = 'music_dashboard/create_playlist_form.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    request_user_profile = None


    if self.request.user.is_authenticated:
      try:
          request_user_profile = self.request.user.get_profile()
      except ObjectDoesNotExist:
          pass

    context['request_user_profile'] = request_user_profile
    return context
  
  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    request_user_profile = None


    if self.request.user.is_authenticated:
      try:
          request_user_profile = self.request.user.get_profile()
      except ObjectDoesNotExist:
          print("Could not find profile")
          redirect("main_page")

    form.instance.profile = request_user_profile
    playlist = form.save()

    songs_to_add = self.request.POST.get('songs_to_add', '')
    if songs_to_add:
        song_names = [name.strip() for name in songs_to_add.split(',') if name.strip()]
        for song_name in song_names:
            # Retrieve or handle the song by its name
            try:
                song = Song.objects.get(name__iexact=song_name)
                PlaylistSong.objects.create(song=song, playlist=playlist)
            except Song.DoesNotExist:
                print(f"Song '{song_name}' does not exist.")


    return super().form_valid(form)
  
  def get_success_url(self):
    request_user_profile = None
    if self.request.user.is_authenticated:
      try:
          request_user_profile = self.request.user.get_profile()
      except ObjectDoesNotExist:
          print("Could not find profile")
          redirect("main_page")
      return reverse("profile", kwargs={"pk": request_user_profile.pk})

  def get_login_url(self):
    return reverse('main_page')
  
class UpdatePlaylistView(LoginRequiredMixin, UpdateView):
  '''view to update a playlist'''
  model = Playlist
  form_class = UpdatePlaylistForm
  template_name = 'music_dashboard/update_playlist_form.html'
  content_object_name = "playlist"

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
     
    context = super().get_context_data(**kwargs)
    playlist = self.get_object()
    context["profile"] = playlist.profile
    return context
  
  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    request_user_profile = None


    if self.request.user.is_authenticated:
      try:
          request_user_profile = self.request.user.get_profile()
      except ObjectDoesNotExist:
          print("Could not find profile")
          redirect("main_page")

    playlist = self.get_object()

    songs_to_add = self.request.POST.get('songs_to_add', '')
    if songs_to_add:
        song_names = [name.strip() for name in songs_to_add.split(',') if name.strip()]
        for song_name in song_names:
            try:
                song = Song.objects.get(name__iexact=song_name)
                PlaylistSong.objects.create(song=song, playlist=playlist)
            except Song.DoesNotExist:
                print(f"Song '{song_name}' does not exist.")


    return super().form_valid(form)

  def get_success_url(self):
      playlist = self.get_object()
      return reverse("playlist", kwargs={"pk": playlist.pk})


  def get_login_url(self):
    return reverse('main_page')



class PlaylistDetail(LoginRequiredMixin, DetailView):
  '''Detailed view of a playlist, can access controls to modify a playlist from here'''
  model = Playlist
  template_name = 'music_dashboard/show_playlist.html'
  context_object_name = 'playlist'

  def dispatch(self, request, *args, **kwargs):
    
    if not request.user.is_authenticated:
      return redirect('main_page')
    
    request_user_profile = None

    if self.request.user.is_authenticated:
      try:
          request_user_profile = self.request.user.get_profile()
      except ObjectDoesNotExist:
          pass

    
    playlist = self.get_object()
    profile = playlist.profile

    if not profile.is_friend(request_user_profile) and not request_user_profile.pk == profile.pk:
       return redirect('main_page')
    
  
    return super().dispatch(request, *args, **kwargs)
  



  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
     
    context = super().get_context_data(**kwargs)
    playlist = self.get_object()

    playlist_songs = playlist.get_songs()

    context["playlist_songs"] = playlist_songs
    context["profile"] = playlist.profile
    return context


  def get_login_url(self):
    return reverse('main_page')

class DeletePlaylistSong(LoginRequiredMixin, DeleteView):
  '''view to delete an entry in a playlist'''
  model = PlaylistSong
  template_name = "music_dashboard/delete_playlist_song.html"
  context_object_name = "playlist_song"

  def get_success_url(self):
    playlist_song = self.get_object()
    playlist = playlist_song.playlist
    return reverse("playlist", kwargs={"pk":playlist.pk})

  def dispatch(self, request, *args, **kwargs):
    playlist_song = self.get_object()
    profile = playlist_song.playlist.profile
    if profile.user != request.user:
        return redirect(reverse('main_page'))
    return super().dispatch(request, *args, **kwargs)

  def get_login_url(self):
    return reverse('main_page')

class DeletePlaylist(LoginRequiredMixin, DeleteView):
  '''view to delete an entire playlist'''
  model = Playlist
  template_name = "music_dashboard/delete_playlist.html"
  context_object_name = "playlist"

  def get_success_url(self):
    playlist = self.get_object()
    profile = playlist.profile
    return reverse("profile", kwargs={"pk":profile.pk})

  def dispatch(self, request, *args, **kwargs):
    playlist = self.get_object()
    profile = playlist.profile
    if profile.user != request.user:
        return redirect(reverse('main_page'))
    return super().dispatch(request, *args, **kwargs)

  def get_login_url(self):
    return reverse('main_page')

# update playlist view can be used to delete songs or add more through text box
# can also delete playlists from profile
# also should have a detailed playlist view

# stretch:
# each detailed song view should have a link to add to a playlist, will open up a new page where a playlist can be chosen
