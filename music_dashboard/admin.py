from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Profile)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Listen)
admin.site.register(Playlist)
admin.site.register(PlaylistSong)
admin.site.register(Friend)

