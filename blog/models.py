# Define data models for use in the blog application
from django.db import models

# Create your models here.

class Article(models.Model):
  '''Encapsulate the data for an article by some author'''

  # data attributes

  title = models.TextField(blank=False)
  author = models.TextField(blank=False)
  text = models.TextField(blank=False)
  published = models.DateTimeField(auto_now=True)
  image_url = models.URLField(blank=True) ## New field


  def __str__(self):
    '''return a sring representation'''
    return f"{self.title} by {self.author}"
