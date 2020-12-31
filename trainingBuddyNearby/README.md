# TrainingBuddy

## Short demo: https://youtu.be/C3r_f7IxXRE

This is "TrainingBuddy" a location-based web application with the Django framework and GeoDjango sub-framework. It lets users create training-sessions, workouts, outdoor activities, hiking etc. and invite fellow athletes. 

On the main page an interactive map is displayed as well as a list which is ranked based on the distance to the user.
Upcoming events can be filtered based on time and type of sport.

It is using a spatial database (PostgreSQL and PostGIS) to store geolocation of the workouts.

The address of the activity is retrieved as a geolocation with the Folium API. Leaflet and Open Street Map are used to visualize.