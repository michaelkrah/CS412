from django.db import models

# Create your models here.

class Profile(models.Model):
  '''Encapsulates the data for a profile of a given user'''

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