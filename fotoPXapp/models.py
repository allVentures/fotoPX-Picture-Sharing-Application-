from django.db import models

class Regions(models.Model):
    voivodeship_id = models.IntegerField(blank=True, null=True)
    county_id = models.IntegerField(blank=True, null=True)
    municipality_id = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)

class ExtendUser(models.Model):
    region = models.ForeignKey('Regions', on_delete=models.SET_NULL, null=True)

