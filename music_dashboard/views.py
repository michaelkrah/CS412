# Views file for music_dashboard project

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

import plotly
import plotly.graph_objects as go
from collections import Counter



from datetime import date

class ShowAllProfilesView(ListView):
  '''View to show all profiles'''

  model = Profile
  template_name = 'music_dashboard/show_all_profiles.html'
  context_object_name = 'profiles'

  def get_context_data(self, **kwargs):
    '''get context data to attach user profile to main page view'''
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
    '''checks if a profile page is friends with the logged in user, also creates and adds pie chart of different genres'''
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
    listens_time = listens.order_by('-time')[:50]
    playlists = profile.get_playlists()

    genres_count = Counter(listen.song.artist.get_genre() for listen in listens)
    genres_count = {genre: count for genre, count in genres_count.items() if count >= 10}
    labels = list(genres_count.keys())
    values = list(genres_count.values())

    fig = go.Pie(labels=labels, values=values)
    pie_div = pie_div = plotly.offline.plot(
    {
        'data': [fig],
        'layout': {
            'paper_bgcolor': '#121212',  
            'plot_bgcolor': '#121212',  
            'font': {'color': 'white'} 
        }
    },
    auto_open=False,
    output_type='div'
)


    context['pie_div'] = pie_div

    context['request_user_profile'] = request_user_profile
    context['request_user_is_friend_with_profile'] = is_friend
    context['last_50_listens'] = listens_time
    context['playlists'] = playlists
    return context


class CreateProfileView(CreateView):
  '''View to create a profile and associate it with a user'''
  form_class = CreateProfileForm

  template_name = 'music_dashboard/create_profile.html'

  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    '''associates a user object with a profile object correctly'''
    user_form = UserCreationForm(self.request.POST)
    if user_form.is_valid():
        user = user_form.save()
        form.instance.user = user
        return super().form_valid(form)
    return self.form_invalid(form)

  def get_context_data(self, **kwargs: Any):
    '''attaches user creation form to html page to create a profile and user'''
    context = super().get_context_data(**kwargs)
    context['user_creation_form'] = UserCreationForm()
    return context

  def get_success_url(self):
    '''return the url to redirect to'''
    return reverse("profile", args=[self.object.pk])


class SongsListView(ListView):
  '''View to display list of songs data along with artist and album.'''

  template_name = 'music_dashboard/songs.html'
  model = Song
  context_object_name = 'songs'

  paginate_by = 100

  def get_context_data(self, **kwargs: any):

      context = super().get_context_data(**kwargs)

      return context
  
  def get_queryset(self) -> QuerySet[any]:
    '''filters by specific attributes as required, depending on what is included in the url'''
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
    '''checks to make sure the user is verified and checks before creating a friend to ensure necessary conditions are met'''
    
    if not request.user.is_authenticated:
      return redirect('main_page')

    profile = self.get_object()
    other_id = self.kwargs.get('other_pk')

    other_profile = get_object_or_404(Profile, pk=other_id)

    if profile.user != request.user:
      return redirect(reverse('main_page'))


    profile.add_friend(other_profile)

    profile_pk = self.get_object().pk
    return redirect(reverse('profile', kwargs={"pk":other_profile.pk}))

  def get_login_url(self):
    '''redirect user that isn't logged in'''
    return reverse('main_page')
  
  def get_object(self):
    return get_object_or_404(Profile, user=self.request.user)



