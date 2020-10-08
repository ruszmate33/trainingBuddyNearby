# Create your models here.
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from .utils import addMarker
from datetime import datetime

class Training(models.Model):
    sport = models.CharField(max_length=100)
    adress = models.CharField(max_length=64, blank=False)
    location = models.PointField(geography=True, default = Point(0, 0))
    date = models.DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M"))
    description = models.CharField(max_length=100, blank=False)

    def getID(self):
        return self.id

    def getLng(self):
        return self.location.x

    def getLat(self):
        return self.location.y

    def getSport(self):
        return self.sport

    def getUrl(self):
        #return "<a href=\"{% url 'trainings:training' "+str(self.getID())+"%}\">Sport</a>"
        return '<a href=http://127.0.0.1:8000/trainings/'+str(self.getID())+' target="_blank">Join</a>'

    def putOnMap(self, mapFolium):
        addMarker(self.getLat(), self.getLng(), self.getSport(), mapFolium, self.getUrl(), self.getDate())

    def getDescription(self):
        return self.description

    def getAdress(self):
        return self.adress

    def getDate(self):
        return self.date.strftime('%Y-%m-%d %H:%M')