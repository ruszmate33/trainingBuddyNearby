import folium 
import geocoder
from geopy.distance import geodesic


def addMarker(lat, lng, name, mapFolium):
    folium.Marker([lat, lng], 
                    tooltip='click here for more',
                    icon=folium.Icon(color='red'), 
                    popup=name).add_to(mapFolium)


def getLatLngFromApi(locationString):
    location = geocoder.osm(locationString)

    if location.ok == True:
        [lat, lng] = location.latlng
        return lat, lng
    else:
        return f"Could not retrieve location: {locationString}."


def getSettlementFromApi(locationString):
    location = geocoder.osm(locationString)
    if location.ok == True:
        city = location.city
        if city is not None:
            return city
        else:
            return location.town