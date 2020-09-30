# Create your models here.
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class Training(models.Model):
    sport = models.CharField(max_length=100)
    adress = models.CharField(max_length=64, default="Gotham")
    location = models.PointField(geography=True, default = Point(0, 0))

    def getLng(self):
        return self.location.x

    def getLat(self):
        return self.location.y

    def getSport(self):
        return self.sport