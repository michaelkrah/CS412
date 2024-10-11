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
  
  def get_comments(self):
    '''gets all comments related to this article'''

    # Use ORM to filter for comments where this is the foreign key

    comments = Comment.objects.filter(article=self)
    return comments


class Comment(models.Model):
  '''Encapsulates a comment on an article'''

  # Need a one to many relationship between Articles and Commments
  article = models.ForeignKey("Article", on_delete=models.CASCADE) # what to do if foreign key is deleted
  
  author = models.TextField(blank=False)
  text = models.TextField(blank=False)
  published = models.DateTimeField(auto_now=True)

  def __str__(self) -> str:
    '''string rep'''
    return f'{self.text}'