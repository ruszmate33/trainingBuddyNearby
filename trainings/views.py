from django.shortcuts import render
import geocoder
import folium
from .forms import TrainingForm
from .models import Training
from .utils import addMarker, getLatLngFromApi, getSettlementFromApi
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

# Create your views here.

user_location = Point(15.6038, 48.4100, srid=4326)


def index(request):
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            myLocation = form.cleaned_data["adress"]
            sport = form.cleaned_data["sport"]
            instance.sport = sport
            instance.adress = getSettlementFromApi(myLocation)
            lat, lng = getLatLngFromApi(myLocation)
            instance.location = Point(lng, lat) # Point takes this way
            instance.save()
    else:
        form = TrainingForm()
        myLocation = geocoder.osm("Wien")

    # marker
    lat, lng = getLatLngFromApi(myLocation)
    name = getSettlementFromApi(myLocation)

    # initialize folium map
    mapFolium = folium.Map(width=800, height=500, location=(lat, lng))
    addMarker(lat, lng, name, mapFolium)

    trainings = Training.objects.all()

    # add marker to locations
    # a nice .map(function) would help here
    for training in trainings:
        lat = training.getLat()
        lng = training.getLng()
        name = training.getSport()
        addMarker(lat, lng, name, mapFolium)

    mapFolium = mapFolium._repr_html_()

    # order by distance to user
    distanceSet = Training.objects.annotate(distance=Distance('location', user_location)).order_by('distance')
    print(distanceSet)

    return render(request, "trainings/index.html", {
        "myLocation": myLocation,
        "myLat": round(lat, 2),
        "myLng": round(lng, 2),
        "form": form,
        "map": mapFolium,
        "distanceSet":distanceSet
    })