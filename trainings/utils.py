import folium 
import geocoder
from geopy.distance import geodesic


def addMarker(lat, lng, name, mapFolium, url, date=None):
    if date is not None:
        #html =  f"<h3>{name}</h3><h3>{date}</h3><h3>{url}</h3>"
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