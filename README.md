# PORTAPLOTTA
#### Video Demo:  https://youtu.be/XIbHZY-bNPE
#### Description:
The purpose of this web app is to allow users to search for events in their area.  Not only can they
search for events by proximity but can also look at a map of all of the listed events on the SQLite server.
Users can also post events that are hosted by themselves or by someone else as long as the required infomation
is known for the event.  The map consists of a nice Folium iFrame featuring text and logos.

#### Files Included:
app.py - The backbone of all features of the program and handles routing between the various templates.
        There are many modules that are included for the functionality of the program especially for
        Folium, which builds on the strengths that the Python ecosystem has on data, as well as
        it's functionality with the mapping library of Leaflet.js. base64, for encoding images to be used inside the iFrame, and branca.element for the creation and embedding of elements inside the iFrame.  Geocodio and geopy.distance were used for access and implementation of API Keys, and for proximity search parameters, respectively.


data.db - The SQLite database file that includes all information about the users that have registered
        (ie. id, username, and password) in the 'users' table, and the information about the events in
        the 'events' table.  The infomation in the events table includes id, title, description, latitude and
        longitude, address, start time, and end time.  Users are able to register and also delete their account if they choose to do so.


helpers.py - There's only one helper function in this file, which is the login_required function.  This
        is used for every route except for login, logout, and register.


geolocator_sql - This file is used to locate the user if they have allowed GPS permissions and they can
        then search for events using to proximity feature.  The function grabs the user's coordinates once
        they submit the search form, and the latitude and longitude input id's are of type 'hidden'. This
        is nice because the user does not see the process other than accepting the geolocation permission
        form.


add_event.html - This is the template used to add a new event to the database.  The user would have to
        include the information on the form which includes the title of the event, a brief description,
        the address, start time, and end time.  For the address, it's best to submit a complete address
        although it is acceptable to include on a city if the country is also provided.


delete_account.html - This template is self-explanatory, the user has the ability to delete their account.
                The user only has to confirm their intent to delete their account by completing the form
                with radio buttons.


error.html - All of the error handling and exceptions are completed with this template. The 'message'
        variable is used so that custom messages can be used from each unique error situation and rendered
        along with the render_template function.


index.html - This is the 'home base' for the web app which is available after logging in.


layout.html - This is the 'boiler plate' template which includes all of the necessary navbar content.  I
        chose a dark theme for the navbar because I thought it was easier on the eyes to look at.  The
        dropdown menus make it more interactive.


login.html - This is the template that is rendered for the user to enter login credentials.


map_page.html - This is the template used for both the 'search_event' and 'all_events' functions.  It will
        print the map with the corresponding map data coming from whether the former or the latter functions
        were called.  search_event is proximity-based and the user only has to input their chosen radius for
        the search results. Custom iFrames were used and look very nice with custom logos.


pong.html - This is the template that hosts the pong game.  It was written in JavaScript and runs pretty
        smooth being client-side.


register.html - The template used to register for an account.  The user must supply a username and password,
        and the passwords must match.


search_event.html - The template used to search for event by proximity.  The user can input their search
        radius in km.


The remaining file are png's and svg's used as images and logos in the program.



#### Final Thoughts
What I liked most about this project was what I learned about Folium which was very new to me and was
a little bit of a learning curve.  Anyone interested in using Folium and Leaflet.js in their programs
and applications need to make sure that the proper modules are imported and even more importantly; when
using the f-string in Folium, you have to use the triple quotes(""") and not single quotes when embedding
the html into the iFrame object.
