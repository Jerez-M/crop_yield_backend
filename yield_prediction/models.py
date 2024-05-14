from django.db import models

class CropData(models.Model):
    year = models.IntegerField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    rainfall = models.FloatField(blank=True, null=True)
    pesticide = models.FloatField(blank=True, null=True)
    country = models.FloatField(blank=True, null=True)
    item = models.FloatField(blank=True, null=True)
    crop_yield = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.item} {self.year}'
