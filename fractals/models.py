from django.db import models

class Fractal(models.Model):
    name = models.CharField(max_length=200)
    transformCount = models.IntegerField()
    transforms = models.TextField()
    thumbnailWidth = models.IntegerField()
    thumbnailHeight = models.IntegerField()
    thumbnail = models.ImageField(upload_to='fractalThumbs', width_field='thumbnailWidth', height_field='thumbnailHeight')
    