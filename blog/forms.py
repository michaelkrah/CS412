from django import forms
from .models import Article


class CreateArticleForm(forms.ModelForm):
   '''Form for a new article'''

   class Meta:
      model = Article 
      fields= ['author', 'title', 'text', 'image_file']