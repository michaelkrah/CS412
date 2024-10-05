from django.db import models

# Create your models here.

class Profile(models.Model):
  '''Encapsulates the data for a profile of a given user'''

  first_name = models.TextField(blank=False)
  last_name = models.TextField(blank=False)
  city = models.TextField(blank=False)
  email_address = models.TextField(blank=False)
  profile_image_url = models.URLField(blank=True)