class ShowFeedView(LoginRequiredMixin, DetailView):
  '''view to display friend suggestions'''
  
  model = Profile
  template_name = 'music_dashboard/feed.html'
  context_object_name = 'profile'

  def get_context_data(self, **kwargs: any):
    '''get list of recently listened to songs for each friend of the user'''
    context = super().get_context_data(**kwargs)

    request_user_profile = None
    try:
      request_user_profile = self.request.user.get_profile()
      request_user_friends = request_user_profile.get_friends()

    except ObjectDoesNotExist:
      pass
    
    recent_listens = []

    for friend in request_user_friends:
      listens = friend.get_listens()
      listens = listens.order_by('-time')[:10] 
      recent_listens.extend(listens) 

    recent_listens = sorted(recent_listens, key=lambda x: x.time, reverse=True)

    context['recent_listens'] = recent_listens

    return context

  def dispatch(self, request, *args, **kwargs):
    '''makes sure the profile is correctly associated with the logged in user'''
    profile = self.get_object()
    
    if profile.user != request.user:
        return redirect(reverse('main_page'))
    
    return super().dispatch(request, *args, **kwargs)

  def get_login_url(self):
    '''redirects a user that is not logged in'''
    return reverse('main_page')
  
  
  def get_object(self):
    return get_object_or_404(Profile, user=self.request.user)






class UploadData(View):
  '''function to upload spotify json data to the user's profile
  will take a spotify file of listening data from their website a process each listen
  this creates a listening object in Django's ORM and associates it with a song, artist, and album'''
  def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main_page')
        
        profile = request.user.get_profile()

        uploaded_file = request.FILES.get('json_file')
        if not uploaded_file:
            return redirect('main_page')

        try:
            data = json.load(uploaded_file)
            for record in data:
              ms_played = record.get("msPlayed")
              if ms_played > 15000: # Only add a track if it's been played for longer than 15 seconds, otherwise it was likely just skipped
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
                  listen_db_results = list(Listen.objects.filter(time=datetime_obj, song__name=song.name))
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
    '''redirect the user when successful'''
    profile_pk = self.get_object().pk
    return reverse("profile", kwargs={"pk": profile_pk})


  def dispatch(self, request, *args, **kwargs):
    '''security check to make sure user can edit correct profile'''
    profile = self.get_object()
    if profile.user != request.user:
        return redirect(reverse('main_page'))
    return super().dispatch(request, *args, **kwargs)
  
  
  def get_login_url(self):
    '''redirect users that aren't logged in'''
    return reverse('main_page')
  
  def get_object(self):
    return get_object_or_404(Profile, user=self.request.user)

class CreatePlaylistView(LoginRequiredMixin, CreateView):
  '''view to create an initial playlist and correctly associate it with a profile'''

  form_class = CreatePlaylistForm
  template_name = 'music_dashboard/create_playlist_form.html'

  def get_context_data(self, **kwargs):
    '''associate a profile with context data for easier modification in html file'''
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
    '''saves playlist, and then iterates over list of songs provided, trying to associate each one with a song from the database,
    if successful, it is added to the playlist'''
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
    '''redirect a user after success'''
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
    '''add playlist to context data for ease of access'''
    context = super().get_context_data(**kwargs)
    playlist = self.get_object()
    context["profile"] = playlist.profile
    return context
  
  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    '''add additional songs to playlist, they need to be added in the form of a csv, and are processed similarly 
    to form_valid in CreatePlaylistView'''
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
      '''redirect user on success'''
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
    '''redirect user if they are not associated with the profile '''
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
    '''get playlist songs associated with a playlist so they can be displayed on the required page'''
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
    '''redirect user when successful'''
    playlist_song = self.get_object()
    playlist = playlist_song.playlist
    return reverse("playlist", kwargs={"pk":playlist.pk})

  def dispatch(self, request, *args, **kwargs):
    '''ensure that the playlist song is correctly associated with the profile of the user'''
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
    '''redirect a user on success'''
    playlist = self.get_object()
    profile = playlist.profile
    return reverse("profile", kwargs={"pk":profile.pk})

  def dispatch(self, request, *args, **kwargs):
    '''ensure that the playlist is correctly associated with the profile of the user'''

    playlist = self.get_object()
    profile = playlist.profile
    if profile.user != request.user:
        return redirect(reverse('main_page'))
    return super().dispatch(request, *args, **kwargs)

  def get_login_url(self):
    return reverse('main_page')
