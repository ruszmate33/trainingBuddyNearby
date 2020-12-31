from datetime import datetime, timedelta
import folium 
import geocoder
from django.contrib.gis.geos import Point


def createUserLocationPoint(locationString):
    # marker for user location
    try:
        user_location = geocoder.osm(locationString)
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
    return user_location_point


def createMapWithUserLocationMark(user_location_point, zoom=10):
    # initialize folium map
    mapFolium = folium.Map(width='100%', height='100%', left='0%', top='0%', min_zoom=zoom, location=(user_location_point.y, user_location_point.x))
    addMarker(user_location_point.y, user_location_point.x, "my location", mapFolium, 0)
    return mapFolium


# filter for trainings
def filterBySport(obj, sportFilter):
    if sportFilter is None:
        return obj
    return obj.filter(sport__contains = sportFilter)

# filter out trainings in the past
def filterPastDates(obj, timePeriod):
    startdate = datetime.now()
    oneWeek = timedelta(days=7)
    if timePeriod == "month":
        latest = startdate + 4*oneWeek
    elif timePeriod == "week":
        latest = startdate + oneWeek
    else:
        latest = datetime.max
    print(f"start: {startdate}")
    print(f"end: {startdate}")
    return obj.filter(date__range=[startdate, latest])

def addMarker(lat, lng, name, mapFolium, url, date=None, color='red'):
    if date is not None:
        html =  f"<h4>{name}</h4><p>{date}</p><p>{url}</p>"
        html = folium.Html(html, script=True)
        popup = folium.Popup(html)
    else:
        popup = folium.Popup(name)
    folium.Marker([lat, lng], 
                    tooltip=name,
                    icon=folium.Icon(color=color), 
                    popup=popup).add_to(mapFolium)


def getLatLngFromApi(locationString):
    try:
        location = geocoder.osm(locationString)
        if location.ok == True:
            [lat, lng] = location.latlng
            return lat, lng
    except:
        print(f"Could not retrieve location {locationString}' lat, lng'.")
        print(f"getLatLngFromApi() returns: {location.latlng}")
        raise


def getSettlementFromApi(locationString):
    location = geocoder.osm(locationString)
    if location.ok == True:
        city = location.city
        if city is not None:
            return city
        else:
            return location.town