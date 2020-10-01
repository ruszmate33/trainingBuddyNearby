# Create your models here.
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from .utils import addMarker

class Training(models.Model):
    sport = models.CharField(max_length=100)
    adress = models.CharField(max_length=64, default="Gotham")
    location = models.PointField(geography=True, default = Point(0, 0))
    time = models.DateTimeField(default='2006-10-25 14:30:59')

    def getLng(self):
        return self.location.x

    def getLat(self):
        return self.location.y

    def getSport(self):
        return self.sport

    def putOnMap(self, mapFolium):
        addMarker(self.getLat(), self.getLng(), self.getSport(), mapFolium)