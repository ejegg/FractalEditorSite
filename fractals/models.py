from django.db import models

class Fractal(models.Model):
    name = models.CharField(max_length=200)
    transformCount = models.IntegerField()
    transforms = models.TextField()
    thumbnailWidth = models.IntegerField()
    thumbnailHeight = models.IntegerField()
    thumbnail = models.ImageField(upload_to='fractalThumbs', width_field='thumbnailWidth', height_field='thumbnailHeight')

    def _get_smallthumbsrc(self):
	return self.thumbnail.url.replace('.png', 'x1.png')

    smallthumbsrc = property(_get_smallthumbsrc)

    def _get_srcset(self):
	return self.thumbnail.url.replace('.png', 'x1.png') + ' 1x, ' + \
            self.thumbnail.url.replace('.png', 'x1.5.png') + ' 1.5x, ' + \
            self.thumbnail.url.replace('.png', 'x2.png') + ' 2x'

    srcset = property(_get_srcset)

    def _get_link(self):
        return 'fractaleditor://fractal/v1?id={0}&name={1}&thumbnail={2}&transforms={3}'.format(
            self.id, self.name, self.thumbnail, self.transforms)

    link = property(_get_link)

