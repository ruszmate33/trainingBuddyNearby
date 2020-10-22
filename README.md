# trainingBuddyNearby

TrainingBuddy
This is web-app in Django, which lets user register and create training sessions, exercises, and outdoor activities and allow fellow users to join these.
Users submit via a form what type of sport will be done in these activities, when and where they meet, can set an upper limit to how many people can join, and can inform via a short description other participants what can they expect, what equipment should bring with themselves.

Users can browse the list of possible training session/activities in a table and a map is showing the starting point locations of the activities. Hovering over the locations in the map shows the type of sport, clicking the marker displays sport and starting time, and a link for joining the activity. This link navigates to the info page of the particular workout, which shows starting time and date, brief description, available spots, the starting location on the map, the name of registered participants. At the bottom of the page, users can register (if there are slots available) or unregister for the workout. If the user created the workout, it can also delete it.

In the table at the index page the workouts are also listed in a tabular form. From here, the info page for the workouts is reachable via a lin. Also sport, location time, distance from user location and available sport are displayed. Results are ranked from closest to furthest starting location from the users location. This is currently hardcoded as downtown Vienna, but the app contains code out-commented, which is supposed to find an approximate user location via the IP-adress.

All available trainings are displayed by default, which will take place from the present moment up to the next seven days. Filtering results is possible by time period and sport. Time period filtering allows filtering via a dropdown either “this week”, “this month” or “all upcoming”. Filtering by sport is looking though “sport” inputs return if it contains the searched word. The filtered results are updated both in the table and the map.

The “My trainings” page shows the workout the user is registered for on the map and in a table. 
For more information about the particular training session, users can click them either in the table or by clicking on the location markers on the map.
Finally, users can Sign out from the web-app.

The web-app was created with the Django framework in Python. In order to improve the appearance of forms I used to crispy-forms package and filters. The project was divided into two apps, “users” takes care of signing up of new users and thereby creating a corresponding “athlete” instance, which can register for workout, create workouts and delete them if he/she created it. Also users can sign out. 

The second app is trainings, which handles all the functionality of creating new workouts, deleting, registering for workouts. Locations are stored in a “post GIS” postgres database. Ranking workouts based of their distance from user is also based on this databases capability. The map is created with the folium, leaflet and OpenStreetMap. Input locations from the form are translated to geolocation points with geocoder.osm API and django.contrib.gis.geos.
