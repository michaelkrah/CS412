from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
  '''Encapsulates the data for a profile of a given user'''


  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="music_dashboard_profiles")

  first_name = models.TextField(blank=False)
  last_name = models.TextField(blank=False)
  city = models.TextField(blank=False)
  email_address = models.TextField(blank=False)
  profile_image_url = models.URLField(blank=True)

  def __str__(self):
    '''return a string representation'''
    return f"{self.first_name} {self.last_name}"
  
  def get_listens(self):
    '''gets all songs listened to by this profile'''

    listens = Listen.objects.filter(profile=self)
    return listens
  
  def get_playlists(self):
    '''get all playlists related to this profile'''
    playlists = Playlist.objects.filter(profile=self)

    return playlists
  

class Artist(models.Model):
  '''Model to refer to a specific music artist or band'''

  name = models.TextField(blank=False)
  genre = models.TextField(blank=False)

  
  def __str__(self):
    return f'Artist {self.name}'
  

class Album(models.Model):
  '''Model to refer to a specifc album from an artist'''

  artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
  name = models.TextField(blank=False)
  released_date = models.DateField(auto_now=True)
  number_songs = models.IntegerField(blank=False)


  def __str__(self):
    return f'Album {self.name} by {self.artist}'
  

class Song(models.Model):
  '''Model to refer to a specific song by an artist'''
  name = models.TextField(blank=False)
  released_date = models.DateField(auto_now=True)
  artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
  album = models.ForeignKey("Album", on_delete=models.CASCADE)
  album_song = models.IntegerField(blank=True)

  def __str__(self):
    return f'Song {self.name} by {self.artist} '


class Listen(models.Model):
  '''Model to refer to a song listened to by a profile at a specific time'''
  song = models.ForeignKey("Song", on_delete=models.CASCADE)
  profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
  time = models.DateField(auto_now=True)

  def __str__(self):
    return f'User {self.profile} listened to {self.song} at {self.time}'

class Playlist(models.Model):
  '''Model to refer to a playlist created by a user'''
  name = models.TextField(blank=False)
  profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

  def __str__(self):
    return f'Playlist {self.name} by {self.profile}'
  

class PlaylistSong(models.Model):
  '''Model to refer to a song on a specific playlist'''
  song = models.ForeignKey("Song", on_delete=models.CASCADE)
  playlist = models.ForeignKey("Playlist", on_delete=models.CASCADE)

  def __str__(self):
    return f'Song {self.song} on playlist {self.playlist}'

