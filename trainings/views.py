from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import TrainingForm, TrainingFilterForm
from .models import Training, Athlete
from .utils import getLatLngFromApi, getSettlementFromApi, filterPastDates, filterBySport, createMapWithUserLocationMark, createUserLocationPoint


locationString = "Lorenz-Müller-Gasse 1A, 1200 Wien"

@login_required(login_url="users:login")
def deleteTraining(request, training_id):
    if request.method == 'POST':
        training = Training.objects.get(id=training_id)
        training.delete()
        return HttpResponseRedirect(reverse("trainings:myTrainings"))

@login_required(login_url="users:login")
def myTrainings(request):
    # get all user trainings
    athlete = Athlete.objects.get(user=request.user)
    myTrainings = athlete.trainings.all()
    myTrainings = filterPastDates(myTrainings, "all")

    user_location_point = createUserLocationPoint(locationString)
    mapFolium = createMapWithUserLocationMark(user_location_point)


    #add marker to locations
    [training.putOnMap(mapFolium) for training in myTrainings]
    mapFolium = mapFolium._repr_html_()
    
    # order by distance to user
    distanceSet = myTrainings.annotate(distance=Distance('location', user_location_point)).order_by('distance').values('id','adress','sport','date','distance')

    return render(request, "trainings/myTrainings.html", {
        "distanceSet":distanceSet,
        "map":mapFolium,
    })


@login_required(login_url="users:login")
def toggleJoined(request, training_id):
    if request.method == "POST":
        training = Training.objects.get(id=training_id)

        
        print(f"training before: {training.participants}")

        # add current user as participant
        athlete = Athlete.objects.get(user=request.user)
        print(f"athlete before: {athlete}")

        myTrainings = athlete.trainings.all()
        
        if training in myTrainings:
            training.participants.remove(athlete)
        else:
            training.participants.add(athlete)
    
        # registrationChanged = True

        # context = {"registrationMessage":registrationMessage,
        #             "registrationChanged":registrationChanged}

        # print(f"training after: {training.participants}")
        # print(f"athlete after: {athlete}")

        # redirect to the training page
        return HttpResponseRedirect(reverse("trainings:training", args=(training.id,)))


@login_required(login_url="users:login")
def training(request, training_id):
    training = Training.objects.get(id=training_id)
     
    sport = training.getSport()
    description = training.getDescription()
    adress = training.getAdress()
    date = training.getDate()
    participants = training.participants.all()
    
    athlete = Athlete.objects.get(user=request.user)

    if training in athlete.getOrganizedTrainings():
        isOrganizer = True
    else:
        isOrganizer = False

    isRegistered = training.isRegistered(athlete)
    
    # create a map for this single training as well
    try:
        long = training.longitude
        latt = training.lattitude
        mapFolium = createMapWithUserLocationMark(Point(long, latt, srid=4326), zoom=14)
        mapFolium = mapFolium._repr_html_()
    except:
        print("sorry could not map location")

    context = {
        "training":training,
        "sport": sport,
        "description": description,
        "adress": adress,
        "date": date,
        "participants": participants,
        "isOrganizer": isOrganizer,
        "isRegistered":isRegistered,
        "map":mapFolium,
        }
    

    return render(request, "trainings/training.html", context)


@login_required(login_url="users:login")
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
                athlete = Athlete.objects.get(user=request.user)
                instance.save()
                # register as organizer and as 1st participant
                athlete.organizedTrainings.add(instance)
                         
                
            except:
                errormessage = f"Sorry, we could not find location {myLocation}."
                return render(request, "trainings/add.html", {
                        "form": form,
                        "errormessage": errormessage,
                })
                        
            return HttpResponseRedirect(reverse("trainings:index"))
    else:
        form = TrainingForm()
        errormassage = None

    context = {
        "form": form,
        "errormessage": errormassage
    }

    return render(request, "trainings/add.html", context)


@login_required(login_url="users:login")
def index(request, timePeriod="week", sportFilter=None):
    if request.method == "POST":
        timePeriod = request.POST.get('timePeriod', None)    
        sportFilter = request.POST.get('sportFilter', None)   
    
    user_location_point = createUserLocationPoint(locationString)
    nameSettlement = getSettlementFromApi(locationString)
    mapFolium = createMapWithUserLocationMark(user_location_point)

    # filter out trainings by time and sport
    trainings = Training.objects.all()
    trainings = filterPastDates(trainings, timePeriod)
    trainings = filterBySport(trainings, sportFilter)
    
    #add marker to locations
    [training.putOnMap(mapFolium) for training in trainings]
    mapFolium = mapFolium._repr_html_()
    
    # order by distance to user
    distanceSet = trainings.annotate(distance=Distance('location', user_location_point)).order_by('distance')
    

    # form to filter results
    trainingFilterForm = TrainingFilterForm()   

    print(f"distanceSet: {distanceSet}")
    
    return render(request, "trainings/index.html", {
        "myLocation": nameSettlement,
        "map": mapFolium,
        "distanceSet": distanceSet,
        "trainingFilter": trainingFilterForm,
    })