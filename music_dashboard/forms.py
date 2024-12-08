from django import forms
from .models import Profile


class CreateProfileForm(forms.ModelForm):
  '''form class to create new profiles on mini_fb'''

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
