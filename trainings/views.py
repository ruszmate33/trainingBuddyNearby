from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import folium
import geocoder
from .forms import TrainingForm
from .models import Training
from .utils import addMarker, getLatLngFromApi, getSettlementFromApi, filterPastDates

# Create your views here.

def training(request, training_id):
    training = Training.objects.get(id=training_id)
    sport = training.getSport()
    description = training.getDescription()
    adress = training.getAdress()
    date = training.getDate()
    context = {
        "sport": sport,
        "description": description,
        "adress": adress,
        "date": date,
        }

    return render(request, "trainings/training.html", context)


def add(request):
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            myLocation = form.cleaned_data["adress"]
            sport = form.cleaned_data["sport"]
            instance.sport = sport
            # here try-catch block, error massage for errors
            try:
                instance.adress = getSettlementFromApi(myLocation)
                lat, lng = getLatLngFromApi(myLocation)
                instance.location = Point(lng, lat) # Point takes this way
                instance.save()
                
            except:
                print(f"Sorry, we could not find location {myLocation}.")
                errormessage = f"Sorry, we could not find location {myLocation}."
                return render(request, "trainings/add.html", {
                        "form": form,
                        "errormessage": errormessage,
                })
                        
            return HttpResponseRedirect(reverse("trainings:index"))
    else:
        form = TrainingForm()
        errormassage = None
        # user_location = geocoder.osm("Wien")

    context = {
        "form": form,
        "errormessage": errormassage
    }

    return render(request, "trainings/add.html", context)


def index(request):
    # marker for user location
    try:
        user_location = geocoder.osm("Wien")
    except:
        print(f"geocoder open street map can not process location {user_location}")
    try:
        lat, lng = getLatLngFromApi(user_location)
    except:
        print(f"lat, lng gets: {getLatLngFromApi(user_location)}")
        # hard code 0, 0 as emergency
        lat, lng = 0, 0
    try:
        nameSettlement = getSettlementFromApi(user_location)
        user_location_point = Point(lng, lat, srid=4326)
    except:
        user_location_point = Point(0, 0, srid=4326)

    # initialize folium map
    mapFolium = folium.Map(width=800, height=500, location=(lat, lng))
    addMarker(lat, lng, "my location", mapFolium, 0)

    # filter out trainings in the past
    # startdate = datetime.now()
    # print(startdate)
    # trainings = Training.objects.all().filter(date__range=[startdate, "2021-10-07"])
    trainings = filterPastDates(Training.objects.all())

    #add marker to locations
    [training.putOnMap(mapFolium) for training in trainings]

    mapFolium = mapFolium._repr_html_()

    
    # order by distance to user
    #distanceSet = Training.objects.annotate(distance=Distance('location', user_location_point)).order_by('distance').values('id','adress','sport','date','distance').distinct().filter(date__range=["2020-10-07", "2021-10-07"])
    distanceSet = trainings.annotate(distance=Distance('location', user_location_point)).order_by('distance').values('id','adress','sport','date','distance').distinct()
    print(distanceSet)

    return render(request, "trainings/index.html", {
        "myLocation": nameSettlement,
        "myLat": round(lat, 2),
        "myLng": round(lng, 2),   
        "map": mapFolium,
        "distanceSet": distanceSet,
    })