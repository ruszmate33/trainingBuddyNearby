# Create your models here.
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.db.models.signals import post_save
from .utils import addMarker


class Training(models.Model):
    sport = models.CharField(max_length=100)
    adress = models.CharField(max_length=64, blank=False)
    location = models.PointField(geography=True, default = Point(0, 0))
    date = models.DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M"))
    description = models.CharField(max_length=100, blank=False)
    maxParticipants = models.PositiveSmallIntegerField(blank=True, default=10)

    def isRegistered(self, athlete):
        return self.participants.filter(id=athlete.id).exists()

    @property
    def organizer(self):
        return self.organizer
      
    def getID(self):
        return self.id

    @property
    def longitude(self):
        return self.location.x

    @property
    def lattitude(self):
        return self.location.y

    def getSport(self):
        return self.sport

    def getUrl(self):
        #return "<a href=\"{% url 'trainings:training' "+str(self.getID())+"%}\">Sport</a>"
        return '<a href=http://127.0.0.1:8000/trainings/'+str(self.getID())+' target="_blank">Join</a>'

    def putOnMap(self, mapFolium):
        addMarker(self.lattitude, self.longitude, self.getSport(), mapFolium, self.getUrl(), self.getDate(), color="blue")

    def getDescription(self):
        return self.description

    def getAdress(self):
        return self.adress

    def getDate(self):
        return self.date.strftime('%Y-%m-%d %H:%M')


class Athlete(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    trainings = models.ManyToManyField(Training, blank=True, related_name="participants")
    organizedTrainings = models.ManyToManyField(Training, blank=True, related_name="organizer")

    def getID(self):
        return self.id

    def getOrganizedTrainings(self):
        return self.organizedTrainings.all()


    def __str__(self):
        full_name = self.user.first_name + " " + self.user.last_name
        return f"{full_name}"


# I saw this trick at https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
def create_athlete(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        athlete = Athlete(user=user)
        athlete.save()
post_save.connect(create_athlete, sender=User)