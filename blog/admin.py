from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Article) #Repeat for every model
admin.site.register(Comment) 