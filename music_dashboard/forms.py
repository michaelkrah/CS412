from django import forms
from .models import Profile, Playlist


class CreateProfileForm(forms.ModelForm):
  '''form class to create new profiles'''

  class Meta:
    model = Profile
    fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url']
    widgets = {
      'first_name': forms.Textarea(attrs={
        'rows': 1, 'cols': 40
        }),
        'last_name': forms.Textarea(attrs={
        'rows': 1, 'cols': 40
        }),
        'city': forms.Textarea(attrs={
        'rows': 1, 'cols': 40
        }),
        'email_address': forms.Textarea(attrs={
        'rows': 1, 'cols': 40
        }),
      }

class EditProfileForm(forms.ModelForm):
  '''Form class for users to update a profile'''
  class Meta:
      model = Profile
      fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url']

class CreatePlaylistForm(forms.ModelForm):
  '''Form class to create a new playlist from a string input of songs'''

  class Meta:
    model = Playlist   
    fields = ['name']

class UpdatePlaylistForm(forms.ModelForm):
  '''Form class to update a playlist to add new songs or change the name'''

  class Meta:
    model = Playlist   
    fields = ['name']