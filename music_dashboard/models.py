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
  
  def get_friends(self):
    '''get all friends related to this profile'''
    friends_list = list(Friend.objects.filter(friend1__pk=self.pk) | Friend.objects.filter(friend2__pk=self.pk))
    profiles_list = []
    for relationship in friends_list:
      if relationship.friend1.pk != self.pk:
        profiles_list.append(relationship.friend1)
      else:
        profiles_list.append(relationship.friend2)
    return profiles_list
  
  def add_friend(self, other):
    '''method to add another profile as a friend relationship'''
    existing_friends = self.get_friends() + other.get_friends()
    if self in existing_friends or other in existing_friends:
      print("Already have a friendship")
      return 
    elif self.pk == other.pk:
      print("Someone can't be friends with themselves")
      return
  
    friend = Friend(friend1=self, friend2=other)
    friend.save()
    print(f"Friendship created between {self} and {other}")
    return
  
  def is_friend(self, other):
    '''method to check if another profile is a friend'''
    friends_list = self.get_friends()
    return other in friends_list


  def get_listens(self):
    '''gets all songs listened to by this profile'''

    listens = Listen.objects.filter(profile=self)
    return listens
  
  def get_playlists(self):
    '''get all playlists related to this profile'''
    playlists = Playlist.objects.filter(profile=self)

    return playlists
  

class Friend(models.Model):
  '''Model to refer to a friend connection between two profiles'''
  friend1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="friend1")
  friend2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="friend2")
  anniversary = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'{self.friend1.first_name} {self.friend1.last_name} & {self.friend2.first_name} {self.friend2.last_name} '


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
    return f'{self.name} by {self.artist} '

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