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
  '''Allows users to update a profile'''
  class Meta:
      model = Profile
      fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url']

class CreatePlaylistForm(forms.ModelForm):
  '''form class to create a new playlist from recently listened to songs'''

  class Meta:
    model = Playlist   
    fields = ['name']