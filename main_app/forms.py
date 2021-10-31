from django import forms
from django.forms import ModelForm
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from .models import Artist

class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'img','bio','user']
        
        
        def __init__(self, *args, **kwargs):
            super(ArtistForm, self).__init__(*args, **kwargs)