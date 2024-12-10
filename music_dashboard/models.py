from django.db import models

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import json
import ast



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
  image = models.TextField(blank=False)

  def __str__(self):
    return f'Artist {self.name}, genres: {self.genre}'


  def get_genre(self):
    genre_list = ast.literal_eval(self.genre)
    if len(genre_list) > 0:
      
      return list(genre_list)[0]
    else:
      return "No genre found"
    
  def get_albums(self):
    albums_list = list(Album.objects.filter(artist=self))
    return albums_list

  def get_songs(self):
    songs_list = list(Song.objects.filter(artist=self))
    return songs_list

class Album(models.Model):
  '''Model to refer to a specifc album from an artist'''

  artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
  name = models.TextField(blank=False)
  release_date = models.DateField()
  number_songs = models.IntegerField(blank=False)
  image = models.TextField(blank=False)

  def __str__(self):
    return f'Album {self.name} by {self.artist}'
  

class Song(models.Model):
  '''Model to refer to a specific song by an artist'''
  name = models.TextField(blank=False)
  release_date = models.DateField()
  artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
  album = models.ForeignKey("Album", on_delete=models.CASCADE)
  spotify_id = models.TextField(blank=False) # useful to associate with uploaded values

  def __str__(self):
    return f'{self.name} by {self.artist}, {self.spotify_id} '

class Listen(models.Model):
  '''Model to refer to a song listened to by a profile at a specific time'''
  song = models.ForeignKey("Song", on_delete=models.CASCADE)
  profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
  time = models.DateTimeField()
  time_listened = models.IntegerField(blank=False)


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
  


def get_profile(self):
    """Returns the profile associated with the user, if it exists."""
    try:
        return list(Profile.objects.filter(user__pk=self.pk))[0]
    except ObjectDoesNotExist:
        return None
    
User.add_to_class("get_profile", get_profile)


def load_data():
  '''Load songs, albums, and artist data records so that when listens are uploaded more detailed data is available
  The file is a JSON made of individual song data from the spotify API
  It is split into artist, album and song objects so that when listening data is uploaded that is missing data, 
  it can be locally matched up with more detailed information.
  This project assumes that listening data will have a song object associated with it in Django's database'''

  Song.objects.all().delete()
  Album.objects.all().delete()
  Artist.objects.all().delete()
  count = 0

  filename = 'C:/Users/Michael/Desktop/BU/2024 Fall/CS 412/Final/DetailedData.json'
  
  with open(filename, 'r', encoding='utf-8') as file:
    count = 0
    for line in file:
      count=count+1
      try:
        record = json.loads(line.strip())
        
        track_artist = record.get("trackArtist", "Unknown Artist")
        artist_genre = record.get("genres")
        album_data = record.get("data", {}).get("item", {}).get("album", {})
        album_image = record.get("albumImage","Unknown" )
        artist_db_query = list(Artist.objects.filter(name=track_artist))
        if len(artist_db_query) == 0: # Artist has not been added yet
          artist = Artist(name=track_artist,
                          genre=artist_genre,
                          image = album_image
                          )

          artist.save()
        else:
          artist = artist_db_query[0]
        
        track_album = album_data.get("name", "Unknown Album")
        release_date = album_data.get("release_date", "Unknown Release Date")
        number_songs = album_data.get("total_tracks", {}).get("$numberInt", "Unknown")
        
        if len(release_date) == 4:
          release_date = release_date + "-01-01"
        elif len(release_date) == 7:
          release_date = release_date + "-01"

        album_db_query = list(Album.objects.filter(name=track_album))
        if len(album_db_query) == 0: # Artist has not been added yet
          album = Album(
            artist = artist,
            name = track_album,
            release_date = release_date,
            number_songs = number_songs,
            image = album_image
          )
          album.save()
        else:
          album = album_db_query[0]

        song_name = record.get("trackTitle")
        release_date = album.release_date
        spotify_id = record.get("data", {}).get("item", {}).get("id", "Unknown Spotify Id")
                
        song_db_query = list(Song.objects.filter(name=song_name))
        if len(song_db_query) == 0:
          song = Song(name=song_name,
                      release_date=release_date,
                      artist=artist,
                      album=album,
                      spotify_id=spotify_id)
          song.save() 
        else:
          song = song_db_query[0]

        
        if count % 25 == 0:
          print(song)
        count+=1
        
      except Exception as e:
        print(f"An error occured: {count}", e)



