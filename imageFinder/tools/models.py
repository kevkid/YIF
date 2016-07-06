from __future__ import unicode_literals

from django.db import models
from datetime import date

# Create your models here.
class Image(models.Model):
    image_location = models.CharField(max_length=500)#extra long incase it freaks out with the path
    date_added = models.DateTimeField(auto_now_add=True, blank=True) 
    image_class_0 = models.IntegerField(default=0)
    image_class_1 = models.IntegerField(default=0)
    image_class_2 = models.IntegerField(default=0)
    image_class_3 = models.IntegerField(default=0)
    image_class_4 = models.IntegerField(default=0)
    image_class_5 = models.IntegerField(default=0)
    image_class_6 = models.IntegerField(default=0)
    image_class_7 = models.IntegerField(default=0)

class Classes(models.Model):
    image_class = models.IntegerField(default=0)
    image_class_desc = models.CharField(max_length=25)
