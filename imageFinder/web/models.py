from __future__ import unicode_literals

from django.db import models
from datetime import date

# Create your models here.
class Image(models.Model):
    image_location = models.CharField(max_length=500)#extra long incase it freaks out with the path
    date_added = models.DateTimeField(auto_now_add=True, blank=True) 
    