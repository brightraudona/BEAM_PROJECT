from datetime import timedelta
from django.shortcuts import render
from App.models import Activity, Challenge
from folium import folium
import requests

# Create your views here.
def home(request):
    # Make your map object
    main_map = folium.Map(location=[54.6872, 25.2797], zoom_start = 12) # Create base map
    main_map_html = main_map._repr_html_() # Get HTML for website

    if request.user.is_anonymous:
        return render(request, 'login.html')
    else:
        user = request.user # Pulls in the Strava User data
        strava_login = user.social_auth.get(provider='strava') # Strava login
        access_token = strava_login.extra_data['access_token'] # Strava Access token
        activites_url = "https://www.strava.com/api/v3/athlete/activities"
        # Get activity data
        header = {'Authorization': 'Bearer ' + str(access_token)}
        activity_df_list = []
        for n in range(5):  # Change this to be higher if you have more than 1000 activities
            param = {'per_page': 5, 'page': n + 1}

            activities_json = requests.get(activites_url, headers=header, params=param).json()
            if not activities_json:
                break
            activity_df_list.append(activities_json)
            Activity.objects.update_or_create(name = activities_json[0]['name'],
                            activity_id = activities_json[0]['id'],
                            athlete = user,
                            start_date = activities_json[0]['start_date'],
                            distance = activities_json[0]['distance'],
                            duration = timedelta(seconds=activities_json[0]['elapsed_time']))

        challenge = Challenge.objects.all()
        data = {
            "user":user,
            "main_map":main_map_html,
            "challenges":challenge
        }
        return render(request, 'home.html', data)
    

def challenge(request, challengeId):
    activities = Challenge.objects.get(id=challengeId).activities.all()
    data = {
        "activities":activities
    }
    return render(request, 'challenge.html', data)

