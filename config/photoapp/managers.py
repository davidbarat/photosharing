from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager


class PhotoManager(models.Manager):

    def get_photos(self, number):
        photo_list = super(
            PhotoManager,
            self).Photo.objects.objects.all().order_by('-id')[:number]
        return(photo_list)


