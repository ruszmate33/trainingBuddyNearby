from datetime import datetime
import folium 
import geocoder
from geopy.distance import geodesic


# filter out trainings in the past
def filterPastDates(obj, latest="2021-10-07"):
    startdate = datetime.now()
    print(startdate)
    return obj.filter(date__range=[startdate, latest])

def addMarker(lat, lng, name, mapFolium, url, date=None):
    if date is not None:
        html =  f"<h4>{name}</h4><p>{date}</p><p>{url}</p>"
        html = folium.Html(html, script=True)
        popup = folium.Popup(html)
    else:
        popup = folium.Popup(name)
    folium.Marker([lat, lng], 
                    tooltip=name,
                    icon=folium.Icon(color='red'), 
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