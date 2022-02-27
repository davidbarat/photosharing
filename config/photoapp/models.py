'''Photoapp Models'''

from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from .managers import PhotoManager


class Photo(models.Model):
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=250) 
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photos/')
    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tags = TaggableManager() 

    def __str__(self):
        return self.title

    def get_photos(self, number):
        photo_list = super(
            PhotoManager,
            self).Photo.objects.objects.all().order_by('-id')[:number]
        return(photo_list)

