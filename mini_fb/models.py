from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
  '''Encapsulates the data for a profile of a given user'''


  user = models.ForeignKey(User, on_delete=models.CASCADE)

  first_name = models.TextField(blank=False)
  last_name = models.TextField(blank=False)
  city = models.TextField(blank=False)
  email_address = models.TextField(blank=False)
  profile_image_url = models.URLField(blank=True)

  def __str__(self):
    '''return a string representation'''
    return f"{self.first_name} {self.last_name}"
  
  def get_status_messages(self):
    '''gets all status messages related to this profile'''

    messages = StatusMessage.objects.filter(profile=self)
    return messages

  def get_friends(self):
    '''get a list of friends for a specific profile'''
    print(Friend.objects.filter(friend1__pk=self.pk) | Friend.objects.filter(friend2__pk=self.pk))
    friends_list = list(Friend.objects.filter(friend1__pk=self.pk) | Friend.objects.filter(friend2__pk=self.pk))
    profiles_list = []
    for relationship in friends_list:
      if relationship.friend1.pk != self.pk:
        profiles_list.append(relationship.friend1)
      else:
        profiles_list.append(relationship.friend2)
    return profiles_list
  
  def add_friend(self, other):
    '''method to add more friends'''
    # make sure no friends exist 
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
  
  def get_friend_suggestions(self):
    '''method to return a list of related friends'''
    friends_list = self.get_friends()
    friend_suggestions = []
    for friend in friends_list:
      
      friends_of_friends = friend.get_friends()
      for f2 in friends_of_friends:
        if f2 not in friend_suggestions and f2.pk != self.pk and f2 not in friends_list:
          friend_suggestions.append(f2)
    
    return friend_suggestions
  

  def get_news_feed(self):
    '''returns a list of status messages for a profile's friends'''

    friend_list = self.get_friends()
    status_list = []
    for friend in friend_list:
      friend_status = list(StatusMessage.objects.filter(profile__pk=friend.pk))
      status_list += friend_status

    sorted_status_list = sorted(status_list, key=lambda status: status.published, reverse=True)
    return sorted_status_list

  

class Friend(models.Model):
  '''Model to store a friend relationship between two people'''

  friend1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="friend1")
  friend2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="friend2")
  anniversary = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'{self.friend1.first_name} {self.friend1.last_name} & {self.friend2.first_name} {self.friend2.last_name} '
  

class StatusMessage(models.Model):
  '''Describes a status message on a profile'''

  profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

  message = models.TextField(blank=False)
  published = models.DateTimeField(auto_now=True)

  def get_images(self):
    '''gets all the images related to a status message'''

    images = Image.objects.filter(status_message=self)
    return images

  def __str__(self):
    return f'{self.message}'
  

  

class Image(models.Model):
  '''Describes a single image attached to a Profile'''

  status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)

  image_file = models.ImageField(blank=True)
  published = models.DateTimeField(auto_now=True) 


  def __str__(self):
    return f'{self.image_file.url}'