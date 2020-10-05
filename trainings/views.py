from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import folium
import geocoder
from .forms import TrainingForm
from .models import Training
from .utils import addMarker, getLatLngFromApi, getSettlementFromApi

# Create your views here.

def add(request):
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            myLocation = form.cleaned_data["adress"]
            sport = form.cleaned_data["sport"]
            instance.sport = sport
            # here try-catch block, landing page for errors
            instance.adress = getSettlementFromApi(myLocation)
            lat, lng = getLatLngFromApi(myLocation)
            instance.location = Point(lng, lat) # Point takes this way
            instance.save()
            form = TrainingForm()
            return HttpResponseRedirect(reverse("trainings:index"))
    else:
        form = TrainingForm()
        # user_location = geocoder.osm("Wien")

    return render(request, "trainings/add.html", {
        "form": form,
    })


def index(request):
    # marker for user location
    user_location = geocoder.osm("Wien")
    lat, lng = getLatLngFromApi(user_location)
    nameSettlement = getSettlementFromApi(user_location)
    user_location_point = Point(lng, lat, srid=4326)

    # initialize folium map
    mapFolium = folium.Map(width=800, height=500, location=(lat, lng))
    addMarker(lat, lng, "my location", mapFolium)

    trainings = Training.objects.all()

    #add marker to locations
    [training.putOnMap(mapFolium) for training in trainings]

    mapFolium = mapFolium._repr_html_()

    # order by distance to user
    distanceSet = Training.objects.annotate(distance=Distance('location', user_location_point)).order_by('distance').values('adress','sport','date','distance').distinct()
    print(distanceSet)

    return render(request, "trainings/index.html", {
        "myLocation": nameSettlement,
        "myLat": round(lat, 2),
        "myLng": round(lng, 2),   
        "map": mapFolium,
        "distanceSet": distanceSet,
    })